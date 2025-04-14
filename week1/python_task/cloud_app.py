# cloud_app.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QToolBar, QAction, QSizePolicy,
                             QSpacerItem, QLabel, QPushButton, QFrame, QApplication, QDialog)
from PyQt5.QtCore import Qt, QSize, QMargins
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainterPath, QColor
from home_page import HomePage
from settings_page import SettingsPage
from themes import setup_app_theme
from login_dialog import LoginDialog
from taskbar_icon_setup import setup_taskbar_icon # Import the taskbar icon setup function

class CloudApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Setup Taskbar Icon (Add this block here) ---
        icon_path = "C:/_Vignesh_N/project_cloud_security/v4/cli/logo.ico" # Path to your icon file
        setup_taskbar_icon(self, icon_path) # Call the setup function, passing 'self' and icon path

        self.setWindowTitle("Cloud Platform")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.central_widget)

        self.top_bar = QWidget()
        self.top_bar.setObjectName("topBar")
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(15, 5, 15, 5)
        self.top_bar_layout.setSpacing(15)
        self.main_layout.addWidget(self.top_bar)

        # --- Left Side (Logo and Horizontal Menu) ---
        self.left_top_bar = QWidget()
        self.left_top_bar_layout = QHBoxLayout(self.left_top_bar)
        self.left_top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.left_top_bar_layout.setSpacing(25)
        self.top_bar_layout.addWidget(self.left_top_bar)
        self.top_bar_layout.setAlignment(self.left_top_bar, Qt.AlignLeft | Qt.AlignVCenter)

        # Logo
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("C:/_Vignesh_N/project_cloud_security/v4/cli/logo.png").scaledToHeight(50, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        self.left_top_bar_layout.addWidget(self.logo_label)
        self.left_top_bar_layout.setAlignment(self.logo_label, Qt.AlignVCenter)

        # Horizontal Menu
        self.menu_bar = QWidget()
        self.menu_bar.setObjectName("menuBar")
        self.menu_layout = QHBoxLayout(self.menu_bar)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(20)
        self.left_top_bar_layout.addWidget(self.menu_bar)
        self.left_top_bar_layout.setAlignment(self.menu_bar, Qt.AlignVCenter | Qt.AlignLeft)

        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        self.menu_layout.addWidget(self.home_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_page))
        self.menu_layout.addWidget(self.settings_button)

        # Add more menu buttons here
        spacer_menu = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.menu_layout.addItem(spacer_menu)


        # --- Right Side (Login Button and Spacer and Username Label) ---
        self.right_top_bar = QWidget()
        self.right_top_bar.setObjectName("rightTopBar")
        self.right_top_bar_layout = QHBoxLayout(self.right_top_bar)
        self.right_top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.right_top_bar_layout.setSpacing(10)
        self.top_bar_layout.addWidget(self.right_top_bar)
        self.top_bar_layout.setAlignment(self.right_top_bar, Qt.AlignRight | Qt.AlignVCenter)

        # Username Label (Initially Hidden)
        self.username_label = QLabel("") # Initially empty
        self.username_label.setObjectName("usernameLabel") # For styling if needed
        self.username_label.setVisible(False) # Initially hide it
        self.right_top_bar_layout.addWidget(self.username_label)
        self.right_top_bar_layout.setAlignment(self.username_label, Qt.AlignRight | Qt.AlignVCenter)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.login_action) # Connect to login function
        self.right_top_bar_layout.addWidget(self.login_button)
        self.right_top_bar_layout.setAlignment(self.login_button, Qt.AlignRight | Qt.AlignVCenter)

        spacer_right_top = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.right_top_bar_layout.addItem(spacer_right_top)


        # --- Content Area (Stacked Widget) ---
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.home_page = HomePage()
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.settings_page)

        self.stacked_widget.setCurrentWidget(self.home_page)
        self.is_initialized = False
        self.logged_in_username = None # Track logged in username

        # --- Window Buttons Toolbar (Minimize, Close) ---
        self.window_buttons_toolbar = QToolBar("Window Controls")
        self.addToolBar(Qt.TopToolBarArea, self.window_buttons_toolbar)
        self.window_buttons_toolbar.setMovable(False)
        self.window_buttons_toolbar.setIconSize(QSize(24,24))
        self.window_buttons_toolbar.setObjectName("windowButtonsToolbar")
        spacer_toolbar = QWidget()
        spacer_toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.window_buttons_toolbar.addWidget(spacer_toolbar)
        self.add_window_buttons()

        self.apply_custom_styles()

    def login_action(self):
        """Opens the Login Dialog and handles login/logout based on result."""
        dialog = LoginDialog(self) # Pass self as parent to center dialog on main window
        dialog.login_successful_signal.connect(self.handle_login_success) # Connect signal

        if dialog.exec_() == QDialog.Accepted: # Show dialog and wait for result
            print("Login dialog accepted (signal should handle UI update)") # UI update is handled by signal now
        else:
            print("Login dialog cancelled.")

    def handle_login_success(self, username):
        """Handles successful login, updates UI."""
        self.logged_in_username = username
        self.login_button.setText("Logout") # Change button text
        self.login_button.clicked.disconnect() # Disconnect login action
        self.login_button.clicked.connect(self.logout_action) # Connect logout action
        self.username_label.setText(f"Logged in as: {username}") # Display username
        self.username_label.setVisible(True) # Make username label visible

    def logout_action(self):
        """Handles logout action."""
        self.logged_in_username = None
        self.login_button.setText("Login") # Change button text back to login
        self.login_button.clicked.disconnect() # Disconnect logout action
        self.login_button.clicked.connect(self.login_action) # Reconnect login action
        self.username_label.setText("") # Clear username label
        self.username_label.setVisible(False) # Hide username label
        print("Logged out")


    def apply_custom_styles(self):
        """Applies custom stylesheets for rounded corners and specific widget styling."""
        self.central_widget.setObjectName("centralWidget")
        self.central_widget.setStyleSheet("""
            #centralWidget {
                background-color: #353535;
                border-radius: 10px;
                margin: 0px;
            }
            QPushButton {
                background-color: #252525;
                color: white;
                border: none;
                padding: 9px 18px;
                border-radius: 7px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #454545;
            }
            QLabel {
                color: white;
                font-size: 15px;
            }
            /* Menu Buttons Style */
            QWidget#menuBar QPushButton {
                background-color: transparent;
                border-radius: 0px;
                padding: 7px 14px;
                font-size: 16px;
                font-weight: normal;
            }
            QWidget#menuBar QPushButton:hover {
                background-color: #454545;
            }
            /* Top Bar Style */
            QWidget#topBar {
                background-color: #252525;
                border-radius: 10px 10px 0 0;
                margin-top: 0px;
            }
             /* Right Top Bar Style - No specific style needed for now */

            /* Window Buttons Toolbar Style */
            QToolBar#windowButtonsToolbar {
                background-color: #252525;
                border: none;
                padding-top: 5px;
                padding-bottom: 5px;
                margin-top: 0px;
            }
             /* Login Button Style (Optional - if you want different style) */
            QPushButton#loginButton {
                background-color: #4285F4; /* Example: Google Blue */
                color: white;
                border-radius: 8px;
                padding: 9px 20px;
                font-weight: bold;
                font-size: 15px;
                margin-right: 10px; /* Add some right margin */
            }
            QPushButton#loginButton:hover {
                background-color: #5A9CF6; /* Slightly lighter blue on hover */
            }
            /* Username Label Style (Optional) */
            QLabel#usernameLabel {
                font-weight: bold;
                margin-right: 15px; /* Add some right margin for spacing */
            }
        """)
        self.menu_bar.setObjectName("menuBar")
        self.top_bar.setObjectName("topBar")
        self.right_top_bar.setObjectName("rightTopBar")
        self.window_buttons_toolbar.setObjectName("windowButtonsToolbar")


    def initialize_ui(self):
        if not self.is_initialized:
            self.showMaximized()
            self.is_initialized = True

    def add_window_buttons(self):
        self.minimize_action = QAction("\u2212", self)
        self.minimize_action.triggered.connect(self.showMinimized)
        self.window_buttons_toolbar.addAction(self.minimize_action)
        self.minimize_action.setToolTip("Minimize")
        self.minimize_action.setObjectName("minimizeButton")

        self.close_action = QAction("\u2715", self)
        self.close_action.triggered.connect(self.close)
        self.window_buttons_toolbar.addAction(self.close_action)
        self.close_action.setToolTip("Close")
        self.close_action.setObjectName("closeButton")
