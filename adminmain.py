from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

class AdminMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("admin_main.ui", self)

        # Map buttons to pages
        self.page_map = {
            self.requestsBtn: self.artistRequestsPage,
            self.manageBtn: self.manageArtistsPage,
            self.analyticsBtn: self.analyticsPage,
            self.usersBtn: self.usersPage,
            self.profileBtn: self.profilePage
        }

        # Connect buttons to handler
        for btn in self.page_map:
            btn.clicked.connect(self.switch_page)

        self.logoutBtn.clicked.connect(self.logout)
        self.themeToggleBtn.clicked.connect(self.toggle_theme)

        # Default theme: dark
        self.dark_mode = True
        self.set_theme(self.dark_mode)

        # Highlight first button by default
        self.highlight_button(self.requestsBtn)
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
            btn.setStyleSheet("QPushButton {background: none; color: #eee; font-size:16px; padding:10px; border-radius:5px;} QPushButton:hover {background-color:#2c2c2c;}")
        # Apply highlight to active
        active_btn.setStyleSheet("QPushButton {background-color: #3a7ef0; color: #fff; font-weight:bold; font-size:16px; padding:10px; border-radius:5px;}")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme(self.dark_mode)

    def set_theme(self, dark=True):
        if dark:
            # Sidebar and page dark theme
            self.sidebar.setStyleSheet("QFrame { background-color: #1e1e1e; }")
            for btn in self.page_map:
                btn.setStyleSheet("QPushButton {background: none; color: #eee; font-size:16px; padding:10px; border-radius:5px;} QPushButton:hover {background-color:#2c2c2c;}")
            self.logoutBtn.setStyleSheet("background:red; color:white; font-weight:bold; border-radius:5px; padding:10px;")
            self.stackedWidget.setStyleSheet("QWidget {background-color: #121212; color: #fff;}")
        else:
            # Light theme
            self.sidebar.setStyleSheet("QFrame { background-color: #f0f0f0; }")
            for btn in self.page_map:
                btn.setStyleSheet("QPushButton {background: none; color: #000; font-size:16px; padding:10px; border-radius:5px;} QPushButton:hover {background-color:#ddd;}")
            self.logoutBtn.setStyleSheet("background:red; color:white; font-weight:bold; border-radius:5px; padding:10px;")
            self.stackedWidget.setStyleSheet("QWidget {background-color: #fff; color: #000;}")

    def logout(self):
        print("Logging out...")
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AdminMainWindow()
    window.show()
    sys.exit(app.exec_())
