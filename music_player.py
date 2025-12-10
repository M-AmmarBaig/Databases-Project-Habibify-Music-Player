"""
Music Player module for the Artist/User Dashboard. 
Handles all media playback functionality using pygame.
"""

import os
from PyQt5 import QtWidgets, QtCore, QtGui
import pygame
from mutagen.mp3 import MP3
from data import get_approved_songs


class MusicPlayer:
    # Playback modes
    MODE_NORMAL = "normal"  # Play from all songs
    MODE_QUEUE = "queue"  # Play from user's queue
    MODE_PLAYLIST = "playlist"  # Play from a playlist

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window = window

        pygame.mixer.init()

        # All available songs from data. py
        self.all_songs = [
        ]  # [(file_path, song_name, artist_name, genre), ...]

        # Current playback state
        self.current_playlist = [
        ]  # Current list being played (queue, playlist, or all songs)
        self.current_index = -1
        self.playback_mode = self.MODE_NORMAL

        self.is_paused = False
        self.song_length = 0
        self.song_position = 0
        self._last_pos = 0

        # Current song info
        self.current_song_name = ""
        self.current_artist_name = ""
        self.current_genre = ""

        # Callback for when queue/playlist ends
        self.on_queue_end_callback = None

        # Load songs from data.py
        self.load_all_songs()

        # Timer for progress updates
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_progress)

        self.setup_ui()
        self.connect_signals()

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

    def load_all_songs(self):
        """Load all songs from data.py that have valid file paths."""
        self.all_songs = []

        approved_songs = get_approved_songs()
        for song_id, data in approved_songs.items():
            song_name = data[0]
            artist_name = data[1]
            genre = data[2]
            file_path = data[6] if len(data) > 6 else None

            if file_path and os.path.exists(file_path):
                self.all_songs.append(
                    (file_path, song_name, artist_name, genre))
                print(f"✓ Loaded: {song_name} by {artist_name}")
            elif file_path:
                print(f"✗ File not found: {file_path}")

        self.all_songs.sort(key=lambda x: x[1].lower())

        # Default playlist is all songs
        self.current_playlist = self.all_songs.copy()

        print(f"\nTotal songs loaded: {len(self. all_songs)}")

    def get_song_file_path(self, song_name):
        """Find file path for a song by name."""
        for file_path, name, artist, genre in self.all_songs:
            if name.lower() == song_name.lower():
                return file_path, name, artist, genre
        return None, None, None, None

    def load_song(self, index):
        """Load a song by index from current playlist."""
        if not self.current_playlist:
            self.show_no_songs_error()
            return False

        if index < 0 or index >= len(self.current_playlist):
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
            self.window.durationLabel.setText(
                self.format_time(self.song_length))

            return True

        except Exception as e:
            print(f"Error loading song: {e}")
            QtWidgets.QMessageBox.critical(self.window, "Error",
                                           f"Failed to load song:\n{str(e)}")
            return False

    def show_no_songs_error(self):
        """Show error message with missing files info."""
        approved_songs = get_approved_songs()
        missing_files = []

        for song_id, data in approved_songs.items():
            file_path = data[6] if len(data) > 6 else None
            if file_path and not os.path.exists(file_path):
                missing_files.append(f"- {os.path.basename(file_path)}")

        msg = "No playable songs found.\n\n"
        if missing_files:
            msg += "Missing files:\n" + "\n".join(missing_files[:5])
            if len(missing_files) > 5:
                msg += f"\n... and {len(missing_files) - 5} more"
            msg += "\n\nPlease add these MP3 files to the 'songs' folder."

        QtWidgets.QMessageBox.warning(self.window, "No Songs", msg)

    def update_song_info(self):
        """Update the song info display."""
        self.window.MP_SongName.setText(self.current_song_name)
        self.window.MP_ArtistName.setText(self.current_artist_name)
        self.window.MP_Genre.setText(self.current_genre)
        self.load_song_image()

    def load_song_image(self):
        """Load the song's cover image if available."""
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
        """Set the default song image."""
        for path in [
                "Song_images/default_song_image.jpg",
                "Song_images/default. jpg"
        ]:
            if os.path.exists(path):
                pixmap = QtGui.QPixmap(path)
                if not pixmap.isNull():
                    self.window.MP_songImage.setPixmap(
                        pixmap.scaled(self.window.MP_songImage.size(),
                                      QtCore.Qt.KeepAspectRatio,
                                      QtCore.Qt.SmoothTransformation))
                    return

    # ==================== PLAYBACK CONTROLS ====================

    def play_pause(self):
        """Toggle play/pause."""
        if not self.current_playlist:
            self.show_no_songs_error()
            return

        if self.current_index < 0:
            if not self.load_song(0):
                return

        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.window.libraryBtn_2.setText("▶️")
            self.timer.stop()
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play(start=self.song_position)

            self.is_paused = False
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_paused = False
        self.song_position = 0
        self._last_pos = 0
        self.window.libraryBtn_2.setText("▶️")
        self.window.progressSlider.setValue(0)
        self.window.elapsedLabel.setText("00:00")
        self.timer.stop()

    def previous_song(self):
        """Play the previous song in current playlist."""
        if not self.current_playlist:
            return

        new_index = self.current_index - 1
        if new_index < 0:
            new_index = len(self.current_playlist) - 1  # Loop to end

        self.stop()
        if self.load_song(new_index):
            pygame.mixer.music.play()
            self.is_paused = False
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def next_song(self):
        """Play the next song in current playlist."""
        if not self.current_playlist:
            return

        new_index = self.current_index + 1

        # Check if we've reached the end
        if new_index >= len(self.current_playlist):
            if self.playback_mode in [self.MODE_QUEUE, self.MODE_PLAYLIST]:
                # End of queue/playlist - switch back to normal mode
                self.playback_mode = self.MODE_NORMAL
                self.current_playlist = self.all_songs.copy()
                self.current_index = -1

                QtWidgets.QMessageBox.information(
                    self.window, "Playback Complete",
                    "Queue/Playlist finished.  Returning to normal playback.")

                if self.on_queue_end_callback:
                    self.on_queue_end_callback()
                return
            else:
                new_index = 0  # Loop in normal mode

        self.stop()
        if self.load_song(new_index):
            pygame.mixer.music.play()
            self.is_paused = False
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def rewind_5s(self):
        """Rewind 5 seconds."""
        if not self.current_playlist or self.current_index < 0:
            return

        self.song_position = max(0, self.song_position - 5)
        pygame.mixer.music.play(start=self.song_position)
        self._last_pos = 0

        if not self.is_paused:
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def forward_5s(self):
        """Forward 5 seconds."""
        if not self.current_playlist or self.current_index < 0:
            return

        self.song_position = min(self.song_length, self.song_position + 5)

        if self.song_position >= self.song_length:
            self.next_song()
            return

        pygame.mixer.music.play(start=self.song_position)
        self._last_pos = 0

        if not self.is_paused:
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

    def slider_pressed(self):
        self.timer.stop()

    def slider_released(self):
        if not self.current_playlist or self.current_index < 0:
            return

        self.song_position = self.window.progressSlider.value()
        pygame.mixer.music.play(start=self.song_position)
        self._last_pos = 0

        self.is_paused = False
        self.window.libraryBtn_2.setText("⏸️")
        self.timer.start()

    def update_progress(self):
        """Update the progress slider and time labels."""
        if pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() / 1000.0
            if pos < 0:
                pos = 0

            delta = pos - self._last_pos
            if delta > 0:
                self.song_position += delta
            self._last_pos = pos

            self.song_position = min(self.song_position, self.song_length)

            self.window.progressSlider.setValue(int(self.song_position))
            self.window.elapsedLabel.setText(
                self.format_time(int(self.song_position)))

        elif not self.is_paused and self.current_index >= 0:
            # Song ended - play next
            self.next_song()

    def format_time(self, seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    # ==================== PLAYBACK METHODS ====================

    def play_song_by_name(self, song_name):
        """Play a single song by name (normal mode)."""
        file_path, name, artist, genre = self.get_song_file_path(song_name)

        if not file_path:
            QtWidgets.QMessageBox.warning(
                self.window, "Song Not Found",
                f"'{song_name}' was not found in the loaded songs.")
            return False

        # Switch to normal mode with all songs
        self.playback_mode = self.MODE_NORMAL
        self.current_playlist = self.all_songs.copy()

        # Find index of the song
        for i, (fp, sn, ar, ge) in enumerate(self.current_playlist):
            if sn.lower() == song_name.lower():
                self.stop()
                if self.load_song(i):
                    pygame.mixer.music.play()
                    self.is_paused = False
                    self.window.libraryBtn_2.setText("⏸️")
                    self.timer.start()
                return True

        return False

    def play_queue(self, queue_songs, on_end_callback=None):
        """
        Play songs from a queue.
        queue_songs: [[song_name, artist_name, genre, date], ...]
        """
        if not queue_songs:
            QtWidgets.QMessageBox.warning(self.window, "Empty Queue",
                                          "The queue is empty.")
            return False

        # Build playlist from queue
        playlist = []
        for song_data in queue_songs:
            song_name = song_data[0]
            file_path, name, artist, genre = self.get_song_file_path(song_name)
            if file_path:
                playlist.append((file_path, name, artist, genre))
            else:
                print(f"Queue song not found: {song_name}")

        if not playlist:
            QtWidgets.QMessageBox.warning(
                self.window, "No Playable Songs",
                "None of the songs in the queue could be found.")
            return False

        # Set queue mode
        self.playback_mode = self.MODE_QUEUE
        self.current_playlist = playlist
        self.on_queue_end_callback = on_end_callback

        # Start playing from beginning
        self.stop()
        if self.load_song(0):
            pygame.mixer.music.play()
            self.is_paused = False
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

            QtWidgets.QMessageBox.information(
                self.window, "Playing Queue",
                f"Playing {len(playlist)} songs from your queue.")
            return True

        return False

    def play_playlist(self,
                      playlist_songs,
                      playlist_name="Playlist",
                      on_end_callback=None):
        """
        Play songs from a playlist.
        playlist_songs: [[song_name, artist_name, genre], ...]
        """
        if not playlist_songs:
            QtWidgets.QMessageBox.warning(self.window, "Empty Playlist",
                                          "The playlist is empty.")
            return False

        # Build playlist
        playlist = []
        for song_data in playlist_songs:
            song_name = song_data[0]
            file_path, name, artist, genre = self.get_song_file_path(song_name)
            if file_path:
                playlist.append((file_path, name, artist, genre))
            else:
                print(f"Playlist song not found: {song_name}")

        if not playlist:
            QtWidgets.QMessageBox.warning(
                self.window, "No Playable Songs",
                "None of the songs in the playlist could be found.")
            return False

        # Set playlist mode
        self.playback_mode = self.MODE_PLAYLIST
        self.current_playlist = playlist
        self.on_queue_end_callback = on_end_callback

        # Start playing from beginning
        self.stop()
        if self.load_song(0):
            pygame.mixer.music.play()
            self.is_paused = False
            self.window.libraryBtn_2.setText("⏸️")
            self.timer.start()

            QtWidgets.QMessageBox.information(
                self.window, f"Playing:  {playlist_name}",
                f"Playing {len(playlist)} songs.")
            return True

        return False

    # ==================== FEEDBACK BUTTONS ====================

    def like_song(self):
        if self.current_song_name and self.current_song_name != "<No Song>":
            QtWidgets.QMessageBox.information(
                self.window, "Liked",
                f"You liked '{self.current_song_name}'!  👍")
        else:
            QtWidgets.QMessageBox.warning(self.window, "No Song",
                                          "No song is currently playing.")

    def dislike_song(self):
        if self.current_song_name and self.current_song_name != "<No Song>":
            QtWidgets.QMessageBox.information(
                self.window, "Disliked",
                f"You disliked '{self.current_song_name}'.  👎\nWe'll play similar songs less often."
            )
        else:
            QtWidgets.QMessageBox.warning(self.window, "No Song",
                                          "No song is currently playing.")

    def report_song(self):
        if not self.current_song_name or self.current_song_name == "<No Song>":
            QtWidgets.QMessageBox.warning(self.window, "No Song",
                                          "No song is currently playing.")
            return

        reasons = [
            "Inappropriate Content", "Copyright Violation",
            "Audio Quality Issues", "Hate Speech", "Violence", "Other"
        ]

        reason, ok = QtWidgets.QInputDialog.getItem(
            self.window, "Report Song",
            f"Report '{self.current_song_name}'?\n\nSelect reason:", reasons,
            0, False)

        if ok and reason:
            QtWidgets.QMessageBox.information(
                self.window, "Report Submitted",
                f"Thank you for reporting '{self.current_song_name}'.\nReason: {reason}"
            )

    def cleanup(self):
        """Clean up resources when closing."""
        self.timer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
