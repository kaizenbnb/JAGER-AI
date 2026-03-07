"""
Jager AI — Threat Hunter
Detects scam patterns in user-submitted messages.
Uses local pattern matching + LLM-assisted analysis.
"""

import re
from dataclasses import dataclass

# ── Pattern Library ────────────────────────────────────────────────────────

SEED_PHRASE_PATTERNS = [
    r"\bseed phrase\b",
    r"\brecovery phrase\b",
    r"\bmnemonic\b",
    r"\b12 words?\b",
    r"\b24 words?\b",
    r"\bprivate key\b",
    r"\bbackup phrase\b",
]

FAKE_SUPPORT_PATTERNS = [
    r"\bbinance support\b",
    r"\bofficial support\b",
    r"\baccount (will be|is being|has been) (suspended|blocked|frozen|disabled)\b",
    r"\bverify your (wallet|account|identity) (now|immediately|urgently)\b",
    r"\bcontact (our|the) support team\b",
    r"\bunauthorized (access|login|activity) detected\b",
]

IMPERSONATION_PATTERNS = [
    r"\bcz binance\b",
    r"\bchangpeng zhao\b",
    r"\bbinance ceo\b",
    r"\bofficial binance\b",
    r"\bbinance team\b",
]

URGENCY_PATTERNS = [
    r"\bact (now|immediately|fast|quickly)\b",
    r"\blimited time\b",
    r"\bexpires (today|soon|in \d+ hours?)\b",
    r"\blast chance\b",
    r"\burgent(ly)?\b",
]

FINANCIAL_BAIT_PATTERNS = [
    r"\bguaranteed (profit|return|gains?)\b",
    r"\b(double|triple|10x|100x) your (investment|money|bnb|bitcoin|crypto)\b",
    r"\bfree (bnb|bitcoin|crypto|tokens?|coins?)\b",
    r"\bairdrop.*click.*link\b",
    r"\bsend.*receive.*back\b",
]

ALL_PATTERNS = {
    "seed_phrase_request": SEED_PHRASE_PATTERNS,
    "fake_support": FAKE_SUPPORT_PATTERNS,
    "impersonation": IMPERSONATION_PATTERNS,
    "urgency_manipulation": URGENCY_PATTERNS,
    "financial_bait": FINANCIAL_BAIT_PATTERNS,
}

THREAT_LABELS = {
    "seed_phrase_request": "🔴 CRITICAL — Seed Phrase / Private Key Request",
    "fake_support": "🔴 HIGH — Fake Support / Account Threat",
    "impersonation": "🟠 HIGH — Impersonation Attempt",
    "urgency_manipulation": "🟡 MEDIUM — Urgency / Pressure Tactics",
    "financial_bait": "🟠 HIGH — Financial Bait / Too-Good-To-Be-True",
}


@dataclass
class ThreatResult:
    is_threat: bool
    threats_found: list[str]
    risk_level: str  # CRITICAL / HIGH / MEDIUM / LOW
    summary: str
    advice: str


def analyze_message(text: str) -> ThreatResult:
    """
    Analyzes a message for known scam patterns.
    Returns a ThreatResult with findings and advice.
    """
    text_lower = text.lower()
    threats_found = []

    for threat_type, patterns in ALL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                threats_found.append(threat_type)
                break  # one match per category is enough

    if not threats_found:
        return ThreatResult(
            is_threat=False,
            threats_found=[],
            risk_level="LOW",
            summary="No known scam patterns detected in this message.",
            advice="Stay vigilant. When in doubt, always verify through official Binance channels at binance.com.",
        )

    # Determine highest risk level
    if "seed_phrase_request" in threats_found or "fake_support" in threats_found:
        risk_level = "CRITICAL"
    elif "impersonation" in threats_found or "financial_bait" in threats_found:
        risk_level = "HIGH"
    else:
        risk_level = "MEDIUM"

    threat_labels = [THREAT_LABELS[t] for t in threats_found]
    summary = f"⚠️ {len(threats_found)} threat pattern(s) detected:\n" + "\n".join(
        f"  • {label}" for label in threat_labels
    )

    advice = _build_advice(threats_found)

    return ThreatResult(
        is_threat=True,
        threats_found=threats_found,
        risk_level=risk_level,
        summary=summary,
        advice=advice,
    )


def _build_advice(threats: list[str]) -> str:
    advice_lines = [
        "**What you should know:**",
        "• Binance staff will **never** ask for your seed phrase or private keys.",
        "• Binance support contacts you through official channels only (support.binance.com).",
        "• No legitimate airdrop or giveaway requires you to send funds first.",
        "• If your account has an issue, log in directly at binance.com — never via a link in a message.",
        "",
        "**Recommended actions:**",
        "• Do NOT share any sensitive information.",
        "• Do NOT click any links in the message.",
        "• Report the message at support.binance.com.",
    ]
    return "\n".join(advice_lines)


def format_threat_response(result: ThreatResult) -> str:
    """Formats a ThreatResult into a clean Telegram-ready message."""
    if not result.is_threat:
        return (
            f"✅ **Threat Hunter — Clear**\n\n"
            f"{result.summary}\n\n"
            f"💡 {result.advice}"
        )

    return (
        f"🚨 **Threat Hunter — {result.risk_level} RISK DETECTED**\n\n"
        f"{result.summary}\n\n"
        f"{result.advice}\n\n"
        f"_This analysis is pattern-based. When in doubt, contact Binance support directly._"
    )
