from PyQt5 import QtWidgets, QtCore, uic
import sys

class UserMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UserMainWindow, self).__init__()
        uic.loadUi("user_main.ui", self)

        # Remove maximize/minimize
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint
        )

        self.showMaximized()
        self.setFixedSize(self.size())

        # Connect nav buttons
        self.homeBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.searchBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.searchPage))
        self.playlistBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.playlistPage))
        self.profileBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.profilePage))

        # Highlight buttons
        self.homeBtn.clicked.connect(lambda: self.highlightButton(self.homeBtn))
        self.searchBtn.clicked.connect(lambda: self.highlightButton(self.searchBtn))
        self.playlistBtn.clicked.connect(lambda: self.highlightButton(self.playlistBtn))
        self.profileBtn.clicked.connect(lambda: self.highlightButton(self.profileBtn))

        self.highlightButton(self.homeBtn)

        # Connect profile page actions
        self.logoutBtn.clicked.connect(self.logout)

        # Populate test data
        self.loadTestData()

    def logout(self):
        QtWidgets.QMessageBox.information(self, "Logout", "You have been logged out!")
        QtWidgets.qApp.quit()

    def highlightButton(self, btn):
        for b in [self.homeBtn, self.searchBtn, self.playlistBtn, self.profileBtn]:
            b.setStyleSheet("font-size:22px; background: transparent; border:none;")
        btn.setStyleSheet("font-size:28px; background: darkgray; border-radius:10px;")

    def loadTestData(self):
        # Home page test songs
        home_songs = ["Song 1 - Artist A", "Song 2 - Artist B", "Song 3 - Artist C",
                      "Song 4 - Artist D", "Song 5 - Artist E"]
        self.homeSongsList.clear()
        self.homeSongsList.addItems(home_songs)

        # Search page dummy results
        search_results = ["Song A - Artist X", "Song B - Artist Y", "Song C - Artist Z"]
        self.searchResults.clear()
        self.searchResults.addItems(search_results)

        # Playlist page dummy songs
        playlists = ["Favorite 1 - Artist AA", "Favorite 2 - Artist BB", "Favorite 3 - Artist CC"]
        self.playlistList.clear()
        self.playlistList.addItems(playlists)

        # Profile page info (can be dynamic later)
        self.usernameLabel.setText("Username: TestUser")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UserMainWindow()
    window.show()
    sys.exit(app.exec_())
