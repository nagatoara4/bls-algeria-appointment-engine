"""
Session helper.
Holds per-user booking context in memory (can be swapped to Redis later).
"""
from typing import Dict, Any

_sessions: Dict[int, Dict[str, Any]] = {}

def get_session(user_id: int) -> Dict[str, Any]:
    if user_id not in _sessions:
        _sessions[user_id] = {}
    return _sessions[user_id]

def clear_session(user_id: int) -> None:
    _sessions.pop(user_id, None)

def update_session(user_id: int, **kwargs) -> None:
    session = get_session(user_id)
    session.update(kwargs)
