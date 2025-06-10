from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from qfluentwidgets import ScrollArea
from qfluentwidgets import FluentIcon as FIF
from .common.style_sheet import StyleSheet
from task.handler.config_handler import config_handler

class FunctionInterface(ScrollArea):
    # 初始化
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.stackedWidget = QStackedWidget(self)
        self.settingLabel = QLabel("功能", self)
        self.__initWidget()
        self.addCard()

    # 初始化界面
    def __initWidget(self):
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 140, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setObjectName("functionInterface")
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)
    
    def addCard(self):
        self