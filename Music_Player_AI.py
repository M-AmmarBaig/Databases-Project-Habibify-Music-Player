import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Music Player")

        self.player = QMediaPlayer()

        # Play button
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_song)

        # Slider (seek bar)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.play_btn)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        # Connect signals
        self.player.positionChanged.connect(self.slider.setValue)
        self.player.durationChanged.connect(self.slider.setRange)

    def play_song(self):
        url = QUrl.fromLocalFile("song.mp3")
        self.player.setMedia(QMediaContent(url))
        self.player.play()

    def set_position(self, position):
        self.player.setPosition(position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MusicPlayer()
    win.show()
    sys.exit(app.exec_())
