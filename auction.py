from bst import LowBidBST

class LowBidAuction:
    def __init__(self, base_cost=1.0, alpha=10.0):
        self.base_cost = base_cost
        self.alpha = alpha
        self.bst = LowBidBST()
        self.bids = []

    def bid_cost(self, price):
        """Returns the cost of one bid using the risk premium formula."""
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
        """Returns the total revenue collected from all bids."""
        total = 0
        for bidder, price in self.bids:
            total += self.bid_cost(price)
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
        """Returns the average total amount paid per player."""
        if not self.bids:
            return 0

        costs = {}
        for bidder, price in self.bids:
            costs[bidder] = costs.get(bidder, 0) + self.bid_cost(price)

        return sum(costs.values()) / len(costs) 