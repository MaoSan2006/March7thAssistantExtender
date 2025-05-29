from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QStackedWidget, QSpacerItem, QScrollArea, QSizePolicy
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import SettingCardGroup, PushSettingCard, ScrollArea, InfoBar, PrimaryPushSettingCard
from app.sub_interfaces.accounts_interface import accounts_interface
from .common.style_sheet import StyleSheet
from .components.pivot import SettingPivot
from .card.comboboxsettingcard1 import ComboBoxSettingCard1
from .card.comboboxsettingcard2 import ComboBoxSettingCard2, ComboBoxSettingCardLog
from .card.switchsettingcard1 import SwitchSettingCard1, SwitchSettingCardNotify, StartMarch7thAssistantSwitchSettingCard, SwitchSettingCardTeam, SwitchSettingCardImmersifier, SwitchSettingCardGardenofplenty, SwitchSettingCardEchoofwar
from .card.rangesettingcard1 import RangeSettingCard1
from .card.pushsettingcard1 import PushSettingCardInstance, PushSettingCardNotifyTemplate, PushSettingCardMirrorchyan, PushSettingCardEval, PushSettingCardDate, PushSettingCardKey, PushSettingCardTeam, PushSettingCardFriends
from .card.timepickersettingcard1 import TimePickerSettingCard1
from module.config import cfg
from module.notification import notif
from tasks.base.tasks import start_task
from .tools.check_update import checkUpdate
import os

class FunctionInterface(ScrollArea):
    # 初始化
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.pivot = FunctionPivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.settingLabel = QLabel("功能", self)
        self.__initWidget()
        self.__initCard()
        self.__initLayout()
        self.__connectSignalToSlot()

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

    # 初始化卡片
    def __initCard(self):
        self.PowerGroup = SettingCardGroup(self.tr("程序功能"), self)
        self.checkupdate = SwitchSettingCard1(
            FIF.SYNC,
            "自动检查更新",
            "开启",
            'check_update'
        )