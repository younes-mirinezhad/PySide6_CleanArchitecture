from PySide6.QtCore import QObject, Slot
from Libs.Common import Common

class Tools(QObject):
    def __init__(self):
        print(Common.func_info())
        super().__init__()
        self.name = "Tools"
        self.uiUrl = "Tools.qml"
        self.iconUrl = "Tools.png"
        self.order = 100

    @Slot()
    def exit(self):
        print(Common.func_info())
