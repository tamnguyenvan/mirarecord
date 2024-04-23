from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import QTimer, Qt
import sys


class Tray(QMainWindow):
    def __init__(self):
        super().__init__()
        self.elapsed_time = 0

        # Create tray icon
        self.tray_icon = QSystemTrayIcon()
        # self.tray_icon.setIcon(QIcon(self.create_tray_icon()))
        self.tray_icon.setIcon(QIcon('/home/tamnv/Projects/exp/mirarecord/assets/stop.png'))
        self.tray_icon.setToolTip("Elapsed Time: 0 seconds")
        self.tray_icon.show()

        # # Timer to update the tray icon
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_tray_icon)
        # self.timer.start(1000)  # Update every second

    def create_tray_icon(self):
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.red)  # Background color

        painter = QPainter(pixmap)
        # Draw rounded rectangle for elapsed time
        elapsed_width = min(100, self.elapsed_time)
        painter.setBrush(Qt.GlobalColor.red)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, elapsed_width, 16, 5, 5)

        # Draw square for remaining time
        remaining_width = max(0, 100 - elapsed_width)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawRoundedRect(elapsed_width, 0, remaining_width, 16, 0, 0)

        painter.end()

        return pixmap

    def update_tray_icon(self):
        self.elapsed_time += 10  # Increment elapsed time (for demo purpose)
        self.tray_icon.setIcon(QIcon(self.create_tray_icon()))
        self.tray_icon.setToolTip(f"Elapsed Time: {self.elapsed_time / 1000} seconds")


def main():
    app = QApplication(sys.argv)
    tray = Tray()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
