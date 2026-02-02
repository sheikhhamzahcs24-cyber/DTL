import sqlite3
import datetime
from typing import List, Dict

DB_NAME = "mood_journal.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create tables if not exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood_value INTEGER,
            note TEXT,
            timestamp TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized.")

def save_mood(mood: int, note: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    ts = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO moods (mood_value, note, timestamp) VALUES (?, ?, ?)", (mood, note, ts))
    conn.commit()
    conn.close()

def save_journal(entry: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    ts = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO journals (entry, timestamp) VALUES (?, ?)", (entry, ts))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Access columns by name
    c = conn.cursor()
    
    history = []
    
    # Get Moods
    c.execute("SELECT id, mood_value, note, timestamp FROM moods ORDER BY timestamp DESC LIMIT 50")
    for row in c.fetchall():
        history.append({
            "type": "mood",
            "val": row["mood_value"],
            "note": row["note"],
            "date": row["timestamp"]
        })
        
    # Get Journals
    c.execute("SELECT id, entry, timestamp FROM journals ORDER BY timestamp DESC LIMIT 50")
    for row in c.fetchall():
        history.append({
            "type": "journal",
            "text": row["entry"],
            "date": row["timestamp"]
        })
    
    conn.close()
    
    # Sort combined list by date descending
    history.sort(key=lambda x: x['date'], reverse=True)
    return history
