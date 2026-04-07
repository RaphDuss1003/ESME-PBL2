class Node:
    def __init__(self, price, bidder):
        self.price = price           # The BST key
        self.bidders = [bidder]      # List for multiple players at the same price
        self.left = None
        self.right = None

class LowBidBST:
    def __init__(self):
        """initializes an empty BST."""
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
            result.append({"price": current.price, "bidders": current.bidders})
            current = current.right
        return result

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
            current.bidders = successor.bidders

            # Remove the successor node
            if p_parent.left == successor:
                p_parent.left = successor.right
            else:
                p_parent.right = successor.right