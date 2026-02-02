# Backend API for mental health chatbot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from pydantic import BaseModel
from typing import List, Dict
from safety import is_crisis, crisis_message
import chat_engine  # Helper for ML model

app = FastAPI(
    title="Mental Health Companion API",
    description="Backend API for mental health companion with chat, mood tracking, and journaling",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Chat Engine on Startup
@app.on_event("startup")
async def startup_event():
    chat_engine.init()
    import database
    database.init_db()

# Models
class ChatRequest(BaseModel):
    history: List[Dict]
    message: str
    mood: str = "neutral"

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
    # Safety Check first (Overrides everything)
    if is_crisis(req.message):
        return ChatResponse(
            reply=crisis_message(),
            crisis=True
        )
    
    # AI Response
    try:
        # Pass history, mood, and context to engine
        reply = chat_engine.predict(req.message, req.history, mood_context=req.mood)
    except Exception as e:
        print(f"Chat Error: {e}")
        reply = "I'm having a bit of trouble connecting to my brain right now. Can we try again?"
        
    return ChatResponse(reply=reply, crisis=False)

@app.post("/mood")
def mood(req: MoodRequest):
    import database
    database.save_mood(req.mood, req.note)
    return {
        "status": "ok",
        "mood": req.mood,
        "note": req.note
    }

@app.post("/journal")
def journal(req: JournalEntry):
    import database
    database.save_journal(req.entry)
    return {
        "status": "saved",
        "summary": req.entry[:180]
    }

@app.get("/history")
def get_history():
    import database
    return database.get_history()