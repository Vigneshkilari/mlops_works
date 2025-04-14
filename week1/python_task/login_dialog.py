# login_dialog_attractive.py
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QHBoxLayout, QStackedWidget, QWidget, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QRectF, pyqtSignal # Import pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient, QGradient, QPainter, QPainterPath, QColor
import sqlite3
import bcrypt

DATABASE_NAME = 'users.db'  # Define database name

def create_database_and_table():
    """Creates the database and users table if they don't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def username_exists_db(username):
    """Checks if a username already exists in the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def register_user_db(username, password_hash):
    """Registers a new user in the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError: # Handle username already exists error again (though should be checked before)
        conn.close()
        return False

def get_password_hash_db(username):
    """Retrieves the password hash for a given username from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0] # Return only the hash string
    return None # Username not found


class GlassFrame(QWidget): # GlassFrame class remains the same as before ... (code from previous response)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def paintEvent(self, event): # paintEvent function remains the same as before ... (code from previous response)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        rect = self.rect().adjusted(5, 5, -5, -5) # Inner rect for border effect
        rectf = QRectF(rect) # Convert QRect to QRectF - FIX: Convert to QRectF here
        path.addRoundedRect(rectf, 10, 10) # Rounded corners, now using QRectF

        # Background with blur effect (simulated with transparency and gradient)
        painter.fillPath(path, QBrush(QColor(255, 255, 255, 20))) # Very light translucent white

        # Glass effect border
        pen = painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor(255, 255, 255, 50)) # Light border
        painter.setPen(pen)
        painter.drawPath(path)


