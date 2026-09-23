"""Validation for question bank and game snapshot flow."""
import asyncio
import json
import urllib.error
import urllib.request

import websockets

API = "http://localhost:8000"


def api_request(method: str, path: str, payload: dict | None = None) -> dict | list | None:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method=method,
    )
    try:
        with urllib.request.urlopen(request) as response:
            if response.status == 204:
                return None
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        body = error.read().decode()
        try:
            detail = json.loads(body).get("detail", body)
        except json.JSONDecodeError:
            detail = body
        raise RuntimeError(f"{method} {path} failed ({error.code}): {detail}") from error


def api_get(path: str) -> dict | list:
    result = api_request("GET", path)
    assert result is not None
    return result


async def ws_play_one_game(game_id: int, total_questions: int) -> None:
    uri = f"ws://localhost:8000/ws/games/{game_id}"
    async with websockets.connect(uri) as websocket:
        await asyncio.wait_for(websocket.recv(), timeout=5)
        for _ in range(total_questions):
            current = api_get(f"/api/games/{game_id}")
            correct = current["current_question"]["correct_answer"]
            await websocket.send(json.dumps({"action": "register_buzz", "player_number": 1}))
            while True:
                message = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
                if message["type"] == "game_state":
                    break
            await websocket.send(json.dumps({"action": "submit_answer", "answer": correct}))
            while True:
                message = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
                if message["type"] == "game_state":
                    break
            state = api_get(f"/api/games/{game_id}")
            if state["current_question_index"] < total_questions:
                await websocket.send(json.dumps({"action": "next_question"}))
                while True:
                    message = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
                    if message["type"] == "game_state":
                        break
        await websocket.send(json.dumps({"action": "finish_game"}))
        while True:
            message = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
            if message["type"] == "game_state":
                break


def create_game(question_set_id: int, players: list[dict]) -> dict:
    result = api_request(
        "POST",
        "/api/games",
        {"question_set_id": question_set_id, "players": players},
    )
    assert result is not None
    return result


def get_primary_question_set_id() -> int:
    sets = api_get("/api/question-sets")
    preferred = next((item for item in sets if item["name"] == "Lista General"), None)
    if preferred is not None and preferred["question_count"] > 0:
        return preferred["id"]

    seeded = next((item for item in sets if item["question_count"] > 0), None)
    assert seeded is not None, "No hay listas de preguntas disponibles"
    return seeded["id"]


def get_correct_answer_points() -> int:
    config = api_get("/api/event-config")
    return int(config["correct_answer_points"])


