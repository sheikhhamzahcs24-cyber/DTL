# How to Run the Mental Health Companion

## Quick Start Guide

### Step 1: Install Python Dependencies

Open terminal/command prompt and navigate to the project folder, then go to backend folder:

```bash
cd backend
pip install fastapi uvicorn pydantic
```

### Step 2: Start the Backend Server

While still in the `backend` folder, run:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see something like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal window open!** The backend needs to keep running.

### Step 3: Start the Frontend

Open a NEW terminal/command prompt window. Navigate to the project folder, then go to frontend folder:

```bash
cd frontend
```

Then start a simple web server. Choose one method:

**Option A - Python (easiest):**
```bash
python -m http.server 5500
```

**Option B - Node.js (if you have it):**
```bash
npx http-server -p 5500
```

### Step 4: Open in Browser

Open your web browser and go to:
```
http://localhost:5500
```

### Step 5: Allow Camera Access

When the page loads, your browser will ask for camera permission. Click "Allow" so the face tracking can work.

## Troubleshooting

**Backend not working?**
- Make sure you're in the `backend` folder when running uvicorn
- Check if port 8000 is already in use
- Make sure you installed all dependencies

**Frontend not connecting to backend?**
- Make sure backend is running on port 8000
- Check browser console (F12) for errors
- Make sure both servers are running

**Face mesh not working?**
- Check internet connection (MediaPipe loads from CDN)
- Make sure you allowed camera access
- Try refreshing the page

**Chat not working?**
- Make sure backend is running
- Check that API_BASE_URL in app.js is correct (should be http://localhost:8000)

## What Each Part Does

- **Backend (port 8000)**: Handles chat messages, mood logging, and journal entries
- **Frontend (port 5500)**: The website you see in the browser
- **Face Mesh**: Detects your facial expressions using your webcam (runs in browser)

## Stopping the Servers

Press `Ctrl+C` in each terminal window to stop the servers.

