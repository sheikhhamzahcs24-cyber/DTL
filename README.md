# Mental Health Companion Website

A web-based mental health companion with facial expression tracking using MediaPipe Face Mesh 468, chat support, mood logging, and journaling features.

## Features

- **Face Expression Tracking**: Real-time facial expression analysis using MediaPipe Face Mesh (468 points) to detect mood
- **Supportive Chat**: Crisis-aware chat interface with empathetic responses
- **Mood Check-in**: Manual mood logging (1-5 scale) with optional notes
- **Daily Journal**: Text-based journaling for reflection

## Setup Instructions

### Prerequisites

- Python 3.7+ (for backend)
- A modern web browser with camera access
- Internet connection (for MediaPipe CDN)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

3. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the frontend using any static file server. Options:

   **Option A: Python HTTP Server**
   ```bash
   python -m http.server 5500
   ```

   **Option B: Node.js http-server**
   ```bash
   npx http-server -p 5500
   ```

   **Option C: VS Code Live Server**
   - Install "Live Server" extension
   - Right-click `index.html` and select "Open with Live Server"

3. Open your browser and navigate to:
   ```
   http://localhost:5500
   ```

4. **Allow camera access** when prompted for face tracking to work

### API Configuration

If your backend is running on a different port or host, update the `API_BASE_URL` constant in `frontend/app.js`:

```javascript
const API_BASE_URL = "http://localhost:8000"; // Change this if needed
```

## Troubleshooting

### Chat Not Working

1. **Check if backend is running**: Make sure the FastAPI server is running on port 8000
2. **Check browser console**: Open Developer Tools (F12) and check for errors
3. **Verify API URL**: Ensure `API_BASE_URL` in `app.js` matches your backend address
4. **Check CORS**: The backend allows all origins in development mode

### Face Mesh Not Working

1. **Check internet connection**: MediaPipe loads from CDN
2. **Allow camera access**: Grant camera permissions when prompted
3. **Check browser console**: Look for MediaPipe loading errors
4. **Try refreshing**: Sometimes scripts need a moment to load

### Common Errors

- **"Failed to fetch"**: Backend server is not running or wrong URL
- **"FaceMesh library not loaded"**: Check internet connection and CDN availability
- **Camera not working**: Check browser permissions and ensure no other app is using the camera

## Project Structure

```
.
├── backend/
│   ├── main.py          # FastAPI backend with chat/mood/journal endpoints
│   └── safety.py        # Crisis detection utilities
├── frontend/
│   ├── index.html       # Main HTML file
│   ├── app.js           # Frontend JavaScript with face mesh integration
│   └── styles.css       # Website styling
└── README.md            # This file
```

## Important Notes

- **Not a substitute for professional help**: This is a supportive tool, not medical advice
- **Crisis detection**: If crisis keywords are detected, users are directed to emergency services
- **Privacy**: Face tracking happens entirely in the browser - no video is sent to servers
- **Development mode**: CORS is open for development; tighten for production

## API Endpoints

- `POST /chat` - Send chat message and get response
- `POST /mood` - Log mood (1-5 scale with optional note)
- `POST /journal` - Save journal entry

## License

This project is for educational purposes.

