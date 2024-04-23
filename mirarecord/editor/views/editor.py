import cv2
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import (
    QMainWindow,
)
from PyQt6.QtGui import QImage, QPixmap
from mirarecord.components.custom_slider import CustomSlider
from mirarecord.utils.image import ImageUtils
from mirarecord.engine.mirarecord import VideoProcessor
from ..bloc.state import EditorState


class Editor(QMainWindow):
    def __init__(self, state: EditorState = EditorState()):
        super().__init__()
        self.state = state

        self.setup_ui()
        self.center()

        self.intit_state()
        self.video_processor = VideoProcessor(state.input_path)

        self.next_frame()

    def setup_ui(self):
        self.setObjectName("MiraRecord")

        self.setMinimumSize(QtCore.QSize(1420, 880))
        self.setStyleSheet("background-color: rgb(11, 13, 15);")
        self.central_widget = QtWidgets.QWidget(parent=self)
        self.central_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.central_widget.setObjectName("central_widget")

        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout_2.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_2.setSpacing(0)
        self.vertical_layout_2.setObjectName("vertical_layout_2")

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("vertical_layout")

        # Top layout (video preview + settings)
        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_layout.setContentsMargins(20, 20, 20, 20)
        self.top_layout.setSpacing(0)
        self.top_layout.setObjectName("top_layout")

        # Video preview layout
        self.display_layout = QtWidgets.QVBoxLayout()
        self.display_layout.setSpacing(0)
        self.display_layout.setObjectName("display_layout")
        self.video_label = QtWidgets.QLabel(parent=self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_label.sizePolicy().hasHeightForWidth())
        self.video_label.setSizePolicy(sizePolicy)
        self.video_label.setObjectName("video_label")
        self.display_layout.addWidget(self.video_label)

        self.horizontal_layout_4 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_4.setObjectName("horizontal_layout_4")
        self.horizontal_widget_5 = QtWidgets.QWidget(parent=self.central_widget)
        self.horizontal_widget_5.setObjectName("horizontal_widget_5")
        self.horizontal_layout_6 = QtWidgets.QHBoxLayout(self.horizontal_widget_5)
        self.horizontal_layout_6.setObjectName("horizontal_layout_6")
        self.horizontal_layout_8 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_8.setSpacing(30)
        self.horizontal_layout_8.setObjectName("horizontal_layout_8")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_8.addItem(spacerItem)

        # Tool bar
        self.crop_button = QtWidgets.QPushButton(parent=self.horizontal_widget_5)
        self.crop_button.setStyleSheet("background-color: transparent;\n"
"border: none;")
        self.crop_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ImageUtils.asset('crop.png')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.crop_button.setIcon(icon)
        self.crop_button.setIconSize(QtCore.QSize(20, 20))
        self.crop_button.setObjectName("crop_button")
        self.horizontal_layout_8.addWidget(self.crop_button)
        self.cut_button = QtWidgets.QPushButton(parent=self.horizontal_widget_5)
        self.cut_button.setStyleSheet("background-color: transparent;\n"
"border: none;")
        self.cut_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(ImageUtils.asset('cut.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.cut_button.setIcon(icon1)
        self.cut_button.setIconSize(QtCore.QSize(20, 20))
        self.cut_button.setObjectName("cut_button")
        self.horizontal_layout_8.addWidget(self.cut_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_8.addItem(spacerItem1)
        self.horizontal_layout_6.addLayout(self.horizontal_layout_8)

        self.horizontal_layout_4.addWidget(self.horizontal_widget_5)
        self.horizontalWidget_4 = QtWidgets.QWidget(parent=self.central_widget)
        self.horizontalWidget_4.setObjectName("horizontalWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalWidget_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontal_layout_7 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_7.setObjectName("horizontalLayout_7")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_7.addItem(spacerItem2)
        self.horizontal_layout_9 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_9.setSpacing(30)
        self.horizontal_layout_9.setObjectName("horizontalLayout_9")

        self.prev_button = QtWidgets.QPushButton(parent=self.horizontalWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prev_button.sizePolicy().hasHeightForWidth())
        self.prev_button.setSizePolicy(sizePolicy)
        self.prev_button.setStyleSheet("background-color: transparent;\n"
"border: none;")
        self.prev_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(ImageUtils.asset('previous.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.prev_button.setIcon(icon2)
        self.prev_button.setIconSize(QtCore.QSize(20, 20))
        self.prev_button.setObjectName("prev_button")
        self.horizontal_layout_9.addWidget(self.prev_button)

        self.play_button = QtWidgets.QPushButton(parent=self.horizontalWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play_button.sizePolicy().hasHeightForWidth())
        self.play_button.setSizePolicy(sizePolicy)
        self.play_button.setStyleSheet("background-color: transparent;\n"
"border: none;")
        self.play_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(ImageUtils.asset('play.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.play_button.setIcon(icon3)
        self.play_button.setIconSize(QtCore.QSize(20, 20))
        self.play_button.setObjectName("play_button")
        self.horizontal_layout_9.addWidget(self.play_button)

        self.next_button = QtWidgets.QPushButton(parent=self.horizontalWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setStyleSheet("background-color: transparent;\n"
"border: none;")
        self.next_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(ImageUtils.asset('next.svg')), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.next_button.setIcon(icon4)
        self.next_button.setIconSize(QtCore.QSize(20, 20))
        self.next_button.setObjectName("next_button")
        self.horizontal_layout_9.addWidget(self.next_button)

        self.horizontal_layout_7.addLayout(self.horizontal_layout_9)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontal_layout_7.addItem(spacerItem3)
        self.horizontal_layout_7.setStretch(0, 1)
        self.horizontal_layout_7.setStretch(1, 2)
        self.horizontal_layout_7.setStretch(2, 3)
        self.horizontalLayout_5.addLayout(self.horizontal_layout_7)
        self.horizontal_layout_4.addWidget(self.horizontalWidget_4)
        self.horizontal_layout_4.setStretch(0, 1)
        self.horizontal_layout_4.setStretch(1, 3)
        self.display_layout.addLayout(self.horizontal_layout_4)
        self.display_layout.setStretch(0, 9)
        self.display_layout.setStretch(1, 1)
        self.top_layout.addLayout(self.display_layout)

        # Sidebar
        self.sidebar_layout = QtWidgets.QVBoxLayout()
        self.sidebar_layout.setSpacing(0)
        self.sidebar_layout.setObjectName("sidebar_layout")
        self.widget = QtWidgets.QWidget(parent=self.central_widget)
        self.widget.setStyleSheet("background-color: rgb(19, 21, 25); border-radius: 20px;")
        self.widget.setObjectName("widget")
        self.vertical_layout_6 = QtWidgets.QVBoxLayout(self.widget)
        self.vertical_layout_6.setContentsMargins(16, 16, 16, 16)
        self.vertical_layout_6.setObjectName("vertical_layout_6")
        self.vertical_layout_4 = QtWidgets.QVBoxLayout()
        self.vertical_layout_4.setObjectName("vertical_layout_4")
        self.vertical_layout_7 = QtWidgets.QVBoxLayout()
        self.vertical_layout_7.setObjectName("vertical_layout_7")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setStyleSheet("color: rgb(110,110,110);")
        self.label_2.setObjectName("label_2")
        self.vertical_layout_7.addWidget(self.label_2)
        self.scroll_area_2 = QtWidgets.QScrollArea(parent=self.widget)
        self.scroll_area_2.setWidgetResizable(True)
        self.scroll_area_2.setObjectName("scrollArea_2")
        self.scroll_area_widget_contents_3 = QtWidgets.QWidget()
        self.scroll_area_widget_contents_3.setGeometry(QtCore.QRect(0, 0, 409, 485))
        self.scroll_area_widget_contents_3.setObjectName("scroll_area_widget_contents_3")
        self.scroll_area_2.setWidget(self.scroll_area_widget_contents_3)
        self.vertical_layout_7.addWidget(self.scroll_area_2)
        self.vertical_layout_7.setStretch(0, 1)
        self.vertical_layout_7.setStretch(1, 9)
        self.vertical_layout_4.addLayout(self.vertical_layout_7)
        self.vertical_layout_6.addLayout(self.vertical_layout_4)
        self.vertical_layout_9 = QtWidgets.QVBoxLayout()
        self.vertical_layout_9.setContentsMargins(16, 16, 16, 16)
        self.vertical_layout_9.setObjectName("vertical_layout_9")
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setStyleSheet("color: rgb(110,110,110);")
        self.label_3.setObjectName("label_3")
        self.vertical_layout_9.addWidget(self.label_3)
        self.horizontal_slider = CustomSlider(parent=self.widget)

        self.vertical_layout_9.addWidget(self.horizontal_slider)
        self.vertical_layout_6.addLayout(self.vertical_layout_9)
        self.sidebar_layout.addWidget(self.widget)
        self.top_layout.addLayout(self.sidebar_layout)
        self.top_layout.setStretch(0, 7)
        self.top_layout.setStretch(1, 3)
        self.vertical_layout.addLayout(self.top_layout)

        # Bottom layout (tracks)
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout.setContentsMargins(20, 20, 20, 20)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setObjectName("bottom_layout")
        self.scroll_area = QtWidgets.QScrollArea(parent=self.central_widget)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 1489, 259))
        self.scroll_area_widget_contents.setStyleSheet("border: none;")
        self.scroll_area_widget_contents.setObjectName("scrollAreaWidgetContents")
        self.vertical_layout_5 = QtWidgets.QVBoxLayout(self.scroll_area_widget_contents)
        self.vertical_layout_5.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_5.setSpacing(0)
        self.vertical_layout_5.setObjectName("vertical_layout_5")
        self.vertical_layout_3 = QtWidgets.QVBoxLayout()
        self.vertical_layout_3.setSpacing(20)
        self.vertical_layout_3.setObjectName("vertical_layout_3")
        self.label = QtWidgets.QLabel(parent=self.scroll_area_widget_contents)
        self.label.setObjectName("label")
        self.vertical_layout_3.addWidget(self.label)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setStyleSheet("background: rgb(67, 41, 244); border-radius: 20px;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.vertical_layout_3.addWidget(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setStyleSheet("background: rgb(134, 90, 14); border-radius: 20px;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.vertical_layout_3.addWidget(self.pushButton_7)
        self.vertical_layout_3.setStretch(0, 1)
        self.vertical_layout_3.setStretch(1, 1)
        self.vertical_layout_3.setStretch(2, 1)
        self.vertical_layout_5.addLayout(self.vertical_layout_3)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.bottom_layout.addWidget(self.scroll_area)
        self.vertical_layout.addLayout(self.bottom_layout)
        self.vertical_layout.setStretch(0, 7)
        self.vertical_layout.setStretch(1, 3)
        self.vertical_layout_2.addLayout(self.vertical_layout)
        self.setCentralWidget(self.central_widget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MiraRecord", "MiraRecord"))
        self.video_label.setText(_translate("MiraRecord", "TextLabel"))
        self.label_2.setText(_translate("MiraRecord", "Background"))
        self.label_3.setText(_translate("MiraRecord", "Background blur"))
        self.label.setText(_translate("MiraRecord", "TextLabel"))
        self.pushButton_6.setText(_translate("MiraRecord", "PushButton"))
        self.pushButton_7.setText(_translate("MiraRecord", "PushButton"))

    def center(self):
        # Get the geometry of the screen
        screen_geometry = self.screen().availableGeometry()

        # Get the geometry of the main window
        window_geometry = self.frameGeometry()

        # Calculate the x-coordinate for centering the window horizontally
        x_coordinate = int(
            (screen_geometry.width() - window_geometry.width()) / 2)

        # Calculate the y-coordinate for positioning the window 100 pixels above the bottom edge
        y_coordinate = int(screen_geometry.height() - 80 - window_geometry.height())

        # Move the window to the calculated position
        self.move(x_coordinate, y_coordinate)

    def intit_state(self):
        self.video_capture = cv2.VideoCapture(self.state.input_path)
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.state.is_video_playing = False

        self.play_button.clicked.connect(self.play_video)
        # self.pause_button.clicked.connect(self.pause_video)
        self.next_button.clicked.connect(self.next_frame)
        self.prev_button.clicked.connect(self.previous_frame)

    def next_frame(self):
        q_image = self.video_processor.get()

        # image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)

        # Scale the image to fit the video_label while maintaining aspect ratio
        if q_image is not None:
            scaled_image = q_image.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            # Draw the scaled image on video_label
            pixmap = QPixmap.fromImage(scaled_image)
            self.video_label.setPixmap(pixmap)
            self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def previous_frame(self):
        # Move back to the previous frame
        current_frame = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 2)  # Move back 2 frames (1 frame for current, 1 frame for previous)
        # self.next_frame()

    def play_video(self):
        if not self.state.is_video_playing:
            self.timer.start(33)  # Update frame every 33 milliseconds (30 fps)
            self.state.is_video_playing = True

    def pause_video(self):
        if self.state.is_video_playing:
            self.timer.stop()
            self.state.is_video_playing = False

    def closeEvent(self, event):
        self.video_capture.release()
        super().closeEvent(event)