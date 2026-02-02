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
    lowered = text.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)

def crisis_message() -> str:
    return (
        "I'm really sorry you're feeling this way. Your safety matters. "
        "If you are in immediate danger, please contact local emergency services. "
        "You can also reach out to a trusted person or a crisis line like 988 (US) "
        "or your country's emergency number."
    )

