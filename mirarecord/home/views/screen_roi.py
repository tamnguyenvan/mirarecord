from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt


class ScreenRoI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        # Set window flags to remove title bar and make it frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setWindowOpacity(0.1)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create a frame
        self.frame = QFrame(self)
        self.frame.setStyleSheet("border: 2px solid white; background-color: transparent;")

        # Create a layout
        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the layout to the frame
        self.frame.setLayout(layout)

        # Add the frame to the main window
        self.setCentralWidget(self.frame)