# 🐺 Jager AI — Intelligence Agent for the Binance Ecosystem

> *Every BNB is made of Jägers. Every good decision is made of small insights.*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Telegram](https://img.shields.io/badge/Interface-Telegram%20Bot-blue)](https://telegram.org)
[![Web3](https://img.shields.io/badge/Framework-OpenClaw%20Compatible-black)](https://github.com/openclaw)
[![Binance](https://img.shields.io/badge/Ecosystem-Binance-F0B90B)](https://binance.com)

---

**An OpenClaw-compatible AI intelligence assistant for the Binance ecosystem, demonstrated through a Telegram interface and a visual command-center prototype.**

## The Name

**Jager** was one of the earliest Binance Angels — a community figure whose name became synonymous with the idea of a very small, fundamental unit of BNB, similar to how *Satoshi* is the smallest unit of Bitcoin.

One Jäger = `0.00000001 BNB`.

This project embraces that metaphor: just as many small Jägers form the value of BNB, many small insights form better decisions for crypto users.

**Jager AI is the intelligence layer that delivers those insights.**

---

## What It Does

Jager AI is designed to help users interact more intelligently and safely with the Binance ecosystem. By adhering to agentic design patterns, it serves as a robust reconnaissance node.

### Four Core Intelligence Modules

| Module | Function |
|--------|----------|
| 🔴 **Threat Hunter** | Detects scams, phishing, seed phrase requests, impersonation |
| 💰 **Opportunity Hunter** | Surfaces Binance products relevant to your goals (live BNB price) |
| 📡 **Market Hunter** | Delivers narrative-level market intelligence from public data |
| ⚠️ **Risk Hunter** | Flags dangerous trading behavior with educational warnings |

---

## Demo

```
User: Someone from Binance support asked me for my seed phrase.

Jager AI:
🚨 Threat Hunter — CRITICAL RISK DETECTED

🔴 CRITICAL — Seed Phrase / Private Key Request

What you should know:
• Binance staff will never ask for your seed phrase or private keys.
• Binance support contacts you through official channels only.
• Report this at support.binance.com.
```

```
User: I hold BNB. What can I do with it?

Jager AI:
🎯 Opportunity Hunter

💰 BNB Price: $612.45 📈 +2.3% (24h)

🌱 Binance Launchpool
   Stake BNB to farm newly listed tokens for free.
   🔗 https://launchpool.binance.com

💰 Simple Earn
   Earn 1–8% APR on your BNB, flexible or locked.
   🔗 https://www.binance.com/en/earn

⛓️ BNB Chain Staking
   Delegate BNB to validators to earn staking rewards.
   🔗 https://www.bnbchain.org/en/staking
```

---

## Visual Command Center

As part of the intelligence suite, Jager AI includes a **Cinematic 3D Mission Control** interface (`demo_interface_3d.html`). 

This command center connects directly to the Python backend via WebSockets, allowing you to watch the Jager AI agents (Threat, Market, Risk, Opportunity) coordinate in real-time on a holographic Binance-themed command ship while interacting via Telegram.

---

## Architecture

```
User Message (Telegram)
        │
        ▼
   OpenClaw Compatible
      Intent Router
        │
   ┌────┴─────────────────────────────┐
   │                                  │
   ▼                                  ▼
Local Pattern Matching          Claude AI (Anthropic)
(Threat / Risk Hunter)          (General Intelligence)
        │                              │
        ▼                              │
 Binance Public API ◄──────────────────┘
 (Opportunity / Market Hunter)
        │
        ▼
 Structured Response (Telegram + 3D Command Center WS)
```

- **No API key required** for Binance data — 100% public endpoints only
- **No database** — lightweight, runs on any machine
- **No GPU** — runs on any laptop including older hardware
- **Per-chat conversation memory** — context-aware responses

---

## Quick Start

### Requirements

- Python 3.11+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- An Anthropic API Key

### Installation

```bash
# Clone the repository
git clone https://github.com/kaizenbnb/JAGER-AI.git
cd JAGER-AI

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY
```

### Running (including older/low-spec laptops)

```bash
python main.py
```

That's it. The bot starts polling Telegram immediately.

---

## Project Structure

```
JAGER-AI/
├── main.py                    # Core agent + Telegram/WebSocket orchestrator
├── config.py                  # Environment & settings
├── demo_interface_3d.html     # Cinematic 3D Visual Command Center
├── demo_interface.html        # 2D Backup Interface
├── .env.example
├── prompts/
│   └── system_prompt.txt      # Agent identity & OpenClaw alignment
├── tools/
│   ├── threat_hunter.py       # Scam detection (pattern-based)
│   ├── opportunity_hunter.py  # Product discovery (live price)
│   ├── risk_hunter.py         # Trading risk education
│   └── market_hunter.py       # Narrative market intelligence
├── utils/
│   └── binance_public.py      # Binance public API wrapper
└── assets/
    └── logo.png
```

---

## Value for the Binance Ecosystem

| Challenge | How Jager AI Helps |
|-----------|-------------------|
| Rising scam activity | Instant pattern-based threat detection |
| Underutilization of products | Contextual, goal-based product discovery |
| Information overload | Narrative summaries instead of raw data |
| Poor risk management | Educational warnings before dangerous trades |

Jager AI demonstrates how AI agents can become an intelligent interface layer between users and the complexity of modern crypto ecosystems.

---

## Roadmap

- [ ] Portfolio analytics module
- [ ] Narrative sentiment tracking via social APIs
- [ ] Multi-language support
- [ ] Webhook deployment mode (production)
- [ ] BNB Chain on-chain activity monitoring

---

## Technical Notes

- All Binance data uses **public API endpoints only** — no personal API key, zero account risk
- Threat Hunter uses **local pattern matching** + LLM fallback — honest about its approach
- Market Hunter uses **live candlestick + ticker data** for real context, not hardcoded narratives
- Opportunity Hunter matches user goals to products using **keyword scoring**

---

## License

MIT License — see [LICENSE](LICENSE)

---

*Built for the Binance ecosystem. Powered by small insights.*
*Every BNB is made of Jägers. Every good decision is made of small insights.*
