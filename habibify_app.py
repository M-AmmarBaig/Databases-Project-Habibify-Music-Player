import sys, re

from PyQt5 import QtWidgets, uic

Users = {
    "Ammar" : ["Muhammad Ammar Baig", "ammarbaig123", "ammar@gmail.com", r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\Profile Pictures\Ammar.jpeg", "Admin"],
    "Sarosh" : ["Sarosh Mehdi Yusuf", "saroshmehdi123", "sarosh@gmail.com", r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\Profile Pictures\Charlie.jpeg", "Admin"],
    "Charlie" : ["Sir Christopher Nolan", "christopher123", "christopher@gmail.com", r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\Profile Pictures\Christopher.jpeg", "Listener"],
    "Ezekiel" : ["Ezekiel Woods", "ezekiel123", "ezekiel@gmail.com", r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\Profile Pictures\Ezekiel.jpeg", "Listener"],
    "Samantha" : ["Samantha Williams", "samantha123", "samantha@gmail.com", r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\Profile Pictures\Samantha.jpeg", "Artist"],
    "Shawn" : ["Shawn Mendes", "shawn123", "shawn@gmail.com", r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\Profile Pictures\Shawn.jpeg", "Artist"]
}


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
                
                self.close() # Close the login window
                
                #Open dashboard depending on type of user
                usertype = data[4]
                if usertype == "Admin":
                    self.dashboard = AdminDashboard(username)
                elif usertype == "Artist":
                    self.dashboard = ArtistDashboard(username)
                else:
                    self.dashboard = ListenerDashboard(username)
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
            self.invalidInputLabel.setText("Password must have at least 8 characters (no spaces)!")
            return
        if password1 != password2:
            self.invalidInputLabel.setText("Passwords do not match!")
            return
        
        
        #Entering valid data into database
        Users[username] = [fullname, password1, email, "", "Listener"]
        QtWidgets.QMessageBox.information(self, "Success", "Signup successful! Returning to login page...")
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

        # Map buttons to pages
        self.page_map = {
            self.artistrequestsBtn: self.artistRequestsPage,
            self.analyticsBtn: self.AnalyticsPage,
            self.usermanagementBtn: self.usersPage,
            self.reportsBtn: self.ReportsPage,
            self.pendingSongsBtn: self.PendingSongsPage
        }

        # Connect buttons to handler
        for btn in self.page_map:
            btn.clicked.connect(self.switch_page)

        # Connect other buttons
        self.logoutBtn.clicked.connect(self.logout)

        # Highlight first button by default
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
            btn.setStyleSheet(
                "QPushButton {background: none; color: #eee; font-size:16px; padding:10px; border-radius:5px;} "
                "QPushButton:hover {background-color:#2c2c2c;}"
            )
        # Apply highlight to active
        active_btn.setStyleSheet(
            "QPushButton {background-color: #3a7ef0; color: #fff; font-weight:bold; font-size:16px; padding:10px; border-radius:5px;}"
        )

    def logout(self):
        print("Logging out of admin menu...")
        self.close()
        self.loginwindow = LoginWindow()
        self.loginwindow.show()
        

    # Placeholder methods for admin actions
    def delete_reported_song(self):
        print("Delete reported song clicked")
        # Logic to delete selected reported song

    def delete_user(self):
        print("Delete user clicked")
        # Logic to delete selected user

    def view_song(self):
        print("View song clicked")
        # Logic to view selected pending song

    def accept_song(self):
        print("Accept song clicked")
        # Logic to accept selected pending song

    def reject_song(self):
        print("Reject song clicked")
        # Logic to reject selected pending song
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())