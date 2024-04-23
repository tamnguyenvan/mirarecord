
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal


class IconButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, icon_path: str, text: str = '', icon_size: int = 36, is_expanding: bool = False):
        super().__init__()

        # Set icon
        self.icon_label = QLabel()
        self.set_icon(icon_path, icon_size)

        # Set text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet('color: black;')

        layout = QVBoxLayout()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

        if is_expanding:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        else:
            self.setFixedSize(self.minimumSizeHint())

    def set_icon(self, icon_path: str, icon_size: int):
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(icon_size, icon_size)  # Set maximum size
        if pixmap.width() > 0.7 * icon_size:
            pixmap = pixmap.scaledToWidth(int(0.7 * icon_size))
        if pixmap.height() > 0.7 * icon_size:
            pixmap = pixmap.scaledToHeight(int(0.7 * icon_size))

        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet('background-color: transparent')

    def set_text(self, text: str):
        self.text_label.setText(text)

    def mousePressEvent(self, event):
        self.clicked.emit()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Icon Button Example")
        self.setGeometry(100, 100, 400, 200)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        icon_button = IconButton("/home/tamnv/Projects/exp/mirarecord/assets/screen.png", "Click me!", icon_size=64, is_expanding=True)
        main_layout.addWidget(icon_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
