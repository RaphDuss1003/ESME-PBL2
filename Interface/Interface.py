from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                            QSpinBox, QGroupBox, QDoubleSpinBox, QPlainTextEdit,
                            QDialog)
from PyQt5.QtCore import Qt


class Interface(QWidget):
    def __init__(self): 
        super().__init__()                                               # Calls the parent QWidget constructor

        self.setObjectName("mainScreen")                                 # Sets an internal object name for styling
        self.setWindowTitle("Lowest Unique Bid Wins")                    # Sets the window title
        self.setFixedSize(1400, 800)                                     # Fixes the window size

        # ==================== TITLE ====================

        self.title = QLabel("Lowest Unique Bid Wins")                    # Creates the main title label
        self.title.setObjectName("titleLabel")                           # Assigns a style name for QSS
        self.title.setAlignment(Qt.AlignCenter)                          # Centers the label text

        self.subtitle = QLabel("Advanced Algorithmic 3 - BST Auction")   # Creates the subtitle label
        self.subtitle.setObjectName("subtitleLabel")                     # Assigns a style name for QSS
        self.subtitle.setAlignment(Qt.AlignCenter)                       # Centers the label text

        # ==================== BUTTONS ====================

        self.btn_load                = QPushButton("Load CSV")                         
        self.btn_load_round          = QPushButton("Load Round")                 # Button to load a specific round from the loaded CSV
        self.btn_demo                = QPushButton("Generate Demo Data")               
        self.btn_place_bid           = QPushButton("Place Bid")                                           
        self.btn_analyse_rounds      = QPushButton("Analyse auction round")    
        self.btn_simulate_strategies = QPushButton("Simulate Strategies")           
        self.btn_reset               = QPushButton("Reset Auction")                    
        
        self.btn_exit = QPushButton("Exit")                             # Button to exit the application
        self.btn_exit.clicked.connect(self.close)                       # Connects the button to the window close function
        
        # ==================== SPINBOXES ====================
        
        self.spinbox_round = QSpinBox()                                 # Spin box to select round number for strategy simulation
        self.spinbox_round.setMinimum(1)
        self.spinbox_round.setMaximum(500)

        self.spinbox_bid = QSpinBox()                                   # Spin box to select bid price 
        self.spinbox_bid.setMinimum(0)
        self.spinbox_bid.setMaximum(999)

        # ==================== BUTTONS LAYOUT ====================

        buttons_layout = QVBoxLayout()                                  # Creates a vertical layout for the buttons
        buttons_layout.setAlignment(Qt.AlignCenter)                     # Centers the layout content
        buttons_layout.addWidget(self.btn_load)        

        buttons_layout.addWidget(self.btn_load_round) 
        buttons_layout.addWidget(self.spinbox_round)      

        buttons_layout.addWidget(self.btn_demo)    

        buttons_layout.addWidget(self.btn_place_bid)
        buttons_layout.addWidget(self.spinbox_bid)     

        buttons_layout.addWidget(self.btn_analyse_rounds)   
        buttons_layout.addWidget(self.btn_simulate_strategies)
        buttons_layout.addWidget(self.btn_reset)                                             
        buttons_layout.addWidget(self.btn_exit)                         

        # ==================== INFO LABELS ====================

        self.dataset_label = QLabel("Dataset: none loaded")             # Label showing dataset status
        self.dataset_label.setObjectName("infoLabel")                   # Style name for QSS
        self.dataset_label.setAlignment(Qt.AlignCenter)                 # Centers the text

        self.status_label = QLabel("Status: ready")                     # Label showing current status
        self.status_label.setObjectName("infoLabel")                    # Style name for QSS
        self.status_label.setAlignment(Qt.AlignCenter)                  # Centers the text

        info_layout = QVBoxLayout()                                     # Layout for dataset and status labels
        info_layout.setAlignment(Qt.AlignCenter)                        # Centers the layout content
        info_layout.addWidget(self.dataset_label)                       # Adds dataset label
        info_layout.addWidget(self.status_label)                        # Adds status label

        # ==================== CENTER COLUMN ====================

        center_column = QVBoxLayout()                                   # Main vertical layout for the center column
        center_column.setAlignment(Qt.AlignCenter)                      # Centers everything
        center_column.addWidget(self.title)                             # Adds the title
        center_column.addWidget(self.subtitle)                          # Adds the subtitle
        center_column.addSpacing(20)                                    # Adds vertical spacing
        center_column.addLayout(buttons_layout)                         # Adds the buttons layout
        center_column.addSpacing(20)                                    # Adds more spacing
        center_column.addLayout(info_layout)                            # Adds the info labels layout

        # ==================== BST DISPLAY PANEL (left side) ====================
 
        self.bst_display = QPlainTextEdit()
        self.bst_display.setReadOnly(True)                              # User cannot edit the BST display
        self.bst_display.setPlaceholderText("BST will appear here after loading a round...")
 
        bst_group = QGroupBox("BST State")
        bst_group.setMaximumWidth(400)
        bst_layout = QVBoxLayout()
        bst_layout.addWidget(self.bst_display)
        bst_group.setLayout(bst_layout)

        # ==================== PARAMETERS PANEL (right side) ====================
 
        # Shared parameters (used by both simulations)
        self.spinbox_base_cost = QDoubleSpinBox()                      # DoubleSpinBox allows decimals numbers
        self.spinbox_base_cost.setMinimum(0.1)
        self.spinbox_base_cost.setMaximum(100.0)
        self.spinbox_base_cost.setSingleStep(0.1)
        self.spinbox_base_cost.setValue(1.0)
 
        self.spinbox_alpha = QDoubleSpinBox()
        self.spinbox_alpha.setMinimum(0.1)
        self.spinbox_alpha.setMaximum(1000.0)
        self.spinbox_alpha.setSingleStep(0.5)
        self.spinbox_alpha.setValue(10.0)
 
        # Strategy simulation only
        self.spinbox_nb_rounds = QSpinBox()
        self.spinbox_nb_rounds.setMinimum(1)
        self.spinbox_nb_rounds.setMaximum(10000)
        self.spinbox_nb_rounds.setValue(500)
 
        self.spinbox_nb_players = QSpinBox()
        self.spinbox_nb_players.setMinimum(2)
        self.spinbox_nb_players.setMaximum(1000)
        self.spinbox_nb_players.setValue(40)
 
        self.spinbox_max_price = QSpinBox()
        self.spinbox_max_price.setMinimum(1)
        self.spinbox_max_price.setMaximum(10000)
        self.spinbox_max_price.setValue(99)
 
        self.spinbox_item_value = QSpinBox()
        self.spinbox_item_value.setMinimum(1)
        self.spinbox_item_value.setMaximum(100000)
        self.spinbox_item_value.setValue(100)
 
        params_layout = QVBoxLayout()                                  # Vertical layout for the parameters on the right side
        params_layout.setAlignment(Qt.AlignTop)
        params_layout.addWidget(QLabel("— Shared Parameters —"))
        params_layout.addWidget(QLabel("Base cost:"))
        params_layout.addWidget(self.spinbox_base_cost)
        params_layout.addWidget(QLabel("Alpha:"))
        params_layout.addWidget(self.spinbox_alpha)
        params_layout.addSpacing(15)
        params_layout.addWidget(QLabel("— Strategy Simulation —"))
        params_layout.addWidget(QLabel("Number of rounds:"))
        params_layout.addWidget(self.spinbox_nb_rounds)
        params_layout.addWidget(QLabel("Number of players:"))
        params_layout.addWidget(self.spinbox_nb_players)
        params_layout.addWidget(QLabel("Max price:"))
        params_layout.addWidget(self.spinbox_max_price)
        params_layout.addWidget(QLabel("Item value:"))
        params_layout.addWidget(self.spinbox_item_value)
 
        params_group = QGroupBox("Simulation Parameters")
        params_group.setMaximumWidth(220)
        params_group.setLayout(params_layout)

        # ==================== MAIN LAYOUT ====================

        main_layout = QHBoxLayout()                                     # Main horizontal layout
        main_layout.addWidget(bst_group)                                # BST panel on the left
        main_layout.addLayout(center_column)                            # Adds the center column
        main_layout.addWidget(params_group)                             # Parameters panel on the right

        self.setLayout(main_layout)                                     # Sets the main layout for the window

        self.setStyleSheet(open("Interface/style.qss").read())          # Loads and applies the QSS stylesheet


class PopUpWindow(QDialog):
    """ 
    Class used to open a new dialog window (pop-up window) to display the results of the simulations, 
    the data of a loaded round and the analysis of said round. """

    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(500, 400)

        self.text_area = QPlainTextEdit()                # Text area to display the content, set to read-only 
        self.text_area.setReadOnly(True)
        self.text_area.setPlainText(text)

        self.btn_close = QPushButton("Close")            # Close button to close the dialog
        self.btn_close.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)