from PySide6.QtCore import QObject, Slot

class Tools(QObject):
    def __init__(self):
        super().__init__()
        self.name = "Tools"
        self.uiUrl = "Tools.qml"
        self.iconUrl = "Tools.png"
        self.order = 100

    @Slot()
    def testFunc(self):
        print("----------> Tools test pass")
