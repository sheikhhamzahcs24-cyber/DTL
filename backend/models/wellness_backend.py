"""
Wellness Backend - Serves the trained 28-feature wellness model
Runs on Port 5001
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Initialize
lemmatizer = WordNetLemmatizer()

# Load wellness model and data
print("Loading wellness model...")
try:
    wellness_model = load_model('wellness_model.h5')
    
    # Fix for Windows encoding issues
    with open('wellness_words.pkl', 'rb') as f:
        wellness_words = pickle.load(f, encoding='latin1')
    
    with open('wellness_classes.pkl', 'rb') as f:
        wellness_classes = pickle.load(f, encoding='latin1')
    
    with open('wellness_module.json', encoding='utf-8') as f:
        wellness_intents = json.load(f)
    
    print(f"✅ Wellness model loaded successfully!")
    print(f"   - {len(wellness_classes)} wellness categories")
    print(f"   - {len(wellness_words)} vocabulary words")
except Exception as e:
    print(f"❌ Error loading wellness model: {e}")
    wellness_model = None

def clean_up_sentence(sentence):
    """Tokenize and lemmatize the sentence"""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    """Convert sentence to bag of words array"""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(wellness_words)
    for w in sentence_words:
        for i, word in enumerate(wellness_words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_wellness_class(sentence):
    """Predict the wellness intent class"""
    bow = bag_of_words(sentence)
    res = wellness_model.predict(np.array([bow]))[0]
    
    ERROR_THRESHOLD = 0.20  # Lower threshold for wellness queries
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    
    return_list = []
    for r in results:
        return_list.append({
            'intent': wellness_classes[r[0]], 
            'probability': str(r[1])
        })
    return return_list

def get_wellness_response(intents_list):
    """Get response from wellness intents"""
    if not intents_list:
        return None
    
    tag = intents_list[0]['intent']
    confidence = float(intents_list[0]['probability'])
    
    # Only return if confidence is reasonable
    if confidence < 0.25:
        return None
    
    for intent in wellness_intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return {
                'response': response,
                'intent': tag,
                'confidence': confidence
            }
    return None

@app.route('/chat', methods=['POST'])
def wellness_chat():
    """Handle wellness chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        if wellness_model is None:
            return jsonify({'error': 'Wellness model not loaded'}), 500
        
        # Predict intent
        intents = predict_wellness_class(message)
        result = get_wellness_response(intents)
        
        if result:
            return jsonify({
                'response': result['response'],
                'intent': result['intent'],
                'confidence': result['confidence'],
                'source': 'wellness_model'
            })
        else:
            return jsonify({
                'response': None,
                'message': 'No wellness match found'
            }), 404
            
    except Exception as e:
        print(f"Error in wellness chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': wellness_model is not None,
        'categories': len(wellness_classes) if wellness_model else 0,
        'features': [
            'Period Support', 'Music Therapy', 'Yoga', 'Breathing',
            'Self-Care', 'Sleep Support', 'Panic Attack Help',
            'Affirmations', 'Social Anxiety', 'Journaling',
            'Exam Stress', 'Procrastination', 'Grief Support',
            'Loneliness', 'Imposter Syndrome', 'Burnout',
            'Family Conflict', 'Comparison', 'Mindfulness',
            'Career Anxiety', 'Seasonal Depression', 'ADHD Tips',
            'Healthy Habits', 'Anger Management', 'Relationships',
            'Overthinking', 'Financial Anxiety', 'Period Emotional'
        ]
    })

if __name__ == '__main__':
    print("\n🌸 Starting Wellness Backend Server...")
    print("📍 Running on: http://localhost:5001")
    print("🎯 28 Mental Health Features Active\n")
    app.run(debug=True, port=5001)
