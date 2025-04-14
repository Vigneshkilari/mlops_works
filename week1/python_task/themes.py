# themes.py
from PyQt5.QtWidgets import QApplication, QStyleFactory, QWidget
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt

def apply_dark_theme(app):
    """Applies a dark theme to the PyQt application's palette."""
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

def apply_dark_theme_to_widget(widget, app):
    """Applies a dark theme palette to a specific widget."""
    widget.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    widget.setPalette(palette)


def apply_toolbar_style(toolbar):
    """Applies a consistent style to the QToolBar for window buttons."""
    toolbar.setStyleSheet("""
        QToolBar {
            background-color: #252525; /* Darker background for toolbar */
            border: none;
            padding: 2px; /* Reduced padding */
        }
        QToolButton {
            background-color: transparent;
            border: none;
            padding: 5px 10px;
            color: white;
            font-weight: bold;
            font-size: 18px;
            font-family: "Arial Unicode MS"; /* Or a suitable Unicode font */
        }
        QToolButton:hover {
            background-color: #454545; /* Hover color */
        }
         QToolButton#closeButton:hover {
            background-color: red; /* Red hover for close button */
        }
    """)

def apply_window_buttons_style(toolbar):
    """Applies specific styles to minimize and close buttons in the toolbar."""
    toolbar.setStyleSheet(toolbar.styleSheet() + """
        QToolButton#minimizeButton {
            background-color: transparent;
            border: none;
            padding: 5px 10px;
            color: white; /* Sets icon color */
            font-weight: bold;
            font-size: 18px; /* Adjust as needed */
        }
        QToolButton#minimizeButton:hover {
            background-color: #454545;
        }
        QToolButton#closeButton {
            background-color: transparent;
            border: none;
            padding: 5px 10px;
            color: white; /* Sets icon color */
            font-weight: bold;
            font-size: 18px; /* Adjust as needed */
        }
        QToolButton#closeButton:hover {
            background-color: red;
        }
        QToolButton:hover {
           background-color: #454545;
        }
    """)

def setup_app_theme(app, main_window, toolbar):
    """Sets up the complete application theme."""
    apply_dark_theme(app) # Apply general dark theme palette
    apply_toolbar_style(toolbar) # Style the toolbar
    apply_window_buttons_style(toolbar) # Style window buttons in toolbar
    main_window.setStyleSheet("background-color: #353535;") # Set main window background color