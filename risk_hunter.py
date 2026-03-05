"""
Jager AI — Risk Hunter
Detects potentially dangerous trading behavior and provides educational warnings.
"""

import re
from dataclasses import dataclass


@dataclass
class RiskResult:
    risk_detected: bool
    risk_type: str
    risk_level: str  # EXTREME / HIGH / MEDIUM
    warning: str
    educational_note: str


# ── Risk Pattern Library ───────────────────────────────────────────────────

LEVERAGE_PATTERNS = {
    r"\b(50x|75x|100x|125x|1000x)\b": "EXTREME",
    r"\b(20x|25x|30x)\b": "HIGH",
    r"\b(10x|15x)\b": "MEDIUM",
}

MEMECOIN_PATTERNS = [
    r"\bmemecoin\b",
    r"\bmeme coin\b",
    r"\bdoge\b",
    r"\bshib\b",
    r"\bpepe\b",
    r"\bfloki\b",
    r"\bbonk\b",
    r"\bwif\b",
]

FOMO_PATTERNS = [
    r"\ball.?in\b",
    r"\bbetting everything\b",
    r"\bput(ting)? (my )?(all|everything|life savings)\b",
    r"\blast (chance|opportunity)\b",
    r"\bcan't miss\b",
    r"\bgoing to (moon|zero)\b",
]

OVERCONFIDENCE_PATTERNS = [
    r"\b(guaranteed|certain|definitely|100%)\b.*\b(profit|gain|moon|pump)\b",
    r"\bcan't lose\b",
    r"\bsure thing\b",
    r"\brisk.?free\b",
]


def analyze_risk(text: str) -> RiskResult:
    """Analyzes user input for risky trading behavior patterns."""
    text_lower = text.lower()

    # Check leverage
    for pattern, level in LEVERAGE_PATTERNS.items():
        if re.search(pattern, text_lower):
            leverage_match = re.search(r"\d+x", text_lower)
            leverage = leverage_match.group(0).upper() if leverage_match else "high"
            return RiskResult(
                risk_detected=True,
                risk_type="extreme_leverage",
                risk_level=level,
                warning=f"⚠️ **{level} RISK — {leverage} Leverage Detected**",
                educational_note=(
                    f"**What {leverage} leverage means:**\n"
                    f"• A 1% move against you = a significant % of your margin lost.\n"
                    f"• At 100x, a 1% adverse move = 100% margin loss (liquidation).\n"
                    f"• Liquidation happens fast — often before you can react.\n\n"
                    f"**Consider:**\n"
                    f"• Starting with 2x–5x to understand leverage mechanics.\n"
                    f"• Using stop-loss orders on every leveraged position.\n"
                    f"• Never risking more than you can afford to lose entirely."
                ),
            )

    # Check memecoin
    for pattern in MEMECOIN_PATTERNS:
        if re.search(pattern, text_lower):
            return RiskResult(
                risk_detected=True,
                risk_type="memecoin_exposure",
                risk_level="HIGH",
                warning="⚠️ **HIGH RISK — Memecoin / High-Volatility Asset**",
                educational_note=(
                    "**Memecoin risk profile:**\n"
                    "• Extreme volatility — can lose 80–99% in hours.\n"
                    "• Often driven by hype, not fundamentals.\n"
                    "• Low liquidity means exits can be difficult at scale.\n\n"
                    "**Consider:**\n"
                    "• Treating memecoins as a small, speculative allocation only.\n"
                    "• Never investing more than you are fully prepared to lose.\n"
                    "• Researching tokenomics and team before entering."
                ),
            )

    # Check FOMO / all-in behavior
    for pattern in FOMO_PATTERNS:
        if re.search(pattern, text_lower):
            return RiskResult(
                risk_detected=True,
                risk_type="fomo_allIn",
                risk_level="HIGH",
                warning="⚠️ **HIGH RISK — All-In / FOMO Behavior Detected**",
                educational_note=(
                    "**Why all-in is dangerous in crypto:**\n"
                    "• Even strong assets can drop 50–80% in bear markets.\n"
                    "• Concentration risk means one bad trade = total loss.\n\n"
                    "**Consider:**\n"
                    "• Position sizing: risk only a defined % of your portfolio per trade.\n"
                    "• Dollar-cost averaging (DCA) instead of lump-sum entries.\n"
                    "• Keeping a cash reserve to manage drawdowns calmly."
                ),
            )

    # Check overconfidence
    for pattern in OVERCONFIDENCE_PATTERNS:
        if re.search(pattern, text_lower):
            return RiskResult(
                risk_detected=True,
                risk_type="overconfidence",
                risk_level="MEDIUM",
                warning="⚠️ **MEDIUM RISK — Overconfidence Pattern Detected**",
                educational_note=(
                    "**In crypto, nothing is guaranteed:**\n"
                    "• Markets are unpredictable — even experienced traders lose.\n"
                    "• Overconfidence is one of the most common causes of large losses.\n\n"
                    "**Consider:**\n"
                    "• Always define your risk before entering a trade.\n"
                    "• Use stop-losses even when you are 'certain' about a trade.\n"
                    "• Past performance does not predict future results."
                ),
            )

    return RiskResult(
        risk_detected=False,
        risk_type="none",
        risk_level="LOW",
        warning="",
        educational_note="",
    )


def format_risk_response(result: RiskResult) -> str:
    """Formats a RiskResult into a clean Telegram-ready message."""
    if not result.risk_detected:
        return (
            "✅ **Risk Hunter — No Critical Patterns Detected**\n\n"
            "Always define your risk before entering any position.\n"
            "Use stop-losses, size positions responsibly, and never invest more than you can afford to lose."
        )

    return (
        f"🚨 **Risk Hunter**\n\n"
        f"{result.warning}\n\n"
        f"{result.educational_note}\n\n"
        f"_This is educational information only, not financial advice._"
    )
