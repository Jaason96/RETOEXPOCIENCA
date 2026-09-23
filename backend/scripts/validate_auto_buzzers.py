"""Validation for automatic buzzer activation flow."""
import asyncio
import json
import urllib.request

import websockets

API = "http://localhost:8000"


def api_post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    request = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def api_get(path: str) -> dict:
    with urllib.request.urlopen(f"{API}{path}") as response:
        return json.loads(response.read())


def get_primary_question_set_id() -> int:
    question_sets = api_get("/api/question-sets")
    preferred = next(
        (item["id"] for item in question_sets if item["name"] == "Lista General"),
        None,
    )
    if preferred is not None:
        return preferred

    seeded = next(item["id"] for item in question_sets if item["question_count"] > 0)
    return seeded


def get_correct_answer_points() -> int:
    config = api_get("/api/event-config")
    return int(config["correct_answer_points"])


async def ws_roundtrip(game_id: int, actions: list[dict]) -> list[dict]:
    messages: list[dict] = []
    uri = f"ws://localhost:8000/ws/games/{game_id}"

    async with websockets.connect(uri) as websocket:
        initial = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
        messages.append(initial)

        for action in actions:
            await websocket.send(json.dumps(action))
            while True:
                message = json.loads(await asyncio.wait_for(websocket.recv(), timeout=5))
                messages.append(message)
                if message["type"] in {"game_state", "error"}:
                    break

    return messages


async def main() -> None:
    results: list[str] = []

    players = [
        {"number": 1, "name": "Ana"},
        {"number": 2, "name": "Carlos"},
        {"number": 3, "name": "Nicolás"},
        {"number": 4, "name": "Laura"},
    ]
    question_set_id = get_primary_question_set_id()
    game_id = api_post(
        "/api/games",
        {"question_set_id": question_set_id, "players": players},
    )["id"]

    game = api_get(f"/api/games/{game_id}")
    assert game["status"] == "BUZZ_OPEN", "La primera pregunta debe iniciar con pulsadores activos"
    results.append("Prueba 1 OK: primera pregunta con pulsadores activos automáticamente")

    buzz_messages = await ws_roundtrip(game_id, [{"action": "register_buzz", "player_number": 3}])
    buzz_states = [m["payload"] for m in buzz_messages if m["type"] == "game_state"]
    assert buzz_states[-1]["status"] == "BUZZ_LOCKED"
    assert buzz_states[-1]["buzz_player"]["name"] == "Nicolás"
    results.append("Prueba 2 OK: Nicolás pulsó primero y los demás quedaron bloqueados")

    reset_messages = await ws_roundtrip(game_id, [{"action": "reset_buzzers"}])
    reset_states = [m["payload"] for m in reset_messages if m["type"] == "game_state"]
    assert reset_states[-1]["status"] == "BUZZ_OPEN"
    assert reset_states[-1]["buzz_player"] is None
    results.append("Prueba 3 OK: reiniciar pulsadores limpia el buzz accidental")

    await ws_roundtrip(game_id, [{"action": "register_buzz", "player_number": 3}])
    current = api_get(f"/api/games/{game_id}")
    correct = current["current_question"]["correct_answer"]
    wrong = next(letter for letter in ["A", "B", "C", "D"] if letter != correct)

    fail_messages = await ws_roundtrip(game_id, [{"action": "submit_answer", "answer": wrong}])
    fail_states = [m["payload"] for m in fail_messages if m["type"] == "game_state"]
    assert fail_states[-1]["status"] == "BUZZ_OPEN"
    nicolas = next(p for p in fail_states[-1]["players"] if p["name"] == "Nicolás")
    assert nicolas["score"] == 0
    results.append("Prueba 4 OK: Nicolás falló y los demás pueden pulsar automáticamente")

    current = api_get(f"/api/games/{game_id}")
    correct = current["current_question"]["correct_answer"]
    win_messages = await ws_roundtrip(
        game_id,
        [
            {"action": "register_buzz", "player_number": 1},
            {"action": "submit_answer", "answer": correct},
        ],
    )
    win_states = [m["payload"] for m in win_messages if m["type"] == "game_state"]
    win_results = [m["payload"] for m in win_messages if m["type"] == "answer_result"]
    assert win_results[-1]["is_correct"] is True
    assert win_results[-1]["player_name"] == "Ana"
    assert win_results[-1]["points_awarded"] == get_correct_answer_points()
    ana = next(p for p in win_states[-1]["players"] if p["name"] == "Ana")
    assert ana["score"] == get_correct_answer_points()
    results.append(f"Prueba 5 OK: Ana acertó y sumó +{get_correct_answer_points()}")

    next_messages = await ws_roundtrip(game_id, [{"action": "next_question"}])
    next_states = [m["payload"] for m in next_messages if m["type"] == "game_state"]
    next_game = next_states[-1]
    assert next_game["status"] == "BUZZ_OPEN"
    assert next_game["buzz_player"] is None
    assert next_game["failed_player_ids"] == []
    results.append("Prueba 6 OK: siguiente pregunta con pulsadores automáticamente activos")

    repeat_messages = await ws_roundtrip(
        game_id,
        [{"action": "register_buzz", "player_number": 2}],
    )
    repeat_states = [m["payload"] for m in repeat_messages if m["type"] == "game_state"]
    assert repeat_states[-1]["buzz_player"]["name"] == "Carlos"
    results.append("Prueba 7 OK: una sola pulsación válida por tecla (sin repeat manual en script)")

    race_game_id = api_post(
        "/api/games",
        {"question_set_id": question_set_id, "players": players},
    )["id"]
    race_messages = await ws_roundtrip(
        race_game_id,
        [
            {"action": "register_buzz", "player_number": 1},
            {"action": "register_buzz", "player_number": 2},
            {"action": "register_buzz", "player_number": 3},
        ],
    )
    race_states = [m["payload"] for m in race_messages if m["type"] == "game_state"]
    first_winner = race_states[1]["buzz_player"]["name"]
    assert race_states[-1]["buzz_player"]["name"] == first_winner
    results.append("Prueba 8 OK: solo el primer buzz válido gana en ráfaga")

    print("\n".join(results))


if __name__ == "__main__":
    asyncio.run(main())
