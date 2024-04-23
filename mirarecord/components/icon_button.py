from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtCore import Qt, pyqtSignal

class IconButton(QWidget):
    clicked = pyqtSignal()

    default_style = 'background-color: transparent; border: none; border-radius: 20px;'
    hover_style = 'background-color: rgb(40,40,40); border: none; border-radius: 20px;'
    active_style = 'background-color: rgb(21,21,21); border: none; border-radius: 20px;'
    hover_active_style = 'background-color: rgb(12,12,12); border: none; border-radius: 20px;'

    def __init__(
        self,
        icon_path: str,
        text: str = '',
        icon_size: int = 40,
        is_active: bool = False
    ):
        super().__init__()
        self.is_active = is_active

        # Set icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_icon(icon_path, icon_size)

        # Set text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet('color: white;')

        icon_text_layout = QVBoxLayout()
        icon_text_layout.addWidget(self.icon_label)
        icon_text_layout.addWidget(self.text_label)
        icon_text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_text_layout.setSpacing(10)

        container_widget = QWidget()
        container_widget.setLayout(icon_text_layout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(container_widget)
        self.setLayout(self.layout)

        if self.is_active:
            self.setStyleSheet('background-color: rgb(21,21,21); border: none; border-radius: 20px;')
        else:
            self.setStyleSheet('background-color: transparent; border: none; border-radius: 20px;')
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_icon(self, icon_path: str, icon_size: int):
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(icon_size, icon_size)

        pixmap = pixmap.scaled(icon_size, icon_size, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                               transformMode=Qt.TransformationMode.SmoothTransformation)

        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet('background-color: transparent')

    def deactivate(self):
        self.is_active = False
        self.setStyleSheet(IconButton.default_style)

    def activate(self):
        self.is_active = True

    def mousePressEvent(self, event):
        self.activate()
        self.setStyleSheet(IconButton.active_style)
        self.clicked.emit()
        event.accept()

    def enterEvent(self, event):
        if self.is_active:
            self.setStyleSheet(IconButton.hover_active_style)
        else:
            self.setStyleSheet(IconButton.hover_style)
        event.accept()

    def leaveEvent(self, event):
        if self.is_active:
            self.setStyleSheet(IconButton.active_style)
        else:
            self.setStyleSheet(IconButton.default_style)
        event.accept()
