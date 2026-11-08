"""
Devil slot engine — high frequency, multi-account ready.
Replace generate_slots with real portal polling for live use.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict
import uuid

def generate_slots(city: str, visa_type: str, category: str, count: int = 6, aggression: int = 8) -> List[Dict]:
    """
    Aggression 1-10 controls how 'hot' the generated slots look.
    Higher aggression = more slots, closer dates, higher scores.
    """
    slots = []
    base = datetime.now() + timedelta(days=1)
    used = set()
    max_days = 90 - (aggression * 6)
    if max_days < 7:
        max_days = 7

    target = count + (aggression // 2)

    while len(slots) < target:
        offset = random.randint(1, max_days)
        day = base + timedelta(days=offset)
        if day.weekday() >= 5:
            continue
        date_str = day.strftime("%Y-%m-%d")
        if date_str in used:
            continue
        used.add(date_str)
        hour = random.choice([8, 9, 10, 11, 13, 14, 15])
        minute = random.choice([0, 15, 30, 45])
        score = random.randint(70 + aggression, 99)
        slots.append({
            "id": str(uuid.uuid4())[:8],
            "date": date_str,
            "time": f"{hour:02d}:{minute:02d}",
            "city": city,
            "visa_type": visa_type,
            "category": category,
            "center": city,
            "score": score,
            "priority": score
        })

    slots.sort(key=lambda x: (-x["priority"], x["date"], x["time"]))
    return slots[:count]
