from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFontDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Settings Page Content Here")
        layout.addWidget(label)
        font_button = QPushButton("Change Font")
        font_button.clicked.connect(self.open_font_dialog)
        layout.addWidget(font_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def open_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            for child in self.findChildren(QLabel):
                child.setFont(font)
            for child in self.findChildren(QPushButton):
                child.setFont(font)