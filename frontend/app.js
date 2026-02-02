// Enhanced Frontend code for mental health chatbot
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "http://localhost:8000"
    : "";

// DOM Elements
const chatLog = document.getElementById("chat-log");
const chatInput = document.getElementById("chat-message");
const sendBtn = document.getElementById("send-btn");

const moodButtons = document.querySelectorAll(".mood-btn");
const moodNoteInput = document.getElementById("mood-note");
const moodStatus = document.getElementById("mood-status");
const logMoodBtn = document.getElementById("log-mood-btn");

const journalInput = document.getElementById("journal-entry");
const journalStatus = document.getElementById("journal-status");

const detectedMoodEl = document.getElementById("detected-mood");
const expressionCuesEl = document.getElementById("expression-cues");
const heroMoodEl = document.getElementById("hero-mood");
const heroCuesEl = document.getElementById("hero-cues");

const videoEl = document.getElementById("video");
const overlay = document.getElementById("overlay");
const ctx = overlay ? overlay.getContext("2d") : null;

const historyList = document.getElementById("history-list");
const loadHistoryBtn = document.getElementById("load-history-btn");

let chatHistory = [];
let currentDetectedMood = "neutral";
let currentFilter = "all"; // all, mood, journal

// --- CHAT LOGIC ---

function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = `chat-msg ${role === "user" ? "user-msg" : "bot-msg"}`;

    // Basic markdown-ish parsing for bold and resources
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/📺 (.*?)\n/g, '<div class="resource-block">📺 $1</div>')
        .replace(/\n/g, '<br>');

    // Bubble structure
    div.innerHTML = `
        <div class="msg-bubble">
            <span class="role-label">${role === "user" ? "You" : "Companion"}</span>
            <div class="msg-text">${formattedText}</div>
        </div>
    `;

    chatLog.appendChild(div);

    // Smooth scroll to bottom
    chatLog.scrollTo({
        top: chatLog.scrollHeight,
        behavior: 'smooth'
    });
}

