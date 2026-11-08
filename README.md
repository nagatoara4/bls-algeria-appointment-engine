# BLS Algeria Appointment Engine — DEVIL v3.1

**Maximum aggression + Real Integration Layer.**

## Status

| Layer | State |
|-------|-------|
| Telegram control plane | ✅ Production |
| Concurrent swarms | ✅ Live |
| Account arsenal + health | ✅ Live |
| War room metrics | ✅ Live |
| **Real BLS portal bridge** | ⚡ Skeleton ready |
| Stealth browser | ⚡ Ready |
| Multi-account claim | ⚡ Ready |

## Real Layer (`bot/services/real_bls.py`)

This is the critical module. It contains:

- `BLSAccount` + session/cookie vault
- Stealth Playwright context factory
- `login()` / `ensure_session()`
- `fetch_available_slots()` — real date extraction point
- `attempt_claim()` — full booking pipeline
- `swarm_scan()` — parallel multi-account scanner

**To activate real mode:**

1. `pip install playwright && playwright install chromium`
2. Open `bot/services/monitor.py`
3. Set `USE_REAL = True`
4. Fill the TODO sections in `real_bls.py` with current selectors / endpoints
5. Add accounts via DB or future `/addaccount` command
6. Run with proxies if needed

## Why this is the strongest version

- The swarm engine already supports dozens of parallel scanners
- Account health rotation is implemented
- Claim pipeline is structured for multi-account race
- Stealth headers + anti-detect hooks are prepared
- Everything is async and cancellation-safe

The only remaining work is mapping the live BLS Algeria DOM / XHR to the functions already defined.

## Commands

- `/swarm` — launch devil scanner
- `/stopall` — kill all
- `/warroom` — live stats
- `/arsenal` — account pool
- `/book` — manual flow

## Disclaimer

Educational / research only.  
Respect laws and terms of service.  
Authors accept no liability.

---

**DEVIL v3.1** — ylivo4real 👾
