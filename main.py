import sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from Interface.Interface import Interface
from data_loader import (detect_and_load, generate_demo_bids, load_round_into_bst, load_single_round_into_bst,
                          display_bst, display_summary, display_single_summary)
from bst import LowBidBST
from auction import LowBidAuction
from simulator import simulate_csv, simulate_strategies, display_csv_results, display_strategy_results

class MainControler:
    def __init__(self, app):
        self.app       = app
        self.window    = Interface()
        self.rounds    = {}                  # Stores the loaded CSV data
        self.bids      = []                  # Current list of bids for the loaded round
        self.tree      = None                # Current BST 
        self.file_mode = None                # "multi" for multi-round CSV, "single" for single-round CSV
        self.auction   = None                # Current auction instance for the loaded round
        
        # Connect buttons to functions
        self.window.btn_load.clicked.connect(self.load_csv_data)
        self.window.btn_load_round.clicked.connect(self.load_round)
        self.window.btn_demo.clicked.connect(self.generate_demo)
        self.window.btn_place_bid.clicked.connect(self.place_bid)
        self.window.btn_analyse_rounds.clicked.connect(self.run_csv_simulation)
        self.window.btn_simulate_strategies.clicked.connect(self.run_strategy_simulation)
        self.window.btn_summary.clicked.connect(self.show_summary)
        #self.window.btn_reset.clicked.connect(self.reset_auction)

        self.window.show()

    def load_csv_data(self):
        """ Opens a file dialog to select a CSV file, loads the data, and updates the interface. """

        PATH, _ = QFileDialog.getOpenFileName(self.window, "Select CSV File", "", "CSV Files (*.csv)") 
        if not PATH:
            return  # User cancelled the dialog

        self.window.status_label.setText("Loading CSV...")
        self.window.dataset_label.setText("Loading...")
        QApplication.processEvents()                                        # Update the interface immediately

        file_mode, data = detect_and_load(PATH)                        # Detect the file format and load the data accordingly

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
        
    def load_round(self):
        if not self.rounds:
            print("No multi-rounds CSV loaded yet.")
            return
        
        round_number = self.window.spinbox_round.value()                           # Get the selected round number from the spin box
        self.tree, self.bids = load_round_into_bst(self.rounds, round_number)      # Load the selected round into a BST and get the list of bids
        
        self.auction = LowBidAuction()
        for bid in self.bids:
            self.auction.add_bid(bid["player"], bid["price"])
        
        self.window.status_label.setText(f"Round {round_number} loaded, {len(self.bids)} bids.") 

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

        print("\nBST for demo round:")
        display_bst(self.tree)

    def show_summary(self):
        """ Displays a summary of the loaded dataset in a message box. """
        if self.file_mode == "multi" and self.rounds:
            display_summary(self.rounds)
        elif self.file_mode == "single" and self.bids:
            display_single_summary(self.bids)
        else:
            print("No data loaded to summarize.\n")


    def place_bid(self):
        """ Allows the user to place a bid and updates the auction state accordingly. """

        if self.auction is None:
            print("No round loaded yet.")
            return

        price = self.window.spinbox_bid.value()
        self.auction.add_bid("Human", price)

        winner = self.auction.get_winner()
        if winner:
            self.window.status_label.setText(f"Winner: {winner['bidder']} with price {winner['price']}")
        else:
            self.window.status_label.setText("No winner yet — no unique bid.")

        print(f"Bid placed: {price}")
        print(f"Seller revenue: {self.auction.seller_revenue():.2f}")

    def run_csv_simulation(self):
        """" Runs the simulation on the loaded CSV data and displays the results, whith simultor.py methods. """

        if self.file_mode != "multi" or not self.rounds:
            print("No multi-round CSV loaded for simulation.")
            return
        # base_cost = float(self.window.spinbox_bid.value())  
        # alpha = float(self.window.spinbox_round.value())
        results = simulate_csv(self.rounds)
        display_csv_results(results)
        self.window.status_label.setText("CSV simulation completed. Check console for results.")

    def run_strategy_simulation(self):
        """" Runs the simulation with different strategies and displays the results. """

        results = simulate_strategies(nb_rounds=500)
        display_strategy_results(results)
        self.window.status_label.setText("Strategy simulation completed. Check console for results.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainControler(app)
    sys.exit(app.exec_())