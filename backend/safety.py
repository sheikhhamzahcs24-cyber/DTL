# keywords that indicate someone might be in crisis
# basic keyword matching - could be improved with NLP later
CRISIS_KEYWORDS = [
    "suicide",
    "kill myself",
    "end it",
    "can't go on",
    "harm myself",
    "hurt myself",
    "hurt others",
    "kill them",
    "overdose",
]

def is_crisis(text: str) -> bool:
    # check if text contains any crisis keywords
    # convert to lowercase so it's case insensitive
    lowered = text.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)

def crisis_message() -> str:
    return (
        "Please reach out for help right now:\n"
        "🆘 **Kiran Helpline:** 1800-599-0019\n"
        "🆘 **Tele MANAS:** 14416\n"
        "🚨 **Emergency:** 112\n"
        "You don't have to face this alone, bro."
    )

