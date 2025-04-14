from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to the Cloud Platform")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.details_label = QLabel("Some details about our amazing cloud services go here.")
        self.details_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.details_label)

        self.base_font_size = 12
        self.min_font_size = 8
        self.max_font_size = 24
        self.setLayout(layout)
        self.update_font_size()
        layout.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        self.update_font_size()

    def update_font_size(self):
        font_size = int(self.width() / 40) + self.base_font_size 
        font_size = max(self.min_font_size, min(font_size, self.max_font_size))
        font = QFont()
        font.setPointSize(font_size)
        self.label.setFont(font)
        self.details_label.setFont(font)