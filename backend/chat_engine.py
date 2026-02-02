import os
import random
import json
from groq import Groq
from safety import is_crisis, crisis_message

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# Local Modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
intents = []

def init():
    global intents
    print("Initializing AI Engine with Wellness & KB Modules...")
    try:
        # Load Main KB
        kb_path = os.path.join(MODELS_DIR, "KB.json")
        if os.path.exists(kb_path):
            with open(kb_path, "r") as f:
                intents.extend(json.load(f).get("intents", []))
        
        # Load Wellness Module (User specifically requested this)
        wellness_path = os.path.join(MODELS_DIR, "wellness_module.json")
        if os.path.exists(wellness_path):
            with open(wellness_path, "r") as f:
                intents.extend(json.load(f).get("intents", []))
                
        print(f"Loaded {len(intents)} total intent categories.")
    except Exception as e:
        print(f"Error loading modules: {e}")

STOP_WORDS = {"a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "in", "on", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "it", "what", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "am", "u"}

def clean_text(text):
    import re
    text = text.lower()
    text = re.sub(r"[^\w\s']", "", text)
    return text

def get_kb_context(message):
    """Retrieve relevant responses from KB/Wellness to ground Groq's answers."""
    if not intents: return ""
    
    msg_clean = clean_text(message)
    msg_words = set(msg_clean.split())
    
    context_bits = []
    for intent in intents:
        for pattern in intent.get('patterns', []):
            pattern_words = set(clean_text(pattern).split())
            if pattern_words & msg_words:
                context_bits.append(f"Source Data for {intent['tag']}: {random.choice(intent['responses'])}")
                break 
    
    return "\n".join(context_bits[:3]) # Limit to top 3 relevant context bits

def get_journal_summary():
    """Fetch last 3 journal entries for life event memory."""
    try:
        import database
        history = database.get_history()
        journals = [h['text'] for h in history if h['type'] == 'journal'][:3]
        if not journals: return "No recent journals."
        return "User's Recent Journal Entries: " + " | ".join(journals)
    except:
        return ""

def get_fallback_response(message):
    if not intents: return "I'm here to listen."
    # (Basic keyword matching logic used for grounding but also for total failure fallback)
    msg_words = set(clean_text(message).split())
    for intent in intents:
        for pattern in intent.get('patterns', []):
            if set(clean_text(pattern).split()) & msg_words:
                return random.choice(intent['responses'])
    return "I'm listening. Tell me more about that?"

def predict(message, history=None, mood_context="neutral"):
    if is_crisis(message):
        return crisis_message()

    if client:
        try:
            # INTEGRATION: Grounding with Wellness Module and KB
            module_grounding = get_kb_context(message)
            journal_memory = get_journal_summary()
            
            system_instruction = (
                "You are a specialized Mental Health Companion.\n\n"
                "STRICT GROUNDING RULE:\n"
                f"Use the following SOURCE DATA to inform your tone and specific advice:\n{module_grounding}\n\n"
                "CONTEXT:\n"
                f"- Real-time user mood: {mood_context}\n"
                f"- User's recent journals: {journal_memory}\n\n"
                "RESPONSE RULES:\n"
                "1. Always respond line-by-line. Never write paragraphs.\n"
                "2. If identity is questioned, use the specific tone and phrasing from the SOURCE DATA provided above.\n"
                "3. Prioritize the advice (yoga, breathing, etc.) found in the SOURCE DATA.\n"
                "4. Be warm, brotherly, and empathetic.\n"
                "5. Conciseness: Maximum 3-4 lines."
            )

            messages = [{"role": "system", "content": system_instruction}]
            context_messages = (history or [])[-10:]
            for h in context_messages:
                role = "user" if h['role'] == 'user' else "assistant"
                messages.append({"role": role, "content": h['content']})
            
            messages.append({"role": "user", "content": message})
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=300,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq Error: {e}")
            return get_fallback_response(message)
    else:
        return get_fallback_response(message)
