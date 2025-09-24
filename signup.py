# login.py
import sys
from PyQt5 import QtWidgets, uic  # Use PyQt6 if you prefer: from PyQt6 import QtWidgets, uic

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("signup.ui", self)  # Load the .ui file

        # Connect buttons
        # self.loginBtn.clicked.connect(self.handle_login)

    # def handle_login(self):
    #     username = self.usernameInput.text()
    #     password = self.passwordInput.text()

    #     # Example: simple check
    #     if username == "admin" and password == "password":
    #         self.errorLabel.setText("")
    #         QtWidgets.QMessageBox.information(self, "Success", "Login successful!")
    #         # Here you can open AdminMainWindow or another page
    #         # e.g., self.open_admin_dashboard()
    #     else:
    #         self.errorLabel.setText("Invalid username or password!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
