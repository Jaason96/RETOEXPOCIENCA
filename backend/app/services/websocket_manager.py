from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[int, list[WebSocket]] = {}

    async def connect(self, game_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.setdefault(game_id, []).append(websocket)

    def disconnect(self, game_id: int, websocket: WebSocket) -> None:
        connections = self._connections.get(game_id, [])

        for index, connection in enumerate(connections):
            if connection is websocket:
                connections.pop(index)
                break

        if not connections:
            self._connections.pop(game_id, None)

    async def broadcast(self, game_id: int, message: dict) -> None:
        dead_connections: list[WebSocket] = []

        for connection in self._connections.get(game_id, []):
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        for websocket in dead_connections:
            self.disconnect(game_id, websocket)


connection_manager = ConnectionManager()
