import csv
import os
import random

from bst import LowBidBST

def _find_column(fieldnames, candidates):
    """Return the first candidate name found in fieldnames, or None."""
    for candidate in candidates:
        if candidate in fieldnames:
            return candidate
    return None

# ============================== LOADERS ==============================

def load_csv(filepath):
    """
    Read a multi-round CSV file and return a dictionary: {"round": [{"player": str, "price": int}, ...], ...}
    Returns an empty dictionary if the file cannot be read or contains bad data.
    """
    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}")
        return {}
    
    rounds = {}

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]  # Normalize header names: strip whitespaces and lowercases
        
        round_col = _find_column(reader.fieldnames, ["manche", "tour"])
        player_col = _find_column(reader.fieldnames, ["joueur", "player"])
        price_col = _find_column(reader.fieldnames, ["prix", "price"])
        
        if round_col is None or player_col is None or price_col is None:
            print(f"Error: CSV must have a round column, a player column, and a price column.")
            return {}
        
        for line_number, row in enumerate(reader, start=2):
            round = row.get(round_col, "").strip()
            player = row.get(player_col, "").strip()
            price = row.get(price_col, "").strip()

            if not round or not player or not price:
                print(f"Warning: line {line_number} skipped (missing round, player or price).")
                continue

            if not round.isdigit() or not price.lstrip("-").isdigit():
                print(f"Warning: line {line_number} skipped. Round and price must be integers, got {round} and {price}.")
                continue

            bid = int(price)

            if bid < 0:
                print(f"Warning: line {line_number} skipped. Price must be >= 0, got {price}.")
                continue

            round_number = int(round)

            if round_number not in rounds:
                rounds[round_number] = []
            rounds[round_number].append({"player": player, "price": bid})
        
        return rounds

def generate_demo_bids(n_players=40, max_price=99, seed=None):
    """
    Generate a synthetic single-round dataset with n_players players.
    Prices are drawn uniformly from [0, max_price].
    """
    rng = random.Random(seed)
    bids = []
    for i in range(1, n_players + 1):
        player = f"J{i}"
        price  = rng.randint(0, max_price)
        bids.append({"player": player, "price": price})
    return bids

# ============================== BST BUILDING ==============================

def load_round_into_bst(rounds, round_number):
    """ Given the rounds dict from load_csv, insert all bids of the given round into a new BST and return it. """

    if round_number not in rounds:
        print(f"Error: round {round_number} not found in data.")
        return LowBidBST(), []
    
    bids = rounds[round_number]
    tree = LowBidBST()
    for bid in bids:
        tree.insert(bid["price"], bid["player"])
    return tree, bids

# ============================== DISPLAY ==============================

def display_summary(rounds):
    """Print a short summary of the loaded dataset."""
    if not rounds:
        print("  No rounds to display.")
        return
    total_bids = sum(len(bids) for bids in rounds.values())
    print(f"Rounds loaded : {len(rounds)}")
    print(f"Total bids    : {total_bids}")
    print(f"Bids/round    : {total_bids / len(rounds):.1f}")

def display_bst(tree):
    """Print the BST state using in_order_traversal (sorted prices)."""
    nodes = tree.in_order_traversal()
    if not nodes:
        print("BST is empty.")
        return
    for node in nodes:
        print(f"Price: {node['price']} | Bidders: {', '.join(node['bidders'])}")

# ============================== MAIN TEST ==============================

if __name__ == "__main__":
    # 1. Hardcode your path here (using 'r' for raw string to handle backslashes)
    CSV_PATH = r"APP_lowbid_data\lowbid_multi_manches_500x40.csv"

    print("=== LowBid System Menu ===")
    print("1. Load data from CSV")
    print("2. Generate demo round")
    choice = input("Select an option (1 or 2): ").strip()

    if choice == "1":
        print(f"\n[data_loader] Loading: {CSV_PATH}")
        rounds = load_csv(CSV_PATH)
        
        if rounds:
            display_summary(rounds)
            
            # Ask for round number and convert to int for the dictionary lookup
            raw_round = input("\nEnter round number to view (e.g., 1): ").strip()
            if raw_round.isdigit():
                round_num = int(raw_round)
                print(f"\n[data_loader] BST for round {round_num}:")
                tree, bids = load_round_into_bst(rounds, round_num)
                display_bst(tree)
            else:
                print("Error: Please enter a valid number.")

    elif choice == "2":
        print("\n[data_loader] Generating demo data...")
        bids = generate_demo_bids(seed=0)
        tree = LowBidBST()
        for bid in bids:
            tree.insert(bid["price"], bid["player"])
        display_bst(tree)

    else:
        print("Invalid choice. Please run the script again.")