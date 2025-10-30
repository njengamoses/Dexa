from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from backend.brain import think
from datetime import datetime
import os

app = FastAPI(title="Dexa API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEMORY_FILE = "backend/memory.json"
MAX_MEMORY = 200

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(memory):
    # keep memory bounded
    memory = memory[-MAX_MEMORY:]
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

@app.get("/")
def root():
    return {"service": "Dexa API", "status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    if message is None:
        raise HTTPException(status_code=400, detail="No message provided")

    memory = load_memory()
    reply = think(message, memory)

    entry = {
        "time": datetime.utcnow().isoformat(),
        "user": message,
        "bot": reply
    }
    memory.append(entry)
    save_memory(memory)

    return {"reply": reply}

@app.get("/history")
async def history(limit: int = 50):
    memory = load_memory()
    return {"count": len(memory), "recent": memory[-limit:]}

@app.post("/clear")
async def clear():
    save_memory([])
    return {"status": "ok", "message": "memory cleared"}
