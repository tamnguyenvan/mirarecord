from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtCore import QCoreApplication

from mirarecord.editor import Editor
from mirarecord.editor.bloc.state import EditorState
from mirarecord.utils.image import ImageUtils
from mirarecord.engine.mirarecord import MiraRecorder


class Tray(QSystemTrayIcon):
    def __init__(self, parent=None, recorder: MiraRecorder = None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.recorder = recorder

    def setup_ui(self):
        tray_menu = QMenu()
        open_action = tray_menu.addAction('Stop & Open studio')
        open_action.triggered.connect(self.open_editor)
        tray_menu.addAction(open_action)

        close_action = tray_menu.addAction('Exit')
        close_action.triggered.connect(self.on_close)
        tray_menu.addAction(close_action)

        self.setContextMenu(tray_menu)
        self.setIcon(QIcon(ImageUtils.asset('stop.png')))

    def open_editor(self):
        self.hide()
        input_path = self.recorder.stop()

        state = EditorState(input_path=input_path)
        self.editor = Editor(state=state)
        self.editor.show()

    def on_close(self):
        if self.parent:
            self.parent.close()
        self.recorder.stop()
        self.recorder.clean()
        QCoreApplication.quit()