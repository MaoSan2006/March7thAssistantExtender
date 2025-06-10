from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from contextlib import redirect_stdout
with redirect_stdout(None):
    from qfluentwidgets import MSFluentWindow, SplashScreen, setThemeColor, setTheme, Theme
    from qfluentwidgets import FluentIcon as FIF

from app.home_interface import HomeInterface
from app.function_interface import FunctionInterface

class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        self.initInterface()
        self.initNavigation()

    def initWindow(self):
        self.setMicaEffectEnabled(False)
        setThemeColor('#f18cb9', lazy=True)
        setTheme(Theme.AUTO, lazy=True)

        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.resize(960, 640)
        self.setWindowIcon(QIcon('app/resource/customize/image/icon.png'))
        self.setWindowTitle("March7th Assistant")

        # 创建启动画面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.titleBar.maxBtn.setHidden(True)
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()
        QApplication.processEvents()
        self.splashScreen.close()

    def initInterface(self):
        self.homeInterface = HomeInterface(self)
        #self.accountInterface = AccountInterface(self)
        self.functionInterface = FunctionInterface(self)
        #self.runInterface = RunInterface(self)
    def initNavigation(self): #左列导航栏
        #上半部分
        self.addSubInterface(self.homeInterface,
            FIF.HOME,
            self.tr("主页")
            )
        '''self.addSubInterface(self.accountInterface,
            FIF.ROBOT,
            self.tr("账号管理")
            )
        '''
        self.addSubInterface(self.functionInterface,
            FIF.SETTING,
            self.tr("功能")
            )
        #下半部分
        '''
        self.addSubInterface(self.runInterface,
            FIF.PLAY,
            self.tr("运行")
            )
        '''
        