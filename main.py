"""
Jager AI — Main Entry Point
Telegram bot powered by Claude (via Anthropic API).
Orchestrates the four intelligence modules as tools.

Run: python main.py
"""

import asyncio
import logging
from pathlib import Path

import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from rich.logging import RichHandler

import config
from tools.threat_hunter import analyze_message, format_threat_response
from tools.opportunity_hunter import get_opportunities
from tools.risk_hunter import analyze_risk, format_risk_response
from tools.market_hunter import get_market_intelligence, get_quick_price

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("jager-ai")

# ── Load System Prompt ─────────────────────────────────────────────────────
SYSTEM_PROMPT = Path(config.SYSTEM_PROMPT_PATH).read_text(encoding="utf-8")

# ── Anthropic Client ───────────────────────────────────────────────────────
anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

# ── Conversation History (in-memory, per chat_id) ──────────────────────────
conversation_history: dict[int, list[dict]] = {}

MAX_HISTORY = 20  # messages to keep per user


# ── Helper: Main Menu Keyboard ─────────────────────────────────────────────
def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔴 Threat Hunter", callback_data="menu_threat"),
            InlineKeyboardButton("💰 Opportunities", callback_data="menu_opportunity"),
        ],
        [
            InlineKeyboardButton("📡 Market Intel", callback_data="menu_market"),
            InlineKeyboardButton("⚠️ Risk Check", callback_data="menu_risk"),
        ],
        [
            InlineKeyboardButton("💰 BNB Price", callback_data="menu_price"),
            InlineKeyboardButton("❓ Help", callback_data="menu_help"),
        ],
    ])


# ── Helper: Detect intent and route to tool ────────────────────────────────
async def route_message(text: str) -> str:
    """
    Routes a message to the appropriate tool based on content,
    or falls back to Claude for general intelligence.
    """
    text_lower = text.lower()

    # Threat detection keywords
    threat_keywords = ["seed", "phrase", "private key", "support", "suspended",
                       "verify", "urgent", "scam", "phishing", "check this message",
                       "is this legit", "is this real"]
    if any(kw in text_lower for kw in threat_keywords):
        result = analyze_message(text)
        return format_threat_response(result)

    # Risk detection keywords
    risk_keywords = ["leverage", "100x", "50x", "20x", "all in", "all-in",
                     "memecoin", "meme coin", "yolo", "bet everything"]
    if any(kw in text_lower for kw in risk_keywords):
        result = analyze_risk(text)
        return format_risk_response(result)

    # Market intelligence keywords
    market_keywords = ["market", "price", "bnb price", "trend", "narrative",
                       "gainers", "briefing", "intel", "analysis"]
    if any(kw in text_lower for kw in market_keywords):
        return await get_market_intelligence()

    # Opportunity keywords
    opportunity_keywords = ["earn", "staking", "launchpool", "yield", "passive",
                             "what can i do", "opportunities", "products", "farming"]
    if any(kw in text_lower for kw in opportunity_keywords):
        return await get_opportunities(user_goal=text)

    # Fall back to Claude for general questions
    return None  # Signal to use Claude


async def ask_claude(chat_id: int, user_message: str) -> str:
    """Sends a message to Claude with conversation history."""
    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    conversation_history[chat_id].append({
        "role": "user",
        "content": user_message
    })

    # Trim history
    if len(conversation_history[chat_id]) > MAX_HISTORY:
        conversation_history[chat_id] = conversation_history[chat_id][-MAX_HISTORY:]

    response = anthropic_client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=conversation_history[chat_id],
    )

    assistant_reply = response.content[0].text

    conversation_history[chat_id].append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply


# ── Command Handlers ───────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "🐺 **Welcome to Jager AI**\n\n"
        "_Every BNB is made of Jägers._\n"
        "_Every good decision is made of small insights._\n\n"
        "I'm your intelligence agent for the Binance ecosystem. I can help you:\n\n"
        "🔴 **Detect scams** — paste any suspicious message\n"
        "💰 **Discover opportunities** — Launchpool, Earn, staking\n"
        "📡 **Read the market** — narrative-level BNB intelligence\n"
        "⚠️ **Assess trading risk** — before you make a move\n\n"
        "What would you like to explore?"
    )
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🐺 **Jager AI — Command Reference**\n\n"
        "/start — Welcome screen + main menu\n"
        "/price — Quick BNB price check\n"
        "/market — Full market intelligence briefing\n"
        "/opportunities — Discover Binance ecosystem products\n"
        "/risk — Explain trading risk awareness\n"
        "/clear — Reset conversation history\n"
        "/help — This message\n\n"
        "Or just **send any message** and I'll route it to the right module.\n"
        "Paste a suspicious message to activate Threat Hunter automatically."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cmd_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    msg = await get_quick_price()
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    msg = await get_market_intelligence()
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    msg = await get_opportunities()
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚠️ **Risk Hunter**\n\n"
        "Send me a message describing your intended trade and I'll flag any risk patterns.\n\n"
        "Examples:\n"
        "• _'I want to trade 100x leverage on a memecoin'_\n"
        "• _'Should I go all-in on this 10x call?'_\n"
        "• _'Is 50x leverage on BNB safe?'_"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conversation_history.pop(chat_id, None)
    await update.message.reply_text("✅ Conversation history cleared.")


# ── Message Handler ────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    await update.message.chat.send_action("typing")

    # Try local routing first
    response = await route_message(text)

    # Fall back to Claude
    if response is None:
        response = await ask_claude(chat_id, text)

    await update.message.reply_text(
        response,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


# ── Callback Query Handler (Inline Buttons) ────────────────────────────────

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu_threat":
        msg = (
            "🔴 **Threat Hunter**\n\n"
            "Paste any suspicious message below and I'll analyze it for scam patterns.\n\n"
            "I look for: seed phrase requests, fake support, impersonation, urgency tactics, "
            "and financial bait."
        )
    elif data == "menu_opportunity":
        await query.message.chat.send_action("typing")
        msg = await get_opportunities()
    elif data == "menu_market":
        await query.message.chat.send_action("typing")
        msg = await get_market_intelligence()
    elif data == "menu_risk":
        msg = (
            "⚠️ **Risk Hunter**\n\n"
            "Describe your intended trade and I'll flag any risk patterns.\n\n"
            "Try: _'I want to use 100x leverage on a memecoin'_"
        )
    elif data == "menu_price":
        await query.message.chat.send_action("typing")
        msg = await get_quick_price()
    elif data == "menu_help":
        msg = (
            "🐺 **Jager AI — Help**\n\n"
            "I have four intelligence modules:\n\n"
            "🔴 **Threat Hunter** — Scam & phishing detection\n"
            "💰 **Opportunity Hunter** — Binance product discovery\n"
            "📡 **Market Hunter** — BNB narrative intelligence\n"
            "⚠️ **Risk Hunter** — Trading risk education\n\n"
            "Just send a message or use the buttons below."
        )
    else:
        msg = "Unknown action."

    await query.message.reply_text(
        msg,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


# ── App Entry Point ────────────────────────────────────────────────────────

def main():
    config.validate()
    log.info("🐺 Jager AI starting up...")

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("price", cmd_price))
    app.add_handler(CommandHandler("market", cmd_market))
    app.add_handler(CommandHandler("opportunities", cmd_opportunities))
    app.add_handler(CommandHandler("risk", cmd_risk))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    log.info("✅ Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
