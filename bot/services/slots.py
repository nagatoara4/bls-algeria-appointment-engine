"""
High-quality slot generation / placeholder for real portal polling.
In production replace generate_slots with real HTTP/browser logic.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict
import uuid

def generate_slots(city: str, visa_type: str, category: str, count: int = 5) -> List[Dict]:
    slots = []
    base = datetime.now() + timedelta(days=1)
    used = set()

    while len(slots) < count:
        offset = random.randint(1, 75)
        day = base + timedelta(days=offset)
        if day.weekday() >= 5:
            continue
        date_str = day.strftime("%Y-%m-%d")
        if date_str in used:
            continue
        used.add(date_str)
        hour = random.choice([8, 9, 10, 11, 13, 14, 15])
        minute = random.choice([0, 15, 30, 45])
        slots.append({
            "id": str(uuid.uuid4())[:8],
            "date": date_str,
            "time": f"{hour:02d}:{minute:02d}",
            "city": city,
            "visa_type": visa_type,
            "category": category,
            "center": city,
            "score": random.randint(60, 99)
        })

    slots.sort(key=lambda x: (x["date"], x["time"]))
    return slots
