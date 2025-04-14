# splash_screen.py
from PyQt5.QtWidgets import QSplashScreen, QApplication, QStyleFactory # Import QStyleFactory
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
# from themes import apply_dark_theme  # Import the theme function - No need to import full app theme here anymore

def apply_dark_theme_to_widget(widget, app):
    """Applies a dark theme palette to a specific widget."""
    widget.setStyle(QStyleFactory.create("Fusion")) # Use QStyleFactory.create to get QStyle object
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


class SplashScreen(QSplashScreen):
    def __init__(self, logo_path, duration=2000):  # Duration in milliseconds
        pixmap = QPixmap(logo_path)
        super().__init__(pixmap)
        self.setWindowFlag(Qt.FramelessWindowHint) # Frameless splash screen
        self.duration = duration

        # Apply dark theme to splash screen
        app = QApplication.instance() # Get the application instance
        if app: # Ensure app instance exists
            apply_dark_theme_to_widget(self, app) # Apply theme to splash screen specifically

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)  # Fade in/out duration
        self.animation.setStartValue(1.0)   # Start with fully opaque
        self.animation.setEndValue(0.2)     # Fade to almost transparent
        self.animation.setEasingCurve(QEasingCurve.InOutSine)
        self.animation.setLoopCount(-1) # Infinite loop for blinking


    def start_animation(self):
        self.show() # Show the splash screen
        self.animation.start()
        QTimer.singleShot(self.duration, self.close_splash) # Close after duration

    def close_splash(self):
        self.animation.stop() # Stop animation
        self.close() # Close splash screen
        self.deleteLater() # Clean up resources

"""

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # Replace 'path/to/your/logo.png' with the actual path to your logo file
    logo_path = 'C:/_Vignesh_N/project_cloud_security/v4/cli/logo.png'
    splash = SplashScreen(logo_path, duration=3000) # 3 seconds splash duration
    splash.start_animation()

    # Simulate application loading (replace with your actual app initialization)
    timer = QTimer()
    timer.singleShot(3000, lambda: print("Main application would start now...")) # Simulate main app start after splash

    sys.exit(app.exec_())"""