import sys
import os
from PyQt5 import QtWidgets, uic, QtCore
import pygame
from mutagen.mp3 import MP3  # To get exact song length

class MP3Player(QtWidgets.QMainWindow):
    def __init__(self):
        super(MP3Player, self).__init__()
        uic.loadUi("media_player.ui", self)

        pygame.mixer.init()

        self.songs = []
        self.current_index = -1
        self.is_paused = False
        self.song_length = 0  # in seconds
        self.song_position = 0  # in seconds, manually track slider

        self.playPauseBtn.clicked.connect(self.play_pause)
        self.nextBtn.clicked.connect(self.next_song)
        self.prevBtn.clicked.connect(self.prev_song)
        self.forwardBtn.clicked.connect(self.skip_forward)
        self.rewindBtn.clicked.connect(self.skip_back)
        self.volumeSlider.valueChanged.connect(self.set_volume)
        self.progressSlider.sliderReleased.connect(self.set_position)

        self.load_songs("songs")

        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_slider)
        self.timer.start()

        self.volumeSlider.setValue(70)
        pygame.mixer.music.set_volume(0.7)

    def load_songs(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.songs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
        if self.songs:
            self.current_index = 0
            self.load_song()

    def load_song(self):
        song_path = self.songs[self.current_index]
        pygame.mixer.music.load(song_path)
        self.songLabel.setText(os.path.basename(song_path))

        audio = MP3(song_path)
        self.song_length = int(audio.info.length)
        self.progressSlider.setMaximum(self.song_length)
        self.song_position = 0
        self.progressSlider.setValue(0)
        self.elapsedLabel.setText("00:00")
        self.durationLabel.setText(self.format_time(self.song_length))

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{int(mins):02d}:{int(secs):02d}"

    def play_pause(self):
        if not self.songs:
            return
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.playPauseBtn.setText("▶️")
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play(start=self.song_position)
            self.is_paused = False
            self.playPauseBtn.setText("⏸️")

    def next_song(self):
        if not self.songs:
            return
        self.current_index = (self.current_index + 1) % len(self.songs)
        self.load_song()
        pygame.mixer.music.play()
        self.playPauseBtn.setText("⏸️")

    def prev_song(self):
        if not self.songs:
            return
        self.current_index = (self.current_index - 1) % len(self.songs)
        self.load_song()
        pygame.mixer.music.play()
        self.playPauseBtn.setText("⏸️")

    def skip_forward(self):
        if not self.songs:
            return
        self.song_position = min(self.song_position + 5, self.song_length)
        pygame.mixer.music.play(start=self.song_position)
        self.playPauseBtn.setText("⏸️")

    def skip_back(self):
        if not self.songs:
            return
        self.song_position = max(self.song_position - 5, 0)
        pygame.mixer.music.play(start=self.song_position)
        self.playPauseBtn.setText("⏸️")

    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100)

    def update_slider(self):
        if pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() / 1000
            if pos < 0: pos = 0

            self.song_position += pos - getattr(self, '_last_pos', 0)
            self._last_pos = pos
            self.song_position = min(self.song_position, self.song_length)
            self.progressSlider.setValue(int(self.song_position))
            self.elapsedLabel.setText(self.format_time(int(self.song_position)))
        elif not self.is_paused:
            # Song ended
            self.next_song()
            self.song_position = 0
            self._last_pos = 0

    def set_position(self):
        val = self.progressSlider.value()
        self.song_position = val
        pygame.mixer.music.play(start=self.song_position)
        self.playPauseBtn.setText("⏸️")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = MP3Player()
    player.show()
    sys.exit(app.exec_())
