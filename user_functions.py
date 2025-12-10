import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from data import *
from datetime import datetime


class PlaylistSongsDialog(QtWidgets.QDialog):

    def __init__(self, parent, playlist_name, songs):
        super().__init__(parent)
        self.setWindowTitle(f"Playlist:  {playlist_name}")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #121212; color: #fff;")

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel(f"🎵 {playlist_name}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Song Name", "Artist", "Genre"])
        self.table.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setRowCount(len(songs))

        for row, song in enumerate(songs):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(song[0]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(song[1]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(song[2]))

        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet(
            "background-color: #1DB954; color: white; padding: 10px; border-radius: 5px;"
        )
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


class AddToPlaylistDialog(QtWidgets.QDialog):

    def __init__(self, parent, playlists):
        super().__init__(parent)
        self.setWindowTitle("Add to Playlist")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #121212; color: #fff;")
        self.selected_playlist = None

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel("Select a Playlist")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        self.playlist_list = QtWidgets.QListWidget()
        self.playlist_list.setStyleSheet(
            "background-color: #FFFFFF; color: #000000;")
        for playlist in playlists:
            self.playlist_list.addItem(playlist)
        layout.addWidget(self.playlist_list)

        btn_layout = QtWidgets.QHBoxLayout()

        add_btn = QtWidgets.QPushButton("Add")
        add_btn.setStyleSheet(
            "background-color: #1DB954; color: white; padding: 10px; border-radius: 5px;"
        )
        add_btn.clicked.connect(self.accept_selection)
        btn_layout.addWidget(add_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "background-color: #ff0000; color: white; padding:  10px; border-radius:  5px;"
        )
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def accept_selection(self):
        if self.playlist_list.currentItem():
            self.selected_playlist = self.playlist_list.currentItem().text()
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "No Selection",
                                          "Please select a playlist.")


class ReportSongDialog(QtWidgets.QDialog):

    def __init__(self, parent, song_name):
        super().__init__(parent)
        self.setWindowTitle(f"Report:  {song_name}")
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #121212; color: #fff;")
        self.report_reason = None

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel(f"Report '{song_name}'")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        layout.addWidget(QtWidgets.QLabel("Select Reason:"))

        self.reason_combo = QtWidgets.QComboBox()
        self.reason_combo.setStyleSheet(
            "background-color: #FFFFFF; color: #000000; padding: 5px;")
        self.reason_combo.addItems([
            "Inappropriate Content", "Copyright Violation",
            "Audio Quality Issues", "Hate Speech", "Violence", "Other"
        ])
        layout.addWidget(self.reason_combo)

        layout.addWidget(QtWidgets.QLabel("Additional Comments (optional):"))

        self.comments_input = QtWidgets.QLineEdit()
        self.comments_input.setStyleSheet(
            "background-color: #FFFFFF; color:  #000000; padding: 5px;")
        layout.addWidget(self.comments_input)

        btn_layout = QtWidgets.QHBoxLayout()

        submit_btn = QtWidgets.QPushButton("Submit Report")
        submit_btn.setStyleSheet(
            "background-color: #ff0000; color: white; padding: 10px; border-radius: 5px;"
        )
        submit_btn.clicked.connect(self.submit_report)
        btn_layout.addWidget(submit_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "background-color: #3a3a3a; color: white; padding: 10px; border-radius: 5px;"
        )
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def submit_report(self):
        self.report_reason = self.reason_combo.currentText()
        self.accept()


