from src.config import CREDENTIALS
from src.platforms.manager import PlatformManager
from src.analysis.arbitrage import find_arbitrage_opportunities
from src.notifications.telegram import send_telegram_message

def test_platform_collection():
    """Test data collection from platforms"""
    platform_manager = PlatformManager(CREDENTIALS)
    
    try:
        markets = platform_manager.collect_all_market_data()
        print(f"Successfully collected {len(markets)} markets")
        
        # Print sample markets
        for i, market in enumerate(markets[:5]):
            print(f"Market {i+1}: {market['market_id']} - {market['outcome']} - ${market['price']}")
        
    finally:
        platform_manager.cleanup()

def test_arbitrage_detection():
    """Test arbitrage detection"""
    opportunities = find_arbitrage_opportunities()
    
    print(f"Found {len(opportunities)} arbitrage opportunities")
    
    for i, opp in enumerate(opportunities):
        print(f"Opportunity {i+1}:")
        print(f"  Profit: {opp['profit']*100:.2f}%")
        print(f"  Total Cost: ${opp['total_cost']:.2f}")
        if opp['apy']:
            print(f"  APY: {opp['apy']*100:.2f}%")
        print("  Positions:")
        for pos in opp['positions']:
            print(f"    {pos.platform} - {pos.outcome} - ${pos.price:.2f}")
        print()

def test_notifications():
    """Test Telegram notifications"""
    message = "🧪 This is a test message from the Prediction Market Arbitrage Bot"
    result = send_telegram_message(message)
    
    if result:
        print("Notification test successful!")
    else:
        print("Notification test failed!")

def run_tests():
    """Run all tests"""
    print("=== TESTING PLATFORM COLLECTION ===")
    test_platform_collection()
    
    print("\n=== TESTING ARBITRAGE DETECTION ===")
    test_arbitrage_detection()
    
    print("\n=== TESTING NOTIFICATIONS ===")
    test_notifications()

if __name__ == "__main__":
    run_tests()