import sys

from PyQt5.QtWidgets import QApplication, QFileDialog
from Interface.Interface import Interface, PopUpWindow
from data_loader import detect_and_load, generate_demo_bids, load_round_into_bst, load_single_round_into_bst
from bst import LowBidBST
from auction import LowBidAuction
from simulator import analyse_csv, simulate_strategies, display_csv_results, display_strategy_results

class MainControler:
    def __init__(self, app):
        self.app           = app
        self.window        = Interface()
        self.rounds        = {}                  # Stores the loaded CSV data
        self.bids          = []                  # Current list of bids for the loaded round
        self.tree          = None                # Current BST 
        self.file_mode     = None                # "multi" for multi-round CSV, "single" for single-round CSV
        self.auction       = None                # Current auction instance for the loaded round
        self.current_round = None                # Currently selected round number 
        
        # Connect buttons to functions
        self.window.btn_load.clicked.connect(self.load_csv_data)
        self.window.btn_load_round.clicked.connect(self.load_round)
        self.window.btn_demo.clicked.connect(self.generate_demo)
        self.window.btn_place_bid.clicked.connect(self.place_bid)
        self.window.btn_analyse_rounds.clicked.connect(self.run_csv_simulation)
        self.window.btn_simulate_strategies.clicked.connect(self.run_strategy_simulation)
        self.window.btn_reset.clicked.connect(self.reset_auction)

        self.window.show()


    # =================================================== CSV Loading ===================================================


    def load_csv_data(self):
        """ Opens a file dialog to select a CSV file, loads the data, and updates the interface. """

        PATH, _ = QFileDialog.getOpenFileName(self.window, "Select CSV File", "", "CSV Files (*.csv)") 
        if not PATH:
            return  # User cancelled the dialog

        self.window.status_label.setText("Loading CSV...")
        self.window.dataset_label.setText("Loading...")
        QApplication.processEvents()                                        # Update the interface immediately

        file_mode, data = detect_and_load(PATH)                             # Detect the file format and load the data accordingly

        if file_mode is None or not data:
            self.window.status_label.setText("Failed to load file.")
            self.window.dataset_label.setText("No file loaded")
            return
        
        self.file_mode = file_mode

        if self.file_mode == "multi":
            self.rounds = data
            self.bids = []
            total_bids = sum(len(bids) for bids in self.rounds.values())
            self.window.status_label.setText(f"Loaded {total_bids} bids from {len(self.rounds)} rounds.")
            self.window.dataset_label.setText(f"Multi-rounds CSV loaded successfully")
        
        elif self.file_mode == "single":
            self.bids = data
            self.rounds = {}
            self.tree, self.bids = load_single_round_into_bst(self.bids)
            self.auction = LowBidAuction()

            for bid in self.bids:
                self.auction.add_bid(bid["player"], bid["price"])
            
            self.window.status_label.setText(f"Loaded {len(self.bids)} bids from single round.")
            self.window.dataset_label.setText(f"Single-round CSV loaded successfully")
            self.refresh_bst_display()
        
    def load_round(self):
        if not self.rounds:
            self.window.status_label.setText("Status: No multi-rounds CSV loaded yet.")
            return
        
        self.current_round = self.window.spinbox_round.value()                           # Get the selected round number from the spin box
        self.tree, self.bids = load_round_into_bst(self.rounds, self.current_round)      # Load the selected round into a BST and get the list of bids
        
        self.auction = LowBidAuction()
        for bid in self.bids:
            self.auction.add_bid(bid["player"], bid["price"])
        
        self.window.status_label.setText(f"Round {self.current_round} loaded, {len(self.bids)} bids.") 
        self.refresh_bst_display()

        # Show round results in a popup window using PopUpWindow
        text   = self.format_round_results(f"Round {self.current_round} Analysis")
        round_window = PopUpWindow(f"Round {self.current_round} Results", text, parent=self.window)
        round_window.exec_()


    # ================================================ DEMO & MANUAL BIDDING ================================================


    def generate_demo(self):
        """ Generates a 1 round synthetic dataset and loads it into the interface. """
        self.bids = generate_demo_bids(seed=None)                                     # Seed=None for random data each time
        self.tree = LowBidBST()

        for bid in self.bids:
            self.tree.insert(bid["price"], bid["player"])

        self.rounds = {}
        self.file_mode = "single"
        self.auction = LowBidAuction()

        for bid in self.bids:
            self.auction.add_bid(bid["player"], bid["price"])

        self.window.dataset_label.setText(f"Demo round, {len(self.bids)} bids generated.")
        self.window.status_label.setText("Demo data generated.")
        self.refresh_bst_display()

    def place_bid(self):
        """ Allows the user to place a bid and updates the auction state accordingly. """

        if self.auction is None:
            print("\nNo round loaded yet.")
            return

        price = self.window.spinbox_bid.value()
        self.auction.add_bid("Human player", price)

        winner = self.auction.get_winner()

        print(f"\nBid placed: {price}\n")
        print(f"Seller revenue: {self.auction.seller_revenue():.2f}€")

        if winner:
            self.window.status_label.setText(f"Winner: {winner['bidder']} with price {winner['price']}")
        else:
            self.window.status_label.setText("No winner yet — no unique bid.")

        self.refresh_bst_display(human_price=price)


    # =================================================== SIMULATIONS ===================================================


    def run_csv_simulation(self):
        """" Runs the simulation on the loaded CSV data and displays the results, whith simultor.py methods. """

        base_cost = self.window.spinbox_base_cost.value()
        alpha     = self.window.spinbox_alpha.value()

        if self.file_mode == "multi":
            if self.current_round is not None:                              # Analyses only selected round from loaded file
                if self.auction is None:
                    print("No round loaded yet.")
                    return
                text   = self.format_round_results(f"Round {self.current_round} Analysis")
                print(text)
                dialog = PopUpWindow(f"Round {self.current_round} Results", text, parent=self.window)
                dialog.exec_()
                self.window.status_label.setText(f"Round {self.current_round} analysis done.")

            else:                                                           # No round selected => analyse all rounds from loaded file
                results = analyse_csv(self.rounds, base_cost, alpha)
                text    = display_csv_results(results)
                dialog  = PopUpWindow("Full CSV Analysis", text, parent=self.window)
                dialog.exec_()
                self.window.status_label.setText("CSV analysis done.")
        
        elif self.file_mode == "single":
            if self.auction is None:
                print("No single round loaded yet.")
                return
            text   = self.format_round_results("Single Round Analysis")
            print(text)
            dialog = PopUpWindow("Single Round Analysis", text, parent=self.window)
            dialog.exec_()
            self.window.status_label.setText("Single-round analysis done.")

        else:
            print("No data loaded yet.")        

    def run_strategy_simulation(self):
        """" Runs the simulation with different strategies and displays the results. """

        results = simulate_strategies(nb_rounds   = self.window.spinbox_nb_rounds.value(),
                                        nb_players  = self.window.spinbox_nb_players.value(),
                                        base_cost  = self.window.spinbox_base_cost.value(),
                                        alpha      = self.window.spinbox_alpha.value(),
                                        max_price  = self.window.spinbox_max_price.value(),
                                        item_value = self.window.spinbox_item_value.value())
    
        text = display_strategy_results(results)                                                     # Prints in the terminal and returns the string in the interface
        strategies_window = PopUpWindow("Strategy Simulation Results", text, parent=self.window)     # Creates a pop-up window for the stratedies results
        strategies_window.exec_()                                                                    # Show the results dialog
        self.window.status_label.setText("Strategy simulation completed. Check console for results.")


    # =================================================== RESET METHOD ===================================================


    def reset_auction(self):
        """ Clears all loaded data and resets the interface to its initial state."""
        self.rounds        = {}
        self.bids          = []
        self.tree          = None
        self.auction       = None
        self.file_mode     = None
        self.current_round = None

        self.window.dataset_label.setText("Dataset: none loaded")
        self.window.status_label.setText("Status: ready")
        self.window.bst_display.clear()
        print("Auction reset. All data cleared.")


    # ===================================================  DISPLAY OF DATA AND BST IN INTERFACE ==================================================


    def format_round_results(self, round_label):
            """
            Formats the analysis of the current auction into a string for display.
            round_label is a string describing which round is being analysed.
            """
            winner = self.auction.get_winner()
            lines  = []
            lines.append(f"=== {round_label} ===\n")
    
            if winner:
                lines.append(f"Winner          : {winner['bidder']}")
                lines.append(f"Winning price   : {winner['price']}")

            else:
                lines.append("Winner : none (no unique bid)")
    
            lines.append(f"Total bids              : {self.auction.total_bids()}")
            lines.append(f"Seller revenue          : {self.auction.seller_revenue():.2f}€")
            lines.append(f"Average cost per player : {self.auction.average_cost_per_player():.2f}€")
    
            return "\n".join(lines)

    def refresh_bst_display(self, human_price=None):
        """
        Updates the BST display panel with the current auction state.
        If human_price is provided, that row is marked with '<- YOU'.
        """
        if self.auction is None:
            self.window.bst_display.setPlainText("No auction loaded.")
            return

        nodes = self.auction.bst.in_order_traversal()
        if not nodes:
            self.window.bst_display.setPlainText("BST is empty.")
            return

        lines = []
        for node in nodes:
            bidders_str = ", ".join(node["bidders"])
            count       = len(node["bidders"])
            unique_mark = " <- unique" if count == 1 else f" ({count} bidders)"
            you_mark    = " <- YOU"   if human_price is not None and node["price"] == human_price else ""
            lines.append(f"Price: {node['price']:<6} | {bidders_str}{unique_mark}{you_mark}")  

        self.window.bst_display.setPlainText("\n".join(lines))

# =============================================== MAIN ===============================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainControler(app)
    sys.exit(app.exec_())