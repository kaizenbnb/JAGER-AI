"""
Jager AI — Binance Public API Layer
All calls use public endpoints only. No API key required. Zero risk.
"""

import httpx
from config import BINANCE_BASE_URL


async def get_bnb_price() -> float:
    """Returns current BNB/USDT spot price."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BINANCE_BASE_URL}/api/v3/ticker/price?symbol=BNBUSDT")
        r.raise_for_status()
        return float(r.json()["price"])


async def get_bnb_24h_stats() -> dict:
    """Returns 24h price change stats for BNB/USDT."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BINANCE_BASE_URL}/api/v3/ticker/24hr?symbol=BNBUSDT")
        r.raise_for_status()
        data = r.json()
        return {
            "price": float(data["lastPrice"]),
            "change_pct": float(data["priceChangePercent"]),
            "high_24h": float(data["highPrice"]),
            "low_24h": float(data["lowPrice"]),
            "volume": float(data["volume"]),
        }


async def get_top_gainers(limit: int = 5) -> list[dict]:
    """Returns top gaining pairs by 24h % change (spot market)."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BINANCE_BASE_URL}/api/v3/ticker/24hr")
        r.raise_for_status()
        tickers = r.json()

    usdt_pairs = [
        {
            "symbol": t["symbol"],
            "change_pct": float(t["priceChangePercent"]),
            "price": float(t["lastPrice"]),
            "volume": float(t["quoteVolume"]),
        }
        for t in tickers
        if t["symbol"].endswith("USDT") and float(t["quoteVolume"]) > 1_000_000
    ]

    return sorted(usdt_pairs, key=lambda x: x["change_pct"], reverse=True)[:limit]


async def get_bnb_klines(interval: str = "1d", limit: int = 7) -> list[dict]:
    """Returns recent candlestick data for BNB/USDT."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            f"{BINANCE_BASE_URL}/api/v3/klines",
            params={"symbol": "BNBUSDT", "interval": interval, "limit": limit},
        )
        r.raise_for_status()
        raw = r.json()

    return [
        {
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
        }
        for k in raw
    ]
