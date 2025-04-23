# Prediction Market Arbitrage Bot

A bot that finds arbitrage opportunities across prediction markets.

## Setup

1. Create a virtual environment:
python -m venv venv

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
pip install -r requirements.txt

4. Configure `.env` file with your API keys and Telegram bot credentials.

## Running

1. Run tests:
python test.py

2. Start the bot:
python run.py

## Notes

- The bot checks for opportunities every 5 minutes
- Minimum profit threshold: 2%
- Minimum APY threshold: 60%