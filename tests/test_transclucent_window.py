import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Thiết lập thuộc tính cửa sổ
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Tạo widget chính
        central_widget = QWidget()
        central_widget.setAutoFillBackground(True)
        central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

        # Tạo widget con
        inner_widget = QLabel("Hello")
        inner_widget.setStyleSheet("background-color: rgb(21,21,21); border: none; border-radius: 20px;")
        inner_widget.setFixedSize(100, 100)

        # Sắp xếp widget chính và widget con
        layout = QVBoxLayout(central_widget)
        layout.addWidget(inner_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.setGeometry(100, 100, 400, 200)  # Đặt kích thước và vị trí cửa sổ
    window.show()
    sys.exit(app.exec())
