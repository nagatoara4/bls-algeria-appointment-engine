# BLS Algeria Appointment Engine — DEVIL v3.0

**Maximum aggression edition.**

Built for one goal: **highest possible appointment capture rate**.

This is no longer a normal bot.  
This is a high-frequency, multi-account, concurrent, stealth-oriented capture system.

> Educational / research tool. Use at your own risk and in accordance with applicable laws and terms of service.

## Devil Mode Features

- **Multi-account arsenal** — run dozens of BLS sessions in parallel
- **Ultra-fast concurrent scanners** — hundreds of checks per minute possible
- **Priority claim queue** — first-seen slot is attacked by multiple accounts instantly
- **Proxy / residential rotation ready**
- **Stealth fingerprints & header rotation**
- **Auto-retry + exponential backoff on every failure**
- **Instant Telegram alerts + auto-claim attempt**
- **Account health scoring & rotation**
- **Session persistence + cookie jar**
- **Rate-limit evasion patterns**
- **Admin war room** (live hits, success rate, account status)

## Architecture (v3)

```
Devil Core
├── Account Pool Manager
├── Proxy Rotator
├── Concurrent Scanner Swarm
├── Priority Claim Queue
├── Session & Cookie Vault
├── Stealth Layer
├── Notification & Auto-Claim
└── War Room Metrics
```

## Quick Start (Devil)

```bash
git clone https://github.com/nagatoara4/bls-algeria-appointment-engine.git
cd bls-algeria-appointment-engine
pip install -r requirements.txt
cp .env.example .env
# fill BOT_TOKEN, ADMIN_IDS, and optionally PROXY_LIST
python -m bot.main
```

## Commands (Devil)

| Command | Power |
|---------|-------|
| `/start` | Activate |
| `/arsenal` | Show account pool status |
| `/addaccount` | Add BLS account to pool |
| `/monitor` | Launch high-frequency scanner |
| `/swarm` | Start multi-account swarm on a target |
| `/warroom` | Live metrics & success rate |
| `/stopall` | Kill every scanner |
| `/claim` | Force claim attempt on latest hit |

## Performance Targets (v3 design)

- Sub-second reaction on slot appearance
- Multiple accounts attacking the same slot simultaneously
- Continuous health checks on every account
- Automatic removal of dead / banned sessions
- Configurable aggression level (1–10)

## Disclaimer

This software is provided for educational and research purposes only.  
The authors are not responsible for any misuse.  
Bypassing security systems or violating terms of service may be illegal.

---

**DEVIL v3.0** — built by ylivo4real 👾
