import QtQuick
import QtQuick.Controls

Pane {
    anchors.fill: parent
    padding: 5

    Connections {
        target: Qt.application
        function onAboutToQuit() { Dashboard_Plugin.exit() }
    }
}
