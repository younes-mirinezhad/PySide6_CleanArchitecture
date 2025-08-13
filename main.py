# This Python file uses the following encoding: utf-8
import sys, os, importlib
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional, Type
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(name)s.%(funcName)s() %(message)s",
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.join(os.path.dirname(__file__), 'Libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Plugins'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Components'))

class PluginLoader(QObject):
    """
    Dynamically loads Python classes from subdirectories in a given folder.
    Can be used for plugins, components, or libraries.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.debug("PluginLoader initialized")
        self.plugins: List[Dict[str, Any]] = []
        self.components: List[Dict[str, Any]] = []

    def load_folder_contents(self, folder_name: str) -> List[Dict[str, Any]]:
        """
        Loads all classes from subfolders in the given folder.
        Each subfolder must contain a .py file with the same name as the folder.
        """
        logger.debug(f"Loading folder contents: {folder_name}")
        class_list = []
        app_folder = Path(__file__).parent.resolve()
        full_path = app_folder / folder_name

        if not full_path.is_dir():
            logger.warning(f"Directory not found: {full_path}")
            return class_list

        for subdir in full_path.iterdir():
            logger.debug(f"Processing subdirectory: {subdir}")
            if not subdir.is_dir():
                continue
            py_file = subdir / (subdir.name + ".py")
            if not py_file.is_file():
                logger.warning(f"Python file not found: {py_file}")
                continue
            try:
                spec = importlib.util.spec_from_file_location(subdir.name, str(py_file))
                if spec is None:
                    logger.error(f"Could not create spec for {py_file}")
                    continue
                logger.debug(f"Creating module from spec: {spec}")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if not hasattr(module, subdir.name):
                    logger.error(f"Class {subdir.name} not found in {py_file}")
                    continue
                cls = getattr(module, subdir.name)
                class_list.append({
                    "name": subdir.name,
                    "class": cls,
                    "file_path": str(py_file),
                    "root_path": str(subdir)
                })
                logger.debug(f"Loaded class: {cls}")
            except Exception as e:
                logger.exception(f"Failed to load {py_file}: {e}")
        return class_list

    def load_plugins(self, folder_name: str):
        """
        Loads plugins from the specified folder.
        """
        logger.info(f"Loading plugins from: {folder_name}")
        class_list = self.load_folder_contents(folder_name)
        plugin_list = []
        for cls in class_list:
            logger.debug(f"Processing class: {cls}")
            try:
                plugin_instance = cls["class"]()
                p_item = {
                    "name": cls["name"],
                    "uiUrl": os.path.join(cls["root_path"], getattr(plugin_instance, "uiUrl", "")),
                    "iconUrl": os.path.join(cls["root_path"], getattr(plugin_instance, "iconUrl", "")),
                    "class": cls["class"],
                    "instance": plugin_instance
                }
                plugin_list.append(p_item)
                logger.debug(f"Added plugin: {cls['name']}")
            except Exception as e:
                logger.exception(f"Failed to instantiate plugin {cls['name']}: {e}")
        self.plugins = sorted(plugin_list, key=lambda x: getattr(x["instance"], "order", 1000))

    def load_components(self, folder_name: str):
        """
        Loads components from the specified folder.
        """
        logger.info(f"Loading components from: {folder_name}")
        class_list = self.load_folder_contents(folder_name)
        for cls in class_list:
            logger.debug(f"Processing class: {cls}")
            try:
                c_item = {
                    "name": cls["name"],
                    "class": cls["class"]
                }
                self.components.append(c_item)
                logger.debug(f"Added component: {cls['name']}")
            except Exception as e:
                logger.exception(f"Failed to load component {cls['name']}: {e}")

if __name__ == "__main__":
    logger.info("Starting application")
    QGuiApplication.setApplicationName("Vision")
    QGuiApplication.setOrganizationName("ParsAI")

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    loader = PluginLoader()

    loader.load_plugins("Plugins")
    engine.rootContext().setContextProperty("pluginsList", loader.plugins)
    for p in loader.plugins:
        logger.info(f"Setting plugin: {p['name']}")
        pname = p["name"]+"_Plugin"
        engine.rootContext().setContextProperty(pname, p["instance"])

    loader.load_components("Components")
    for c in loader.components:
        logger.info(f"Registering component: {c['name']}")
        qmlRegisterType(c["class"], c["name"] + "Module", 1, 0, c["name"])

    qml_file = Path(__file__).parent / 'main.qml'
    logger.debug(f"Loading main.qml: {qml_file}")
    engine.load(qml_file)

    rootObjects = engine.rootObjects()
    if not rootObjects:
        sys.exit(-1)

    window = rootObjects[0]
    window.setIcon(QIcon('Icons/logo.png'))

    sys.exit(app.exec())
