// Update API calls to check wellness module first
const API_URL = 'http://localhost:5000/api';
const WELLNESS_API = 'http://localhost:5001/api';

// ... (keep existing code)

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    userInput.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        // First, check wellness module (faster, no ML needed)
        const wellnessResponse = await fetch(`${WELLNESS_API}/wellness`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        }).catch(() => null);

        if (wellnessResponse && wellnessResponse.ok) {
            const wellnessData = await wellnessResponse.json();

            if (wellnessData.type === 'wellness') {
                // Use wellness response
                removeTypingIndicator(typingId);
                addMessage(wellnessData.response, 'bot', {
                    intent: wellnessData.intent,
                    confidence: wellnessData.confidence
                });
                return;
            }
        }

        // If not wellness, use main chatbot
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        removeTypingIndicator(typingId);
        addMessage(data.response, 'bot', {
            intent: data.intent,
            confidence: data.confidence
        });

    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('Sorry, I\'m having trouble connecting. Please make sure the backend servers are running.', 'bot');
        console.error('Error:', error);
    }
}

// ... (keep rest of the code)
