# This Python file uses the following encoding: utf-8
import sys, os, importlib
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot

class PluginLoader(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._plugins_folderName = "Plugins"
        self.plugins = []

    def load_plugins(self):
        appFolder = os.path.dirname(os.path.abspath(__file__))
        plugins_folderPath = appFolder + "/" + self._plugins_folderName
        if not os.path.isdir(plugins_folderPath):
            return

        pluginList = []
        for plugin_name in os.listdir(plugins_folderPath):
            folder_path = os.path.join(plugins_folderPath, plugin_name)
            if not os.path.isdir(folder_path):
                continue

            plugin_path = os.path.join(folder_path, plugin_name+".py")
            if not os.path.isfile(plugin_path):
                continue

            try:
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                if spec is None:
                    print(f"***** Failed to load {plugin_name}")
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if not hasattr(module, plugin_name):
                    print(f"***** Failed to find class {plugin_name} in {plugin_path}")
                    continue

                plugin_class = getattr(module, plugin_name)
                plugin_instance = plugin_class()

                pIthem = {
                "name": plugin_instance.name,
                "uiUrl": os.path.join(folder_path , plugin_instance.uiUrl),
                "iconUrl": os.path.join(folder_path , plugin_instance.iconUrl),
                "instance": plugin_instance
                }
                pluginList.append(pIthem)
                print(f"----- {plugin_instance.name} loads successfully")
            except Exception as e:
                print(f"***** Failed to load {plugin_name} {e}")

        self.plugins = sorted(pluginList, key=lambda x: x["instance"].order)

if __name__ == "__main__":
    QGuiApplication.setApplicationName("PySide6")
    QGuiApplication.setOrganizationName("ParsAI")

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    loader = PluginLoader()
    loader.load_plugins()
    engine.rootContext().setContextProperty("pluginsList", loader.plugins)

    qml_file = Path(__file__).parent / 'main.qml'
    engine.load(qml_file)

    rootObjects = engine.rootObjects()
    if not rootObjects:
        sys.exit(-1)

    window = rootObjects[0]
    window.setIcon(QIcon('Icons/logo.png'))

    sys.exit(app.exec())
