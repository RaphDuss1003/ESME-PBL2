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

# ===================================================== LOADERS =====================================================

def load_csv(filepath):
    """
    Read a multi-round CSV file and return a dictionary: {"round": [{"player": str, "price": int}, ...], ...}
    Returns an empty dictionary if the file cannot be read or contains bad data.
    """

    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}")
        return {}
    
    rounds = {}

    with open(filepath, newline="", encoding="utf-8") as f:                       # newline tells Python not to do any automatic newline translation when reading the file
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]  # Normalizes header names: strip whitespaces and lowercases
        
        round_col  = _find_column(reader.fieldnames, ["manche", "tour"])
        player_col = _find_column(reader.fieldnames, ["joueur", "player"])
        price_col  = _find_column(reader.fieldnames, ["prix", "price"])
        
        if round_col is None or player_col is None or price_col is None:
            print(f"Error: CSV must have a round column, a player column, and a price column.")
            return {}
        
        for line_number, row in enumerate(reader, start=2):
            round  = row.get(round_col, "").strip()                               # Strips whitespace (extra spaces, tabs)
            player = row.get(player_col, "").strip()
            price  = row.get(price_col, "").strip()

            if not round or not player or not price:                              # Checks for missing values in any of the required columns
                print(f"Warning: line {line_number} skipped (missing round, player or price).")
                continue

            if not round.isdigit() or not price.lstrip("-").isdigit():            # Checks that the round and the price are integers
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
    
def load_single_round(filepath):
    """
    Read a single-round CSV file (no manche column) and return a list of bids: [{"player": str, "price": int}, ...]
    Returns an empty list if the file cannot be read or contains bad data.
    """
    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}")
        return []

    bids = []

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

        player_col = _find_column(reader.fieldnames, ["joueur", "player"])
        price_col  = _find_column(reader.fieldnames, ["prix", "price"])

        if player_col is None or price_col is None:
            print(f"Error: CSV must have a player column and a price column.")
            return []

        for line_number, row in enumerate(reader, start=2):
            player = row.get(player_col, "").strip()
            price  = row.get(price_col,  "").strip()

            if not player or not price:
                print(f"Warning: line {line_number} skipped (missing player or price).")
                continue

            if not price.lstrip("-").isdigit():
                print(f"Warning: line {line_number} skipped (price must be an integer, got {price}).")
                continue

            bid = int(price)

            if bid < 0:
                print(f"Warning: line {line_number} skipped (price must be >= 0, got {bid}).")
                continue

            bids.append({"player": player, "price": bid})

    return bids

def detect_and_load(filepath):
    """
    Looks at the first line of the CSV to detect its format (single or multi-round), then call the
    appropriate loader automatically.
 
    Returns:
        ("multi-rounds",  rounds_dict)  if a manche/round column is detected.
        ("single-round", bids_list)    if no manche column is found.
        (None, None)         if the file cannot be opened.
    """
    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}")
        return None, None
 
    with open(filepath, newline="", encoding="utf-8") as f:
        first_line = f.readline().strip().lower()
 
    if "manche" in first_line or "round" in first_line or "tour" in first_line:
        return "multi", load_csv(filepath)
    else:
        return "single", load_single_round(filepath)
    

# ===================================================== DEMO DATA ===================================================== 


def generate_demo_bids(nb_players=40, max_price=99, seed=None):
    """
    Generate a synthetic single-round dataset with nb_players players.
    Prices are drawn uniformly from [0, max_price].
    """
    random_nd_gen = random.Random(seed)                   # Seed is None so each demo is different
    bids = []
    for i in range(1, nb_players + 1):
        player = f"J{i}"
        price  = random_nd_gen.randint(0, max_price)
        bids.append({"player": player, "price": price})
    return bids

# ===================================================== BST BUILDING =====================================================

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

def load_single_round_into_bst(bids):
    """Given a bids list from load_single_round, insert all bids into a new BST and return it."""
    tree = LowBidBST()
    for bid in bids:
        tree.insert(bid["price"], bid["player"])
    return tree, bids

# ===================================================== DISPLAY =====================================================

def display_single_summary(bids):
    """Print a short summary of a single-round CSV file."""
    if not bids:
        print("No bids to display.")
        return
    
    prices = [bid["price"] for bid in bids]
    print(f"Players loaded : {len(bids)}")
    print(f"Price range    : {min(prices)} - {max(prices)}")
    print(f"Avg price      : {sum(prices) / len(prices):.2f}")

def display_bst(tree):
    """Print the BST state using in_order_traversal (sorted prices)."""
    nodes = tree.in_order_traversal()

    if not nodes:
        print("BST is empty.")
        return
    for node in nodes:
        print(f"Price: {node['price']} | Bidders: {', '.join(node['bidders'])}")

