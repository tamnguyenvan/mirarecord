import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

import cv2

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.video_path = "/home/tamnv/Downloads/upwork-contract-exporter.mp4"
        self.video_capture = cv2.VideoCapture(self.video_path)
        self.frame_label = QLabel()
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_video)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_frame)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_frame)

        self.frame_index_input = QLineEdit()
        self.frame_index_input.setPlaceholderText("Enter frame index")
        self.frame_index_input.returnPressed.connect(self.go_to_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.frame_label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.frame_index_input)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setFixedSize(1024, 970)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.playing = False

    def next_frame(self):
        # if self.playing:
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
            self.frame_label.setPixmap(QPixmap.fromImage(image))

    def previous_frame(self):
        # if not self.playing:
        # Move back to the previous frame
        current_frame = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 2)  # Move back 2 frames (1 frame for current, 1 frame for previous)
        self.next_frame()

    def play_video(self):
        if not self.playing:
            self.timer.start(33)  # Update frame every 33 milliseconds (30 fps)
            self.playing = True

    def pause_video(self):
        if self.playing:
            self.timer.stop()
            self.playing = False

    def go_to_frame(self):
        frame_index = int(self.frame_index_input.text())
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        self.next_frame()

    def closeEvent(self, event):
        self.video_capture.release()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
