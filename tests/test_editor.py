import sys
sys.path.insert(0, '..')
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.editor import Ui_MainWindow

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Tạo một đối tượng giao diện từ Ui_MainWindow
        self.ui = Ui_MainWindow()

        # Khởi tạo giao diện của main window
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()

    window.show()
    sys.exit(app.exec())