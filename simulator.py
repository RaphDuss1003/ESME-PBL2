"""
Simulator for analysing strategies.

This file has two distinct modes:

MODE 1 — CSV Analysis:
    Loops through all 500 rounds from the loaded CSV file, builds an auction
    for each round, finds the winner, and computes statistics:
        - Average winning price across all rounds
        - Average seller revenue per round
        - How often there is no winner (no unique bid)
        - The most common winning prices

    Usage:
        results = analyse_csv(rounds, base_cost, alpha)

MODE 2 — Strategy Simulation:
    Generates synthetic rounds where each player follows a strategy defined
    in strategies.py. Runs a configurable number of rounds and compares
    strategies against each other based on:
        - Win rate (how often each strategy wins)
        - Average profit per round (item value - bid cost when winning)
        - Average seller revenue
        - Effect of changing base_cost and alpha

    Usage:
        results = simulate_strategies(nb_rounds, nb_players, strategies, base_cost, alpha)

Both modes return a results dictionary that can be displayed by the interface
or printed to the console.
"""

from auction import LowBidAuction
from data_loader import load_round_into_bst
from strategies import random_strategy, low_cost_strategy, adaptive_strategy


# ============================================== MODE 1 — CSV Analysis ==============================================


def analyse_csv(rounds, base_cost=1.0, alpha=10.0):
    """
    Loops through all rounds from the CSV data, build an auction for each, and collect statistics.

    rounds      : the dict returned by load_csv() containing all rounds and their bids
    base_cost   : base cost of a bid (used for revenue computation)
    alpha       : parameter that controls the intensity of the risk premium (larger alpha => higher cost for low bids)

    Returns a dict with aggregate statistics.
    """
    total_rounds          = len(rounds)
    rounds_with_winner    = 0
    rounds_without_winner = 0
    total_revenue         = 0.0
    total_winning_price   = 0
    winning_prices        = []

    for round_number in range(1, total_rounds + 1):
        tree, bids = load_round_into_bst(rounds, round_number)           # Load the round into a BST and get the list of bids

        auction = LowBidAuction(base_cost=base_cost, alpha=alpha)        # Create a new auction instance for this round
        for bid in bids:
            auction.add_bid(bid["player"], bid["price"])

        winner         = auction.get_winner()
        revenue        = auction.seller_revenue()
        total_revenue += revenue                                         # Accumulate total revenue from the bids across all rounds

        if winner:
            rounds_with_winner  += 1
            total_winning_price += winner["price"]                       # Accumulate winning prices to compute average later
            winning_prices.append(winner["price"])
        else:
            rounds_without_winner += 1

    avg_revenue       = total_revenue / total_rounds if total_rounds > 0 else 0
    avg_winning_price = total_winning_price / rounds_with_winner if rounds_with_winner > 0 else 0

    results = {
        "total_rounds"          : total_rounds,
        "rounds_with_winner"    : rounds_with_winner,
        "rounds_without_winner" : rounds_without_winner,
        "avg_seller_revenue"    : avg_revenue,
        "avg_winning_price"     : avg_winning_price,
        "winning_prices"        : winning_prices,
    }

    return results


# ============================================== MODE 2 — Strategy Simulation ==============================================


