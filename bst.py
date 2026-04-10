class Node:
    def __init__(self, price, bidder):
        self.price = price           # The BST key
        self.bidders = [bidder]      # List for multiple players at the same price
        self.left = None
        self.right = None

class LowBidBST:
    def __init__(self):
        """Initializes an empty binary search tree for managing auction bids."""
        self.root = None

    def insert(self, price, bidder):
        """Iteratively inserts a bid into the BST."""
        if self.root is None:
            self.root = Node(price, bidder)
            return

        current = self.root
        while True:
            if price == current.price:
                current.bidders.append(bidder)
                break
            elif price < current.price:
                if current.left is None:
                    current.left = Node(price, bidder)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(price, bidder)
                    break
                current = current.right
                
    def search(self, price):
        """Searches for a price in the BST and returns the node if found, otherwise None."""
        current = self.root
        while current:
            if price == current.price:
                return current
            elif price < current.price:
                current = current.left
            else:
                current = current.right
        return None
    
    def delete(self, price):
        """Iteratively deletes a price node from the BST."""
        parent = None
        current = self.root

        # Search for the node to delete
        while current and current.price != price:
            parent = current
            if price < current.price:
                current = current.left
            else:
                current = current.right

        if current is None:
            return  # Price not found

        # Case 1 & 2: Node has 0 or 1 child
        if current.left is None or current.right is None:
            new_child = current.left if current.left else current.right
            
            if parent is None:
                self.root = new_child
            elif parent.left == current:
                parent.left = new_child
            else:
                parent.right = new_child

        # Case 3: Node has two children
        else:
            # Find the in-order successor (min of right subtree)
            p_parent = current
            successor = current.right
            while successor.left:
                p_parent = successor
                successor = successor.left

            # Replace current node data with successor data
            current.price = successor.price
            current.bidders = successor.bidders[:]

            # Remove the successor node
            if p_parent.left == successor:
                p_parent.left = successor.right
            else:
                p_parent.right = successor.right
                
    def find_min(self):
        """Returns the node with the minimum price in the BST, or None if the tree is empty."""
        if self.root is None:
            return None
        current = self.root
        while current.left:
            current = current.left
        return current

    def find_max(self):
        """Returns the node with the maximum price in the BST, or None if the tree is empty."""
        if self.root is None:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current
    
    def successor(self, price):
        """
        Returns the node with the smallest price greater than the given price,
        or None if no such price exists.
        """
        current = self.root
        successor = None
        while current:
            if current.price > price:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor
    
    def predecessor(self, price):
        """
        Returns the node with the largest price less than the given price,
        or None if no such price exists.
        """
        current = self.root
        predecessor = None
        while current:
            if current.price < price:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor

    def in_order_traversal(self):
        """Iterative in-order traversal using a stack to return sorted auction state."""
        result = []
        stack = []
        current = self.root
        
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append({"price": current.price, "bidders": current.bidders[:]})
            current = current.right
        return result

    def lowest_unique_bid(self):
        """Returns the lowest unique bid and its bidder, or None if there is no winner."""
        stack = []
        current = self.root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()

            if len(current.bidders) == 1:
                return {"price": current.price, "bidder": current.bidders[0]}

            current = current.right

        return None
