import logging
from PySide6.QtCore import QObject, Slot

# Get logger instance
logger = logging.getLogger(__name__)

class Dashboard(QObject):
    def __init__(self):
        super().__init__()
        logger.debug("")
        self.name = "Dashboard"
        self.uiUrl = "Dashboard.qml"
        self.iconUrl = "Dashboard.png"
        self.order = 1

    @Slot()
    def exit(self):
        pass
