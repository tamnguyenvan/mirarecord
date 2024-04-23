from PyQt6.QtWidgets import QApplication, QPushButton, QWidget
from PyQt6.QtGui import QCursor


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton("Click me", self)
        self.button.setGeometry(100, 100, 200, 50)
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        relative_pos = self.button.mapFromGlobal(QCursor().pos())
        print("Relative position:", relative_pos.x(), relative_pos.y())


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()