class LoginDialog(QDialog):
    login_successful_signal = pyqtSignal(str) # Signal to emit username on successful login

    def __init__(self, parent=None):
        super().__init__(parent)
        create_database_and_table() # Ensure database and table exist on dialog creation
        self.setWindowTitle("Login / Register")
        self.setWindowFlag(Qt.FramelessWindowHint) # Frameless dialog for custom look

        # Glass background frame
        self.glass_frame = GlassFrame(self)
        self.glass_frame.setGeometry(self.rect()) # Cover entire dialog

        # Styles (styles remain same as before ...)
        self.setStyleSheet("color: white;")
        self.label_style = "QLabel { font-weight: bold; margin-bottom: 5px; }"
        self.input_style = """ ... """ # Input style (same as before)
        self.button_style = """ ... """ # Button style (same as before)
        self.alt_button_style = """ ... """ # Alt Button style (same as before)
        self.switch_button_style = """ ... """ # Switch button style (same as before)


        # --- Login Form --- (Login form widgets and layout remain same as before ...)
        self.login_widget = QWidget()
        login_layout = QVBoxLayout(self.login_widget)

        self.login_title_label = QLabel("Login")
        self.login_title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.login_title_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(self.login_title_label)

        self.login_username_label = QLabel("Username:")
        self.login_username_label.setStyleSheet(self.label_style)
        self.login_username_input = QLineEdit()
        self.login_username_input.setStyleSheet(self.input_style)
        login_layout.addWidget(self.login_username_label)
        login_layout.addWidget(self.login_username_input)

        self.login_password_label = QLabel("Password:")
        self.login_password_label.setStyleSheet(self.label_style)
        self.login_password_input = QLineEdit()
        self.login_password_input.setStyleSheet(self.input_style)
        self.login_password_input.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.login_password_label)
        login_layout.addWidget(self.login_password_input)

        login_button_layout = QHBoxLayout()
        self.login_login_button = QPushButton("Login")
        self.login_login_button.setStyleSheet(self.button_style)
        self.login_cancel_button = QPushButton("Cancel")
        self.login_cancel_button.setStyleSheet(self.alt_button_style)
        login_button_layout.addWidget(self.login_login_button)
        login_button_layout.addWidget(self.login_cancel_button)
        login_button_layout.setAlignment(Qt.AlignRight)
        login_layout.addLayout(login_button_layout)

        self.login_register_switch_button = QPushButton("Register here")
        self.login_register_switch_button.setStyleSheet(self.switch_button_style)
        login_layout.addWidget(self.login_register_switch_button, alignment=Qt.AlignCenter)


        # --- Register Form --- (Register form widgets and layout remain same as before ...)
        self.register_widget = QWidget()
        register_layout = QVBoxLayout(self.register_widget)

        self.register_title_label = QLabel("Register")
        self.register_title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.register_title_label.setAlignment(Qt.AlignCenter)
        register_layout.addWidget(self.register_title_label)

        self.register_username_label = QLabel("Username:")
        self.register_username_label.setStyleSheet(self.label_style)
        self.register_username_input = QLineEdit()
        self.register_username_input.setStyleSheet(self.input_style)
        register_layout.addWidget(self.register_username_label)
        register_layout.addWidget(self.register_username_input)

        self.register_password_label = QLabel("Password:")
        self.register_password_label.setStyleSheet(self.label_style)
        self.register_password_input = QLineEdit()
        self.register_password_input.setStyleSheet(self.input_style)
        self.register_password_input.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_password_label)
        register_layout.addWidget(self.register_password_input)

        self.register_confirm_password_label = QLabel("Confirm Password:")
        self.register_confirm_password_label.setStyleSheet(self.label_style)
        self.register_confirm_password_input = QLineEdit()
        self.register_confirm_password_input.setStyleSheet(self.input_style)
        self.register_confirm_password_input.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_confirm_password_label)
        register_layout.addWidget(self.register_confirm_password_input)

        register_button_layout = QHBoxLayout()
        self.register_register_button = QPushButton("Register")
        self.register_register_button.setStyleSheet(self.button_style)
        self.register_cancel_button = QPushButton("Cancel")
        self.register_cancel_button.setStyleSheet(self.alt_button_style)
        register_button_layout.addWidget(self.register_register_button)
        register_button_layout.addWidget(self.register_cancel_button)
        register_button_layout.setAlignment(Qt.AlignRight)
        register_layout.addLayout(register_button_layout)

        self.register_login_switch_button = QPushButton("Already have an account? Login")
        self.register_login_switch_button.setStyleSheet(self.switch_button_style)
        register_layout.addWidget(self.register_login_switch_button, alignment=Qt.AlignCenter)


        # --- Stacked Widget to switch between Login and Register --- (Stacked widget setup remains same as before ...)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        main_layout.setContentsMargins(30, 30, 30, 30) # More padding
        main_layout.setSpacing(15)

        # Connections (Connections remain mostly same, accept_login and accept_register are updated)
        self.login_login_button.clicked.connect(self.accept_login)
        self.login_cancel_button.clicked.connect(self.reject)
        self.login_register_switch_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1)) # Switch to Register

        self.register_register_button.clicked.connect(self.accept_register)
        self.register_cancel_button.clicked.connect(self.reject)
        self.register_login_switch_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0)) # Switch to Login

        self.resize(400, 300) # Set initial size


    def accept_login(self):
        """Process login and accept dialog if successful."""
        username = self.login_username_input.text()
        password = self.login_password_input.text()

        stored_password_hash = get_password_hash_db(username)

        if stored_password_hash:
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print(f"Login Successful - Username: {username}")
                self.login_successful_signal.emit(username) # Emit login success signal with username
                self.done(QDialog.Accepted)
            else:
                QMessageBox.warning(self, "Login Failed", "Incorrect password.")
        else:
            QMessageBox.warning(self, "Login Failed", "Username not found.")


    def accept_register(self):
        """Process registration and register user in database."""
        username = self.register_username_input.text()
        password = self.register_password_input.text()
        confirm_password = self.register_confirm_password_input.text()

        if username_exists_db(username):
            QMessageBox.warning(self, "Registration Failed", "Username already taken.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Passwords do not match!")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # Hash and decode for storing as string

        if register_user_db(username, hashed_password):
            QMessageBox.information(self, "Registration Successful", "Registration successful. You can now log in.")
            self.stacked_widget.setCurrentIndex(0) # Switch back to login form
        else:
            QMessageBox.critical(self, "Registration Failed", "Registration failed. Please try again.")


    def get_user_credentials(self):
        """Returns a tuple containing username and password if dialog is accepted (not really used now)."""
        if self.result() == QDialog.Accepted: # Check result from done() - still relevant for cancel
            if self.stacked_widget.currentIndex() == 0: # Login form is active
                return "login", self.login_username_input.text(), self.login_password_input.text()
            elif self.stacked_widget.currentIndex() == 1: # Register form is active
                return "register", self.register_username_input.text(), self.register_password_input.text() # You might want to return more data for registration
        return None, None, None # Return None for operation type if cancelled


    def resizeEvent(self, event): # resizeEvent remains the same as before ...
        super().resizeEvent(event)
        self.glass_frame.setGeometry(self.rect()) # Keep glass frame covering dialog

"""
if __name__ == '__main__': # Main application part remains similar, but needs to be updated to handle signals and UI changes
    app = QApplication(sys.argv)

    # Apply a dark palette globally (optional) (palette code remains same as before ...)
    app.setStyle("Fusion") # Or "Windows", "macOS", etc.
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


    dialog = LoginDialog()
    if dialog.exec_() == QDialog.Accepted: # Dialog exec handling remains mostly the same, but login info is now handled via signal in a real application
        operation_type, username, password = dialog.get_user_credentials() # get_user_credentials is less important now, signal is primary way to get login info
        if operation_type == "login":
            print(f"Login Dialog Accepted (from get_user_credentials) - Username: {username}, Password: {password}") # This part is less relevant now, UI update will be driven by signal
        elif operation_type == "register":
            print(f"Registration Dialog Accepted (from get_user_credentials) - Username: {username}, Password: {password}")
    else:
        print("Login/Register dialog cancelled.")
    sys.exit(app.exec_())"""