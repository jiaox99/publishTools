from PyQt5.QtWidgets import QWidget
import PyQt5.Qt as Qt


class VABaseWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(Qt.Qt.WindowTitleHint | Qt.Qt.WindowCloseButtonHint)

    def closeEvent(self, event):
        if self.main_window:
            self.main_window.show()

    def show(self):
        if self.main_window:
            self.main_window.hide()
        super().show()


if __name__ == "__main__":
    pass

