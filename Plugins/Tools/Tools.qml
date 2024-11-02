import QtQuick
import QtQuick.Controls

Pane {
    anchors.fill: parent
    padding: 5
    Component.onCompleted: Tools_plugin.testFunc();

    Rectangle {
        anchors.fill: parent
        color: "red"
    }
}
