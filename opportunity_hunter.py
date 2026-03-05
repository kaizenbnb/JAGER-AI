"""
Jager AI — Opportunity Hunter
Surfaces relevant Binance ecosystem products based on user goals.
Uses live BNB price from public API + curated product knowledge.
"""

from utils.binance_public import get_bnb_price, get_bnb_24h_stats


# ── Product Catalog ────────────────────────────────────────────────────────
# Curated list of Binance products with descriptions and links.
# Update periodically as Binance launches new products.

PRODUCT_CATALOG = {
    "launchpool": {
        "name": "Binance Launchpool",
        "description": "Stake BNB, FDUSD or USDC to farm newly listed tokens for free.",
        "ideal_for": ["holding bnb", "passive income", "new tokens", "farming"],
        "url": "https://launchpool.binance.com",
        "emoji": "🌱",
    },
    "simple_earn": {
        "name": "Simple Earn",
        "description": "Earn yield on your BNB with flexible or locked terms (typically 1–8% APR).",
        "ideal_for": ["passive income", "holding bnb", "savings", "yield"],
        "url": "https://www.binance.com/en/earn",
        "emoji": "💰",
    },
    "bnb_fee_discount": {
        "name": "BNB Trading Fee Discount",
        "description": "Pay trading fees with BNB and receive a 25% discount on every trade.",
        "ideal_for": ["active trading", "reducing costs", "fees", "trading"],
        "url": "https://www.binance.com/en/fee/schedule",
        "emoji": "🏷️",
    },
    "bnb_chain_staking": {
        "name": "BNB Chain Staking",
        "description": "Delegate BNB to validators on BNB Chain to earn staking rewards.",
        "ideal_for": ["staking", "long term", "defi", "bnb chain"],
        "url": "https://www.bnbchain.org/en/staking",
        "emoji": "⛓️",
    },
    "launchpad": {
        "name": "Binance Launchpad",
        "description": "Commit BNB to participate in token sales before public listing.",
        "ideal_for": ["new tokens", "ido", "early access", "token sale"],
        "url": "https://launchpad.binance.com",
        "emoji": "🚀",
    },
    "bnb_vault": {
        "name": "BNB Vault",
        "description": "Combines Simple Earn, Launchpool and BEP20 savings in one auto-optimized product.",
        "ideal_for": ["auto", "optimize", "passive", "hands off"],
        "url": "https://www.binance.com/en/bnb",
        "emoji": "🔒",
    },
    "dual_investment": {
        "name": "Dual Investment",
        "description": "Sell BNB at a target price to earn enhanced yield while waiting for your target.",
        "ideal_for": ["target price", "sell orders", "enhanced yield", "options"],
        "url": "https://www.binance.com/en/dual-investment",
        "emoji": "📈",
    },
}


def _match_products(user_goal: str) -> list[dict]:
    """Matches user goal keywords to relevant products."""
    goal_lower = user_goal.lower()
    matched = []

    for key, product in PRODUCT_CATALOG.items():
        score = sum(1 for keyword in product["ideal_for"] if keyword in goal_lower)
        if score > 0:
            matched.append((score, product))

    # Sort by relevance score, return top 3
    matched.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in matched[:3]]


async def get_opportunities(user_goal: str = "") -> str:
    """
    Returns a formatted message with BNB price and relevant product suggestions.
    If no specific goal is provided, shows the top 3 most popular products.
    """
    try:
        stats = await get_bnb_24h_stats()
        price = stats["price"]
        change = stats["change_pct"]
        direction = "📈" if change >= 0 else "📉"
        change_str = f"{'+' if change >= 0 else ''}{change:.2f}%"
    except Exception:
        price = None
        change_str = "N/A"
        direction = "📊"

    price_line = (
        f"💰 **BNB Price:** ${price:,.2f} {direction} {change_str} (24h)\n\n"
        if price
        else "💰 **BNB Price:** Unavailable\n\n"
    )

    if user_goal:
        products = _match_products(user_goal)
        if not products:
            # Fallback to top 3 if no keyword match
            products = list(PRODUCT_CATALOG.values())[:3]
        intro = f"Based on your goal — **\"{user_goal}\"** — here are the most relevant Binance products:\n\n"
    else:
        products = list(PRODUCT_CATALOG.values())[:3]
        intro = "Here are the top Binance ecosystem opportunities for BNB holders:\n\n"

    product_lines = []
    for p in products:
        product_lines.append(
            f"{p['emoji']} **{p['name']}**\n"
            f"   {p['description']}\n"
            f"   🔗 {p['url']}"
        )

    products_text = "\n\n".join(product_lines)

    return (
        f"🎯 **Opportunity Hunter**\n\n"
        f"{price_line}"
        f"{intro}"
        f"{products_text}\n\n"
        f"_All products are official Binance offerings. This is not financial advice._"
    )
