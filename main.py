# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
from PySide6 import QtWidgets
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType


import Core.Database.Database as db
import Plugins.PluginLoader as PL
import Plugins.Tools.Tools as Tls
import Plugins.Dashboard.Dashboard as Dsb


if __name__ == "__main__":
    QGuiApplication.setApplicationName("CrowNet")
    QGuiApplication.setOrganizationName("ParsAI")

    app = QGuiApplication(sys.argv)

    qmlRegisterType(PL.Plugins, "core.PluginLoader", 1, 0, "Plugins")
    qmlRegisterType(Tls.Tools, "plugins.Tools", 1, 0, "Tools")
    qmlRegisterType(Dsb.Dashboard, "plugins.Dashboard", 1, 0, "Dashboard")

    _db = db.Database()
    _db.createTables()

    engine = QQmlApplicationEngine()

    qml_file = Path(__file__).parent / 'main.qml'
    engine.load(qml_file)
    rootObjects = engine.rootObjects()
    if not rootObjects:
        sys.exit(-1)

    window = rootObjects[0]
    window.setIcon(QIcon('Icons/logo.png'))

    sys.exit(app.exec())
