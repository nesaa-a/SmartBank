from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.core.websocket import websocket_manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    channel: str = Query(default="risk_alerts"),
):
    await websocket_manager.connect(websocket, channel=channel)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket, channel=channel)
