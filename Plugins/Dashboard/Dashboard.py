from PySide6.QtCore import QObject, Slot
from Core.Database.Database import Database, Projects
from sqlalchemy import select, bindparam


class DashboardLoader():
    def __init__(self):
        super(DashboardLoader, self).__init__()
        self._pageUrl = "Plugins/Dashboard/Dashboard.qml"
        self._iconUrl = "Plugins/Dashboard/Dashboard.png"
        self._btnText = "Dashboard"


class Dashboard(QObject):
    def __init__(self):
        super(Dashboard, self).__init__()
        print("-- Dashboard")
        self._db = Database()

    @Slot(result=list)
    def getProjectsList(self):
        print("---- getProjectsList")

        prj = []
        query = select(Projects)
        with self._db.engine.connect() as conn:
            for row in conn.execute(query):
                prj.append(Projects.__repr__(row))
        return prj
