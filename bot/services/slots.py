"""
Slot generation / monitoring service.
In production you replace the generator with real portal polling
(httpx + browser automation or reverse-engineered endpoints).
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict
import uuid

def generate_slots(city: str, visa_type: str, category: str, count: int = 4) -> List[Dict]:
    """Generate realistic future weekday slots for demo / testing."""
    slots = []
    base = datetime.now() + timedelta(days=1)
    used_dates = set()

    while len(slots) < count:
        offset = random.randint(1, 60)
        day = base + timedelta(days=offset)
        if day.weekday() >= 5:  # skip weekend
            continue
        date_str = day.strftime("%Y-%m-%d")
        if date_str in used_dates:
            continue
        used_dates.add(date_str)
        hour = random.choice([8, 9, 10, 11, 13, 14, 15])
        minute = random.choice([0, 15, 30, 45])
        slots.append({
            "id": str(uuid.uuid4())[:8],
            "date": date_str,
            "time": f"{hour:02d}:{minute:02d}",
            "city": city,
            "visa_type": visa_type,
            "category": category,
            "center": city
        })

    slots.sort(key=lambda x: (x["date"], x["time"]))
    return slots
