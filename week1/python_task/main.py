import sys
from PyQt5.QtWidgets import QApplication, QToolTip # Keep QApplication and QToolTip from QtWidgets
from PyQt5.QtGui import QFontDatabase, QFont # Import QFontDatabase and QFont from QtGui
from PyQt5.QtCore import QTimer
from cloud_app import CloudApp # Import the CloudApp class from cloud_app.py
from themes import setup_app_theme # Import the theme setup function
from splash_screen import SplashScreen # Import SplashScreen

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QToolTip.setFont(QFont('Arial', 12))
    font_db = QFontDatabase() # Now QFontDatabase is correctly imported
    if not font_db.families().__contains__("Arial Unicode MS"):
        print("Arial Unicode MS font not found.  Symbols may not display correctly.")
    else:
        print("Arial Unicode MS font Found!!")

    # --- Splash Screen Integration ---
    logo_path = 'C:/_Vignesh_N/project_cloud_security/v4/cli/logo.png'  # !!! ACTUAL LOGO PATH - REMEMBERED !!!
    splash = SplashScreen(logo_path, duration=3000) # Create SplashScreen instance, duration in milliseconds
    splash.start_animation() # Start the splash screen animation

    cloud_app = CloudApp() # Create the main application window (CloudApp) instance

    # Apply theme *after* CloudApp instance is created and *in main_app.py*
    setup_app_theme(app, cloud_app, cloud_app.window_buttons_toolbar) # Apply theme from themes.py - CORRECT PLACEMENT

    # Delay showing the main window until after the splash screen duration
    QTimer.singleShot(splash.duration, cloud_app.initialize_ui)

    sys.exit(app.exec_())