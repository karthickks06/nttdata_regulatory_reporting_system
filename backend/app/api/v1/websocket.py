"""WebSocket endpoints for real-time updates"""

from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
import json

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect client"""
        await websocket.accept()

        if client_id not in self.active_connections:
            self.active_connections[client_id] = set()

        self.active_connections[client_id].add(websocket)

    def disconnect(self, websocket: WebSocket, client_id: str):
        """Disconnect client"""
        if client_id in self.active_connections:
            self.active_connections[client_id].discard(websocket)

            if not self.active_connections[client_id]:
                del self.active_connections[client_id]

    async def send_personal_message(self, message: dict, client_id: str):
        """Send message to specific client"""
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

    async def broadcast(self, message: dict):
        """Broadcast message to all clients"""
        for client_connections in self.active_connections.values():
            for connection in client_connections:
                try:
                    await connection.send_json(message)
                except:
                    pass


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time updates.

    Clients can subscribe to:
    - Workflow status updates
    - Agent execution progress
    - Report generation status
    - System notifications
    """
    await manager.connect(websocket, client_id)

    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        while True:
            # Receive messages from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                # Handle different message types
                message_type = message.get("type")

                if message_type == "ping":
                    # Respond to ping
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                elif message_type == "subscribe":
                    # Subscribe to specific topics
                    topics = message.get("topics", [])
                    await websocket.send_json({
                        "type": "subscribed",
                        "topics": topics,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                elif message_type == "unsubscribe":
                    # Unsubscribe from topics
                    topics = message.get("topics", [])
                    await websocket.send_json({
                        "type": "unsubscribed",
                        "topics": topics,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                else:
                    # Echo back unknown messages
                    await websocket.send_json({
                        "type": "echo",
                        "message": message,
                        "timestamp": datetime.utcnow().isoformat()
                    })

            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON",
                    "timestamp": datetime.utcnow().isoformat()
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)


async def send_workflow_update(workflow_id: int, status: str, data: dict = None):
    """Send workflow status update to all clients"""
    message = {
        "type": "workflow_update",
        "workflow_id": workflow_id,
        "status": status,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast(message)


async def send_agent_progress(agent_name: str, progress: float, message: str):
    """Send agent execution progress"""
    update = {
        "type": "agent_progress",
        "agent_name": agent_name,
        "progress": progress,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast(update)


async def send_notification(notification_type: str, message: str, severity: str = "info"):
    """Send system notification"""
    notification = {
        "type": "notification",
        "notification_type": notification_type,
        "message": message,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast(notification)
