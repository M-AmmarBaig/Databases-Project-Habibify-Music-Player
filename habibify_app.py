import sys, re
from PyQt5 import QtWidgets, uic
from data import *
from admin_functions import AdminDashboardHandler


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        #Load the Login Page
        uic.loadUi(r"App UI\login.ui", self)

        #Initializing Widgets
        self.invalidInputLabel.setText("")

        #Connecting buttons
        self.loginBtn.clicked.connect(self.authenticate)
        self.signupBtn.clicked.connect(self.open_signup)

    #Function to check if username and passwords are correct
    def authenticate(self):

        #Obtaining field inputs
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        #Checking if inputs are correct
        if username in Users.keys():
            data = Users[username]
            if data[1] == password:
                self.invalidInputLabel.setText("")

                #Showing success prompt for acknowledgement
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setWindowTitle("Success")
                msg.setText("Login successful!")
                msg.exec()

                self.close()  # Close the login window

                #Open dashboard depending on type of user
                usertype = data[4]
                if usertype == "Admin":
                    self.dashboard = AdminDashboard(username)  # Pass username
                elif usertype == "Artist":
                    # self.dashboard = ArtistDashboard(username) # Placeholder
                    print("Artist Dashboard not implemented yet.")
                    return
                else:
                    # self.dashboard = ListenerDashboard(username) # Placeholder
                    print("Listener Dashboard not implemented yet.")
                    return

                self.dashboard.show()

            else:
                self.invalidInputLabel.setText("Invalid password!")
            # Here you can open AdminMainWindow or another page
            # e.g., self.open_admin_dashboard()
        else:
            self.invalidInputLabel.setText("Invalid username!")

    #Open the signup page
    def open_signup(self):
        self.close()
        self.view_signup = SignupWindow()
        self.view_signup.show()


class SignupWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        #Load the signup page
        uic.loadUi(r"App UI\signup.ui", self)

        #Initialize Widgets
        self.invalidInputLabel.setText("")

        #Connect Buttons
        self.signupBtn.clicked.connect(self.authenticate)
        self.returnBtn.clicked.connect(self.open_login)

    #Verify field inputs and add to field
    def authenticate(self):

        #Obtain field inputs
        username = self.usernameInput.text()
        fullname = self.fullnameInput.text()
        email = self.emailInput.text()
        password1 = self.passwordInput.text()
        password2 = self.confirmPasswordInput.text()

        #Checking for empty fields
        if not username or not fullname or not email or not password1 or not password2:
            self.invalidInputLabel.setText("Please fill out all fields!")
            return

        #Checking if username exists already
        if username in Users.keys():
            self.invalidInputLabel.setText("Username already exists!")
            return

        #Validating email field
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            self.invalidInputLabel.setText("Invalid email entered!")
            return

        #Validating password input
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
                "Username must be alphanumeric, and 2 to 15 characters!")
            return

        #Entering valid data into database
        today = datetime.now().strftime("%Y-%m-%d")
        Users[username] = [
            fullname, password1, email, r"Profile Pictures\default.jpg",
            "Listener", "Free", 0, today
        ]

        QtWidgets.QMessageBox.information(
            self, "Success", "Signup successful! Returning to login page...")
        self.open_login()

    #Return back to the login page
    def open_login(self):
        self.close()
        self.view_login = LoginWindow()
        self.view_login.show()


class AdminDashboard(QtWidgets.QMainWindow):

    def __init__(self, username):
        super().__init__()
        uic.loadUi(r"App UI\admin_main.ui", self)

        # Store username and set welcome label
        self.username = username
        self.welcomeLabel.setText(f"Welcome back, {self.username}!")

        #Sidebar Page Navigation
        self.page_map = {
            self.artistrequestsBtn: self.artistRequestsPage,
            self.analyticsBtn: self.AnalyticsPage,
            self.usermanagementBtn: self.usersPage,
            self.reportsBtn: self.ReportsPage,
            self.pendingSongsBtn: self.PendingSongsPage
        }
        self.welcomeLabel.setText(f"Welcome back, {username}!")
        self.reportedSongsTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.pendingSongsTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.artistsRequestTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        # Connect sidebar buttons
        for btn in self.page_map:
            btn.clicked.connect(self.switch_page)

        # Connect logout button
        self.logoutBtn.clicked.connect(self.logout)

        # This one line creates the handler and passes it a reference to this window
        self.handler = AdminDashboardHandler(self)

        # Call the handler's methods to load data and connect signals
        self.handler.load_all_data()
        self.handler.connect_signals()

        # Set initial view to artistsRequestsPage
        self.highlight_button(self.artistrequestsBtn)
        self.stackedWidget.setCurrentWidget(self.artistRequestsPage)

    def switch_page(self):

        sender = self.sender()
        page = self.page_map.get(sender)
        if page:
            self.stackedWidget.setCurrentWidget(page)
            self.highlight_button(sender)

    def highlight_button(self, active_btn):

        # Reset all buttons first
        for btn in self.page_map:
            btn.setChecked(False)

        # Set the active button to checked
        active_btn.setChecked(True)

    def logout(self):

        print("Logging out of admin menu...")
        self.close()
        self.loginwindow = LoginWindow()
        self.loginwindow.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
