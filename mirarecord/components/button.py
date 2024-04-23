from typing import Tuple
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, icon_path: str, icon_size: Tuple[int] = (60, 60)):
        super().__init__()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        style = '''
            QPushButton {
                background-color: transparent;
                border: none;
            }
        '''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(*icon_size))
        self.setStyleSheet(style)
