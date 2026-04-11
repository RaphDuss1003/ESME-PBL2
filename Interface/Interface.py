from PyQt5.QtWidgets import (
        QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
        QSpinBox, QTableWidget, QTableWidgetItem, QGroupBox,
        QPlainTextEdit, QApplication
    )
from PyQt5.QtCore import Qt
import sys                                                              # Gives access to system argument

class Interface(QWidget):
    def __init__(self):
        super().__init__()                                              # Calls the parent QWidget constructor

        self.setObjectName("mainScreen")                                # Sets an internal object name for styling
        self.setWindowTitle("Lowest Unique Bid Wins")                   # Sets the window title
        self.setFixedSize(1200, 800)                                    # Fixes the window size

        self.title = QLabel("Lowest Unique Bid Wins")                   # Creates the main title label
        self.title.setObjectName("titleLabel")                          # Assigns a style name for QSS
        self.title.setAlignment(Qt.AlignCenter)                         # Centers the label text

        self.subtitle = QLabel("Advanced Algorithms 3 - BST Auction")   # Creates the subtitle label
        self.subtitle.setObjectName("subtitleLabel")                    # Assigns a style name for QSS
        self.subtitle.setAlignment(Qt.AlignCenter)                      # Centers the label text

        self.btn_load                = QPushButton("Load CSV")                         
        self.btn_load_round          = QPushButton("Load Round")                 # Button to load a specific round from the loaded CSV
        self.btn_demo                = QPushButton("Generate Demo Data")               
        self.btn_place_bid           = QPushButton("Place Bid")                                           
        self.btn_analyse_rounds      = QPushButton("Analyse CSV rounds")    
        self.btn_simulate_strategies = QPushButton("Simulate Strategies")           
        self.btn_summary             = QPushButton("Show Summary")               # Button to show summary of loaded data
        self.btn_reset               = QPushButton("Reset Auction")                    
        
        self.btn_exit = QPushButton("Exit")                             # Button to exit the application
        self.btn_exit.clicked.connect(self.close)                       # Connects the button to the window close function

        self.spinbox_round = QSpinBox()                                 # Spin box to select round number 
        self.spinbox_round.setMinimum(1)
        self.spinbox_round.setMaximum(500)

        self.spinbox_bid = QSpinBox()                                   # Spin box to select bid price 
        self.spinbox_bid.setMinimum(0)
        self.spinbox_bid.setMaximum(999)

        buttons_layout = QVBoxLayout()                                  # Creates a vertical layout for the buttons
        buttons_layout.setAlignment(Qt.AlignCenter)                     # Centers the layout content
        buttons_layout.addWidget(self.btn_load)                                             
        buttons_layout.addWidget(self.btn_load_round) 
        buttons_layout.addWidget(self.spinbox_round)                  
        buttons_layout.addWidget(self.btn_demo)     
        buttons_layout.addWidget(self.btn_place_bid)
        buttons_layout.addWidget(self.spinbox_bid)                    
        buttons_layout.addWidget(self.btn_reset)                        
        buttons_layout.addWidget(self.btn_analyse_rounds)   
        buttons_layout.addWidget(self.btn_simulate_strategies)                       
        buttons_layout.addWidget(self.btn_summary)                      
        buttons_layout.addWidget(self.btn_exit)                         

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

        center_column = QVBoxLayout()                                   # Main vertical layout for the center column
        center_column.setAlignment(Qt.AlignCenter)                      # Centers everything
        center_column.addWidget(self.title)                             # Adds the title
        center_column.addWidget(self.subtitle)                          # Adds the subtitle
        center_column.addSpacing(20)                                    # Adds vertical spacing
        center_column.addLayout(buttons_layout)                         # Adds the buttons layout
        center_column.addSpacing(20)                                    # Adds more spacing
        center_column.addLayout(info_layout)                            # Adds the info labels layout

        main_layout = QHBoxLayout()                                     # Main horizontal layout
        main_layout.addStretch()                                        # Adds stretchable empty space (left)
        main_layout.addLayout(center_column)                            # Adds the center column
        main_layout.addStretch()                                        # Adds stretchable empty space (right)

        self.setLayout(main_layout)                                     # Sets the main layout for the window

        self.setStyleSheet(open("Interface/style.qss").read())          # Loads and applies the QSS stylesheet


"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())"""
