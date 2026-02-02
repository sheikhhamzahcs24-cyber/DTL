# 🌸 Training Guide for Wellness Module Only

## Training the Comprehensive Wellness Model in Google Colab

This creates a **separate specialized model** with **28 mental health features** covering:
- Period support, sleep, panic attacks, grief, relationships
- Music therapy, yoga, breathing, mindfulness, meditation
- Exam stress, procrastination, career anxiety, ADHD tips
- Social anxiety, loneliness, imposter syndrome, burnout
- Family conflict, anger, financial anxiety, overthinking
- And much more!

This is a **COMPLETE mental wellness companion** - more comprehensive than most commercial apps!

### Step 1: Upload File to Colab
Upload **`wellness_module.json`** to your Colab notebook.

### Step 2: Run This Training Code

```python
import json
import numpy as np
import random
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Download NLTK
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

print('--- Loading wellness_module.json ---')
with open('wellness_module.json') as f:
    data = json.load(f)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Process patterns
for intent in data['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

print(f'Found {len(documents)} patterns and {len(classes)} wellness classes.')
print(f'Classes: {classes}')

pickle.dump(words, open('wellness_words.pkl', 'wb'))
pickle.dump(classes, open('wellness_classes.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in document[0]]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Build Neural Network (Larger for 28 classes)
print('--- Building Wellness Model ---')
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))  # Increased from 128
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))  # Increased from 64
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train (Increased epochs for 28 classes)
print('--- Training Wellness Model (400 Epochs) ---')
print('This will take 5-8 minutes. Be patient!')
hist = model.fit(np.array(train_x), np.array(train_y), epochs=400, batch_size=5, verbose=1)

# Save
model.save('wellness_model.h5')
print('✅ Wellness Model Trained & Saved!')

# Download files
from google.colab import files
files.download('wellness_model.h5')
files.download('wellness_words.pkl')
files.download('wellness_classes.pkl')

print('\n🌸 Download complete!')
print('Move these 3 files to your project folder:')
print('- wellness_model.h5')
print('- wellness_words.pkl')
print('- wellness_classes.pkl')
```

### Step 3: Test the Model (Optional)

After training, run this in a new cell to test:

```python
from tensorflow.keras.models import load_model
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import random

lemmatizer = WordNetLemmatizer()
model = load_model('wellness_model.h5')
words = pickle.load(open('wellness_words.pkl', 'rb'))
classes = pickle.load(open('wellness_classes.pkl', 'rb'))

with open('wellness_module.json') as f:
    intents = json.load(f)

def predict_wellness(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    
    res = model.predict(np.array([bag]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    
    if results:
        tag = classes[results[0][0]]
        confidence = results[0][1]
        
        for intent in intents['intents']:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                return response, tag, confidence
    
    return "Not sure", "unknown", 0.0

# Test it!
print("🧪 Testing Wellness Model\n")

test_messages = [
    "I have period pain",
    "Recommend some music",
    "I want to do yoga",
    "Breathing exercises please",
    "I can't sleep",
    "I'm having a panic attack",
    "I need positive affirmations",
    "I feel so alone",
    "Exam stress is killing me",
    "I'm procrastinating so much",
    "Someone died",
    "I'm so angry",
    "Breakup advice",
    "Can't stop overthinking",
    "Money problems"
]

for msg in test_messages:
    response, tag, conf = predict_wellness(msg)
    print(f"You: {msg}")
    print(f"Bot: {response[:100]}...")
    print(f"[Intent: {tag} | Confidence: {conf*100:.1f}%]\n")
```

### Expected Results:
- **28 classes**: period_pain, period_support, music_sad, yoga_request, breathing_exercise, self_care, sleep_support, panic_attack, affirmations, social_anxiety, journaling, exam_stress, procrastination, grief_support, loneliness, imposter_syndrome, burnout, family_conflict, comparison_jealousy, mindfulness_meditation, career_anxiety, seasonal_depression, adhd_focus, healthy_habits, anger_management, relationship_breakup, overthinking_decisions, financial_anxiety
- **Accuracy**: Should reach 92-97% (comprehensive but well-structured dataset)
- **Training time**: 5-8 minutes (400 epochs with 28 classes)

### Next Steps:
1. Download the 3 files
2. Place in your project folder
3. Your updated `backend.py` will automatically use both models!
