# session_store.py
SESSIONS: dict[str, list[dict]] = {}

def get_history(session_id: str) -> list[dict]:
    return SESSIONS.get(session_id, [])

def append_turn(session_id: str, role: str, content: str):
    if session_id not in SESSIONS:
        SESSIONS[session_id] = []
    SESSIONS[session_id].append({"role": role, "content": content})
    # keep last 10 turns to bound context size
    SESSIONS[session_id] = SESSIONS[session_id][-10:]