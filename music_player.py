import os
import sys
import pyodbc
from PyQt5 import QtWidgets, QtCore, QtGui
import pygame
from mutagen.mp3 import MP3

# ==================== DATABASE CONFIG ====================
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

class MusicPlayer:
    # Playback modes
    MODE_NORMAL = "normal"
    MODE_QUEUE = "queue"
    MODE_PLAYLIST = "playlist"

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window = window
        pygame.mixer.init()

        # Song Data
        self.all_songs = [] 
        self.current_playlist = []
        self.current_index = -1
        self.playback_mode = self.MODE_NORMAL
        
        # Playback State
        self.is_paused = False
        self.song_length = 0
        self.song_position = 0
        self._last_pos = 0

        # UI Info
        self.current_song_name = ""
        self.current_artist_name = ""
        self.current_genre = ""
        self.on_queue_end_callback = None

        # Load Data from DB
        self.load_all_songs_from_db()

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_progress)

        self.setup_ui()
        self.connect_signals()

    def load_all_songs_from_db(self):
        """Fetch active songs from SQL Server."""
        self.all_songs = []
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Fetch FilePath (MetaData), Name, Artist, Genre
            query = """
                SELECT sd.MetaData, sd.SongName, sd.Username, g.GenreName 
                FROM SongDetails sd
                LEFT JOIN SongGenre sg ON sd.SongID = sg.SongID
                LEFT JOIN Genre g ON sg.GenreID = g.GenreID
                WHERE sd.SongStatus = 'Active'
                ORDER BY sd.SongName
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for row in rows:
                file_path = row[0]
                # If path exists or looks like a valid path, add it
                if file_path: 
                    self.all_songs.append((file_path, row[1], row[2], row[3] or "Unknown"))

            self.current_playlist = self.all_songs.copy()
            print(f"MusicPlayer loaded {len(self.all_songs)} songs.")

        except Exception as e:
            print(f"MusicPlayer DB Error: {e}")
        finally:
            if conn: conn.close()

    def set_permissions(self, plan_name):
        """
        Locks controls for Free Tier users.
        Unlocks them for Premium users.
        """
        is_premium = (plan_name != "Free Tier" and plan_name != "Free")
        
        # Controls to toggle
        # libraryBtn_3 = Rewind
        # libraryBtn_5 = Fast Forward
        # libraryBtn_4 = Previous Song / Restart
        # progressSlider = Seek Bar

        self.window.libraryBtn_3.setEnabled(is_premium)
        self.window.libraryBtn_5.setEnabled(is_premium)
        self.window.libraryBtn_4.setEnabled(is_premium)
        self.window.progressSlider.setEnabled(is_premium)
        
        if not is_premium:
            tooltip = "Upgrade to Premium to use this feature."
            self.window.progressSlider.setToolTip(tooltip)
            self.window.libraryBtn_3.setToolTip(tooltip)
            self.window.libraryBtn_4.setToolTip(tooltip)
            self.window.libraryBtn_5.setToolTip(tooltip)
        else:
            self.window.progressSlider.setToolTip("")
            self.window.libraryBtn_3.setToolTip("Rewind")
            self.window.libraryBtn_4.setToolTip("Previous")
            self.window.libraryBtn_5.setToolTip("Skip")

    def setup_ui(self):
        self.window.progressSlider.setRange(0, 0)
        self.window.elapsedLabel.setText("00:00")
        self.window.durationLabel.setText("00:00")
        self.window.MP_SongName.setText("<No Song>")
        self.window.MP_ArtistName.setText("<Select a song>")
        self.window.MP_Genre.setText("")
        self.set_default_image()

    def connect_signals(self):
        self.window.libraryBtn_2.clicked.connect(self.play_pause)
        self.window.libraryBtn_3.clicked.connect(self.rewind_5s)
        self.window.libraryBtn_4.clicked.connect(self.previous_song)
        self.window.libraryBtn_5.clicked.connect(self.forward_5s)
        self.window.libraryBtn_7.clicked.connect(self.next_song)

        self.window.progressSlider.sliderPressed.connect(self.slider_pressed)
        self.window.progressSlider.sliderReleased.connect(self.slider_released)

        self.window.MP_LikeBtn.clicked.connect(self.like_song)
        self.window.MP_DislikeBtn.clicked.connect(self.dislike_song)
        self.window.MP_ReportBtn.clicked.connect(self.report_song)

    def get_song_file_path(self, song_name):
        for file_path, name, artist, genre in self.all_songs:
            if name.lower() == song_name.lower():
                return file_path, name, artist, genre
        return None, None, None, None

    def load_song(self, index):
        if not self.current_playlist or index < 0 or index >= len(self.current_playlist):
            return False

        self.current_index = index
        file_path, song_name, artist_name, genre = self.current_playlist[index]

        try:
            pygame.mixer.music.load(file_path)
            self.current_song_name = song_name
            self.current_artist_name = artist_name
            self.current_genre = genre

            audio = MP3(file_path)
            self.song_length = int(audio.info.length)
            self.song_position = 0
            self._last_pos = 0

            self.update_song_info()
            self.window.progressSlider.setRange(0, self.song_length)
            self.window.progressSlider.setValue(0)
            self.window.elapsedLabel.setText("00:00")
            self.window.durationLabel.setText(self.format_time(self.song_length))
            return True
        except Exception as e:
            print(f"Error loading song: {e}")
            return False

    def update_song_info(self):
        self.window.MP_SongName.setText(self.current_song_name)
        self.window.MP_ArtistName.setText(self.current_artist_name)
        self.window.MP_Genre.setText(self.current_genre)
        self.load_song_image()

    def load_song_image(self):
        if 0 <= self.current_index < len(self.current_playlist):
            file_path = self.current_playlist[self.current_index][0]
            base_name = os.path.splitext(file_path)[0]
            for ext in ['.jpg', '.jpeg', '.png']:
                image_path = base_name + ext
                if os.path.exists(image_path):
                    pixmap = QtGui.QPixmap(image_path)
                    if not pixmap.isNull():
                        self.window.MP_songImage.setPixmap(
                            pixmap.scaled(self.window.MP_songImage.size(),
                                          QtCore.Qt.KeepAspectRatio,
                                          QtCore.Qt.SmoothTransformation))
                        return
        self.set_default_image()

    def set_default_image(self):
        path = "Song_images/default_song_image.jpg"
        if os.path.exists(path):
            pixmap = QtGui.QPixmap(path)
            self.window.MP_songImage.setPixmap(
                pixmap.scaled(self.window.MP_songImage.size(),
                              QtCore.Qt.KeepAspectRatio,
                              QtCore.Qt.SmoothTransformation))

    def play_pause(self):
        if self.current_index < 0:
            if not self.load_song(0): return

        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.window.libraryBtn_2.setText("▶️")
            self.timer.stop()
        else:
            if self.is_paused: pygame.mixer.music.unpause()
            else: pygame.mixer.music.play(start=self.song_position)
            self.is_paused = False
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.song_position = 0
        self.window.libraryBtn_2.setText("▶️")
        self.window.progressSlider.setValue(0)
        self.timer.stop()

    def previous_song(self):
        # Controlled by set_permissions, but we add a check just in case
        if not self.window.libraryBtn_4.isEnabled(): return

        if not self.current_playlist: return
        new_index = self.current_index - 1
        if new_index < 0: new_index = len(self.current_playlist) - 1
        self.stop()
        if self.load_song(new_index):
            pygame.mixer.music.play()
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def next_song(self):
        if not self.current_playlist: return
        new_index = self.current_index + 1
        if new_index >= len(self.current_playlist):
            if self.playback_mode != self.MODE_NORMAL:
                self.playback_mode = self.MODE_NORMAL
                self.current_playlist = self.all_songs.copy()
                self.current_index = -1
                if self.on_queue_end_callback: self.on_queue_end_callback()
                return
            new_index = 0
        self.stop()
        if self.load_song(new_index):
            pygame.mixer.music.play()
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def rewind_5s(self):
        # Controlled by set_permissions
        if not self.window.libraryBtn_3.isEnabled(): return
        self.song_position = max(0, self.song_position - 5)
        pygame.mixer.music.play(start=self.song_position)
        if not self.is_paused: self.timer.start()

    def forward_5s(self):
        # Controlled by set_permissions
        if not self.window.libraryBtn_5.isEnabled(): return
        self.song_position = min(self.song_length, self.song_position + 5)
        if self.song_position >= self.song_length:
            self.next_song()
            return
        pygame.mixer.music.play(start=self.song_position)
        if not self.is_paused: self.timer.start()

    def slider_pressed(self):
        self.timer.stop()

    def slider_released(self):
        if not self.window.progressSlider.isEnabled(): return
        self.song_position = self.window.progressSlider.value()
        pygame.mixer.music.play(start=self.song_position)
        self.is_paused = False
        self.window.libraryBtn_2.setText("⏸️")
        self.timer.start()

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() / 1000.0
            if pos < 0: pos = 0
            delta = pos - self._last_pos
            if delta > 0: self.song_position += delta
            self._last_pos = pos
            self.song_position = min(self.song_position, self.song_length)
            self.window.progressSlider.setValue(int(self.song_position))
            self.window.elapsedLabel.setText(self.format_time(int(self.song_position)))
        elif not self.is_paused and self.current_index >= 0:
            self.next_song()

    def format_time(self, seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def play_song_by_name(self, song_name):
        file_path, name, artist, genre = self.get_song_file_path(song_name)
        if not file_path:
            QtWidgets.QMessageBox.warning(self.window, "Not Found", f"File for '{song_name}' not found.")
            return False
        
        self.playback_mode = self.MODE_NORMAL
        self.current_playlist = self.all_songs.copy()
        
        for i, (fp, sn, ar, ge) in enumerate(self.current_playlist):
            if sn.lower() == song_name.lower():
                self.stop()
                if self.load_song(i):
                    pygame.mixer.music.play()
                    self.window.libraryBtn_2.setText("⏸️")
                    self.timer.start()
                return True
        return False

    def play_queue(self, queue_songs, on_end_callback=None):
        if not queue_songs: return False
        playlist = []
        for row in queue_songs:
            path, name, art, gen = self.get_song_file_path(row[0])
            if path: playlist.append((path, name, art, gen))
        
        if not playlist: return False
        self.playback_mode = self.MODE_QUEUE
        self.current_playlist = playlist
        self.on_queue_end_callback = on_end_callback
        self.stop()
        if self.load_song(0):
            pygame.mixer.music.play()
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()
            return True
        return False

    def play_playlist(self, playlist_songs, playlist_name="Playlist"):
        if not playlist_songs: return False
        playlist = []
        for row in playlist_songs:
            path, name, art, gen = self.get_song_file_path(row[0])
            if path: playlist.append((path, name, art, gen))
            
        if not playlist: return False
        self.playback_mode = self.MODE_PLAYLIST
        self.current_playlist = playlist
        self.stop()
        if self.load_song(0):
            pygame.mixer.music.play()
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()
            return True
        return False

    def like_song(self):
        if self.current_song_name:
            QtWidgets.QMessageBox.information(self.window, "Liked", f"Liked '{self.current_song_name}'!")

    def dislike_song(self):
        if self.current_song_name:
            QtWidgets.QMessageBox.information(self.window, "Disliked", f"Disliked '{self.current_song_name}'.")

    def report_song(self):
        if not self.current_song_name: return
        reasons = ["Inappropriate Content", "Audio Quality", "Other"]
        reason, ok = QtWidgets.QInputDialog.getItem(self.window, "Report", f"Report {self.current_song_name}?", reasons, 0, False)
        if ok and reason:
            QtWidgets.QMessageBox.information(self.window, "Reported", "Report submitted.")

    def cleanup(self):
        self.timer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()