from PySide6.QtCore import QObject, Property, Signal


class Plugins(QObject):
    pluginsListChanged = Signal()

    def __init__(self):
        super(Plugins, self).__init__()
        print("-- PluginLoader")
        self._PluginsList = []
        self.set_pluginsList(self.loadPlugins())

# ---------- Plugins
    def loadPlugins(self):
        _tmp_plugins = []

        try:
            from Plugins.Dashboard.Dashboard import DashboardLoader
            _tmp_plugins.append({
                "pageUrl": DashboardLoader()._pageUrl,
                "iconUrl": DashboardLoader()._iconUrl,
                "btnText": DashboardLoader()._btnText
                })
            print("---- Dashboard loads successfully")
        except Exception:
            print("---- can't load Dashboard")

        try:
            from Plugins.Tools.Tools import ToolsLoader
            _tmp_plugins.append({
                "pageUrl": ToolsLoader()._pageUrl,
                "iconUrl": ToolsLoader()._iconUrl,
                "btnText": ToolsLoader()._btnText
                })
            print("---- Tools loads successfully")
        except Exception:
            print("---- can't load Tools")

        return _tmp_plugins

# ---------- pluginsList Property
    def get_pluginsList(self):
        return self._PluginsList

    def set_pluginsList(self, pluginsList):
        if(self._PluginsList == pluginsList):
            return
        self._PluginsList = pluginsList
        self.pluginsListChanged.emit()

    pluginsList = Property(list, get_pluginsList, set_pluginsList, notify=pluginsListChanged)
