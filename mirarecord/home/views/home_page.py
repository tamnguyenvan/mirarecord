from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy,
)
from PyQt6.QtWidgets import QMainWindow

from mirarecord.components.icon_button import IconButton
from mirarecord.components.button import Button
from mirarecord.tray import Tray
from mirarecord.utils.image import ImageUtils

from .screen_roi import ScreenRoI
from mirarecord.engine.mirarecord import MiraRecorder


WINDOW_WIDTH, WINDOW_HEIGHT = 340, 220
BORDER_RADIUS = 30


class HomePage(QMainWindow):
    default_style = 'background-color: rgb(29,29,29); border: 2px solid rgb(80,80,80); border-radius: 40px;'

    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.tray = None

    def setup_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # set fix size
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Create central widget
        self.central_widget = QWidget()
        self.central_widget.setAutoFillBackground(True)
        self.central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

        self.rounded_widget = QWidget()
        self.rounded_widget.setStyleSheet(HomePage.default_style)
        self.vertical_layout_1 = QVBoxLayout()
        self.rounded_widget.setLayout(self.vertical_layout_1)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.rounded_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setup_selection_row()
        self.setup_action_row()

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.center()

        self.roi = ScreenRoI()
        self.roi.showFullScreen()

    def setup_selection_row(self):
        # Create selection layout
        self.horizontal_layout_1 = QHBoxLayout()

        # Create custom selection button
        self.custom_selection_btn = IconButton(text='Selection', icon_path=ImageUtils.asset('custom.png'))
        self.custom_selection_btn.clicked.connect(self.on_custom_selection_click)

        self.horizontal_layout_1.addWidget(self.custom_selection_btn)

        # Create screen selection button
        self.screen_selection_btn = IconButton(text='Screen', icon_path=ImageUtils.asset('screen.png'), is_active=True)
        self.screen_selection_btn.clicked.connect(self.on_screen_selection_click)
        self.horizontal_layout_1.addWidget(self.screen_selection_btn)

        # Create window selection button
        self.window_selection_btn = IconButton(text='Window', icon_path=ImageUtils.asset('window.png'))
        self.window_selection_btn.clicked.connect(self.on_window_selection_click)
        self.horizontal_layout_1.addWidget(self.window_selection_btn)

        # Add horizontal layout to vertical layout
        self.vertical_layout_1.addLayout(self.horizontal_layout_1)

    def setup_action_row(self):
        self.horizontal_layout_2 = QHBoxLayout()
        self.vertical_layout_1.addLayout(self.horizontal_layout_2)

        self.horizontal_layout_3 = QHBoxLayout()
        self.horizontal_layout_2.addLayout(self.horizontal_layout_3)

        self.horizontal_layout_4 = QHBoxLayout()
        self.horizontal_layout_2.addLayout(self.horizontal_layout_4)

        spacer_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontal_layout_3.addItem(spacer_item)
        self.record_button = Button(ImageUtils.asset('record.png'))
        self.record_button.clicked.connect(self.on_record_click)
        size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.record_button.sizePolicy().hasHeightForWidth())
        self.record_button.setSizePolicy(size_policy)

        self.horizontal_layout_3.addWidget(self.record_button)

        spacer_item_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontal_layout_4.addItem(spacer_item_1)

        spacer_item_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontal_layout_4.addItem(spacer_item_2)

        self.horizontal_layout_3.setStretch(0, 1)
        self.horizontal_layout_3.setStretch(1, 1)

        self.horizontal_layout_4.setStretch(0, 4)
        self.horizontal_layout_4.setStretch(1, 3)

        self.horizontal_layout_2.setStretch(0, 2)
        self.horizontal_layout_2.setStretch(1, 1)

    def on_custom_selection_click(self):
        self.screen_selection_btn.deactivate()
        self.window_selection_btn.deactivate()
        self.custom_selection_btn.activate()

    def on_screen_selection_click(self):
        self.screen_selection_btn.activate()
        self.window_selection_btn.deactivate()
        self.custom_selection_btn.deactivate()

    def on_window_selection_click(self):
        self.screen_selection_btn.deactivate()
        self.window_selection_btn.activate()
        self.custom_selection_btn.deactivate()

    def on_record_click(self):
        # Create tray icon
        if not self.tray:
            recorder = MiraRecorder()
            self.tray = Tray(self, recorder=recorder)

            # Start recording
            recorder.record()

        self.tray.show()
        self.hide()
        self.roi.hide()

    def center(self):
        # Get the geometry of the screen
        screen_geometry = self.screen().availableGeometry()

        # Get the geometry of the main window
        window_geometry = self.frameGeometry()

        # Calculate the x-coordinate for centering the window horizontally
        x_coordinate = int(
            (screen_geometry.width() - window_geometry.width()) / 2)

        # Calculate the y-coordinate for positioning the window 100 pixels above the bottom edge
        y_coordinate = int(screen_geometry.height() -
                           80 - window_geometry.height())

        # Move the window to the calculated position
        self.move(x_coordinate, y_coordinate)

    def closeEvent(self, event):
        self.roi.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()