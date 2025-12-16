import sys
import pyodbc
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime

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

def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
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
        print(f"Database error: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

# ==================== HELPER DIALOGS ====================

class PlaylistSongsDialog(QtWidgets.QDialog):
    def __init__(self, parent, playlist_name, songs):
        super().__init__(parent)
        self.setWindowTitle(f"Playlist: {playlist_name}")
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
            # song = (SongName, ArtistName, GenreName)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(song[0]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(song[1]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(song[2]))

        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)
        
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet("background-color: #1DB954; color: white; padding: 10px; border-radius: 5px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

class AddToPlaylistDialog(QtWidgets.QDialog):
    def __init__(self, parent, playlists):
        super().__init__(parent)
        self.setWindowTitle("Add to Playlist")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #121212; color: #fff;")
        self.selected_playlist_id = None
        self.selected_playlist_name = None

        layout = QtWidgets.QVBoxLayout(self)
        title_label = QtWidgets.QLabel("Select a Playlist")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        self.playlist_list = QtWidgets.QListWidget()
        self.playlist_list.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        
        # playlists is list of tuples (PlaylistID, PlaylistName)
        self.playlists_data = playlists 
        for pid, pname in playlists:
            self.playlist_list.addItem(pname)
            
        layout.addWidget(self.playlist_list)

        btn_layout = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Add")
        add_btn.setStyleSheet("background-color: #1DB954; color: white; padding: 10px; border-radius: 5px;")
        add_btn.clicked.connect(self.accept_selection)
        btn_layout.addWidget(add_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #ff0000; color: white; padding: 10px; border-radius: 5px;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def accept_selection(self):
        row = self.playlist_list.currentRow()
        if row >= 0:
            self.selected_playlist_id = self.playlists_data[row][0]
            self.selected_playlist_name = self.playlists_data[row][1]
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a playlist.")

class ReportSongDialog(QtWidgets.QDialog):
    def __init__(self, parent, song_name):
        super().__init__(parent)
        self.setWindowTitle(f"Report: {song_name}")
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
        self.reason_combo.setStyleSheet("background-color: #FFFFFF; color: #000000; padding: 5px;")
        self.reason_combo.addItems(["Inappropriate Content", "Copyright Violation", "Audio Quality Issues", "Hate Speech", "Violence", "Other"])
        layout.addWidget(self.reason_combo)

        layout.addWidget(QtWidgets.QLabel("Additional Comments (optional):"))
        self.comments_input = QtWidgets.QLineEdit()
        self.comments_input.setStyleSheet("background-color: #FFFFFF; color: #000000; padding: 5px;")
        layout.addWidget(self.comments_input)

        btn_layout = QtWidgets.QHBoxLayout()
        submit_btn = QtWidgets.QPushButton("Submit Report")
        submit_btn.setStyleSheet("background-color: #ff0000; color: white; padding: 10px; border-radius: 5px;")
        submit_btn.clicked.connect(self.submit_report)
        btn_layout.addWidget(submit_btn)
        
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #3a3a3a; color: white; padding: 10px; border-radius: 5px;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def submit_report(self):
        self.report_reason = self.reason_combo.currentText()
        if self.comments_input.text():
            self.report_reason += f" - {self.comments_input.text()}"
        self.accept()

class AnalyticsGraphDialog(QtWidgets.QDialog):
    def __init__(self, parent, title, data, x_label, y_label):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #121212; color: #fff;")
        layout = QtWidgets.QVBoxLayout(self)
        
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
            for spine in ax.spines.values(): spine.set_color('white')
            
            if data:
                x_vals = [str(d[0]) for d in data]
                y_vals = [d[1] for d in data]
                ax.plot(x_vals, y_vals, marker='o', linestyle='-', linewidth=2, color='#1DB954')
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.set_title(title)
                ax.grid(True, alpha=0.3)
                fig.autofmt_xdate(rotation=45)
            else:
                ax.text(0.5, 0.5, 'No Data', color='white', ha='center')
            
            layout.addWidget(canvas)
        except ImportError:
            layout.addWidget(QtWidgets.QLabel("Matplotlib not installed."))
        
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

# ==================== USER DASHBOARD HANDLER ====================

class UserDashboardHandler:
    def __init__(self, window: QtWidgets.QMainWindow, username: str, music_player=None):
        self.window = window
        self.username = username
        self.music_player = music_player
        self.selected_queue_row = None
        self.selected_playlist_id = None
        self.selected_song_id = None

    def connect_signals(self):
        # Navigation
        self.window.homeBtn.clicked.connect(lambda: self.switch_page(self.window.homePage, self.window.homeBtn))
        self.window.searchNavBtn.clicked.connect(lambda: self.switch_page(self.window.searchPage, self.window.searchNavBtn))
        self.window.libraryBtn.clicked.connect(lambda: self.switch_page(self.window.libraryPage, self.window.libraryBtn))
        self.window.analyticsBtn.clicked.connect(lambda: self.switch_page(self.window.analyticsPage, self.window.analyticsBtn))
        self.window.profileBtn.clicked.connect(lambda: self.switch_page(self.window.profilePage, self.window.profileBtn))
        self.window.logoutBtn.clicked.connect(self.handle_logout)

        # Home Page
        self.window.RR_Table.cellClicked.connect(self.populate_recent_rotation_form)
        self.window.RR_PlaySongBtn.clicked.connect(self.handle_play_song)
        self.window.RR_AddQueueBtn.clicked.connect(self.handle_add_to_queue)
        self.window.RR_AddPlaylistBtn.clicked.connect(self.handle_add_to_playlist)
        self.window.RR_RefreshBtn.clicked.connect(self.load_home_data)

        # Library Page
        self.window.PL_Table.cellClicked.connect(self.populate_playlist_form)
        self.window.PL_ViewBtn.clicked.connect(self.handle_view_playlist)
        self.window.PL_PlayBtn.clicked.connect(self.handle_play_playlist)
        self.window.PL_DeleteBtn.clicked.connect(self.handle_delete_playlist)
        self.window.PL_ViewBtn_3.clicked.connect(self.handle_create_playlist)
        
        self.window.Queue_Table.cellClicked.connect(self.populate_queue_selection)
        self.window.Queue_PlayBtn.clicked.connect(self.handle_play_queue)
        self.window.Queue_RemoveBtn.clicked.connect(self.handle_remove_from_queue)
        self.window.Queue_ClearBtn.clicked.connect(self.handle_clear_queue)

        # Search Page
        self.window.S_SearchBtn.clicked.connect(self.handle_search)
        self.window.searchSongs_Table.cellClicked.connect(self.populate_search_song_form)
        self.window.S_AddQueueBtn.clicked.connect(self.handle_search_add_to_queue)
        self.window.S_AddPlBtn.clicked.connect(self.handle_search_add_to_playlist)
        self.window.S_AddPlBtn_2.clicked.connect(self.handle_search_play_song)
        self.window.S_ReportBtn.clicked.connect(self.handle_report_song)

        # Analytics/Artist Page
        self.window.tableWidget_2.cellClicked.connect(self.populate_artist_song_form)
        self.window.S_AddQueueBtn_2.clicked.connect(self.handle_add_new_song) # Upload Song
        self.window.S_ReportBtn_3.clicked.connect(self.handle_delete_artist_song)
        self.window.RevenueViewBtn.clicked.connect(self.handle_view_analytics)

        # Profile
        self.window.tableWidget.cellClicked.connect(self.populate_subscription_form)
        self.window.P_BuyPlanBtn.clicked.connect(self.handle_buy_plan)
        self.window.S_ReportBtn_2.clicked.connect(self.handle_delete_account)

    def load_all_data(self):
        self.load_home_data()
        self.load_library_data()
        self.load_analytics_data()
        self.load_profile_data()
        self.window.stackedWidget.setCurrentWidget(self.window.homePage)

    def switch_page(self, page, button):
        self.window.stackedWidget.setCurrentWidget(page)
        # Reset button styles if needed, here we just assume the QRadioButton logic handles standard switching

    def handle_logout(self):
        self.window.logout()

    # ==================== HOME PAGE LOGIC ====================

    def load_home_data(self):
        # 1. Recent Rotation (Top 5 listened by this user)
        query_rr = """
            SELECT TOP 5 s.SongName, s.Username as Artist, COUNT(*) as Plays
            FROM PlayHistory ph
            JOIN SongDetails s ON ph.SongID = s.SongID
            WHERE ph.Username = ?
            GROUP BY s.SongName, s.Username
            ORDER BY Plays DESC
        """
        rr_data = execute_query(query_rr, (self.username,), fetch_all=True)
        self.fill_table(self.window.RR_Table, rr_data or [])

        # 2. Top Artists (Global)
        query_ta = """
            SELECT TOP 5 s.Username as Artist, COUNT(*) as Plays, MAX(s.SongName) as TopSong
            FROM PlayHistory ph
            JOIN SongDetails s ON ph.SongID = s.SongID
            GROUP BY s.Username
            ORDER BY Plays DESC
        """
        ta_data = execute_query(query_ta, fetch_all=True)
        self.fill_table(self.window.Top5Artists_Table, ta_data or [])

        # 3. Top Songs (Global)
        query_ts = """
            SELECT TOP 5 s.SongName, s.Username as Artist, COUNT(*) as Plays
            FROM PlayHistory ph
            JOIN SongDetails s ON ph.SongID = s.SongID
            GROUP BY s.SongName, s.Username
            ORDER BY Plays DESC
        """
        ts_data = execute_query(query_ts, fetch_all=True)
        self.fill_table(self.window.Top5Songs_Table, ts_data or [])

    def fill_table(self, table, data):
        table.setRowCount(len(data))
        for row, item in enumerate(data):
            # item is a tuple
            for col, val in enumerate(item):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(val)))
        table.resizeColumnsToContents()

    def populate_recent_rotation_form(self, row, col):
        self.window.RR_SongName.setText(self.window.RR_Table.item(row, 0).text())
        self.window.RR_ArtistName.setText(self.window.RR_Table.item(row, 1).text())
        self.window.RR_Listens.setText(self.window.RR_Table.item(row, 2).text())
        # Set default image
        self.window.RR_SongImage.setPixmap(QtGui.QPixmap("Song_images/default_song_image.jpg"))

    def get_song_id_by_name(self, song_name, artist_name):
        query = "SELECT SongID FROM SongDetails WHERE SongName = ? AND Username = ?"
        res = execute_query(query, (song_name, artist_name), fetch_one=True)
        return res[0] if res else None

    def handle_play_song(self):
        song_name = self.window.RR_SongName.text()
        if not song_name: return
        if self.music_player:
            self.music_player.play_song_by_name(song_name)
            # Log play
            artist = self.window.RR_ArtistName.text()
            sid = self.get_song_id_by_name(song_name, artist)
            if sid:
                execute_query("INSERT INTO PlayHistory (Username, SongID, PlayDate) VALUES (?, ?, GETDATE())", 
                              (self.username, sid), commit=True)

    def handle_add_to_queue(self):
        song_name = self.window.RR_SongName.text()
        artist = self.window.RR_ArtistName.text()
        if not song_name: return

        sid = self.get_song_id_by_name(song_name, artist)
        if not sid: return

        # Get or Create Queue
        q_res = execute_query("SELECT QueueID FROM Queue WHERE Username = ?", (self.username,), fetch_one=True)
        if q_res:
            qid = q_res[0]
        else:
            # Generate new QID
            max_q = execute_query("SELECT ISNULL(MAX(QueueID), 0) + 1 FROM Queue", fetch_one=True)[0]
            execute_query("INSERT INTO Queue (QueueID, Username, QueueTimeDate) VALUES (?, ?, GETDATE())", 
                          (max_q, self.username), commit=True)
            qid = max_q
        
        # Add to QueueContains
        try:
            execute_query("INSERT INTO QueueContains (QueueID, SongID) VALUES (?, ?)", (qid, sid), commit=True)
            QtWidgets.QMessageBox.information(self.window, "Success", "Added to queue.")
            self.load_queue_table()
        except:
            QtWidgets.QMessageBox.warning(self.window, "Info", "Song already in queue.")

    def handle_add_to_playlist(self):
        song_name = self.window.RR_SongName.text()
        artist = self.window.RR_ArtistName.text()
        if not song_name: return
        self.show_add_playlist_dialog(song_name, artist)

    def show_add_playlist_dialog(self, song_name, artist_name):
        # Fetch user playlists
        playlists = execute_query("SELECT PlaylistID, PlaylistName FROM Playlist WHERE Username = ?", (self.username,), fetch_all=True)
        if not playlists:
            QtWidgets.QMessageBox.warning(self.window, "No Playlists", "Create a playlist first!")
            return

        dialog = AddToPlaylistDialog(self.window, playlists)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            pid = dialog.selected_playlist_id
            sid = self.get_song_id_by_name(song_name, artist_name)
            if sid:
                try:
                    execute_query("INSERT INTO PlaylistSong (PlaylistID, SongID) VALUES (?, ?)", (pid, sid), commit=True)
                    QtWidgets.QMessageBox.information(self.window, "Success", f"Added to {dialog.selected_playlist_name}")
                except:
                     QtWidgets.QMessageBox.warning(self.window, "Error", "Song already in playlist.")

    # ==================== LIBRARY LOGIC ====================

    def load_library_data(self):
        self.load_playlists_table()
        self.load_queue_table()

    def load_playlists_table(self):
        query = """
            SELECT p.PlaylistID, p.PlaylistName, COUNT(ps.SongID) as SongCount, p.Visits, p.DateOfCreation
            FROM Playlist p
            LEFT JOIN PlaylistSong ps ON p.PlaylistID = ps.PlaylistID
            WHERE p.Username = ?
            GROUP BY p.PlaylistID, p.PlaylistName, p.Visits, p.DateOfCreation
        """
        data = execute_query(query, (self.username,), fetch_all=True)
        # Table expects: Name, Count, Visits, Date
        display_data = []
        self.playlist_map = {} # Map row to ID
        if data:
            for i, row in enumerate(data):
                display_data.append((row[1], row[2], row[3], row[4]))
                self.playlist_map[i] = row[0]
        
        self.fill_table(self.window.PL_Table, display_data)

    def load_queue_table(self):
        query = """
            SELECT s.SongName, s.Username, g.GenreName, q.QueueTimeDate
            FROM Queue q
            JOIN QueueContains qc ON q.QueueID = qc.QueueID
            JOIN SongDetails s ON qc.SongID = s.SongID
            LEFT JOIN SongGenre sg ON s.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE q.Username = ?
        """
        data = execute_query(query, (self.username,), fetch_all=True)
        self.fill_table(self.window.Queue_Table, data or [])

    def populate_playlist_form(self, row, col):
        if row in self.playlist_map:
            self.selected_playlist_id = self.playlist_map[row]
            self.window.PL_Name.setText(self.window.PL_Table.item(row, 0).text())
            self.window.PL_Visits.setText(self.window.PL_Table.item(row, 2).text())
            date_str = self.window.PL_Table.item(row, 3).text()
            self.window.PL_Date.setDate(QtCore.QDate.fromString(str(date_str), "yyyy-MM-dd"))

    def handle_create_playlist(self):
        name, ok = QtWidgets.QInputDialog.getText(self.window, "New Playlist", "Enter Name:")
        if ok and name:
            max_id = execute_query("SELECT ISNULL(MAX(PlaylistID), 0) + 1 FROM Playlist", fetch_one=True)[0]
            execute_query("INSERT INTO Playlist (PlaylistID, PlaylistName, Username, DateOfCreation, Visits) VALUES (?, ?, ?, GETDATE(), 0)",
                          (max_id, name, self.username), commit=True)
            self.load_playlists_table()

    def handle_delete_playlist(self):
        if not self.selected_playlist_id: return
        execute_query("DELETE FROM PlaylistSong WHERE PlaylistID = ?", (self.selected_playlist_id,), commit=True)
        execute_query("DELETE FROM Playlist WHERE PlaylistID = ?", (self.selected_playlist_id,), commit=True)
        self.load_playlists_table()
        self.selected_playlist_id = None

    def handle_view_playlist(self):
        if not self.selected_playlist_id: return
        query = """
            SELECT s.SongName, s.Username, g.GenreName
            FROM PlaylistSong ps
            JOIN SongDetails s ON ps.SongID = s.SongID
            LEFT JOIN SongGenre sg ON s.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE ps.PlaylistID = ?
        """
        songs = execute_query(query, (self.selected_playlist_id,), fetch_all=True)
        dialog = PlaylistSongsDialog(self.window, self.window.PL_Name.text(), songs or [])
        dialog.exec_()
        # Increment visits
        execute_query("UPDATE Playlist SET Visits = Visits + 1 WHERE PlaylistID = ?", (self.selected_playlist_id,), commit=True)
        self.load_playlists_table()

    def handle_play_playlist(self):
        # Implement play logic sending list of songs to music player
        pass

    def populate_queue_selection(self, row, col):
        self.selected_queue_row = row
        self.selected_queue_song = self.window.Queue_Table.item(row, 0).text()

    def handle_remove_from_queue(self):
        if self.selected_queue_row is None: return
        song_name = self.window.Queue_Table.item(self.selected_queue_row, 0).text()
        
        # Get QID
        q_res = execute_query("SELECT QueueID FROM Queue WHERE Username = ?", (self.username,), fetch_one=True)
        if q_res:
            qid = q_res[0]
            sid_res = execute_query("SELECT SongID FROM SongDetails WHERE SongName = ?", (song_name,), fetch_one=True)
            if sid_res:
                execute_query("DELETE FROM QueueContains WHERE QueueID = ? AND SongID = ?", (qid, sid_res[0]), commit=True)
                self.load_queue_table()

    def handle_clear_queue(self):
        execute_query("DELETE FROM QueueContains WHERE QueueID IN (SELECT QueueID FROM Queue WHERE Username = ?)", (self.username,), commit=True)
        self.load_queue_table()
    
    def handle_play_queue(self):
        # Fetch songs and send to player
        pass

    # ==================== SEARCH LOGIC ====================

    def handle_search(self):
        term = self.window.SearchSong.text().strip()
        if not term: return
        
        # Search Songs
        query_s = """
            SELECT s.SongName, s.Username as Artist, g.GenreName
            FROM SongDetails s
            LEFT JOIN SongGenre sg ON s.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE s.SongStatus = 'Active' AND (s.SongName LIKE ? OR s.Username LIKE ?)
        """
        pattern = f"%{term}%"
        s_data = execute_query(query_s, (pattern, pattern), fetch_all=True)
        self.fill_table(self.window.searchSongs_Table, s_data or [])

        # Search Artists (Aggregate)
        query_a = """
            SELECT s.Username, COUNT(s.SongID), MAX(s.SongName)
            FROM SongDetails s
            WHERE s.Username LIKE ? AND s.SongStatus = 'Active'
            GROUP BY s.Username
        """
        a_data = execute_query(query_a, (pattern,), fetch_all=True)
        self.fill_table(self.window.searchArtists_Table, a_data or [])

    def populate_search_song_form(self, row, col):
        self.window.S_SongName.setText(self.window.searchSongs_Table.item(row, 0).text())
        self.window.S_ArtistName.setText(self.window.searchSongs_Table.item(row, 1).text())

    def handle_search_add_to_queue(self):
        # Uses S_SongName and S_ArtistName
        self.window.RR_SongName.setText(self.window.S_SongName.text())
        self.window.RR_ArtistName.setText(self.window.S_ArtistName.text())
        self.handle_add_to_queue()

    def handle_search_add_to_playlist(self):
        self.show_add_playlist_dialog(self.window.S_SongName.text(), self.window.S_ArtistName.text())

    def handle_search_play_song(self):
        if self.music_player:
            self.music_player.play_song_by_name(self.window.S_SongName.text())

    def handle_report_song(self):
        song = self.window.S_SongName.text()
        artist = self.window.S_ArtistName.text()
        if not song: return
        sid = self.get_song_id_by_name(song, artist)
        
        dialog = ReportSongDialog(self.window, song)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            if sid:
                execute_query("INSERT INTO Reports (Username, SongID, ReportReason) VALUES (?, ?, ?)",
                              (self.username, sid, dialog.report_reason), commit=True)
                QtWidgets.QMessageBox.information(self.window, "Reported", "Report submitted.")

    # ==================== ARTIST / UPLOAD LOGIC ====================

    def load_analytics_data(self):
        # Load user's uploaded songs
        query = """
            SELECT s.SongName, g.GenreName, s.ReleaseDate, s.Likes, s.Dislikes
            FROM SongDetails s
            LEFT JOIN SongGenre sg ON s.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE s.Username = ? AND s.SongStatus != 'Deleted'
        """
        data = execute_query(query, (self.username,), fetch_all=True)
        self.fill_table(self.window.tableWidget_2, data or [])
        
        # Populate Genre Combo for upload
        genres = execute_query("SELECT GenreName FROM Genre", fetch_all=True)
        self.window.comboBox.clear()
        if genres:
            for g in genres: self.window.comboBox.addItem(g[0])

    def populate_artist_song_form(self, row, col):
        self.window.S_SongName_2.setText(self.window.tableWidget_2.item(row, 0).text())
        # Find ID for deletion
        # This is a bit weak if names duplicate, but works for basic app
        self.selected_song_to_delete = self.window.S_SongName_2.text()

    def handle_add_new_song(self):
        name = self.window.S_SongName_2.text()
        path = self.window.S_SongName_3.text()
        genre = self.window.comboBox.currentText()
        date = self.window.PL_Date_2.date().toString("yyyy-MM-dd")

        if not name or not path: return

        # New Song ID
        max_sid = execute_query("SELECT ISNULL(MAX(SongID), 0) + 1 FROM SongDetails", fetch_one=True)[0]
        
        # Insert Song
        execute_query("""
            INSERT INTO SongDetails (SongID, Username, SongName, Likes, Dislikes, Listens, ReleaseDate, MetaData, SongStatus)
            VALUES (?, ?, ?, 0, 0, 0, ?, ?, 'Pending')
        """, (max_sid, self.username, name, date, path), commit=True)

        # Link Genre
        gid_res = execute_query("SELECT GenreID FROM Genre WHERE GenreName = ?", (genre,), fetch_one=True)
        if gid_res:
            execute_query("INSERT INTO SongGenre (SongID, GenreID) VALUES (?, ?)", (max_sid, gid_res[0]), commit=True)
        
        QtWidgets.QMessageBox.information(self.window, "Success", "Song submitted for approval.")
        self.load_analytics_data()

    def handle_delete_artist_song(self):
        name = self.window.S_SongName_2.text()
        if not name: return
        execute_query("UPDATE SongDetails SET SongStatus = 'Deleted' WHERE SongName = ? AND Username = ?", 
                      (name, self.username), commit=True)
        self.load_analytics_data()

    def handle_view_analytics(self):
        # Simple Revenue View based on user type (Demo logic mapped to BillingRecord for simplicity)
        # Assuming artists get a cut of billing records? Or just show subscription payments
        # Let's show total listens over time from PlayHistory
        start = self.window.ReveueStartDate.date().toString("yyyy-MM-dd")
        end = self.window.ReveueStartDate_2.date().toString("yyyy-MM-dd")
        
        query = """
            SELECT FORMAT(PlayDate, 'yyyy-MM-dd') as D, COUNT(*) 
            FROM PlayHistory ph
            JOIN SongDetails s ON ph.SongID = s.SongID
            WHERE s.Username = ? AND ph.PlayDate BETWEEN ? AND ?
            GROUP BY FORMAT(PlayDate, 'yyyy-MM-dd')
            ORDER BY D
        """
        data = execute_query(query, (self.username, start, end), fetch_all=True)
        dialog = AnalyticsGraphDialog(self.window, "Daily Plays", data, "Date", "Plays")
        dialog.exec_()

    # ==================== PROFILE LOGIC ====================

    def load_profile_data(self):
        # Load subscription plans
        plans = execute_query("SELECT PlanName, PlanPrice, 'Monthly' FROM Plans", fetch_all=True)
        self.fill_table(self.window.tableWidget, plans or [])
        
        # Show current plan
        curr = execute_query("""
            SELECT TOP 1 p.PlanName FROM Subscription s 
            JOIN Plans p ON s.PlanID = p.PlanID 
            WHERE s.Username = ? AND s.EndDate > GETDATE()
            ORDER BY s.EndDate DESC
        """, (self.username,), fetch_one=True)
        self.window.P_Subscription.setText(curr[0] if curr else "Free")

    def populate_subscription_form(self, row, col):
        self.window.P_PlanName.setText(self.window.tableWidget.item(row, 0).text())
        self.window.P_Price.setText(self.window.tableWidget.item(row, 1).text())

    def handle_buy_plan(self):
        plan_name = self.window.P_PlanName.text()
        if not plan_name: return
        
        pid_res = execute_query("SELECT PlanID, PlanPrice FROM Plans WHERE PlanName = ?", (plan_name,), fetch_one=True)
        if pid_res:
            pid, price = pid_res
            # Create Subscription
            max_sub = execute_query("SELECT ISNULL(MAX(SubscriptionID), 0) + 1 FROM Subscription", fetch_one=True)[0]
            execute_query("""
                INSERT INTO Subscription (SubscriptionID, Username, PlanID, StartDate, EndDate)
                VALUES (?, ?, ?, GETDATE(), DATEADD(month, 1, GETDATE()))
            """, (max_sub, self.username, pid), commit=True)
            
            # Create Billing Record
            execute_query("""
                INSERT INTO BillingRecord (Username, SubscriptionID, Amount, PaymentDate)
                VALUES (?, ?, ?, GETDATE())
            """, (self.username, max_sub, price), commit=True)
            
            QtWidgets.QMessageBox.information(self.window, "Success", f"Subscribed to {plan_name}")
            self.load_profile_data()

    def handle_delete_account(self):
        if not self.window.checkBox.isChecked():
            QtWidgets.QMessageBox.warning(self.window, "Check Box", "Please confirm deletion.")
            return
        
        reply = QtWidgets.QMessageBox.question(self.window, "Confirm", "Delete account?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            execute_query("UPDATE Users SET UserStatus = 'Deleted' WHERE Username = ?", (self.username,), commit=True)
            self.window.logout()