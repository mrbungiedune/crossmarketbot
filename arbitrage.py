import datetime
from src.database.operations import get_latest_markets
from src.config import MINIMUM_PROFIT, MINIMUM_APY

def find_arbitrage_opportunities():
    """Find arbitrage opportunities across platforms"""
    markets = get_latest_markets()
    
    # Group by market_id
    market_groups = {}
    for market in markets:
        if market.market_id not in market_groups:
            market_groups[market.market_id] = []
        market_groups[market.market_id].append(market)
    
    opportunities = []
    
    for market_id, group in market_groups.items():
        # Group by outcome
        outcome_groups = {}
        for market in group:
            if market.outcome not in outcome_groups:
                outcome_groups[market.outcome] = []
            outcome_groups[market.outcome].append(market)
        
        # Find cheapest price for each outcome
        cheapest_outcomes = []
        for outcome, outcome_markets in outcome_groups.items():
            cheapest = min(outcome_markets, key=lambda x: x.price)
            cheapest_outcomes.append(cheapest)
        
        # Calculate total cost
        total_cost = sum(market.price for market in cheapest_outcomes)
        
        # Check if this is an arbitrage opportunity
        if total_cost < (1.0 - MINIMUM_PROFIT):
            profit = 1.0 - total_cost
            
            # Calculate APY if resolution date is available
            apy = None
            resolution_date = None
            
            # Try to get resolution date from any of the markets
            for market in group:
                if market.resolution_date:
                    resolution_date = market.resolution_date
                    break
            
            if resolution_date:
                days_to_resolution = (resolution_date - datetime.datetime.utcnow()).days
                if days_to_resolution > 0:
                    apy = (profit / days_to_resolution) * 365
            
            # Only add if APY is unknown or meets minimum
            if apy is None or apy >= MINIMUM_APY:
                opportunities.append({
                    'market_id': market_id,
                    'profit': profit,
                    'total_cost': total_cost,
                    'positions': cheapest_outcomes,
                    'apy': apy,
                    'resolution_date': resolution_date
                })
    
    return opportunities