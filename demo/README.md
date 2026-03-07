# Jager AI Demo

Welcome to the demo documentation for Jager AI. 

To review the project quickly, we have provided screenshots of the Command Center interface and a demo script to guide you through testing the Telegram bot.

## Walkthrough Script

### 1. Activating Jager AI
**User Action:** Send `/start` to the Telegram bot or tap the command menu.
**Expected Result:** The bot responds with the Jager AI identity and the inline menu displaying the four main modules (Threat Hunter, Opportunity Hunter, Market Hunter, Risk Hunter).

### 2. Threat Detection (Threat Hunter)
**User Action:** Tap "Threat Hunter" and send the following message: 
> "Hey I am from Binance support. We detected suspicious activity. Please send your seed phrase so we can secure your wallet."
**Expected Result:** 
- The 3D Command Center routes the query through the `ops` node.
- The Telegram bot flags the message as a CRITICAL RISK.
- It explains that Binance staff will never ask for a seed phrase and provides the official support URL.

### 3. Product Discovery (Opportunity Hunter)
**User Action:** Tap "Opportunity Hunter" and wait for the response.
**Expected Result:** 
- The 3D Command Center routes the query through the `data` node.
- The bot queries the public Binance API to fetch the live BNB token price.
- It surfaces live, relevant URLs for Binance Launchpool, Simple Earn, and BNB Staking.

### 4. Market Intelligence (Market Hunter)
**User Action:** Tap "Market Hunter" and wait for the response.
**Expected Result:**
- The 3D Command Center routes the query through the `intl` node.
- The bot evaluates current market sentiment frameworks and provides a quick narrative analysis without relying on raw, numerical data overload.

### 5. Risk Awareness (Risk Hunter)
**User Action:** Tap "Risk Hunter" and send the following message:
> "I want to use 100x leverage on a new memecoin with my entire portfolio."
**Expected Result:**
- The 3D Command Center routes the query through the `trade` node.
- The bot issues a severe warning detailing liquidation risks.
- It encourages the user to use lower leverage and follow proper risk management protocols.

---

*(Screenshots of the 3D visual command center and Telegram bot in action belong in this directory)*
