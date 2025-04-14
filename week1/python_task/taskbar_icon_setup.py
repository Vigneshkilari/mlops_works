# taskbar_icon_setup.py
import sys
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

# --- Import ctypes for setting AppUserModelID (Windows specific) ---
import ctypes

def setup_taskbar_icon(main_window, icon_path):
    """
    Sets up the taskbar icon for the PyQt application.

    Args:
        main_window (QMainWindow): The main window of the application.
        icon_path (str): The file path to the icon file (.ico).
    """
    # --- 1. Set AppUserModelID (Windows Specific - Before icon loading) ---
    if sys.platform == 'win32': # Only on Windows
        myappid = 'mycompany.myproduct.cloudplatform.version'  # Replace with your own AppUserModelID
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except AttributeError:
            # Handle cases where SetCurrentProcessExplicitAppUserModelID is not available
            print("Warning: Could not set AppUserModelID (Windows version might be too old).")

    # --- 2. Load the Icon using QIcon ---
    app_icon = QIcon() # Initialize an empty QIcon
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path) # Load the icon from the file path
        print(f"Successfully loaded icon from: {icon_path}")
    else:
        print(f"Error: Icon file not found at: {icon_path}")
        QMessageBox.warning(main_window, "Icon Not Found",
                            f"The icon file at '{icon_path}' was not found.\n"
                            f"Please ensure the file exists at this location.")
        return # Exit if icon not found

    # --- 3. Set the Window Icon using setWindowIcon() ---
    main_window.setWindowIcon(app_icon)