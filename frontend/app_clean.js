const API_BASE_URL = "http://localhost:8000";

const chatLog = document.getElementById("chat-log");
const chatInput = document.getElementById("chat-message");
const sendBtn = document.getElementById("send-btn");

const moodButtons = document.querySelectorAll(".mood-btn");
const moodNoteInput = document.getElementById("mood-note");
const moodStatus = document.getElementById("mood-status");

const journalInput = document.getElementById("journal-entry");
const journalStatus = document.getElementById("journal-status");

const detectedMoodEl = document.getElementById("detected-mood");
const expressionCuesEl = document.getElementById("expression-cues");
const heroMoodEl = document.getElementById("hero-mood");
const heroCuesEl = document.getElementById("hero-cues");

const videoEl = document.getElementById("video");
const overlay = document.getElementById("overlay");
const ctx = overlay.getContext("2d");

let chatHistory = [];

function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = "chat-msg";
    div.innerHTML = `<strong>${role === "user" ? "You" : "Companion"}:</strong> ${text}`;
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendChat() {
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    chatHistory.push({ role: "user", content: message });
    chatInput.value = "";

    try {
        const res = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, history: chatHistory }),
        });

        if (!res.ok) {
            throw new Error(`Server error: ${res.status} ${res.statusText}`);
        }

        const data = await res.json();
        appendMessage("bot", data.reply);
        chatHistory.push({ role: "bot", content: data.reply });

        if (data.crisis) {
            alert("Crisis detected. Please reach out to emergency services or a crisis line immediately.");
        }

    } catch (err) {
        console.error("Chat error:", err);
        appendMessage("bot", `Sorry, I had trouble connecting. Error: ${err.message}. Make sure backend is running at ${API_BASE_URL}`);
    }
}

sendBtn.addEventListener("click", sendChat);
chatInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") sendChat();
});

async function logMood(mood) {
    const note = moodNoteInput.value.trim();
    moodStatus.textContent = "Saving...";

    try {
        await fetch(`${API_BASE_URL}/mood`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mood, note }),
        });

        moodStatus.textContent = "Saved ✔️";
        moodNoteInput.value = "";

    } catch (err) {
        console.error("Mood logging error:", err);
        moodStatus.textContent = `Could not save. Error: ${err.message}. Make sure backend is running at ${API_BASE_URL}`;
    }
}

moodButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        moodButtons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const moodValue = Number(btn.dataset.mood);
        logMood(moodValue);
    });
});

document.getElementById("save-journal-btn").addEventListener("click", async () => {
    const entry = journalInput.value.trim();
    if (!entry) {
        journalStatus.textContent = "Please write something before saving.";
        return;
    }

    journalStatus.textContent = "Saving...";

    try {
        await fetch(`${API_BASE_URL}/journal`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ entry }),
        });

        journalStatus.textContent = "Saved ✔️";
        journalInput.value = "";

    } catch (err) {
        console.error("Journal save error:", err);
        journalStatus.textContent = `Could not save. Error: ${err.message}. Make sure backend is running at ${API_BASE_URL}`;
    }
});

function drawLandmarks(landmarks) {
    ctx.clearRect(0, 0, overlay.width, overlay.height);
    ctx.fillStyle = "rgba(255, 0, 0, 0.6)";

    landmarks.forEach((pt) => {
        ctx.beginPath();
        ctx.arc(
            pt.x * overlay.width,
            pt.y * overlay.height,
            2,
            0,
            2 * Math.PI
        );
        ctx.fill();
    });
}

function interpretExpression(landmarks) {
    const xs = landmarks.map((p) => p.x);
    const ys = landmarks.map((p) => p.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    const width = maxX - minX;
    const height = maxY - minY;

    const mouthOpen = Math.abs(landmarks[13].y - landmarks[14].y) * height;
    const mouthWidth = Math.abs(landmarks[61].x - landmarks[291].x) * width;
    const cornerAvgY = (landmarks[61].y + landmarks[291].y) / 2;
    const smileCurve = (landmarks[13].y - cornerAvgY) * height;
    const browLift = ((landmarks[159].y + landmarks[386].y) / 2 -
        (landmarks[65].y + landmarks[295].y) / 2) * height;

    let mood = "Neutral";
    const cues = [];

    if (smileCurve < -0.02 && mouthOpen > 0.03) {
        mood = "Happy";
        cues.push("smile detected");
    } else if (browLift > 0.05 && mouthOpen > 0.02) {
        mood = "Surprised/Alert";
        cues.push("raised brows");
    } else if (smileCurve > 0.02 && mouthOpen < 0.025) {
        mood = "Sad";
        cues.push("downturned mouth");
    } else {
        mood = "Neutral";
        cues.push("neutral expression");
    }

    return { mood, cues: cues.join(", ") };
}

function onResults(results) {
    if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
        detectedMoodEl.textContent = "No face";
        expressionCuesEl.textContent = "Align face to camera";
        ctx.clearRect(0, 0, overlay.width, overlay.height);
        if (heroMoodEl) heroMoodEl.textContent = "No face";
        if (heroCuesEl) heroCuesEl.textContent = "Align face to camera";
        return;
    }

    const landmarks = results.multiFaceLandmarks[0];
    drawLandmarks(landmarks);

    const { mood, cues } = interpretExpression(landmarks);

    detectedMoodEl.textContent = mood;
    expressionCuesEl.textContent = cues;
    if (heroMoodEl) heroMoodEl.textContent = mood;
    if (heroCuesEl) heroCuesEl.textContent = cues;
}

function init() {
    if (typeof FaceMesh === 'undefined' || typeof Camera === 'undefined') {
        console.error("MediaPipe libraries not loaded. Check internet connection.");
        detectedMoodEl.textContent = "Error";
        expressionCuesEl.textContent = "MediaPipe libraries failed to load. Please refresh.";
        return;
    }

    const faceMesh = new FaceMesh({
        locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
        },
    });

    faceMesh.setOptions({
        maxNumFaces: 1,
        refineLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
    });

    faceMesh.onResults(onResults);

    const camera = new Camera(videoEl, {
        onFrame: async () => {
            await faceMesh.send({ image: videoEl });
        },
        width: 640,
        height: 480,
    });

    camera.start();
}

window.onload = init;

