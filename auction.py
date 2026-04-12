from bst import LowBidBST

class LowBidAuction:
    """
    Implements the low-bid auction logic using a binary search tree to manage the bids.
    Each bid has a cost based on the price and a risk premium (alpha/(price+1)).
    The auction can compute the winner (lowest unique bid) and the total revenue for the seller.
    The auction also provides methods to analyze the bids, such as price distribution and average cost per player.
    """

    def __init__(self, base_cost=1.0, alpha=10.0):
        self.base_cost = base_cost
        self.alpha     = alpha
        self.bst       = LowBidBST()
        self.bids      = []

    def bid_cost(self, price):
        """Returns the cost of one bid using the risk premium formula from the instructions."""
        return self.base_cost + self.alpha / (price + 1)

    def add_bid(self, bidder, price):
        """Adds one bid to the auction and inserts it into the BST."""
        self.bids.append((bidder, price))
        self.bst.insert(price, bidder)

    def load_bids(self, bid_list):
        """Loads a list of (bidder, price) pairs into the auction."""
        for bidder, price in bid_list:
            self.add_bid(bidder, price)

    def get_winner(self):
        """Returns the lowest unique bid and bidder, or None if there is no winner."""
        return self.bst.lowest_unique_bid()

    def seller_revenue(self):
        """
        Returns the total revenue collected from all bids (bids cost + winning price).
        If there is no winner, the winning price is 0.
        """
        total = sum(self.bid_cost(price) for bidder, price in self.bids)
 
        winner = self.get_winner()
        if winner:
            total += winner["price"]
 
        return total

    def total_bids(self):
        """Returns the total number of bids."""
        return len(self.bids)

    def price_distribution(self):
        """Returns a dictionary {price: number_of_bids_at_that_price}."""
        distribution = {}
        for item in self.bst.in_order_traversal():
            distribution[item["price"]] = len(item["bidders"])
        return distribution

    def average_cost_per_player(self):
        """Returns the average total amount paid per player as they bid."""
        if not self.bids:
            return 0

        costs = {}
        for bidder, price in self.bids:
            costs[bidder] = costs.get(bidder, 0) + self.bid_cost(price) 

        return sum(costs.values()) / len(costs) 