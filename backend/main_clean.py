from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from safety import is_crisis, crisis_message

app = FastAPI(
    title="Mental Health Companion API",
    description="Backend API for mental health companion with chat, mood tracking, and journaling",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    history: List[Dict]
    message: str

class ChatResponse(BaseModel):
    reply: str
    crisis: bool

class MoodRequest(BaseModel):
    mood: int
    note: str = ""

class JournalEntry(BaseModel):
    entry: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if is_crisis(req.message):
        return ChatResponse(
            reply=crisis_message(),
            crisis=True
        )
    
    reply = (
        "Thanks for sharing. I hear that you're going through a lot. "
        "Can you tell me more about how this is affecting your day? "
        "If you'd like, we can try a grounding exercise."
    )
    
    return ChatResponse(reply=reply, crisis=False)

@app.post("/mood")
def mood(req: MoodRequest):
    return {
        "status": "ok",
        "mood": req.mood,
        "note": req.note
    }

@app.post("/journal")
def journal(req: JournalEntry):
    return {
        "status": "saved",
        "summary": req.entry[:180]
    }

