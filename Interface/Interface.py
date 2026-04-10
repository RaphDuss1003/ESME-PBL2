from PyQt5.QtWidgets import (
        QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
        QSpinBox, QTableWidget, QTableWidgetItem, QGroupBox,
        QPlainTextEdit, QApplication
    )
from PyQt5.QtCore import Qt
import sys

class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainScreen")
        self.setWindowTitle("Lowest Unique Bid Wins")
        self.setFixedSize(1200, 800)

        self.title = QLabel("Lowest Unique Bid Wins")
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel("Advanced Algorithms 3 - BST Auction")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.btn_load = QPushButton("Load CSV")
        self.btn_demo = QPushButton("Generate Demo Data")
        self.btn_reset = QPushButton("Reset Auction")
        self.btn_run = QPushButton("Run Full Analysis")
        
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.clicked.connect(self.close)

        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.addWidget(self.btn_load)
        buttons_layout.addWidget(self.btn_demo)
        buttons_layout.addWidget(self.btn_reset)
        buttons_layout.addWidget(self.btn_run)
        buttons_layout.addWidget(self.btn_exit)

        self.dataset_label = QLabel("Dataset: none loaded")
        self.dataset_label.setObjectName("infoLabel")
        self.dataset_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Status: ready")
        self.status_label.setObjectName("infoLabel")
        self.status_label.setAlignment(Qt.AlignCenter)

        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.dataset_label)
        info_layout.addWidget(self.status_label)

        center_column = QVBoxLayout()
        center_column.setAlignment(Qt.AlignCenter)
        center_column.addWidget(self.title)
        center_column.addWidget(self.subtitle)
        center_column.addSpacing(20)
        center_column.addLayout(buttons_layout)
        center_column.addSpacing(20)
        center_column.addLayout(info_layout)

        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(center_column)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.setStyleSheet(open("Interface/style.qss").read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())
