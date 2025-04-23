import requests
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message):
    """Send a message via Telegram bot"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured.")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

def notify_arbitrage_opportunity(opportunity):
    """Notify about a new arbitrage opportunity"""
    profit_percent = opportunity['profit'] * 100
    
    message = f"🔍 *NEW ARBITRAGE OPPORTUNITY*\n\n"
    message += f"Profit: *{profit_percent:.2f}%*\n"
    
    if opportunity['apy']:
        message += f"APY: *{opportunity['apy']*100:.2f}%*\n"
    
    if opportunity['resolution_date']:
        message += f"Resolution: *{opportunity['resolution_date'].strftime('%Y-%m-%d')}*\n"
    
    message += "\n*Required Positions:*\n"
    
    for position in opportunity['positions']:
        message += f"- Buy *{position.outcome}* on *{position.platform}* at *${position.price:.2f}*\n"
    
    message += f"\nTotal cost: *${opportunity['total_cost']:.2f}*"
    message += f"\nExpected return: *${1.0:.2f}*"
    
    return send_telegram_message(message)