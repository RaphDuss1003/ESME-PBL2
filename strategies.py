import random

def random_strategy(max_price=20):
    """
    Picks a random number between 0 and the maximum bidding price (inclusive).
    No logic, just used to see the statistics of a purely random strategy."""
    return random.randint(0, max_price)

def low_cost_strategy(alpha, base_cost, max_price=99):
    """
    Bids low but accounts for the risk premium.
    
    Instead of blindly spamming 0 (which is expensive due to alpha/(price+1)), 
    it finds the price range where the bid cost starts becoming reasonable,
    then picks randomly within that range toward lower values.
    """
    
    costs = [(price, base_cost + alpha / (price + 1)) for price in range(0, max_price + 1)]   # Compute cost for each price and find the median cost
    median_cost = sorted(c for price, c in costs)[len(costs) // 2]
 
    affordable = [price for price, cost in costs if cost <= median_cost]                      # Keep only prices whose cost is below the median (the cheaper half)
 
    proba = [1 / (p + 1) for p in affordable]                                                 # List of "probabilities" to each price in affordable, favoring lower prices
    return random.choices(affordable, weights=proba, k=1)[0]                                  # Pick 1 price at random, biased toward lower prices (because of higher proba)


def adaptive_strategy(history_wins, max_price=1000):
    """
    Targets prices near past winning prices.
 
    Past winners were unique and low — so bidding near them is a reasonable
    strategy. It looks at the last 10 winners and picks a price within
    a small random offset of a randomly chosen recent winner.
 
    If no history exists yet, falls back to random_strategy.
    """
    if not history_wins:
        return random_strategy(max_price)
 
    recent = history_wins[-10:]                # Pick a recent winning price as the target
    target = random.choice(recent)
 
    offset = random.randint(-5, 5)             # Add a small offset so we don't always pick the exact same price
    result = target + offset
 
    return max(0, min(result, max_price)) 