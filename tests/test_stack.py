import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt

class StackedWidgetExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False
        self.offset = None

    def initUI(self):
        # Tạo widget 1 (nền)
        widget1 = QLabel("Widget 1", parent=self)
        widget1.setStyleSheet("background-color: red; border: 2px solid black; padding: 20px;")
        widget1.setFixedSize(800, 800)

        # Tạo widget 2 (hiển thị trên cùng)
        self.widget2 = QLabel("Widget 2", parent=self)
        self.widget2.setStyleSheet("background-color: green; border: 2px solid black; padding: 20px;")
        self.widget2.setFixedSize(10, 800)
        self.widget2.move(100, 100)

        self.setWindowTitle("StackedWidget Example")
        self.setGeometry(100, 100, 900, 800)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.widget2.geometry().contains(event.pos()):
                self.dragging = True
                self.offset = event.pos() - self.widget2.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.widget2.move(event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.offset = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackedWidgetExample()
    window.show()
    sys.exit(app.exec())
