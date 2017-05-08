import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt5 import Qt
import VABase


class VAResourceToolBox(VABase.VABaseWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowFlags(Qt.Qt.Widget)
        self.init_ui()
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        group = QGroupBox("已识别")
        h_box.addWidget(group)
        btn = QPushButton("将资源拖到这里")
        h_box.addWidget(btn)
        group = QGroupBox("未识别")
        h_box.addWidget(group)
        v_box.addLayout(h_box)

        h_box = QHBoxLayout()
        btn = QPushButton("确认")
        h_box.addStretch(1)
        h_box.addWidget(btn)
        h_box.addStretch(1)
        v_box.addLayout(h_box)
        self.setLayout(v_box)
        # self.setAcceptDrops(True)

    def init_ui(self):
        self.resize(300, 400)
        self.move(300, 300)
        self.setWindowTitle('VA 资源工具箱')

    def dragEnterEvent(self, drag_event):
        print("Handling drag enter")
        print(drag_event.mimeData().urls())
        print(drag_event.mimeData().text())
        drag_event.accept()

    def dropEvent(self, drop_event):
        print("Handling drop event")
        print(drop_event.mimeData())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    box = VAResourceToolBox()
    box.show()

    app.exec_()
