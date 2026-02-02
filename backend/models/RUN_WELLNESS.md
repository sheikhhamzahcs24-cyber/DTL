# 🌸 Running Mind Connect with Wellness Features

## Quick Start (No Retraining Needed!)

### Step 1: Start Main Chatbot (Port 5000)
```powershell
cd "C:\Users\sahan\OneDrive\Desktop\dtl project mental health"
venv\Scripts\activate
python backend.py
```

### Step 2: Start Wellness Module (Port 5001)
Open a **NEW terminal window**:
```powershell
cd "C:\Users\sahan\OneDrive\Desktop\dtl project mental health"
venv\Scripts\activate
python wellness_api.py
```

### Step 3: Open the App
Double-click `index.html`

## What Works Now:

✅ **Main Chatbot** (Port 5000)
- Greetings, about, help
- Emotional support (sad, stressed, anxiety)
- All your trained intents

✅ **Wellness Module** (Port 5001) - NEW!
- Period pain support
- Music recommendations
- Yoga guidance
- Breathing exercises
- Self-care tips

## Try These:
- "I have period pain"
- "Recommend some music"
- "I want to do yoga"
- "Breathing exercises"
- "I need self care"

The system checks wellness module first (instant), then falls back to main chatbot!
