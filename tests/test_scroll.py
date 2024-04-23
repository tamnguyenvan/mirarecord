import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QScrollArea, QVBoxLayout

class ScrollAreaExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Horizontal Scroll Area Example')
        self.setGeometry(100, 100, 400, 200)

        # Tạo một QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # Luôn hiển thị thanh cuộn ngang
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Tạo một widget con để chứa nội dung cuộn
        content_widget = QWidget()

        # Tạo QVBoxLayout cho widget con
        self.content_layout = QVBoxLayout()

        # Thêm các nút vào widget con và đặt vị trí cho từng nút
        for i in range(50):
            print(i)
            button = QPushButton(f'Button {i+1}')
            self.content_layout.addWidget(button)
            button.setGeometry(10, (i * 30) + 10, 80, 25)  # Thiết lập vị trí và kích thước cho mỗi nút

        # Thiết lập kích thước của widget con
        content_widget.setLayout(self.content_layout)
        content_widget.setMinimumSize(400, 100)

        # Thiết lập widget con làm nội dung của QScrollArea
        scroll_area.setWidget(content_widget)

        # Đặt kích thước tối thiểu cho QScrollArea
        scroll_area.setMinimumSize(400, 100)

        # Đặt widget con vào layout chính
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        plus_button = QPushButton('+')
        plus_button.clicked.connect(self.on_click)
        main_layout.addWidget(plus_button)

        self.setLayout(main_layout)

    def on_click(self):
        ratio = 1.2

        for i in range(self.content_layout.count()):
            item = self.content_layout.itemAt(i)
            widget = item.widget()
            height = int(widget.height() * ratio)

            new_y = int(widget.y() * ratio)
            widget.setGeometry(widget.x(), new_y, widget.width(), height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec())
