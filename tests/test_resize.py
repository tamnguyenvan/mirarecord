import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QCursor


class ResizableButton(QPushButton):
    def __init__(self, text, min_height: int = 100):
        super().__init__(text)
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)
        self.setMinimumHeight(min_height)
        self.setMouseTracking(True)
        self.is_resizing_left = False
        self.is_resizing_right = False
        self.is_moving = False
        self.start_pos = QPoint(0, 0)
        self.start_width = 0
        self.start_x = 0

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            x_pos = event.position().x()
            if x_pos <= 5:
                self.is_resizing_left = True
            elif self.width() - x_pos <= 5:
                self.is_resizing_right = True
            else:
                self.is_moving = True

            self.start_pos = QCursor().pos()
            self.start_width = self.width()
            self.start_x = self.x()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing_left or self.is_resizing_right:
            current_pos = QCursor().pos()
            delta = current_pos - self.start_pos
            if self.is_resizing_left:
                new_width = max(5, self.start_width - delta.x())
            else:
                new_width = max(5, self.start_width + delta.x())

            if self.is_resizing_left:
                new_x = current_pos.x()
            else:
                new_x = current_pos.x() - new_width
            self.setFixedSize(new_width, self.height())
            self.move(new_x, self.y())
            # self.setGeometry(new_x, self.y(), new_width, self.height())
        elif self.is_moving:
            delta = QCursor().pos() - self.start_pos
            new_x = self.start_x + delta.x()
            self.move(new_x, self.y())
        else:
            if event.buttons() == Qt.MouseButton.NoButton:
                x_pos = event.position().x()
                if x_pos <= 5 or self.width() - x_pos <= 5:
                    self.setCursor(Qt.CursorShape.SizeHorCursor)
                else:
                    self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_resizing_left = False
            self.is_resizing_right = False
            self.is_moving = False
        super().mouseReleaseEvent(event)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        tool_layout = QHBoxLayout()
        layout.addLayout(tool_layout)

        minus_button = QPushButton('-')
        plus_button = QPushButton('+')
        tool_layout.addWidget(minus_button)
        tool_layout.addWidget(plus_button)

        self.track_layout = QHBoxLayout()

        for i in range(50):
            button = ResizableButton(f'Button {i}')
            button.setFixedSize(100, 100)
            self.track_layout.addWidget(button)
            self.track_layout.addSpacing(100)

        content_widget = QWidget()
        content_widget.setLayout(self.track_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(content_widget)
        # self.scroll_area.setMinimumSize(400, 100)
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        layout.addWidget(self.scroll_area)

        self.setLayout(layout)
        self.setGeometry(800, 100, 800, 600)
        self.setWindowTitle('Resizable Widget')

        minus_button.clicked.connect(lambda: self.scale_buttons(0.8))
        plus_button.clicked.connect(lambda: self.scale_buttons(1.2))

    def scale_buttons(self, ratio):
        most_right = 0
        for i in range(self.track_layout.count()):
            item = self.track_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    width = int(widget.width() * ratio)
                    new_x = int(widget.x() * ratio)

                    # widget.setGeometry(new_x, widget.y(), width, widget.height())
                    widget.setFixedSize(width, widget.height())
                    widget.move(new_x, widget.y())
                    most_right = widget.x() + width

        print(most_right)
        self.update_content_widget_size(most_right)

    def update_content_widget_size(self, most_right):
        content_widget = self.scroll_area.widget()
        content_widget.setMinimumSize(most_right, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
