import os
import sys
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)else os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from app.main_interface import MainWindow

# 启用 DPI 缩放
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())