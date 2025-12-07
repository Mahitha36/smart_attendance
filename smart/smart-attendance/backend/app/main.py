from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware

from . import crud, schemas
from .deps import get_db

import uvicorn


app = FastAPI(title="Smart Attendance Backend")

# CORS settings – allows frontend (React) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # in production: put your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------ WebSocket Connection Manager ------------------ #
class ConnectionManager:
    def __init__(self):
        # list of currently connected websocket clients
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        """Accept a new WebSocket connection and store it."""
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        """Remove a WebSocket connection when it closes/errors."""
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: dict):
        """Send a JSON message to all connected WebSocket clients."""
        for c in list(self.active):  # make a copy of list to safely remove
            try:
                await c.send_json(message)
            except Exception:
                # if sending fails, drop that connection
                self.disconnect(c)


# single global manager object
manager = ConnectionManager()


# ------------------ REST API ENDPOINTS ------------------ #

@app.post("/api/events")
async def post_event(event: dict, db=Depends(get_db)):
    """
    1. Receive an event from inference pipeline (run_inference.py etc.)
    2. Store it in DB using crud.create_event
    3. Broadcast the event to all WebSocket clients (frontend live UI)
    """
    crud.create_event(db, event)
    await manager.broadcast({"type": "event", "payload": event})
    return {"status": "ok"}


@app.post("/api/enroll")
async def enroll(payload: schemas.EnrollIn, db=Depends(get_db)):
    """
    Enroll a student:
    - payload is validated by Pydantic schema EnrollIn
    - crud.create_student writes to DB
    - returns created student info (JSON)
    """
    student = crud.create_student(db, payload)
    return student


# ------------------ WEBSOCKET ENDPOINT ------------------ #

@app.websocket("/ws/live")
async def websocket_endpoint(ws: WebSocket):
    """
    WebSocket endpoint for live updates.
    Frontend connects here to receive:
      - events broadcast from /api/events
      - possibly future live video/behavior updates
    """
    await manager.connect(ws)
    try:
        while True:
            # just receive messages to keep connection alive
            # (client can send "ping" or anything)
            _ = await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)


# ------------------ LOCAL RUN ENTRYPOINT ------------------ #

if __name__ == "__main__":
    # Run using: python backend/app/main.py
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
