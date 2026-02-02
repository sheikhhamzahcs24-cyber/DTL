from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re

app = Flask(__name__)
CORS(app)

# Load wellness module
with open('wellness_module.json', 'r', encoding='utf-8') as f:
    wellness_data = json.load(f)

def match_wellness_intent(message):
    """Simple pattern matching for wellness features"""
    message_lower = message.lower()
    
    for intent in wellness_data['intents']:
        for pattern in intent['patterns']:
            # Convert pattern to regex (simple matching)
            pattern_lower = pattern.lower()
            if pattern_lower in message_lower or any(word in message_lower for word in pattern_lower.split()):
                return {
                    'tag': intent['tag'],
                    'response': random.choice(intent['responses']),
                    'confidence': 0.95
                }
    
    return None

@app.route('/api/wellness', methods=['POST'])
def wellness_chat():
    data = request.json
    message = data.get('message', '')
    
    # Check if it's a wellness-related query
    result = match_wellness_intent(message)
    
    if result:
        return jsonify({
            'response': result['response'],
            'intent': result['tag'],
            'confidence': result['confidence'],
            'type': 'wellness'
        })
    else:
        return jsonify({
            'response': None,
            'type': 'skip'
        })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'wellness_module'})

if __name__ == '__main__':
    print("🌸 Mind Connect Wellness Module Starting...")
    print("📡 Wellness API running on http://localhost:5001")
    print("\nSupports:")
    print("- Period pain support")
    print("- Music recommendations")
    print("- Yoga guidance")
    print("- Breathing exercises")
    print("- Self-care tips")
    app.run(debug=True, port=5001)
