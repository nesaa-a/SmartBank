import asyncio
import json
from typing import Any

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = {
            "risk_alerts": set(),
            "general": set(),
        }
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, channel: str = "risk_alerts") -> None:
        await websocket.accept()
        async with self._lock:
            if channel not in self._connections:
                self._connections[channel] = set()
            self._connections[channel].add(websocket)

    async def disconnect(self, websocket: WebSocket, channel: str = "risk_alerts") -> None:
        async with self._lock:
            if channel in self._connections:
                self._connections[channel].discard(websocket)

    async def broadcast_json(self, message: dict[str, Any], channel: str = "risk_alerts") -> None:
        payload = json.dumps(message, default=str)
        async with self._lock:
            connections = list(self._connections.get(channel, set()))

        stale: list[WebSocket] = []
        for connection in connections:
            try:
                await connection.send_text(payload)
            except (WebSocketDisconnect, RuntimeError):
                stale.append(connection)

        if stale:
            async with self._lock:
                for connection in stale:
                    self._connections.get(channel, set()).discard(connection)


websocket_manager = ConnectionManager()
