from PySide6.QtCore import QObject, Slot

class Dashboard(QObject):
    def __init__(self):
        super().__init__()
        self.name = "Dashboard"
        self.uiUrl = "Dashboard.qml"
        self.iconUrl = "Dashboard.png"
        self.order = 1