def simulate_strategies(nb_rounds=500, nb_players=40, base_cost=1.0, alpha=10.0, max_price=99, item_value=100):
    """
    Run a synthetic simulation where each player follows one of the available strategies. 
    Players are split evenly between strategies.

    nb_rounds    : number of rounds to simulate
    nb_players   : number of players per round
    base_cost   : base cost of a bid
    alpha       : risk premium parameter
    max_price   : maximum bid price
    item_value  : value of the item being auctioned (used to compute profit)

    Returns a dict with the statistics of each strategy.
    """
    strategy_names    = ["random", "low cost", "adaptive"]
    nb_strategies     = len(strategy_names)
    player_strategies = {}                                                  # Dictionary mapping each player to their assigned strategy 

    for i in range(1, nb_players + 1):                                      # Assign a strategy to each player (split evenly)
        player = f"J{i}"
        player_strategies[player] = strategy_names[(i - 1) % nb_strategies]

    # Stats trackers per strategy
    stats = {name: {"wins": 0, "total_profit": 0.0, "total_cost": 0.0} for name in strategy_names}
    total_revenue  = 0.0
    winner_history = []                                                     # Tracks winning prices across rounds for adaptive strategy

    for _ in range(nb_rounds):
        auction    = LowBidAuction(base_cost=base_cost, alpha=alpha)
        round_bids = {}                                                     # Dictionnary of bids for the round

        for player, strategy in player_strategies.items():                  # Each player chooses a bid price based on their strategy
            if strategy == "random":
                price = random_strategy(max_price)
            elif strategy == "low cost":
                price = low_cost_strategy(alpha, base_cost, max_price)
            else:
                price = adaptive_strategy(winner_history, max_price)

            round_bids[player] = price
            auction.add_bid(player, price)                                  # Add the bid to the auction                         

        winner         = auction.get_winner()
        revenue        = auction.seller_revenue()
        total_revenue += revenue

        if winner:
            winning_player   = winner["bidder"]
            winning_price    = winner["price"]
            winning_strategy = player_strategies[winning_player]
            bid_cost         = auction.bid_cost(winning_price)
            profit           = item_value - winning_price - bid_cost

            stats[winning_strategy]["wins"]         += 1
            stats[winning_strategy]["total_profit"] += profit
            winner_history.append(winning_price)

        for player, price in round_bids.items():                            # Compute the cost of each player's bid and accumulate it for average cost computation
            strategy = player_strategies[player]
            stats[strategy]["total_cost"] += auction.bid_cost(price)

    # Aggregate results
    results = {"total_rounds": nb_rounds, "avg_seller_revenue": total_revenue / nb_rounds, "strategies": {}}

    for name in strategy_names:                                             # Compute win rate, average profit, and average cost for each strategy
        wins = stats[name]["wins"]
        results["strategies"][name] = {
            "wins"       : wins,
            "win_rate"   : wins / nb_rounds,
            "avg_profit" : stats[name]["total_profit"] / wins if wins > 0 else 0,
            "avg_cost"   : stats[name]["total_cost"] / nb_rounds,
        }

    return results


# ============================================== Display helpers ==============================================


def display_csv_results(results):
    """
    Print and formats the results of a CSV simulation to the console. They are printed in the terminal
    and also returned as a string to be displayed in the interface when the "Run CSV Analysis" button is clicked.
    """

    lines = []                                                                      # List of lines to join into the final string to display
    lines.append("=== CSV Analysis Results ===\n")
    lines.append(f"Total rounds           : {results['total_rounds']}")
    lines.append(f"Rounds with winner     : {results['rounds_with_winner']}")
    lines.append(f"Rounds no winner       : {results['rounds_without_winner']}")
    lines.append(f"Average seller revenue : {results['avg_seller_revenue']:.2f}€")   # Format  with 2 decimals
    lines.append(f"Average winning price  : {results['avg_winning_price']:.2f}€")

    text = "\n".join(lines)
    print(text)
    return text

def display_strategy_results(results):
    """
    Format and prints the results of the strategies simulation. They are printed in the terminal 
    and also displayed in the interface when the "Run Strategy Simulation" button is clicked.
    """

    lines = []                                                                    # List of lines to join into the final string to display
    lines.append(f"=== Strategy Simulation Results ===")
    lines.append(f"Total rounds       : {results['total_rounds']}")
    lines.append(f"Avg seller revenue : {results['avg_seller_revenue']:.2f}€\n")

    for name, data in results["strategies"].items():                              # Loops through each strategy and prints its stats
        lines.append(f"Strategy: {name}")
        lines.append(f" Wins           : {data['wins']}")
        lines.append(f" Win rate       : {data['win_rate']:.2%}")
        lines.append(f" Average profit : {data['avg_profit']:.2f}€")
        lines.append(f" Average cost   : {data['avg_cost']:.2f}€\n")

    text = "\n".join(lines)                                                       # Join all lines into a single string to display in the interface
    print(text)                                                                   # Print the results in the terminal          
    return text                                                                   # Returns the string to be displayed in the interface