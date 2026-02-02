import sqlite3
import os

DB_NAME = "mood_journal.db"

def check_db():
    if not os.path.exists(DB_NAME):
        print(f"Database {DB_NAME} does not exist.")
        return

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print("--- Moods ---")
    c.execute("SELECT * FROM moods")
    rows = c.fetchall()
    for row in rows:
        print(dict(row))

    print("--- Journals ---")
    c.execute("SELECT * FROM journals")
    rows = c.fetchall()
    for row in rows:
        print(dict(row))

    conn.close()

if __name__ == "__main__":
    check_db()
