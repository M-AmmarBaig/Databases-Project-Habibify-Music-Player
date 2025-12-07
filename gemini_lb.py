from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
import sys
import sqlite3
from datetime import datetime
import os

class ListenerDashboard(QtWidgets.QMainWindow):
    def __init__(self, user_id, username):
        super(ListenerDashboard, self).__init__()
        uic.loadUi(r"C:\Users\User\OneDrive - Habib University\Habib University\Semester 3\Database Management Systems\DBMS Project - Music App\App UI\user_main.ui", self)

        # Store user info
        self.username = username
        
        
        # Media player setup
        self.player = QMediaPlayer()
        self.current_playlist = []
        self.current_index = 0
        self.is_playing = False
        
        # Remove maximize/minimize and set fixed size
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        self.setFixedSize(1223, 892)
        self.seePassword = False

        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.load_initial_data()

    def setup_ui(self):
        """Initialize UI components"""
        # Set up tables
        self.setup_tables()
        
        # Set up media player
        self.progressSlider.setRange(0, 0)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        
        # Timer for updating progress
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_ui)

    def setup_tables(self):
        """Configure all table widgets"""
        # Recent Rotation Table
        self.RR_Table.setColumnWidth(0, 150)
        self.RR_Table.setColumnWidth(1, 150)
        self.RR_Table.setColumnWidth(2, 100)
        self.RR_Table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        # Top 5 Artists Table
        self.Top5Artists_Table.setColumnWidth(0, 200)
        self.Top5Artists_Table.setColumnWidth(1, 150)
        self.Top5Artists_Table.setColumnWidth(2, 250)
        
        # Top 5 Songs Table
        self.Top5Songs_Table.setColumnWidth(0, 200)
        self.Top5Songs_Table.setColumnWidth(1, 200)
        self.Top5Songs_Table.setColumnWidth(2, 200)
        
        # Playlists Table
        self.PL_Table.setColumnWidth(0, 200)
        self.PL_Table.setColumnWidth(1, 120)
        self.PL_Table.setColumnWidth(2, 100)
        self.PL_Table.setColumnWidth(3, 120)
        
        # Queue Table
        self.Queue_Table.setColumnWidth(0, 150)
        self.Queue_Table.setColumnWidth(1, 150)
        self.Queue_Table.setColumnWidth(2, 100)
        self.Queue_Table.setColumnWidth(3, 100)
        
        # Search Tables
        self.searchSongs_Table.setColumnWidth(0, 200)
        self.searchSongs_Table.setColumnWidth(1, 200)
        self.searchSongs_Table.setColumnWidth(2, 120)
        
        self.searchArtists_Table.setColumnWidth(0, 200)
        self.searchArtists_Table.setColumnWidth(1, 150)
        self.searchArtists_Table.setColumnWidth(2, 200)

    def setup_connections(self):
        """Connect all signals and slots"""
        # Navigation buttons
        self.homeBtn.clicked.connect(lambda: self.switch_page(self.homePage, self.homeBtn))
        self.searchNavBtn.clicked.connect(lambda: self.switch_page(self.searchPage, self.searchNavBtn))
        self.libraryBtn.clicked.connect(lambda: self.switch_page(self.libraryPage, self.libraryBtn))
        self.profileBtn.clicked.connect(lambda: self.switch_page(self.profilePage, self.profileBtn))
        self.logoutBtn.clicked.connect(self.logout)
        
        # Home Page
        self.RR_Table.itemSelectionChanged.connect(self.rr_selection_changed)
        self.RR_PlaySongBtn.clicked.connect(self.rr_play_song)
        self.RR_AddQueueBtn.clicked.connect(self.rr_add_to_queue)
        self.RR_AddPlaylistBtn.clicked.connect(self.rr_add_to_playlist)
        self.RR_RefreshBtn.clicked.connect(self.load_recent_rotation)
        
        # Library Page - Playlists
        self.PL_Table.itemSelectionChanged.connect(self.pl_selection_changed)
        self.PL_ViewBtn.clicked.connect(self.pl_view_playlist)
        self.PL_PlayBtn.clicked.connect(self.pl_play_playlist)
        self.PL_DeleteBtn.clicked.connect(self.pl_delete_playlist)
        self.PL_ViewBtn_3.clicked.connect(self.pl_create_new)
        
        # Library Page - Queue
        self.Queue_Table.itemSelectionChanged.connect(self.queue_selection_changed)
        self.Queue_PlayBtn.clicked.connect(self.queue_play)
        self.Queue_RemoveBtn.clicked.connect(self.queue_remove_song)
        self.Queue_ClearBtn.clicked.connect(self.queue_clear)
        
        # Library Page - Media Player
        self.libraryBtn_2.clicked.connect(self.mp_play_pause)
        self.libraryBtn_3.clicked.connect(lambda: self.mp_skip(-5))
        self.libraryBtn_4.clicked.connect(self.mp_previous)
        self.libraryBtn_5.clicked.connect(lambda: self.mp_skip(5))
        self.libraryBtn_7.clicked.connect(self.mp_next)
        self.progressSlider.sliderMoved.connect(self.mp_set_position)
        self.MP_LikeBtn.clicked.connect(self.mp_like_song)
        self.MP_DislikeBtn.clicked.connect(self.mp_dislike_song)
        self.MP_ReportBtn.clicked.connect(self.mp_report_song)
        
        # Search Page
        self.S_SearchBtn.clicked.connect(self.search_songs)
        self.SearchSong.returnPressed.connect(self.search_songs)
        self.searchSongs_Table.itemSelectionChanged.connect(self.search_song_selected)
        self.searchArtists_Table.itemSelectionChanged.connect(self.search_artist_selected)
        self.S_AddQueueBtn.clicked.connect(self.search_add_to_queue)
        self.S_AddPlBtn.clicked.connect(self.search_add_to_playlist)
        self.S_ReportBtn.clicked.connect(self.search_report_song)
        
        # Profile Page
        self.P_UpdateInfoBtn.clicked.connect(self.profile_update_info)
        self.P_UpdatePasswordBtn.clicked.connect(self.profile_update_password)
        self.P_ShowPassBtn.clicked.connect(self.profile_toggle_password)
        self.P_ApplyArtistBtn.clicked.connect(self.profile_apply_artist)
        self.P_BuyPlanBtn.clicked.connect(self.profile_buy_plan)
        self.S_ReportBtn_2.clicked.connect(self.profile_delete_account)
        self.tableWidget.itemSelectionChanged.connect(self.profile_plan_selected)

    def load_initial_data(self):
        """Load all initial data"""
        self.load_home_data()
        self.load_library_data()
        self.load_profile_data()
        self.highlightButton(self.homeBtn)

    # ==================== NAVIGATION ====================
    def switch_page(self, page, button):
        """Switch to a different page"""
        self.stackedWidget.setCurrentWidget(page)
        self.highlightButton(button)
        
        # Refresh data when switching pages
        if page == self.homePage:
            self.load_home_data()
        elif page == self.libraryPage:
            self.load_library_data()
        elif page == self.profilePage:
            self.load_profile_data()

    def highlightButton(self, btn):
        """Highlight the active navigation button"""
        for b in [self.homeBtn, self.searchNavBtn, self.libraryBtn, self.profileBtn]:
            b.setStyleSheet("font-size:24px; background: transparent; border:none; color:#eee;")
        btn.setStyleSheet("font-size:28px; background: #3a3a3a; border-radius:10px; color:#fff;")

    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conn.close()
            QtWidgets.qApp.quit()

    # ==================== HOME PAGE ====================
    def load_home_data(self):
        """Load all home page data"""
        self.load_recent_rotation()
        self.load_top_artists()
        self.load_top_songs()

    def load_recent_rotation(self):
        """Load user's recent rotation"""
        try:
            self.RR_Table.setRowCount(0)
            # Query to get user's most listened songs this week
            query = """
                SELECT s.song_name, a.artist_name, COUNT(*) as listens
                FROM listening_history lh
                JOIN songs s ON lh.song_id = s.song_id
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE lh.user_id = ? 
                AND lh.listen_date >= date('now', '-7 days')
                GROUP BY s.song_id
                ORDER BY listens DESC
                LIMIT 10
            """
            self.cursor.execute(query, (self.user_id,))
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.RR_Table.rowCount()
                self.RR_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.RR_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load recent rotation: {str(e)}")

    def load_top_artists(self):
        """Load top 5 artists of the week"""
        try:
            self.Top5Artists_Table.setRowCount(0)
            query = """
                SELECT a.artist_name, COUNT(*) as listens, 
                       (SELECT s2.song_name FROM songs s2 
                        WHERE s2.artist_id = a.artist_id 
                        ORDER BY s2.play_count DESC LIMIT 1) as best_song
                FROM listening_history lh
                JOIN songs s ON lh.song_id = s.song_id
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE lh.listen_date >= date('now', '-7 days')
                GROUP BY a.artist_id
                ORDER BY listens DESC
                LIMIT 5
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.Top5Artists_Table.rowCount()
                self.Top5Artists_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.Top5Artists_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load top artists: {str(e)}")

    def load_top_songs(self):
        """Load top 5 songs of the week"""
        try:
            self.Top5Songs_Table.setRowCount(0)
            query = """
                SELECT s.song_name, a.artist_name, COUNT(*) as listens
                FROM listening_history lh
                JOIN songs s ON lh.song_id = s.song_id
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE lh.listen_date >= date('now', '-7 days')
                GROUP BY s.song_id
                ORDER BY listens DESC
                LIMIT 5
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.Top5Songs_Table.rowCount()
                self.Top5Songs_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.Top5Songs_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load top songs: {str(e)}")

    def rr_selection_changed(self):
        """Handle Recent Rotation table selection"""
        selected_items = self.RR_Table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.RR_SongName.setText(self.RR_Table.item(row, 0).text())
            self.RR_ArtistName.setText(self.RR_Table.item(row, 1).text())
            self.RR_Listens.setText(self.RR_Table.item(row, 2).text())
            
            # Load song image
            song_name = self.RR_Table.item(row, 0).text()
            self.load_song_image(song_name, self.RR_SongImage)

    def rr_play_song(self):
        """Play selected song from Recent Rotation"""
        if self.RR_SongName.text():
            song_name = self.RR_SongName.text()
            artist_name = self.RR_ArtistName.text()
            self.play_song_by_name(song_name, artist_name)
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    def rr_add_to_queue(self):
        """Add selected song to queue"""
        if self.RR_SongName.text():
            song_name = self.RR_SongName.text()
            self.add_to_queue(song_name)
            QMessageBox.information(self, "Success", "Song added to queue")
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    def rr_add_to_playlist(self):
        """Add selected song to playlist"""
        if self.RR_SongName.text():
            song_name = self.RR_SongName.text()
            self.show_playlist_selector(song_name)
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    # ==================== LIBRARY PAGE ====================
    def load_library_data(self):
        """Load library page data"""
        self.load_playlists()
        self.load_queue()

    def load_playlists(self):
        """Load user's playlists"""
        try:
            self.PL_Table.setRowCount(0)
            query = """
                SELECT playlist_name, 
                       (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = p.playlist_id) as song_count,
                       visits, created_date
                FROM playlists p
                WHERE user_id = ?
                ORDER BY created_date DESC
            """
            self.cursor.execute(query, (self.user_id,))
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.PL_Table.rowCount()
                self.PL_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.PL_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load playlists: {str(e)}")

    def load_queue(self):
        """Load user's queue"""
        try:
            self.Queue_Table.setRowCount(0)
            query = """
                SELECT s.song_name, a.artist_name, s.genre, q.added_date
                FROM queue q
                JOIN songs s ON q.song_id = s.song_id
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE q.user_id = ?
                ORDER BY q.queue_position
            """
            self.cursor.execute(query, (self.user_id,))
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.Queue_Table.rowCount()
                self.Queue_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.Queue_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load queue: {str(e)}")

    def pl_selection_changed(self):
        """Handle playlist selection"""
        selected_items = self.PL_Table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.PL_Name.setText(self.PL_Table.item(row, 0).text())
            self.PL_Visits.setText(self.PL_Table.item(row, 2).text())
            date_str = self.PL_Table.item(row, 3).text()
            self.PL_Date.setDate(QtCore.QDate.fromString(date_str, "yyyy-MM-dd"))

    def pl_view_playlist(self):
        """View playlist contents"""
        if not self.PL_Name.text():
            QMessageBox.warning(self, "Warning", "Please select a playlist first")
            return
        
        playlist_name = self.PL_Name.text()
        # Create dialog to show playlist songs
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"Playlist: {playlist_name}")
        dialog.setFixedSize(600, 400)
        
        layout = QtWidgets.QVBoxLayout()
        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Song Name", "Artist", "Duration"])
        
        try:
            query = """
                SELECT s.song_name, a.artist_name, s.duration
                FROM playlist_songs ps
                JOIN songs s ON ps.song_id = s.song_id
                JOIN artists a ON s.artist_id = a.artist_id
                JOIN playlists p ON ps.playlist_id = p.playlist_id
                WHERE p.playlist_name = ? AND p.user_id = ?
            """
            self.cursor.execute(query, (playlist_name, self.user_id))
            results = self.cursor.fetchall()
            
            table.setRowCount(len(results))
            for i, row_data in enumerate(results):
                for j, data in enumerate(row_data):
                    table.setItem(i, j, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load playlist songs: {str(e)}")
        
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

    def pl_play_playlist(self):
        """Play entire playlist"""
        if not self.PL_Name.text():
            QMessageBox.warning(self, "Warning", "Please select a playlist first")
            return
        
        playlist_name = self.PL_Name.text()
        # Load playlist songs and play
        QMessageBox.information(self, "Playing", f"Playing playlist: {playlist_name}")

    def pl_delete_playlist(self):
        """Delete selected playlist"""
        if not self.PL_Name.text():
            QMessageBox.warning(self, "Warning", "Please select a playlist first")
            return
        
        playlist_name = self.PL_Name.text()
        reply = QMessageBox.question(self, "Delete Playlist", 
                                    f"Are you sure you want to delete '{playlist_name}'?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM playlists WHERE playlist_name = ? AND user_id = ?"
                self.cursor.execute(query, (playlist_name, self.user_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Playlist deleted successfully")
                self.load_playlists()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete playlist: {str(e)}")

    def pl_create_new(self):
        """Create new playlist"""
        name, ok = QInputDialog.getText(self, "New Playlist", "Enter playlist name:")
        if ok and name:
            try:
                query = "INSERT INTO playlists (playlist_name, user_id, created_date, visits) VALUES (?, ?, date('now'), 0)"
                self.cursor.execute(query, (name, self.user_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Playlist created successfully")
                self.load_playlists()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to create playlist: {str(e)}")

    def queue_selection_changed(self):
        """Handle queue selection"""
        pass

    def queue_play(self):
        """Play queue"""
        if self.Queue_Table.rowCount() > 0:
            QMessageBox.information(self, "Playing Queue", "Playing queue...")
        else:
            QMessageBox.warning(self, "Warning", "Queue is empty")

    def queue_remove_song(self):
        """Remove selected song from queue"""
        selected_items = self.Queue_Table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            song_name = self.Queue_Table.item(row, 0).text()
            try:
                query = """
                    DELETE FROM queue 
                    WHERE user_id = ? AND song_id = (SELECT song_id FROM songs WHERE song_name = ?)
                """
                self.cursor.execute(query, (self.user_id, song_name))
                self.conn.commit()
                self.load_queue()
                QMessageBox.information(self, "Success", "Song removed from queue")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to remove song: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    def queue_clear(self):
        """Clear entire queue"""
        reply = QMessageBox.question(self, "Clear Queue", 
                                    "Are you sure you want to clear the queue?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM queue WHERE user_id = ?"
                self.cursor.execute(query, (self.user_id,))
                self.conn.commit()
                self.load_queue()
                QMessageBox.information(self, "Success", "Queue cleared")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to clear queue: {str(e)}")

    # ==================== MEDIA PLAYER ====================
    def mp_play_pause(self):
        """Toggle play/pause"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.libraryBtn_2.setText("▶️")
        else:
            self.player.play()
            self.libraryBtn_2.setText("⏸️")

    def mp_previous(self):
        """Play previous song"""
        if self.current_index > 0:
            self.current_index -= 1
            self.play_current_song()

    def mp_next(self):
        """Play next song"""
        if self.current_index < len(self.current_playlist) - 1:
            self.current_index += 1
            self.play_current_song()

    def mp_skip(self, seconds):
        """Skip forward or backward"""
        position = self.player.position() + (seconds * 1000)
        self.player.setPosition(position)

    def mp_set_position(self, position):
        """Set player position from slider"""
        self.player.setPosition(position)

    def position_changed(self, position):
        """Update UI when position changes"""
        self.progressSlider.setValue(position)
        self.elapsedLabel.setText(self.format_time(position))

    def duration_changed(self, duration):
        """Update UI when duration changes"""
        self.progressSlider.setRange(0, duration)
        self.durationLabel.setText(self.format_time(duration))

    def state_changed(self, state):
        """Handle player state changes"""
        if state == QMediaPlayer.PlayingState:
            self.libraryBtn_2.setText("⏸️")
        else:
            self.libraryBtn_2.setText("▶️")

    def format_time(self, ms):
        """Format milliseconds to MM:SS"""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def mp_like_song(self):
        """Like current song"""
        QMessageBox.information(self, "Liked", "Song added to liked songs")

    def mp_dislike_song(self):
        """Dislike current song"""
        QMessageBox.information(self, "Disliked", "Noted. We'll play this less")

    def mp_report_song(self):
        """Report current song"""
        reason, ok = QInputDialog.getText(self, "Report Song", "Enter reason for reporting:")
        if ok and reason:
            QMessageBox.information(self, "Reported", "Song reported successfully")

    def play_current_song(self):
        """Play song at current index"""
        if 0 <= self.current_index < len(self.current_playlist):
            song_path = self.current_playlist[self.current_index]
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(song_path)))
            self.player.play()

    def play_song_by_name(self, song_name, artist_name):
        """Play a song by name"""
        try:
            query = "SELECT file_path FROM songs s JOIN artists a ON s.artist_id = a.artist_id WHERE s.song_name = ? AND a.artist_name = ?"
            self.cursor.execute(query, (song_name, artist_name))
            result = self.cursor.fetchone()
            
            if result:
                file_path = result[0]
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.player.play()
                self.MP_SongName.setText(song_name)
                self.MP_ArtistName.setText(artist_name)
                self.load_song_image(song_name, self.MP_songImage)
                
                # Record listen
                self.record_listen(song_name)
            else:
                QMessageBox.warning(self, "Error", "Song file not found")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to play song: {str(e)}")

    def update_ui(self):
        """Update UI periodically"""
        pass

    # ==================== SEARCH PAGE ====================
    def search_songs(self):
        """Search for songs and artists"""
        search_text = self.SearchSong.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Warning", "Please enter a search term")
            return
        
        # Search songs
        try:
            self.searchSongs_Table.setRowCount(0)
            query = """
                SELECT s.song_name, a.artist_name, s.genre
                FROM songs s
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE s.song_name LIKE ? OR a.artist_name LIKE ?
                LIMIT 20
            """
            self.cursor.execute(query, (f"%{search_text}%", f"%{search_text}%"))
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.searchSongs_Table.rowCount()
                self.searchSongs_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.searchSongs_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Search failed: {str(e)}")
        
        # Search artists
        try:
            self.searchArtists_Table.setRowCount(0)
            query = """
                SELECT a.artist_name, 
                       COUNT(s.song_id) as songs_released,
                       (SELECT s2.song_name FROM songs s2 WHERE s2.artist_id = a.artist_id ORDER BY s2.play_count DESC LIMIT 1) as top_song
                FROM artists a
                LEFT JOIN songs s ON a.artist_id = s.artist_id
                WHERE a.artist_name LIKE ?
                GROUP BY a.artist_id
                LIMIT 10
            """
            self.cursor.execute(query, (f"%{search_text}%",))
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.searchArtists_Table.rowCount()
                self.searchArtists_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.searchArtists_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Artist search failed: {str(e)}")

    def search_song_selected(self):
        """Handle song selection in search results"""
        selected_items = self.searchSongs_Table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.S_SongName.setText(self.searchSongs_Table.item(row, 0).text())
            self.S_ArtistName.setText(self.searchSongs_Table.item(row, 1).text())

    def search_artist_selected(self):
        """Handle artist selection in search results"""
        selected_items = self.searchArtists_Table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            artist_name = self.searchArtists_Table.item(row, 0).text()
            self.load_artist_songs(artist_name)

    def load_artist_songs(self, artist_name):
        """Load songs by selected artist"""
        try:
            self.artistSongs_Table.setRowCount(0)
            self.artistSongs_Table.setColumnCount(2)
            self.artistSongs_Table.setHorizontalHeaderLabels(["Song Name", "Genre"])
            
            query = """
                SELECT s.song_name, s.genre
                FROM songs s
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE a.artist_name = ?
                ORDER BY s.play_count DESC
            """
            self.cursor.execute(query, (artist_name,))
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.artistSongs_Table.rowCount()
                self.artistSongs_Table.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.artistSongs_Table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load artist songs: {str(e)}")

    def search_add_to_queue(self):
        """Add selected song to queue from search"""
        if self.S_SongName.text():
            song_name = self.S_SongName.text()
            self.add_to_queue(song_name)
            QMessageBox.information(self, "Success", "Song added to queue")
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    def search_add_to_playlist(self):
        """Add selected song to playlist from search"""
        if self.S_SongName.text():
            song_name = self.S_SongName.text()
            self.show_playlist_selector(song_name)
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    def search_report_song(self):
        """Report selected song from search"""
        if self.S_SongName.text():
            song_name = self.S_SongName.text()
            reason, ok = QInputDialog.getText(self, "Report Song", "Enter reason for reporting:")
            if ok and reason:
                try:
                    query = """
                        INSERT INTO song_reports (song_id, user_id, reason, report_date)
                        SELECT song_id, ?, ?, date('now')
                        FROM songs WHERE song_name = ?
                    """
                    self.cursor.execute(query, (self.user_id, reason, song_name))
                    self.conn.commit()
                    QMessageBox.information(self, "Success", "Song reported successfully")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to report song: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a song first")

    # ==================== PROFILE PAGE ====================
    def load_profile_data(self):
        """Load user profile data"""
        try:
            # Load user info
            query = "SELECT username, full_name, email, phone FROM users WHERE user_id = ?"
            self.cursor.execute(query, (self.user_id,))
            result = self.cursor.fetchone()
            
            if result:
                self.P_Username.setText(result[0])
                self.P_Fullname.setText(result[1] or "")
                self.P_Email.setText(result[2] or "")
                self.P_Number.setText(result[3] or "")
            
            # Load subscription info
            query = "SELECT subscription_type FROM subscriptions WHERE user_id = ?"
            self.cursor.execute(query, (self.user_id,))
            result = self.cursor.fetchone()
            self.P_Subscription.setText(result[0] if result else "Free")
            
            # Load artist request status
            query = "SELECT status FROM artist_requests WHERE user_id = ? ORDER BY request_date DESC LIMIT 1"
            self.cursor.execute(query, (self.user_id,))
            result = self.cursor.fetchone()
            self.P_RequestStatus.setText(result[0] if result else "No request submitted")
            
            # Load subscription plans
            self.load_subscription_plans()
            
            # Clear error label
            self.label_66.setText("")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load profile: {str(e)}")

    def load_subscription_plans(self):
        """Load available subscription plans"""
        try:
            self.tableWidget.setRowCount(0)
            query = "SELECT plan_name, price, features FROM subscription_plans ORDER BY price"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            for row_data in results:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for column, data in enumerate(row_data):
                    self.tableWidget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            # If table doesn't exist, add some default plans
            self.tableWidget.setRowCount(3)
            plans = [
                ("Free", "0", "Basic features"),
                ("Premium", "9.99", "Ad-free, HD quality"),
                ("Family", "14.99", "6 accounts, all features")
            ]
            for i, plan in enumerate(plans):
                for j, data in enumerate(plan):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(data))

    def profile_update_info(self):
        """Update user information"""
        try:
            full_name = self.P_Fullname.text()
            email = self.P_Email.text()
            phone = self.P_Number.text()
            
            query = "UPDATE users SET full_name = ?, email = ?, phone = ? WHERE user_id = ?"
            self.cursor.execute(query, (full_name, email, phone, self.user_id))
            self.conn.commit()
            
            QMessageBox.information(self, "Success", "Profile updated successfully")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update profile: {str(e)}")

    def profile_update_password(self):
        """Update user password"""
        current_pw = self.P_CurrentPass.text()
        new_pw1 = self.P_NewPass1.text()
        new_pw2 = self.P_NewPass2.text()
        
        if not current_pw or not new_pw1 or not new_pw2:
            self.label_66.setText("❌ All fields are required")
            return
        
        if new_pw1 != new_pw2:
            self.label_66.setText("❌ New passwords do not match")
            return
        
        if len(new_pw1) < 6:
            self.label_66.setText("❌ Password must be at least 6 characters")
            return
        
        try:
            # Verify current password
            query = "SELECT password FROM users WHERE user_id = ?"
            self.cursor.execute(query, (self.user_id,))
            result = self.cursor.fetchone()
            
            if result and result[0] == current_pw:
                # Update password
                query = "UPDATE users SET password = ? WHERE user_id = ?"
                self.cursor.execute(query, (new_pw1, self.user_id))
                self.conn.commit()
                
                self.label_66.setText("✅ Password updated successfully")
                self.P_CurrentPass.clear()
                self.P_NewPass1.clear()
                self.P_NewPass2.clear()
            else:
                self.label_66.setText("❌ Current password is incorrect")
        except Exception as e:
            self.label_66.setText(f"❌ Error: {str(e)}")

    def profile_toggle_password(self):
        """Toggle password visibility"""
        self.seePassword = not self.seePassword
        
        if self.seePassword:
            self.P_NewPass1.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.P_NewPass2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.P_ShowPassBtn.setStyleSheet("""
                background-color: #3a3a3a;
                color: white;
                border: 3px solid white;
                border-radius: 8px;
                font-size: 20px;
            """)
        else:
            self.P_NewPass1.setEchoMode(QtWidgets.QLineEdit.Password)
            self.P_NewPass2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.P_ShowPassBtn.setStyleSheet("""
                background-color: transparent;
                color: white;
                border: 3px solid white;
                border-radius: 8px;
                font-size: 20px;
            """)

    def profile_apply_artist(self):
        """Apply to become an artist"""
        try:
            # Check if already applied
            query = "SELECT status FROM artist_requests WHERE user_id = ? ORDER BY request_date DESC LIMIT 1"
            self.cursor.execute(query, (self.user_id,))
            result = self.cursor.fetchone()
            
            if result and result[0] == "Pending":
                QMessageBox.warning(self, "Warning", "You already have a pending request")
                return
            
            # Submit new request
            query = "INSERT INTO artist_requests (user_id, request_date, status) VALUES (?, date('now'), 'Pending')"
            self.cursor.execute(query, (self.user_id,))
            self.conn.commit()
            
            self.P_RequestStatus.setText("Pending")
            QMessageBox.information(self, "Success", "Artist request submitted successfully")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to submit request: {str(e)}")

    def profile_plan_selected(self):
        """Handle subscription plan selection"""
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.P_PlanName.setText(self.tableWidget.item(row, 0).text())
            self.P_Price.setText(self.tableWidget.item(row, 1).text())

    def profile_buy_plan(self):
        """Purchase subscription plan"""
        plan_name = self.P_PlanName.text()
        price = self.P_Price.text()
        
        if not plan_name:
            QMessageBox.warning(self, "Warning", "Please select a plan first")
            return
        
        reply = QMessageBox.question(self, "Confirm Purchase", 
                                    f"Do you want to purchase {plan_name} for ${price}/month?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = """
                    INSERT OR REPLACE INTO subscriptions (user_id, subscription_type, start_date, status)
                    VALUES (?, ?, date('now'), 'Active')
                """
                self.cursor.execute(query, (self.user_id, plan_name))
                self.conn.commit()
                
                self.P_Subscription.setText(plan_name)
                QMessageBox.information(self, "Success", "Subscription activated successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to purchase plan: {str(e)}")

    def profile_delete_account(self):
        """Delete user account"""
        if not self.checkBox.isChecked():
            QMessageBox.warning(self, "Warning", "Please acknowledge the account deletion")
            return
        
        reply = QMessageBox.question(self, "Delete Account", 
                                    "Are you ABSOLUTELY sure? This action cannot be undone!",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM users WHERE user_id = ?"
                self.cursor.execute(query, (self.user_id,))
                self.conn.commit()
                
                QMessageBox.information(self, "Account Deleted", "Your account has been deleted")
                self.conn.close()
                QtWidgets.qApp.quit()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete account: {str(e)}")

    # ==================== HELPER FUNCTIONS ====================
    def add_to_queue(self, song_name):
        """Add a song to the queue"""
        try:
            # Get next queue position
            query = "SELECT COALESCE(MAX(queue_position), 0) + 1 FROM queue WHERE user_id = ?"
            self.cursor.execute(query, (self.user_id,))
            next_position = self.cursor.fetchone()[0]
            
            # Add to queue
            query = """
                INSERT INTO queue (user_id, song_id, queue_position, added_date)
                SELECT ?, song_id, ?, date('now')
                FROM songs WHERE song_name = ?
            """
            self.cursor.execute(query, (self.user_id, next_position, song_name))
            self.conn.commit()
            
            self.load_queue()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add to queue: {str(e)}")

    def show_playlist_selector(self, song_name):
        """Show dialog to select playlist"""
        try:
            # Get user's playlists
            query = "SELECT playlist_name FROM playlists WHERE user_id = ?"
            self.cursor.execute(query, (self.user_id,))
            playlists = [row[0] for row in self.cursor.fetchall()]
            
            if not playlists:
                QMessageBox.warning(self, "No Playlists", "Create a playlist first")
                return
            
            playlist, ok = QInputDialog.getItem(self, "Select Playlist", 
                                               "Choose a playlist:", playlists, 0, False)
            if ok and playlist:
                # Add song to playlist
                query = """
                    INSERT INTO playlist_songs (playlist_id, song_id)
                    SELECT p.playlist_id, s.song_id
                    FROM playlists p, songs s
                    WHERE p.playlist_name = ? AND p.user_id = ? AND s.song_name = ?
                """
                self.cursor.execute(query, (playlist, self.user_id, song_name))
                self.conn.commit()
                
                QMessageBox.information(self, "Success", f"Song added to '{playlist}'")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add to playlist: {str(e)}")

    def load_song_image(self, song_name, label_widget):
        """Load and display song image"""
        try:
            # Try to load from database or file system
            query = "SELECT image_path FROM songs WHERE song_name = ?"
            self.cursor.execute(query, (song_name,))
            result = self.cursor.fetchone()
            
            if result and result[0] and os.path.exists(result[0]):
                pixmap = QtGui.QPixmap(result[0])
                label_widget.setPixmap(pixmap.scaled(label_widget.size(), 
                                                     QtCore.Qt.KeepAspectRatio, 
                                                     QtCore.Qt.SmoothTransformation))
            else:
                # Use default image
                default_path = "../Song_images/default_song_image.jpg"
                if os.path.exists(default_path):
                    pixmap = QtGui.QPixmap(default_path)
                    label_widget.setPixmap(pixmap.scaled(label_widget.size(), 
                                                         QtCore.Qt.KeepAspectRatio, 
                                                         QtCore.Qt.SmoothTransformation))
        except Exception as e:
            print(f"Failed to load image: {e}")

    def record_listen(self, song_name):
        """Record a song listen in history"""
        try:
            query = """
                INSERT INTO listening_history (user_id, song_id, listen_date)
                SELECT ?, song_id, datetime('now')
                FROM songs WHERE song_name = ?
            """
            self.cursor.execute(query, (self.user_id, song_name))
            
            # Update song play count
            query = "UPDATE songs SET play_count = play_count + 1 WHERE song_name = ?"
            self.cursor.execute(query, (song_name,))
            
            self.conn.commit()
        except Exception as e:
            print(f"Failed to record listen: {e}")


# ==================== MAIN ====================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # For testing purposes, use dummy user_id and username
    # In production, these would come from your login system
    window = ListenerDashboard(user_id=1, username="test_user")
    window.show()
    
    sys.exit(app.exec_())