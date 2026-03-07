"""
Jager AI — Market Hunter
Provides narrative-level market intelligence using live Binance public data.
No predictions. No advice. Just context.
"""

from utils.binance_public import get_bnb_24h_stats, get_top_gainers, get_bnb_klines


# ── Narrative Engine ───────────────────────────────────────────────────────

def _bnb_narrative(change_pct: float, price: float) -> str:
    """Generates a contextual BNB narrative based on price movement."""
    if change_pct >= 5:
        return (
            f"BNB is up **{change_pct:.1f}%** today — a strong move. "
            f"Historically, sharp BNB gains correlate with increased Launchpool activity and ecosystem momentum. "
            f"Worth checking if any new Launchpool campaigns just launched."
        )
    elif change_pct >= 2:
        return (
            f"BNB is showing positive momentum, up **{change_pct:.1f}%** today. "
            f"Moderate strength — could reflect broader market optimism or BNB-specific catalysts."
        )
    elif change_pct >= -2:
        return (
            f"BNB is relatively flat today (**{change_pct:+.1f}%**). "
            f"Consolidation periods often precede significant moves in either direction. "
            f"Good time to review your Launchpool and Earn positions."
        )
    elif change_pct >= -5:
        return (
            f"BNB is down **{abs(change_pct):.1f}%** today — mild correction territory. "
            f"Historically, BNB has recovered strongly from short-term dips. "
            f"Simple Earn and staking remain active regardless of price direction."
        )
    else:
        return (
            f"BNB is down **{abs(change_pct):.1f}%** today — a notable pullback. "
            f"Strong pullbacks can create opportunities for long-term accumulators. "
            f"Consider reviewing your risk exposure before making any moves."
        )


def _weekly_trend(klines: list[dict]) -> str:
    """Derives a simple trend description from 7-day candles."""
    if len(klines) < 2:
        return "Insufficient data for weekly trend."

    first_close = klines[0]["close"]
    last_close = klines[-1]["close"]
    weekly_change = ((last_close - first_close) / first_close) * 100

    highs = [k["high"] for k in klines]
    lows = [k["low"] for k in klines]
    weekly_high = max(highs)
    weekly_low = min(lows)

    trend = "uptrend 📈" if weekly_change > 1 else ("downtrend 📉" if weekly_change < -1 else "sideways 🔄")

    return (
        f"**7-Day Overview:**\n"
        f"• Trend: {trend}\n"
        f"• Weekly change: {weekly_change:+.2f}%\n"
        f"• 7-day high: ${weekly_high:,.2f}\n"
        f"• 7-day low: ${weekly_low:,.2f}"
    )


async def get_market_intelligence() -> str:
    """
    Returns a full market intelligence briefing for BNB.
    Includes price, narrative, weekly trend, and top gainers.
    """
    try:
        stats = await get_bnb_24h_stats()
        klines = await get_bnb_klines(interval="1d", limit=7)
        gainers = await get_top_gainers(limit=5)
    except Exception as e:
        return f"⚠️ **Market Hunter** — Data temporarily unavailable.\nPlease try again in a moment.\n\n_Error: {e}_"

    price = stats["price"]
    change = stats["change_pct"]
    high_24h = stats["high_24h"]
    low_24h = stats["low_24h"]
    volume = stats["volume"]

    narrative = _bnb_narrative(change, price)
    weekly = _weekly_trend(klines)

    direction = "📈" if change >= 0 else "📉"
    change_str = f"{'+' if change >= 0 else ''}{change:.2f}%"

    top_gainers_text = "\n".join(
        f"  {i+1}. **{g['symbol']}** {g['change_pct']:+.1f}%"
        for i, g in enumerate(gainers)
    )

    return (
        f"📡 **Market Hunter — BNB Intelligence Briefing**\n\n"
        f"**BNB/USDT** — ${price:,.2f} {direction} {change_str}\n"
        f"24h High: ${high_24h:,.2f} | Low: ${low_24h:,.2f}\n"
        f"24h Volume: {volume:,.0f} BNB\n\n"
        f"**Narrative:**\n{narrative}\n\n"
        f"{weekly}\n\n"
        f"**Top 5 Gainers (24h):**\n{top_gainers_text}\n\n"
        f"_Data sourced from Binance public API. This is market context, not financial advice._"
    )


async def get_quick_price() -> str:
    """Returns a one-line BNB price update."""
    try:
        stats = await get_bnb_24h_stats()
        price = stats["price"]
        change = stats["change_pct"]
        direction = "📈" if change >= 0 else "📉"
        return f"💰 **BNB:** ${price:,.2f} {direction} {change:+.2f}% (24h)"
    except Exception:
        return "💰 **BNB:** Price data temporarily unavailable."
