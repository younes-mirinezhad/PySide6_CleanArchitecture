# This Python file uses the following encoding: utf-8
import sys, os, importlib
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject

sys.path.append(os.path.join(os.path.dirname(__file__), 'Libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Plugins'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Components'))

class PluginLoader(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plugins = []
        self.components = []

    def loadFolderContents(self, folderName) -> list:
        classList = []
        appFolder = os.path.dirname(os.path.abspath(__file__))
        fullPath = appFolder + "/" + folderName
        if not os.path.isdir(fullPath): 
            return classList

        for className in os.listdir(fullPath):
            folder_path = os.path.join(fullPath, className)
            if not os.path.isdir(folder_path): 
                continue
            
            filePath = os.path.join(folder_path, className+".py")
            if not os.path.isfile(filePath):
                continue

            try:
                spec = importlib.util.spec_from_file_location(className, filePath)
                if spec is None:
                    print(f"***** Failed to load {className}")
                    continue

                thisModule = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(thisModule)
                if not hasattr(thisModule, className):
                    print(f"***** Failed to find class {className} in {filePath}")
                    continue

                thisClass = getattr(thisModule, className)

                classList.append({"name":className, 
                                  "class":thisClass, 
                                  "filePath":filePath, 
                                  "rootPath":folder_path})
            except Exception as e:
                print(f"***** Failed to load {className} : {e}")
        
        return classList

    def load_plugins(self, folderName):
        classList = self.loadFolderContents(folderName)

        pluginList = []
        for cls in classList:
            plugin_class = cls["class"]
            plugin_instance = plugin_class()

            pItem = {"name": cls["name"],
                     "uiUrl": os.path.join(cls["rootPath"] , plugin_instance.uiUrl),
                     "iconUrl": os.path.join(cls["rootPath"] , plugin_instance.iconUrl),
                     "class": plugin_class,
                     "instance": plugin_instance}
            pluginList.append(pItem)
            print(f"-----> plugin ", {cls["name"]}, " loads successfully")

        self.plugins = sorted(pluginList, key=lambda x: x["instance"].order)

    def load_components(self, folderName):
        classList = self.loadFolderContents(folderName)

        for cls in classList:
            component_class = cls["class"]

            cItem = {"name": cls["name"],
                     "class": component_class}
            self.components.append(cItem)
            print(f"-----> component ", {cls["name"]}, " loads successfully")

if __name__ == "__main__":
    QGuiApplication.setApplicationName("Vision")
    QGuiApplication.setOrganizationName("ParsAI")

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    loader = PluginLoader()

    loader.load_plugins("Plugins")
    engine.rootContext().setContextProperty("pluginsList", loader.plugins)
    for p in loader.plugins:
        pname = p["name"]+"_Plugin"
        engine.rootContext().setContextProperty(pname, p["instance"])

    loader.load_components("Components")
    for c in loader.components:
        qmlRegisterType(c["class"], c["name"] + "Module", 1, 0, c["name"])

    qml_file = Path(__file__).parent / 'main.qml'
    engine.load(qml_file)

    rootObjects = engine.rootObjects()
    if not rootObjects:
        sys.exit(-1)

    window = rootObjects[0]
    window.setIcon(QIcon('Icons/logo.png'))

    sys.exit(app.exec())
