import sys
import re
import pyodbc
from PyQt5 import QtWidgets, uic
from datetime import datetime
from admin_functions import AdminDashboardHandler
from user_functions import UserDashboardHandler
from music_player import MusicPlayer

# ==================== DATABASE CONNECTION ====================

server = 'Ammars-Laptop\SQLSERVER1'
database = 'HabibifyDatabase'
use_windows_authentication = False
username = 'sa'
password = 'paxxific1_'


def get_connection():
    if use_windows_authentication:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    else:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    return pyodbc.connect(connection_string)


def execute_query(query,
                  params=None,
                  fetch_one=False,
                  fetch_all=True,
                  commit=False):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if commit:
            connection.commit()
            return cursor.rowcount
        elif fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return None

    except pyodbc.Error as e:
        print(f"Database error:  {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def db_authenticate_user(username, password):
    query = """
        SELECT Username, Password, UserType, EmailAddress, UserStatus, 
               PhoneNo, FullName, DateJoined
        FROM Users 
        WHERE Username = ? AND Password = ?  AND UserStatus = 'Active'
    """
    return execute_query(query, (username, password), fetch_one=True)


def db_check_username_exists(username):
    query = "SELECT COUNT(*) FROM Users WHERE Username = ?"
    result = execute_query(query, (username, ), fetch_one=True)
    return result[0] > 0 if result else False


def db_check_email_exists(email):
    query = "SELECT COUNT(*) FROM Users WHERE EmailAddress = ?"
    result = execute_query(query, (email, ), fetch_one=True)
    return result[0] > 0 if result else False


def db_create_user(username, password, fullname, email, phone=None):
    query = """
        INSERT INTO Users (Username, Password, UserType, EmailAddress, UserStatus, PhoneNo, FullName, DateJoined)
        VALUES (?, ?, 'User', ?, 'Active', ?, ?, GETDATE())
    """
    return execute_query(query, (username, password, email, phone, fullname),
                         commit=True) > 0


def db_get_user(username):
    query = """
        SELECT Username, Password, UserType, EmailAddress, UserStatus, 
               PhoneNo, FullName, DateJoined
        FROM Users 
        WHERE Username = ?
    """
    return execute_query(query, (username, ), fetch_one=True)


# ==================== LOGIN WINDOW ====================


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r"App UI\login.ui", self)
        self.invalidInputLabel.setText("")
        self.loginBtn.clicked.connect(self.authenticate)
        self.signupBtn.clicked.connect(self.open_signup)

    def authenticate(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()

        if not username or not password:
            self.invalidInputLabel.setText(
                "Please enter username and password!")
            return

        try:
            user_data = db_authenticate_user(username, password)

            if user_data:
                self.invalidInputLabel.setText("")

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Login successful!")
                msg.exec()

                self.close()

                # user_data:  (Username, Password, UserType, EmailAddress, UserStatus, PhoneNo, FullName, DateJoined)
                usertype = user_data[2]

                if usertype == "Admin":
                    self.dashboard = AdminDashboard(username)
                else:
                    self.dashboard = UserDashboard(username)

                self.dashboard.show()
            else:
                # Check if username exists to give better error message
                if db_check_username_exists(username):
                    self.invalidInputLabel.setText("Invalid password!")
                else:
                    self.invalidInputLabel.setText("Invalid username!")

        except Exception as e:
            self.invalidInputLabel.setText("Database connection error!")
            print(f"Login error: {e}")

    def open_signup(self):
        self.close()
        self.view_signup = SignupWindow()
        self.view_signup.show()


# ==================== SIGNUP WINDOW ====================


class SignupWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r"App UI\signup.ui", self)
        self.invalidInputLabel.setText("")
        self.signupBtn.clicked.connect(self.authenticate)
        self.returnBtn.clicked.connect(self.open_login)

    def authenticate(self):
        username = self.usernameInput.text().strip()
        fullname = self.fullnameInput.text().strip()
        email = self.emailInput.text().strip()
        password1 = self.passwordInput.text()
        password2 = self.confirmPasswordInput.text()

        # Validate all fields are filled
        if not username or not fullname or not email or not password1 or not password2:
            self.invalidInputLabel.setText("Please fill out all fields!")
            return

        # Validate username format
        pattern = r'^[A-Za-z0-9._]{2,15}$'
        if not re.match(pattern, username):
            self.invalidInputLabel.setText(
                "Username must be alphanumeric, 2-15 characters!")
            return

        # Check if username already exists
        try:
            if db_check_username_exists(username):
                self.invalidInputLabel.setText("Username already exists!")
                return
        except Exception as e:
            self.invalidInputLabel.setText("Database connection error!")
            print(f"Username check error: {e}")
            return

        # Validate email format
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            self.invalidInputLabel.setText("Invalid email entered!")
            return

        # Check if email already exists
        try:
            if db_check_email_exists(email):
                self.invalidInputLabel.setText("Email already registered!")
                return
        except Exception as e:
            self.invalidInputLabel.setText("Database connection error!")
            print(f"Email check error: {e}")
            return

        # Validate password
        if len(password1) < 8 or " " in password1:
            self.invalidInputLabel.setText(
                "Password must have at least 8 characters (no spaces)!")
            return

        # Check passwords match
        if password1 != password2:
            self.invalidInputLabel.setText("Passwords do not match!")
            return

        # Validate full name
        if len(fullname) < 2:
            self.invalidInputLabel.setText(
                "Full name must be at least 2 characters!")
            return

        # Create user in database
        try:
            if db_create_user(username, password1, fullname, email):
                QtWidgets.QMessageBox.information(
                    self, "Success", "Signup successful!  You can now login.")
                self.open_login()
            else:
                self.invalidInputLabel.setText(
                    "Failed to create account.  Try again!")
        except Exception as e:
            self.invalidInputLabel.setText("Database error occurred!")
            print(f"Signup error: {e}")

    def open_login(self):
        self.close()
        self.view_login = LoginWindow()
        self.view_login.show()


