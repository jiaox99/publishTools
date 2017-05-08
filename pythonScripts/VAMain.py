#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import VABase
import VAResource
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QVBoxLayout, QDialog
import VACommonPublishTool as PubTool


class VAToolBox(VABase.VABaseWindow):
    def __init__(self):
        super().__init__(None)
        self.v_box = QVBoxLayout()
        self.res_box = VAResource.VAResourceToolBox(self)
        self.init_qa_tool()
        self.init_designer_and_art_tool()
        self.init_other_tool()
        self.init_base()

    def init_base(self):
        self.setLayout(self.v_box)
        self.resize(300, 450)
        self.move(300, 300)
        self.setWindowTitle('VA 工具箱')

    def init_qa_tool(self):
        g_box = QGroupBox("For QA")
        g_v_box = QVBoxLayout()
        g_v_box.addWidget(QPushButton("修改发布配置"))
        g_v_box.addWidget(QPushButton("发布正式版本"))
        btn = QPushButton("发布功能测试版本")
        g_v_box.addWidget(btn)
        btn.clicked.connect(self.feature_test)
        g_box.setLayout(g_v_box)
        self.v_box.addWidget(g_box)

    def feature_test(self):
        pass

    def init_designer_and_art_tool(self):
        g_box = QGroupBox("For 策划 或 美术")
        g_v_box = QVBoxLayout()
        btn = QPushButton("修改资源")
        btn.clicked.connect(self.show_res_window)
        g_v_box.addWidget(btn)
        g_v_box.addWidget(QPushButton("更新 Lang"))
        g_v_box.addWidget(QPushButton("更新 CommonLang"))
        g_box.setLayout(g_v_box)
        self.v_box.addWidget(g_box)

    def init_other_tool(self):
        g_box = QGroupBox("其他")
        g_v_box = QVBoxLayout()
        g_v_box.addWidget(QPushButton("重新生成资源配置"))
        g_v_box.addWidget(QPushButton("本地游戏"))
        g_v_box.addWidget(QPushButton("本地游戏配置"))
        g_box.setLayout(g_v_box)
        self.v_box.addWidget(g_box)

    def show_res_window(self):
        self.res_box.show()

    def closeEvent(self, e):
        print("Closing")
        # e.ignore()
        sys.exit()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tool = VAToolBox()
    MAIN_WINDOW = tool
    tool.show()

    app.exec_()