class AnalyticsGraphDialog(QtWidgets.QDialog):
    """Dialog to display analytics graphs.  Accepts data as 2D array [[x, y], ...]"""

    def __init__(self, parent, title, data, x_label, y_label):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color:  #121212; color: #fff;")

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        try:
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.figure import Figure

            fig = Figure(figsize=(10, 6), facecolor='#121212')
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)

            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')

            if data:
                x_values = [item[0] for item in data]
                y_values = [item[1] for item in data]

                ax.plot(x_values,
                        y_values,
                        marker='o',
                        linestyle='-',
                        linewidth=2,
                        color='#1DB954',
                        markersize=8)
                ax.fill_between(x_values, y_values, alpha=0.3, color='#1DB954')

                ax.set_xlabel(x_label, fontsize=12, color='white')
                ax.set_ylabel(y_label, fontsize=12, color='white')
                ax.set_title(title.replace('\n', ' '),
                             fontsize=14,
                             color='white')
                ax.grid(True, alpha=0.3, color='gray')

                if len(x_values) > 6:
                    ax.set_xticks(x_values[::max(1, len(x_values) // 6)])
                fig.autofmt_xdate(rotation=45)
            else:
                ax.text(0.5,
                        0.5,
                        'No data available',
                        ha='center',
                        va='center',
                        fontsize=16,
                        color='white',
                        transform=ax.transAxes)

            fig.tight_layout()
            layout.addWidget(canvas)

        except ImportError:
            error_label = QtWidgets.QLabel(
                "Matplotlib not installed.\npip install matplotlib")
            error_label.setStyleSheet("font-size: 14px; color: #ff6666;")
            error_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(error_label)

            if data:
                table = QtWidgets.QTableWidget()
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels([x_label, y_label])
                table.setStyleSheet(
                    "background-color: #FFFFFF; color: #000000;")
                table.setRowCount(len(data))

                for row, item in enumerate(data):
                    table.setItem(row, 0,
                                  QtWidgets.QTableWidgetItem(str(item[0])))
                    table.setItem(row, 1,
                                  QtWidgets.QTableWidgetItem(str(item[1])))

                table.resizeColumnsToContents()
                layout.addWidget(table)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet(
            "background-color: #1DB954; color: white; padding: 10px; border-radius: 5px;"
        )
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


class UserDashboardHandler:

    def __init__(self,
                 window: QtWidgets.QMainWindow,
                 username: str,
                 music_player=None):
        self.window = window
        self.username = username
        self.user_data = get_user(username)
        self.music_player = music_player
        self.selected_queue_row = None
        self.selected_artist_song_id = None

    def set_music_player(self, music_player):
        self.music_player = music_player

    def connect_signals(self):
        # Navigation
        self.window.homeBtn.clicked.connect(lambda: self.switch_page(
            self.window.homePage, self.window.homeBtn))
        self.window.searchNavBtn.clicked.connect(lambda: self.switch_page(
            self.window.searchPage, self.window.searchNavBtn))
        self.window.libraryBtn.clicked.connect(lambda: self.switch_page(
            self.window.libraryPage, self.window.libraryBtn))
        self.window.analyticsBtn.clicked.connect(lambda: self.switch_page(
            self.window.analyticsPage, self.window.analyticsBtn))
        self.window.profileBtn.clicked.connect(lambda: self.switch_page(
            self.window.profilePage, self.window.profileBtn))
        self.window.logoutBtn.clicked.connect(self.handle_logout)

        # Home Page
        self.window.RR_Table.cellClicked.connect(
            self.populate_recent_rotation_form)
        self.window.RR_PlaySongBtn.clicked.connect(self.handle_play_song)
        self.window.RR_AddQueueBtn.clicked.connect(self.handle_add_to_queue)
        self.window.RR_AddPlaylistBtn.clicked.connect(
            self.handle_add_to_playlist)
        self.window.RR_RefreshBtn.clicked.connect(self.load_home_data)

        # Library Page - Playlists
        self.window.PL_Table.cellClicked.connect(self.populate_playlist_form)
        self.window.PL_ViewBtn.clicked.connect(self.handle_view_playlist)
        self.window.PL_PlayBtn.clicked.connect(self.handle_play_playlist)
        self.window.PL_DeleteBtn.clicked.connect(self.handle_delete_playlist)
        self.window.PL_ViewBtn_3.clicked.connect(self.handle_create_playlist)

        # Library Page - Queue
        self.window.Queue_Table.cellClicked.connect(
            self.populate_queue_selection)
        self.window.Queue_PlayBtn.clicked.connect(self.handle_play_queue)
        self.window.Queue_RemoveBtn.clicked.connect(
            self.handle_remove_from_queue)
        self.window.Queue_ClearBtn.clicked.connect(self.handle_clear_queue)

        # Search Page
        self.window.S_SearchBtn.clicked.connect(self.handle_search)
        self.window.SearchSong.returnPressed.connect(self.handle_search)
        self.window.searchSongs_Table.cellClicked.connect(
            self.populate_search_song_form)
        self.window.searchArtists_Table.cellClicked.connect(
            self.populate_search_artist_form)
        self.window.S_AddQueueBtn.clicked.connect(
            self.handle_search_add_to_queue)
        self.window.S_AddPlBtn.clicked.connect(
            self.handle_search_add_to_playlist)
        self.window.S_AddPlBtn_2.clicked.connect(self.handle_search_play_song)
        self.window.S_ReportBtn.clicked.connect(self.handle_report_song)

        # Analytics Page
        self.window.tableWidget_2.cellClicked.connect(
            self.populate_artist_song_form)
        self.window.S_AddQueueBtn_2.clicked.connect(self.handle_add_new_song)
        self.window.S_ReportBtn_3.clicked.connect(
            self.handle_delete_artist_song)
        self.window.RevenueViewBtn.clicked.connect(self.handle_view_analytics)

        # Profile Page
        self.window.tableWidget.cellClicked.connect(
            self.populate_subscription_form)
        self.window.P_BuyPlanBtn.clicked.connect(self.handle_buy_plan)
        self.window.S_ReportBtn_2.clicked.connect(self.handle_delete_account)

    def load_all_data(self):
        self.load_home_data()
        self.load_library_data()
        self.load_analytics_data()
        self.load_profile_data()
        self.clear_search_form()
        self.switch_page(self.window.homePage, self.window.homeBtn)

    # ==================== UTILITY METHODS ====================

    def get_song_genre(self, song_name):
        for data in get_approved_songs().values():
            if data[0] == song_name:
                return data[2]
        return "Unknown"

    def get_analytics_data(self, analytics_type, group_by, start_date,
                           end_date) -> list:
        """Get analytics data as 2D array [[x, y], ...]"""
        if analytics_type == "views":
            raw_data = get_artist_views_data(self.username)
        else:
            raw_data = get_artist_revenue_data(self.username)

        if not raw_data:
            return []

        # Filter by date range
        filtered = {
            k: v
            for k, v in raw_data.items() if start_date <= k <= end_date
        }

        if not filtered:
            return []

        # Group by period
        grouped = {}
        for date_str, value in sorted(filtered.items()):
            if group_by == "day":
                key = date_str
            elif group_by == "month":
                key = date_str[:7]
            elif group_by == "year":
                key = date_str[:4]
            else:
                key = date_str

            grouped[key] = grouped.get(key, 0) + value

        return [[k, v] for k, v in sorted(grouped.items())]

    def add_song_to_playlist_dialog(self, song_name, artist_name):
        user_playlists = get_user_playlists(self.username)
        playlist_names = list(user_playlists.keys())

        if not playlist_names:
            QtWidgets.QMessageBox.warning(self.window, "No Playlists",
                                          "Create a playlist first!")
            return

        dialog = AddToPlaylistDialog(self.window, playlist_names)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_playlist = dialog.selected_playlist
            genre = self.get_song_genre(song_name)
            add_song_to_playlist(self.username, selected_playlist,
                                 [song_name, artist_name, genre])
            self.load_playlists_table()
            self.window.S_ArtistName_3.setText(selected_playlist)
            QtWidgets.QMessageBox.information(
                self.window, "Added",
                f"'{song_name}' added to '{selected_playlist}'.")

    # ==================== NAVIGATION ====================

    def switch_page(self, page, button):
        self.window.stackedWidget.setCurrentWidget(page)
        for btn in [
                self.window.homeBtn, self.window.searchNavBtn,
                self.window.libraryBtn, self.window.analyticsBtn,
                self.window.profileBtn
        ]:
            btn.setChecked(False)
        button.setChecked(True)

    def handle_logout(self):
        reply = QtWidgets.QMessageBox.question(
            self.window, "Logout", "Are you sure you want to logout?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.window.logout()

    # ==================== HOME PAGE ====================

    def load_home_data(self):
        self.load_recent_rotation_table()
        self.load_top_artists_table()
        self.load_top_songs_table()
        self.window.RR_SongName.clear()
        self.window.RR_ArtistName.clear()
        self.window.RR_Listens.clear()

    def load_recent_rotation_table(self):
        recent_rotation = get_user_recent_rotation(self.username)
        table = self.window.RR_Table
        table.setRowCount(len(recent_rotation))
        for row, data in enumerate(recent_rotation):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[2])))
        table.resizeColumnsToContents()

    def load_top_artists_table(self):
        top_artists = get_top_artists_weekly()
        table = self.window.Top5Artists_Table
        table.setRowCount(len(top_artists))
        for row, data in enumerate(top_artists):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[1])))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
        table.resizeColumnsToContents()

    def load_top_songs_table(self):
        top_songs = get_top_songs_weekly()
        table = self.window.Top5Songs_Table
        table.setRowCount(len(top_songs))
        for row, data in enumerate(top_songs):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[2])))
        table.resizeColumnsToContents()

    def populate_recent_rotation_form(self, row, column):
        table = self.window.RR_Table
        self.window.RR_SongName.setText(table.item(row, 0).text())
        self.window.RR_ArtistName.setText(table.item(row, 1).text())
        self.window.RR_Listens.setText(table.item(row, 2).text())

        pixmap = QtGui.QPixmap("Song_images/default_song_image.jpg")
        if not pixmap.isNull():
            self.window.RR_SongImage.setPixmap(
                pixmap.scaled(self.window.RR_SongImage.size(),
                              QtCore.Qt.KeepAspectRatio,
                              QtCore.Qt.SmoothTransformation))

    def handle_play_song(self):
        song_name = self.window.RR_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to play.")
            return
        if self.music_player:
            self.music_player.play_song_by_name(song_name)

    def handle_add_to_queue(self):
        song_name = self.window.RR_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song.")
            return

        artist_name = self.window.RR_ArtistName.text()
        genre = self.get_song_genre(song_name)
        today = datetime.now().strftime("%Y-%m-%d")

        add_to_user_queue(self.username,
                          [song_name, artist_name, genre, today])
        self.load_queue_table()
        QtWidgets.QMessageBox.information(
            self.window, "Added to Queue",
            f"'{song_name}' added to your queue.")

    def handle_add_to_playlist(self):
        song_name = self.window.RR_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song.")
            return
        self.add_song_to_playlist_dialog(song_name,
                                         self.window.RR_ArtistName.text())

    # ==================== LIBRARY PAGE ====================

    def load_library_data(self):
        self.load_playlists_table()
        self.load_queue_table()
        self.window.PL_Name.clear()
        self.window.PL_Visits.clear()
        self.window.PL_Date.setDate(QtCore.QDate.currentDate())

    def load_playlists_table(self):
        user_playlists = get_user_playlists(self.username)
        table = self.window.PL_Table
        table.setRowCount(len(user_playlists))
        for row, (name, data) in enumerate(user_playlists.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            table.setItem(row, 1,
                          QtWidgets.QTableWidgetItem(str(len(data["songs"]))))
            table.setItem(row, 2,
                          QtWidgets.QTableWidgetItem(str(data["visits"])))
            table.setItem(row, 3,
                          QtWidgets.QTableWidgetItem(data["created_date"]))
        table.resizeColumnsToContents()

    def load_queue_table(self):
        user_queue = get_user_queue(self.username)
        table = self.window.Queue_Table
        table.setRowCount(len(user_queue))
        for row, data in enumerate(user_queue):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[3]))
        table.resizeColumnsToContents()

    def populate_playlist_form(self, row, column):
        table = self.window.PL_Table
        self.window.PL_Name.setText(table.item(row, 0).text())
        self.window.PL_Visits.setText(table.item(row, 2).text())
        self.window.PL_Date.setDate(
            QtCore.QDate.fromString(table.item(row, 3).text(), "yyyy-MM-dd"))

    def populate_queue_selection(self, row, column):
        self.selected_queue_row = row

    def handle_view_playlist(self):
        playlist_name = self.window.PL_Name.text()
        if not playlist_name:
            QtWidgets.QMessageBox.warning(self.window, "No Playlist Selected",
                                          "Please select a playlist.")
            return

        user_playlists = get_user_playlists(self.username)
        if playlist_name in user_playlists:
            songs = user_playlists[playlist_name]["songs"]
            dialog = PlaylistSongsDialog(self.window, playlist_name, songs)
            dialog.exec_()
            increment_playlist_visits(self.username, playlist_name)
            self.load_playlists_table()

    def handle_play_playlist(self):
        playlist_name = self.window.PL_Name.text()
        if not playlist_name:
            QtWidgets.QMessageBox.warning(self.window, "No Playlist Selected",
                                          "Please select a playlist.")
            return

        user_playlists = get_user_playlists(self.username)
        if playlist_name not in user_playlists:
            return

        songs = user_playlists[playlist_name]["songs"]
        if not songs:
            QtWidgets.QMessageBox.warning(self.window, "Empty Playlist",
                                          "This playlist has no songs.")
            return

        if self.music_player:
            self.music_player.play_playlist(songs, playlist_name)

    def handle_delete_playlist(self):
        playlist_name = self.window.PL_Name.text()
        if not playlist_name:
            QtWidgets.QMessageBox.warning(self.window, "No Playlist Selected",
                                          "Please select a playlist.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Delete Playlist", f"Delete '{playlist_name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            delete_user_playlist(self.username, playlist_name)
            self.load_playlists_table()
            self.window.PL_Name.clear()
            self.window.PL_Visits.clear()
            self.window.PL_Date.setDate(QtCore.QDate.currentDate())
            QtWidgets.QMessageBox.information(self.window, "Deleted",
                                              f"'{playlist_name}' deleted.")

    def handle_create_playlist(self):
        name, ok = QtWidgets.QInputDialog.getText(self.window, "New Playlist",
                                                  "Enter playlist name:")
        if not ok or not name:
            return

        user_playlists = get_user_playlists(self.username)
        if name in user_playlists:
            QtWidgets.QMessageBox.warning(self.window, "Exists",
                                          f"'{name}' already exists.")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        add_user_playlist(self.username, name, {
            "songs": [],
            "visits": 0,
            "created_date": today
        })
        self.load_playlists_table()
        QtWidgets.QMessageBox.information(self.window, "Created",
                                          f"'{name}' created.")

    def handle_play_queue(self):
        user_queue = get_user_queue(self.username)
        if not user_queue:
            QtWidgets.QMessageBox.warning(self.window, "Empty Queue",
                                          "Your queue is empty.")
            return

        if self.music_player:
            self.music_player.play_queue(user_queue)

    def handle_remove_from_queue(self):
        if self.selected_queue_row is None:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to remove.")
            return

        user_queue = get_user_queue(self.username)
        if 0 <= self.selected_queue_row < len(user_queue):
            removed = remove_from_user_queue(self.username,
                                             self.selected_queue_row)
            self.load_queue_table()
            self.selected_queue_row = None
            if removed:
                QtWidgets.QMessageBox.information(
                    self.window, "Removed",
                    f"'{removed[0]}' removed from queue.")

    def handle_clear_queue(self):
        user_queue = get_user_queue(self.username)
        if not user_queue:
            QtWidgets.QMessageBox.warning(self.window, "Empty",
                                          "Queue is already empty.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Clear Queue", "Clear entire queue?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            clear_user_queue(self.username)
            self.load_queue_table()
            QtWidgets.QMessageBox.information(self.window, "Cleared",
                                              "Queue cleared.")

    # ==================== SEARCH PAGE ====================

    def clear_search_form(self):
        self.window.searchSongs_Table.setRowCount(0)
        self.window.searchArtists_Table.setRowCount(0)
        self.window.artistSongs_Table.setRowCount(0)
        self.window.S_SongName.clear()
        self.window.S_ArtistName.clear()
        self.window.S_ArtistName_3.clear()

    def handle_search(self):
        search_term = self.window.SearchSong.text().strip().lower()
        if not search_term:
            QtWidgets.QMessageBox.warning(self.window, "Empty Search",
                                          "Please enter a search term.")
            return

        approved_songs = get_approved_songs()
        matching_songs = []
        matching_artists = {}

        for song_id, data in approved_songs.items():
            song_name, artist_name, genre = data[0], data[1], data[2]
            if search_term in song_name.lower(
            ) or search_term in artist_name.lower():
                matching_songs.append([song_name, artist_name, genre])
                if artist_name not in matching_artists:
                    matching_artists[artist_name] = {
                        "songs": 0,
                        "top_song": song_name
                    }
                matching_artists[artist_name]["songs"] += 1

        songs_table = self.window.searchSongs_Table
        songs_table.setRowCount(len(matching_songs))
        for row, data in enumerate(matching_songs):
            songs_table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            songs_table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            songs_table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
        songs_table.resizeColumnsToContents()

        artists_table = self.window.searchArtists_Table
        artists_table.setRowCount(len(matching_artists))
        for row, (artist, info) in enumerate(matching_artists.items()):
            artists_table.setItem(row, 0, QtWidgets.QTableWidgetItem(artist))
            artists_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(info["songs"])))
            artists_table.setItem(row, 2,
                                  QtWidgets.QTableWidgetItem(info["top_song"]))
        artists_table.resizeColumnsToContents()

        if not matching_songs:
            QtWidgets.QMessageBox.information(
                self.window, "No Results", f"No results for '{search_term}'.")

    def populate_search_song_form(self, row, column):
        table = self.window.searchSongs_Table
        self.window.S_SongName.setText(table.item(row, 0).text())
        self.window.S_ArtistName.setText(table.item(row, 1).text())

    def populate_search_artist_form(self, row, column):
        table = self.window.searchArtists_Table
        artist_name = table.item(row, 0).text()

        approved_songs = get_approved_songs()
        artist_songs = [[data[0], data[2]] for data in approved_songs.values()
                        if data[1] == artist_name]

        artist_table = self.window.artistSongs_Table
        artist_table.setRowCount(len(artist_songs))
        for row, data in enumerate(artist_songs):
            artist_table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            artist_table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
        artist_table.resizeColumnsToContents()

    def handle_search_add_to_queue(self):
        song_name = self.window.S_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song.")
            return

        artist_name = self.window.S_ArtistName.text()
        genre = self.get_song_genre(song_name)
        today = datetime.now().strftime("%Y-%m-%d")

        add_to_user_queue(self.username,
                          [song_name, artist_name, genre, today])
        self.load_queue_table()
        QtWidgets.QMessageBox.information(self.window, "Added to Queue",
                                          f"'{song_name}' added to queue.")

    def handle_search_add_to_playlist(self):
        song_name = self.window.S_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song.")
            return
        self.add_song_to_playlist_dialog(song_name,
                                         self.window.S_ArtistName.text())

    def handle_search_play_song(self):
        song_name = self.window.S_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to play.")
            return
        if self.music_player:
            self.music_player.play_song_by_name(song_name)

    def handle_report_song(self):
        song_name = self.window.S_SongName.text()
        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to report.")
            return

        dialog = ReportSongDialog(self.window, song_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            QtWidgets.QMessageBox.information(
                self.window, "Report Submitted",
                f"'{song_name}' reported.\nReason: {dialog.report_reason}")

    # ==================== ANALYTICS PAGE ====================

    def load_analytics_data(self):
        self.load_artist_songs_table()
        self.window.S_SongName_2.clear()
        self.window.S_SongName_3.clear()
        self.window.comboBox.setCurrentIndex(0)
        self.window.PL_Date_2.setDate(QtCore.QDate.currentDate())
        self.selected_artist_song_id = None

        # Setup analytics defaults
        today = QtCore.QDate.currentDate()
        one_month_ago = today.addMonths(-1)
        self.window.ReveueStartDate.setDate(one_month_ago)
        self.window.ReveueStartDate_2.setDate(today)
        self.window.RevenueMonth.setChecked(True)
        self.window.RevenueDay_2.setChecked(True)

    def load_artist_songs_table(self):
        artist_songs = get_artist_songs(self.username)
        table = self.window.tableWidget_2
        table.setRowCount(len(artist_songs))
        for row, (song_id, data) in enumerate(artist_songs.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(data[3])))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(data[4])))
        table.resizeColumnsToContents()

    def populate_artist_song_form(self, row, column):
        table = self.window.tableWidget_2
        song_name = table.item(row, 0).text()
        genre = table.item(row, 1).text()
        release_date = table.item(row, 2).text()

        self.window.S_SongName_2.setText(song_name)
        index = self.window.comboBox.findText(genre)
        if index >= 0:
            self.window.comboBox.setCurrentIndex(index)
        self.window.PL_Date_2.setDate(
            QtCore.QDate.fromString(release_date, "yyyy-MM-dd"))

        artist_songs = get_artist_songs(self.username)
        for song_id, data in artist_songs.items():
            if data[0] == song_name:
                self.selected_artist_song_id = song_id
                break

    def handle_add_new_song(self):
        song_name = self.window.S_SongName_2.text().strip()
        file_path = self.window.S_SongName_3.text().strip()
        genre = self.window.comboBox.currentText()
        release_date = self.window.PL_Date_2.date().toString("yyyy-MM-dd")

        if not song_name:
            QtWidgets.QMessageBox.warning(self.window, "Missing Info",
                                          "Please enter a song name.")
            return

        if not file_path:
            QtWidgets.QMessageBox.warning(self.window, "Missing Info",
                                          "Please enter the file path.")
            return

        artist_songs = get_artist_songs(self.username)
        new_id = f"AS{len(artist_songs) + 100: 03d}"

        add_artist_song(self.username, new_id,
                        [song_name, genre, release_date, 0, 0, file_path])

        pending_id = f"PS{len(get_pending_songs()) + 100:03d}"
        PendingSongs[pending_id] = [
            song_name, self.username, genre, release_date, file_path,
            "Song_images/default_song_image.jpg"
        ]

        self.load_artist_songs_table()
        self.window.S_SongName_2.clear()
        self.window.S_SongName_3.clear()
        self.window.comboBox.setCurrentIndex(0)
        self.window.PL_Date_2.setDate(QtCore.QDate.currentDate())
        self.selected_artist_song_id = None
        QtWidgets.QMessageBox.information(
            self.window, "Submitted", f"'{song_name}' submitted for approval.")

    def handle_delete_artist_song(self):
        if not self.selected_artist_song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to delete.")
            return

        artist_songs = get_artist_songs(self.username)
        if self.selected_artist_song_id not in artist_songs:
            return

        song_name = artist_songs[self.selected_artist_song_id][0]
        reply = QtWidgets.QMessageBox.question(
            self.window, "Delete Song", f"Delete '{song_name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            delete_artist_song(self.username, self.selected_artist_song_id)
            self.load_artist_songs_table()
            self.window.S_SongName_2.clear()
            self.window.S_SongName_3.clear()
            self.window.comboBox.setCurrentIndex(0)
            self.window.PL_Date_2.setDate(QtCore.QDate.currentDate())
            self.selected_artist_song_id = None
            QtWidgets.QMessageBox.information(self.window, "Deleted",
                                              f"'{song_name}' deleted.")

    def handle_view_analytics(self):
        # Get group by selection
        group_by = "day"
        if self.window.RevenueDay.isChecked():
            group_by = "day"
        elif self.window.RevenueMonth.isChecked():
            group_by = "month"
        elif self.window.RevenueYear.isChecked():
            group_by = "year"

        # Get analytics type
        analytics_type = "views"
        if self.window.RevenueDay_2.isChecked():
            analytics_type = "views"
        elif self.window.RevenueMonth_2.isChecked():
            analytics_type = "revenue"

        # Get date range
        start_date = self.window.ReveueStartDate.date().toString("yyyy-MM-dd")
        end_date = self.window.ReveueStartDate_2.date().toString("yyyy-MM-dd")

        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Dates",
                "Start date must be before end date.")
            return

        # Get data as 2D array [[x, y], ...]
        data = self.get_analytics_data(analytics_type, group_by, start_date,
                                       end_date)

        if not data:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                f"No {analytics_type} data available for the selected date range.\n\n"
                "Note: Analytics data is only available for artists.")
            return

        # Set labels
        if analytics_type == "views":
            title = f"Views Analytics\n({start_date} to {end_date})"
            y_label = "Views"
        else:
            title = f"Revenue Analytics\n({start_date} to {end_date})"
            y_label = "Revenue ($)"

        x_label = "Date" if group_by == "day" else group_by.capitalize()

        dialog = AnalyticsGraphDialog(self.window, title, data, x_label,
                                      y_label)
        dialog.exec_()

    # ==================== PROFILE PAGE ====================

    def load_profile_data(self):
        if self.user_data:
            self.window.P_Subscription.setText(self.user_data[5])
        self.load_subscription_plans_table()

    def load_subscription_plans_table(self):
        plans = get_subscription_plans()
        table = self.window.tableWidget
        table.setRowCount(len(plans))
        for row, (plan_id, data) in enumerate(plans.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[1])))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[3]))
        table.resizeColumnsToContents()

    def populate_subscription_form(self, row, column):
        table = self.window.tableWidget
        self.window.P_PlanName.setText(table.item(row, 0).text())
        self.window.P_Price.setText(table.item(row, 1).text())

    def handle_buy_plan(self):
        plan_name = self.window.P_PlanName.text()
        price = self.window.P_Price.text()

        if not plan_name:
            QtWidgets.QMessageBox.warning(self.window, "No Plan Selected",
                                          "Please select a plan.")
            return

        current_plan = self.window.P_Subscription.text()
        if plan_name == current_plan:
            QtWidgets.QMessageBox.information(
                self.window, "Already Subscribed",
                f"You already have {plan_name}.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm", f"Subscribe to {plan_name} for ${price}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if self.username in Users:
                Users[self.username][5] = plan_name
                self.user_data = get_user(self.username)
            self.window.P_Subscription.setText(plan_name)
            QtWidgets.QMessageBox.information(self.window, "Success",
                                              f"Subscribed to {plan_name}!")

    def handle_delete_account(self):
        if not self.window.checkBox.isChecked():
            QtWidgets.QMessageBox.warning(
                self.window, "Required",
                "Please acknowledge account deletion.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Delete Account",
            "Are you SURE?  This cannot be undone! ",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if remove_user(self.username):
                QtWidgets.QMessageBox.information(self.window, "Deleted",
                                                  "Account deleted.")
                self.window.logout()
