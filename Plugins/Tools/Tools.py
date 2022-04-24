from PySide6.QtCore import QObject, Slot
from Core.Database.Database import Database, Projects
from sqlalchemy import insert


class ToolsLoader():
    def __init__(self):
        super(ToolsLoader, self).__init__()
        self._pageUrl = "Plugins/Tools/Tools.qml"
        self._iconUrl = "Plugins/Tools/tools.png"
        self._btnText = "Tools"


class Tools(QObject):
    def __init__(self):
        super(Tools, self).__init__()
        print("-- Tools")
        self._db = Database()

    @Slot(str, str)
    def createProject(self, pName, pDesc):
        print("---- createProject:", pName, ", ", pDesc)
        query = insert(Projects).values(name=pName, description=pDesc)
        with self._db.engine.connect() as conn:
            conn.execute(query)
            conn.commit()
