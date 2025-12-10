import sys
import re
from PyQt5 import QtWidgets, uic
from data import *
from admin_functions import AdminDashboardHandler
from user_functions import UserDashboardHandler
from music_player import MusicPlayer


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r"App UI\login.ui", self)
        self.invalidInputLabel.setText("")
        self.loginBtn.clicked.connect(self.authenticate)
        self.signupBtn.clicked.connect(self.open_signup)

    def authenticate(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if username in Users.keys():
            data = Users[username]
            if data[1] == password:
                self.invalidInputLabel.setText("")

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Login successful!")
                msg.exec()

                self.close()

                usertype = data[4]
                if usertype == "Admin":
                    self.dashboard = AdminDashboard(username)
                else:
                    self.dashboard = UserDashboard(username)

                self.dashboard.show()
            else:
                self.invalidInputLabel.setText("Invalid password!")
        else:
            self.invalidInputLabel.setText("Invalid username!")

    def open_signup(self):
        self.close()
        self.view_signup = SignupWindow()
        self.view_signup.show()


class SignupWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r"App UI\signup.ui", self)
        self.invalidInputLabel.setText("")
        self.signupBtn.clicked.connect(self.authenticate)
        self.returnBtn.clicked.connect(self.open_login)

    def authenticate(self):
        username = self.usernameInput.text()
        fullname = self.fullnameInput.text()
        email = self.emailInput.text()
        password1 = self.passwordInput.text()
        password2 = self.confirmPasswordInput.text()

        if not username or not fullname or not email or not password1 or not password2:
            self.invalidInputLabel.setText("Please fill out all fields!")
            return

        if username in Users.keys():
            self.invalidInputLabel.setText("Username already exists!")
            return

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            self.invalidInputLabel.setText("Invalid email entered!")
            return

        if (len(password1) < 8) or (" " in password1):
            self.invalidInputLabel.setText(
                "Password must have at least 8 characters (no spaces)!")
            return

        if password1 != password2:
            self.invalidInputLabel.setText("Passwords do not match!")
            return

        pattern = r'^[A-Za-z0-9._]{2,15}$'
        if not re.match(pattern, username):
            self.invalidInputLabel.setText(
                "Username must be alphanumeric, 2-15 characters!")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        Users[username] = [
            fullname, password1, email, r"Profile Pictures\default. jpg",
            "Listener", "Free", 0, today
        ]

        QtWidgets.QMessageBox.information(self, "Success",
                                          "Signup successful!")
        self.open_login()

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
        self.user_data = get_user(username)

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
