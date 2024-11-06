from PySide6.QtCore import QObject, Slot
from Libs.Common import Common

class Dashboard(QObject):
    def __init__(self):
        print(Common.func_info())
        super().__init__()
        self.name = "Dashboard"
        self.uiUrl = "Dashboard.qml"
        self.iconUrl = "Dashboard.png"
        self.order = 1

    @Slot()
    def exit(self):
        print(Common.func_info())