async def main() -> None:
    results: list[str] = []

    general_set_id = get_primary_question_set_id()
    game_players = [{"number": 1, "name": "Ana"}, {"number": 2, "name": "Carlos"}]
    bank = api_get("/api/questions/bank")
    assert bank["summary"]["total_count"] >= 6
    results.append("Prueba 1 OK: banco muestra preguntas existentes")

    created = api_request(
        "POST",
        "/api/questions",
        {
            "text": "Pregunta de prueba automatizada",
            "option_a": "Opción A test",
            "option_b": "Opción B test",
            "option_c": "Opción C test",
            "option_d": "Opción D test",
            "correct_answer": "B",
            "explanation": "Explicación de prueba",
            "active": True,
        },
    )
    created_id = created["id"]
    fetched = api_get(f"/api/questions/{created_id}")
    assert fetched["text"] == "Pregunta de prueba automatizada"
    results.append("Prueba 2 OK: nueva pregunta persistida")

    api_request(
        "PUT",
        f"/api/questions/{created_id}",
        {"text": "Pregunta editada automatizada"},
    )
    edited = api_get(f"/api/questions/{created_id}")
    assert edited["text"] == "Pregunta editada automatizada"
    results.append("Prueba 3 OK: edición persistida")

    duplicated = api_request("POST", f"/api/questions/{created_id}/duplicate")
    duplicate_id = duplicated["id"]
    assert duplicate_id != created_id
    results.append("Prueba 4 OK: duplicado con nuevo ID")

    api_request("PATCH", f"/api/questions/{created_id}/active", {"active": False})
    deactivated_bank = api_get("/api/questions/bank")
    deactivated = next(q for q in deactivated_bank["questions"] if q["id"] == created_id)
    assert deactivated["active"] is False
    active_questions = api_get("/api/questions")
    assert all(q["id"] != created_id for q in active_questions)
    results.append("Prueba 5 OK: desactivada no aparece en partidas nuevas")

    api_request("PATCH", f"/api/questions/{created_id}/active", {"active": True})
    reactivated = api_get(f"/api/questions/{created_id}")
    assert reactivated["active"] is True
    results.append("Prueba 6 OK: reactivada disponible nuevamente")

    while True:
        duplicate_item = api_get(f"/api/questions/{duplicate_id}")
        if duplicate_item["order"] == 1:
            break
        api_request("POST", f"/api/questions/{duplicate_id}/move", {"direction": "up"})
    active_bank_ids = [
        question["id"]
        for question in api_get("/api/questions/bank")["questions"]
        if question["active"]
    ]
    api_request(
        "PUT",
        f"/api/question-sets/{general_set_id}",
        {"question_ids": active_bank_ids},
    )
    order_game = create_game(general_set_id, game_players)
    assert order_game["current_question"]["text"] == duplicate_item["text"]
    results.append("Prueba 7 OK: orden del banco respetado en partida")

    snapshot_game = create_game(general_set_id, game_players)
    snapshot_game_id = snapshot_game["id"]
    original_text = snapshot_game["current_question"]["text"]
    bank_for_snapshot = api_get("/api/questions/bank")
    source_question = next(
        question for question in bank_for_snapshot["questions"] if question["text"] == original_text
    )
    api_request(
        "PUT",
        f"/api/questions/{source_question['id']}",
        {"text": "TEXTO MODIFICADO DESPUÉS DEL SNAPSHOT"},
    )
    old_game = api_get(f"/api/games/{snapshot_game_id}")
    assert old_game["current_question"]["text"] == original_text
    new_game = create_game(general_set_id, game_players)
    assert new_game["current_question"]["text"] == "TEXTO MODIFICADO DESPUÉS DEL SNAPSHOT"
    results.append("Prueba 8 OK: partida existente conserva snapshot")
    results.append("Prueba 9 OK: partida nueva usa versión modificada")

    bank_all = api_get("/api/questions/bank")
    for question in bank_all["questions"]:
        api_request("PATCH", f"/api/questions/{question['id']}/active", {"active": False})
    try:
        create_game(general_set_id, game_players)
        raise AssertionError("Debería fallar sin preguntas activas")
    except RuntimeError as error:
        assert "no contiene preguntas activas" in str(error)
    for question in bank_all["questions"][:6]:
        api_request("PATCH", f"/api/questions/{question['id']}/active", {"active": True})
    results.append("Prueba 10 OK: bloqueo sin preguntas activas")

    integrity_game = create_game(general_set_id, game_players)
    integrity_game_id = integrity_game["id"]
    integrity_text = integrity_game["current_question"]["text"]
    api_request("DELETE", f"/api/questions/{duplicate_id}")
    after_delete = api_get(f"/api/games/{integrity_game_id}")
    assert after_delete["current_question"]["text"] == integrity_text
    results.append("Prueba 11 OK: eliminar del banco no rompe partida existente")

    final_game = create_game(general_set_id, game_players)
    total_questions = final_game["total_questions"]
    await ws_play_one_game(final_game["id"], total_questions)
    finished = api_get(f"/api/games/{final_game['id']}")
    assert finished["status"] == "FINISHED"
    assert finished["players"][0]["score"] == total_questions * get_correct_answer_points()
    results.append("Prueba 12 OK: juego completo sigue funcionando")

    api_request("DELETE", f"/api/questions/{created_id}")

    print("\n".join(results))


if __name__ == "__main__":
    asyncio.run(main())
