from bot.services.slots import generate_slots

def test_generate_slots_count():
    slots = generate_slots("ALG1", "C - Short Stay", "Tourism", count=4)
    assert len(slots) == 4

def test_generate_slots_structure():
    slots = generate_slots("ORAN2", "D - Long Stay", "Study", count=2)
    for s in slots:
        assert "id" in s
        assert "date" in s
        assert "time" in s
        assert s["city"] == "ORAN2"