class AdminDashboard(QtWidgets.QMainWindow):

    def __init__(self, username):
        super().__init__()
        uic.loadUi(r"App UI\admin_main.ui", self)

        self.username = username
        self.welcomeLabel.setText(f"Welcome back, {username}!")

        self.page_map = {
            self.artistrequestsBtn: self.artistRequestsPage,
            self.analyticsBtn: self.AnalyticsPage,
            self.usermanagementBtn: self.usersPage,
            self.reportsBtn: self.ReportsPage,
            self.pendingSongsBtn: self.PendingSongsPage
        }

        self.reportedSongsTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.pendingSongsTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.artistsRequestTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        for btn in self.page_map:
            btn.clicked.connect(self.switch_page)

        self.logoutBtn.clicked.connect(self.logout)

        self.handler = AdminDashboardHandler(self)
        self.handler.load_all_data()
        self.handler.connect_signals()

        self.highlight_button(self.artistrequestsBtn)
        self.stackedWidget.setCurrentWidget(self.artistRequestsPage)

    def switch_page(self):
        sender = self.sender()
        page = self.page_map.get(sender)
        if page:
            self.stackedWidget.setCurrentWidget(page)
            self.highlight_button(sender)
            # Refresh data when switching pages
            self.refresh_current_page(page)

    def refresh_current_page(self, page):
        try:
            if page == self.artistRequestsPage:
                self.handler.load_artist_requests_table()
            elif page == self.usersPage:
                self.handler.load_users_table()
            elif page == self.PendingSongsPage:
                self.handler.load_pending_songs_table()
            elif page == self.ReportsPage:
                self.handler.load_reported_songs_table()
            elif page == self.AnalyticsPage:
                self.handler.load_subscription_plans_table()
                self.handler.load_genre_table()
        except Exception as e:
            print(f"Error refreshing page:  {e}")

    def highlight_button(self, active_btn):
        for btn in self.page_map:
            btn.setChecked(False)
        active_btn.setChecked(True)

    def logout(self):
        self.close()
        self.loginwindow = LoginWindow()
        self.loginwindow.show()


class UserDashboard(QtWidgets.QMainWindow):

    def __init__(self, username):
        super().__init__()
        uic.loadUi(r"App UI\artist_main.ui", self)

        self.username = username

        # Get user data from database
        try:
            self.user_data = db_get_user(username)
        except Exception as e:
            print(f"Error getting user data: {e}")
            self.user_data = None

        # Setup table headers
        tables = [
            self.RR_Table, self.Top5Artists_Table, self.Top5Songs_Table,
            self.PL_Table, self.Queue_Table, self.searchSongs_Table,
            self.searchArtists_Table, self.artistSongs_Table,
            self.tableWidget_2, self.tableWidget
        ]
        for table in tables:
            table.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        # Create music player first
        self.music_player = MusicPlayer(self)

        # Create handler and pass music player
        self.handler = UserDashboardHandler(self, username, self.music_player)

        # Load data and connect signals
        self.handler.load_all_data()
        self.handler.connect_signals()

    def logout(self):
        if hasattr(self, 'music_player'):
            self.music_player.cleanup()
        self.close()
        self.loginwindow = LoginWindow()
        self.loginwindow.show()

    def closeEvent(self, event):
        if hasattr(self, 'music_player'):
            self.music_player.cleanup()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
