import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"

def _load() -> Dict[str, Any]:
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _save(data: Dict[str, Any]) -> None:
    USERS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def register_user(user_id: int, username: str | None = None) -> None:
    data = _load()
    key = str(user_id)
    if key not in data:
        data[key] = {
            "id": user_id,
            "username": username,
            "joined": True,
            "bookings": 0
        }
        _save(data)

def increment_booking(user_id: int) -> None:
    data = _load()
    key = str(user_id)
    if key in data:
        data[key]["bookings"] = data[key].get("bookings", 0) + 1
        _save(data)

def get_all_users() -> List[Dict[str, Any]]:
    return list(_load().values())

def get_user_count() -> int:
    return len(_load())
