import logging
from PySide6.QtCore import QObject, Slot

# Get logger instance
logger = logging.getLogger(__name__)

class Tools(QObject):
    def __init__(self):
        super().__init__()
        logger.debug("")
        self.name = "Tools"
        self.uiUrl = "Tools.qml"
        self.iconUrl = "Tools.png"
        self.order = 100

    @Slot()
    def exit(self):
        pass
