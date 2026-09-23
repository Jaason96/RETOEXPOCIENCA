"""Validation for question sets (Phase 4.1)."""
import asyncio
import json
import urllib.error
import urllib.request

import websockets

API = "http://localhost:8000"


def api_request(method: str, path: str, payload: dict | None = None):
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


def api_get(path: str):
    return api_request("GET", path)


def get_correct_answer_points() -> int:
    config = api_get("/api/event-config")
    return int(config["correct_answer_points"])


def create_game(question_set_id: int, players=None):
    if players is None:
        players = [{"number": 1, "name": "Ana"}, {"number": 2, "name": "Carlos"}]
    return api_request("POST", "/api/games", {"question_set_id": question_set_id, "players": players})


async def play_full_game(game_id: int, total_questions: int) -> None:
    uri = f"ws://localhost:8000/ws/games/{game_id}"
    async with websockets.connect(uri) as websocket:
        await asyncio.wait_for(websocket.recv(), timeout=5)
        for _ in range(total_questions):
            state = api_get(f"/api/games/{game_id}")
            correct = state["current_question"]["correct_answer"]
            await websocket.send(json.dumps({"action": "register_buzz", "player_number": 1}))
            while json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))["type"] != "game_state":
                pass
            await websocket.send(json.dumps({"action": "submit_answer", "answer": correct}))
            while json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))["type"] != "game_state":
                pass
            state = api_get(f"/api/games/{game_id}")
            if state["current_question_index"] < total_questions:
                await websocket.send(json.dumps({"action": "next_question"}))
                while json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))["type"] != "game_state":
                    pass
        await websocket.send(json.dumps({"action": "finish_game"}))
        while json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))["type"] != "game_state":
            pass


async def main() -> None:
    results: list[str] = []

    sets = api_get("/api/question-sets")
    seeded = next((item for item in sets if item["question_count"] >= 5), None)
    assert seeded is not None and seeded["question_count"] > 0
    results.append(f"Prueba 1 OK: lista base '{seeded['name']}' con preguntas")

    bank = api_get("/api/questions/bank")
    active_ids = [question["id"] for question in bank["questions"] if question["active"]][:6]
    list_a = api_request(
        "POST",
        "/api/question-sets",
        {"name": "Lista A", "description": "Ronda 1", "question_ids": active_ids},
    )
    results.append("Prueba 2 OK: Lista A creada con 6 preguntas")

    other_ids = [question_id for question_id in active_ids[1:5]]
    list_b = api_request(
        "POST",
        "/api/question-sets",
        {"name": "Lista B", "description": "Ronda 2", "question_ids": other_ids},
    )
    results.append("Prueba 3 OK: Lista B creada con otras preguntas")

    shared_question_id = active_ids[0]
    list_b_with_shared = api_request(
        "PUT",
        f"/api/question-sets/{list_b['id']}",
        {"question_ids": [shared_question_id, *other_ids]},
    )
    list_a_detail = api_get(f"/api/question-sets/{list_a['id']}")
    list_b_detail = api_get(f"/api/question-sets/{list_b_with_shared['id']}")
    assert shared_question_id in [item["question_id"] for item in list_a_detail["items"]]
    assert shared_question_id in [item["question_id"] for item in list_b_detail["items"]]
    results.append("Prueba 4 OK: misma pregunta en A y B sin duplicar banco")

    first_in_a = list_a_detail["items"][0]["question_id"]
    api_request("POST", f"/api/question-sets/{list_a['id']}/move", {"question_id": first_in_a, "direction": "down"})
    list_a_moved = api_get(f"/api/question-sets/{list_a['id']}")
    list_b_unchanged = api_get(f"/api/question-sets/{list_b['id']}")
    assert list_a_moved["items"][0]["question_id"] != list_a_detail["items"][0]["question_id"]
    assert list_b_unchanged["items"] == list_b_detail["items"]
    results.append("Prueba 5 OK: orden independiente por lista")

    duplicated = api_request("POST", f"/api/question-sets/{list_a['id']}/duplicate")
    assert duplicated["id"] != list_a["id"]
    assert len(duplicated["items"]) == len(list_a_moved["items"])
    results.append("Prueba 6 OK: duplicar lista conserva preguntas")

    game_a = create_game(list_a["id"])
    first_text = game_a["current_question"]["text"]
    first_item = list_a_moved["items"][0]
    source = next(q for q in bank["questions"] if q["id"] == first_item["question_id"])
    assert first_text == source["text"]
    results.append("Prueba 7 OK: partida usa preguntas y orden de Lista A")

    api_request("PUT", f"/api/question-sets/{list_a['id']}", {"name": "Lista A modificada"})
    old_game = api_get(f"/api/games/{game_a['id']}")
    assert old_game["current_question"]["text"] == first_text
    results.append("Prueba 8 OK: partida existente no cambia al editar lista")

    new_game_a = create_game(list_a["id"])
    assert new_game_a["current_question"]["text"] == first_text
    results.append("Prueba 9 OK: nueva partida con lista modificada")

    game_b = create_game(list_b["id"])
    list_b_first = list_b_detail["items"][0]
    source_b = next(q for q in bank["questions"] if q["id"] == list_b_first["question_id"])
    assert game_b["current_question"]["text"] == source_b["text"]
    assert game_b["current_question"]["text"] != game_a["current_question"]["text"]
    results.append("Prueba 10 OK: partida con Lista B usa solo Lista B")

    deactivated_id = list_b_detail["items"][-1]["question_id"]
    active_count_before = sum(1 for item in list_b_detail["items"] if item["active"])
    api_request("PATCH", f"/api/questions/{deactivated_id}/active", {"active": False})
    game_b_filtered = create_game(list_b["id"])
    assert game_b_filtered["total_questions"] == active_count_before - 1
    api_request("PATCH", f"/api/questions/{deactivated_id}/active", {"active": True})
    results.append("Prueba 11 OK: pregunta inactiva excluida de nuevas partidas")

    list_b_id = list_b["id"]
    api_request("DELETE", f"/api/question-sets/{list_b_id}")
    remaining_bank = api_get("/api/questions/bank")
    assert any(question["id"] == deactivated_id for question in remaining_bank["questions"])
    results.append("Prueba 12 OK: eliminar lista no borra preguntas del banco")

    final_game = create_game(list_a["id"])
    await play_full_game(final_game["id"], final_game["total_questions"])
    finished = api_get(f"/api/games/{final_game['id']}")
    assert finished["status"] == "FINISHED"
    assert finished["players"][0]["score"] == finished["total_questions"] * get_correct_answer_points()
    results.append("Prueba 13 OK: juego completo funcional con lista")

    print("\n".join(results))


if __name__ == "__main__":
    asyncio.run(main())