function showTypingIndicator() {
    const div = document.createElement("div");
    div.className = "chat-msg bot-msg typing-indicator";
    div.id = "typing";
    div.innerHTML = `
        <div class="msg-bubble">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function hideTypingIndicator() {
    const el = document.getElementById("typing");
    if (el) el.remove();
}

async function sendChat() {
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    chatHistory.push({ role: "user", content: message });
    chatInput.value = "";

    showTypingIndicator();

    try {
        const res = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                history: chatHistory,
                mood: currentDetectedMood
            }),
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        const data = await res.json();

        // Add a slight delay for realism
        setTimeout(() => {
            hideTypingIndicator();
            appendMessage("bot", data.reply);
            chatHistory.push({ role: "bot", content: data.reply });

            if (data.crisis) {
                const crisisDiv = document.createElement("div");
                crisisDiv.className = "crisis-alert";
                crisisDiv.innerHTML = "<strong>Safety Alert:</strong> If you're in immediate danger, please call emergency services (911/112).";
                chatLog.appendChild(crisisDiv);
            }
        }, 600);

    } catch (err) {
        hideTypingIndicator();
        console.error("Chat error:", err);
        appendMessage("bot", "I'm sorry, I'm having a hard time responding right now. Please check if the backend is running.");
    }
}

// Event Listeners
if (sendBtn && chatInput) {
    sendBtn.addEventListener("click", sendChat);
    chatInput.addEventListener("keyup", (e) => {
        if (e.key === "Enter") sendChat();
    });
}

// --- MOOD LOGGING ---
if (moodButtons.length > 0 && logMoodBtn) {
    let selectedMood = 0;
    moodButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            moodButtons.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            selectedMood = Number(btn.dataset.mood);
        });
    });

    logMoodBtn.addEventListener("click", async () => {
        if (selectedMood === 0) {
            moodStatus.textContent = "Please select a mood rating.";
            return;
        }
        moodStatus.textContent = "Saving...";
        try {
            await fetch(`${API_BASE_URL}/mood`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mood: selectedMood, note: moodNoteInput.value.trim() }),
            });
            moodStatus.textContent = "Saved to your history!";
            moodNoteInput.value = "";

            // Refresh history if we are on the history page or it exists
            if (historyList) loadHistory();
        } catch (err) {
            moodStatus.textContent = "Couldn't save mood. Is backend running?";
        }
    });
}

// --- JOURNAL ---
const saveJournalBtn = document.getElementById("save-journal-btn");
if (saveJournalBtn && journalInput) {
    saveJournalBtn.addEventListener("click", async () => {
        const entry = journalInput.value.trim();
        if (!entry) return;
        journalStatus.textContent = "Saving...";
        try {
            await fetch(`${API_BASE_URL}/journal`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ entry }),
            });
            journalStatus.textContent = "Journal entry saved.";
            journalInput.value = "";

            // Refresh history if it exists
            if (historyList) loadHistory();
        } catch (err) {
            journalStatus.textContent = "Error saving journal.";
        }
    });
}

// --- HISTORY ---
async function loadHistory() {
    if (!historyList) return;
    historyList.innerHTML = "Loading journey...";

    try {
        const res = await fetch(`${API_BASE_URL}/history`);
        const data = await res.json();

        historyList.innerHTML = "";

        // Filter the data based on current selection
        const filteredData = currentFilter === "all"
            ? data
            : data.filter(item => item.type === currentFilter);

        if (filteredData.length === 0) {
            const typeLabel = currentFilter === "all" ? "entries" : (currentFilter === "mood" ? "mood logs" : "journal entries");
            historyList.innerHTML = `<p class='muted'>No ${typeLabel} found. Start logging to see your journey.</p>`;
            return;
        }

        filteredData.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item card";
            const date = new Date(item.date).toLocaleString();

            if (item.type === "mood") {
                div.innerHTML = `
                    <div style="border-left: 4px solid var(--primary); padding-left: 15px;">
                        <span class="role-label" style="color: var(--primary)">Mood Log</span>
                        <div style="font-size: 1.2rem; font-weight: 700;">Rating: ${item.val}/5</div>
                        ${item.note ? `<p style="margin-top: 5px; font-style: italic;">"${item.note}"</p>` : ""}
                        <small class="muted">${date}</small>
                    </div>
                `;
            } else {
                div.innerHTML = `
                    <div style="border-left: 4px solid var(--secondary); padding-left: 15px;">
                        <span class="role-label" style="color: var(--secondary)">Journal Entry</span>
                        <p style="margin: 10px 0; font-size: 1.05rem;">${item.text}</p>
                        <small class="muted">${date}</small>
                    </div>
                `;
            }
            historyList.appendChild(div);
        });
    } catch (err) {
        historyList.innerHTML = `<p style="color: #ef4444;">Error loading history: ${err.message}</p>`;
    }
}

if (loadHistoryBtn) {
    loadHistoryBtn.addEventListener("click", () => loadHistory());
}

// History Tabs
const tabBtns = document.querySelectorAll(".tab-btn");
if (tabBtns.length > 0) {
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentFilter = btn.dataset.filter;
            loadHistory();
        });
    });
}

// --- FACE TRACKING ---
async function setupCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        videoEl.srcObject = stream;
        return new Promise(resolve => videoEl.onloadedmetadata = () => { videoEl.play(); resolve(); });
    } catch (err) {
        if (heroMoodEl) heroMoodEl.textContent = "Camera Blocked";
    }
}

async function loadModels() {
    const MODEL_URL = 'https://justadudewhohacks.github.io/face-api.js/models';
    try {
        await Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
            faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL)
        ]);
        return true;
    } catch (err) {
        return false;
    }
}

async function onPlay() {
    if (!videoEl || !overlay || typeof faceapi === 'undefined') return;

    const displaySize = { width: videoEl.width, height: videoEl.height };
    faceapi.matchDimensions(overlay, displaySize);

    setInterval(async () => {
        if (videoEl.paused || videoEl.ended) return;
        const detections = await faceapi.detectAllFaces(videoEl, new faceapi.TinyFaceDetectorOptions()).withFaceExpressions();

        if (ctx) ctx.clearRect(0, 0, overlay.width, overlay.height);

        if (detections.length > 0) {
            const expressions = detections[0].expressions;
            const sorted = Object.entries(expressions).sort((a, b) => b[1] - a[1]);
            const mood = sorted[0][0];
            const confidence = Math.round(sorted[0][1] * 100);

            currentDetectedMood = mood;
            const moodText = mood.charAt(0).toUpperCase() + mood.slice(1);

            // Update Hero elements (Home page)
            if (heroMoodEl) heroMoodEl.textContent = moodText;
            if (heroCuesEl) heroCuesEl.textContent = `${confidence}% confident`;

            // Update Stats elements (Face Tracking page)
            if (detectedMoodEl) detectedMoodEl.textContent = moodText;
            if (expressionCuesEl) expressionCuesEl.textContent = `${confidence}% confident`;

            // UI Color Pulse
            let color = "#8b5cf6";
            if (mood === 'happy') color = "#22c55e";
            if (mood === 'sad') color = "#3b82f6";
            if (mood === 'angry') color = "#ef4444";

            if (heroMoodEl) heroMoodEl.style.color = color;
            if (detectedMoodEl) detectedMoodEl.style.color = color;
        }
    }, 150);
}

// --- THEME MANAGEMENT ---
const themeToggle = document.getElementById("theme-toggle");
const body = document.body;

function toggleTheme() {
    body.classList.toggle("dark-theme");
    const isDark = body.classList.contains("dark-theme");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    updateThemeUI(isDark);
}

function updateThemeUI(isDark) {
    if (themeToggle) {
        themeToggle.innerHTML = isDark ? "☀️" : "🌙";
    }
}

// Init theme on load
(() => {
    const savedTheme = localStorage.getItem("theme");
    const isDark = savedTheme === "dark";
    if (isDark) {
        body.classList.add("dark-theme");
    }
    updateThemeUI(isDark);

    if (themeToggle) {
        themeToggle.addEventListener("click", toggleTheme);
    }
})();

// --- INIT ---
(async () => {
    // 1. Face tracking setup
    if (videoEl) {
        await setupCamera();
        await loadModels();
        onPlay();
    }

    // 2. History setup
    if (historyList) {
        loadHistory();
    }
})();
