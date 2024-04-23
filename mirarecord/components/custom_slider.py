from PyQt6.QtCore import QUrl
from PyQt6.QtQuickWidgets import QQuickWidget


class CustomSlider(QQuickWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setSource(QUrl.fromLocalFile('/home/tamnv/Projects/exp/mirarecord/mirarecord/components/sources/custom_slider.qml'))