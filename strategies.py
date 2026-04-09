import random

def random_strategy(max_price=20):
    return random.randint(0, max_price)

def cost_aware_strategy(alpha, base_cost, max_price=1000):
    best_price = 0
    best_cost = float('inf')
    
    for price in range(0, max_price+1):
        cost = base_cost + alpha/(price+1)
        if cost < best_cost:
            best_cost = cost
            best_price = price
    
    offset = random.randint(-2, 2)
    result = best_price + offset
    return max(0, min(result, max_price))


def adaptive_strategy(historique_gagnants, max_price=1000):
    avoid_prices = set(historique_gagnants[-10:])
    
    candidats = [p for p in range(0, max_price+1) if p not in avoid_prices]
    
    if candidats:
        return random.choice(candidats)
    else:
        return random.randint(0, max_price) 