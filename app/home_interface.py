from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QImage,
    QPainter,
    QPainterPath
)
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTextBrowser
)
from qfluentwidgets import FluentIcon, ScrollArea

from task.handler.config_handler import config_handler

from .common.style_sheet import StyleSheet
from .components.link_card import LinkCardView

import numpy as np

class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.setFixedHeight(320)

        # 创建水平(卡片)+垂直布局
        self.vBoxLayout = QVBoxLayout(self) # 垂直布局
        linkCardLayout = QHBoxLayout() # 水平布局

        # 设置标签样式与内容
        self.galleryLabel = QLabel(f'三月七小助手拓展包 {config_handler.read("version")}\nMarch7thAssistantExtender', self) # 创建标签
        self.galleryLabel.setStyleSheet("color: white;font-size: 30px; font-weight: 600;")

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect() # 创建阴影效果
        shadow.setBlurRadius(20) # 阴影模糊半径
        shadow.setColor(Qt.black) # 阴影颜色
        shadow.setOffset(1.2, 1.2) # 阴影偏移量
        self.galleryLabel.setGraphicsEffect(shadow) # 将阴影效果应用于小部件

        # 初始化图片与路径
        self.img = Image.open("app/resource/customize/image/background.jpg")
        self.banner = None
        self.path = None

        # 卡片设置
        self.linkCardView = LinkCardView(self) # 创建链接卡片
        self.linkCardView.setContentsMargins(0, 0, 0, 36) # 设置边距
        linkCardLayout.addWidget(self.linkCardView) # 添加链接卡片
        linkCardLayout.setAlignment(Qt.AlignBottom) # 设置对齐方式

        # 布局设置
        self.galleryLabel.setObjectName('galleryLabel') # 设置对象名称
        self.vBoxLayout.setSpacing(0) # 设置间距
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0) # 设置边距
        self.vBoxLayout.addWidget(self.galleryLabel) # 添加标签
        self.vBoxLayout.addLayout(linkCardLayout) # 添加布局
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop) # 设置对齐方式(居左)
        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub'),
            self.tr('三月七小助手Github链接\n这个是主脚本链接\n希望你也能支持一下'),
            "https://github.com/moesnow/March7thAssistant"
        )
        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub'),
            self.tr('为了能使用方便\n苦学1个月Qt\n球球了你给个⭐吧QAQ'),
            "https://github.com/MaoSan2006/March7thAssistantExtender"
        )

    # 重写并自动调用图片处理
    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        if not self.banner or not self.path:
            image_height = self.img.width * self.height() // self.width()
            crop_area = (0, 0, self.img.width, image_height)  # (left, upper, right, lower)
            cropped_img = self.img.crop(crop_area)
            img_data = np.array(cropped_img)  # Convert PIL Image to numpy array
            height, width, channels = img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

            path = QPainterPath()
            path.addRoundedRect(0, 0, width + 50, height + 50, 10, 10)  # 10 is the radius for corners
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)

class HomeInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # 禁用水平滚动条
        self.setWidget(self.view)# 设置主视图部件
        self.setWidgetResizable(True)# 允许部件随窗口大小调整
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)# 设置布局边距(左,上,右,下)
        self.vBoxLayout.setSpacing(25)# 设置布局内部件间距
        self.vBoxLayout.addWidget(self.banner)# 将横幅部件添加到布局
        self.vBoxLayout.setAlignment(Qt.AlignTop)# 设置布局对齐方式为顶部对齐
        self.UpdateLog() # 添加更新日志

    # 添加更新日志
    def UpdateLog(self):
        self.changelogBrowser = QTextBrowser(self)
        with open('app/resource/customize/text/UpdateLog.html', 'r', encoding='utf-8') as f:
            self.changelogBrowser.setHtml(f.read())
        # 添加样式表设置
        self.changelogBrowser.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                border: none;
                color: white;
            }
        """)
        self.vBoxLayout.addWidget(self.changelogBrowser)