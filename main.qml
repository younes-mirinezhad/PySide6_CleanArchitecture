import QtQuick 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "./Core"
import core.PluginLoader 1.0

ApplicationWindow {
    id: root
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red
    width: 1280
    height: 720
    title: qsTr("CrowNet")

    Plugins { id: pluginLoader }

    Item {
        id: mainItm
        anchors.fill: parent

        MenuBar {
            id: leftMenue
            width: 40
            anchors {
                top: mainItm.top
                bottom: mainItm.bottom
                left: mainItm.left
                margins: 2
            }
            pagesList: pluginLoader.pluginsList
            onSelectedPageChanged: page_Loader.source = selectedPage
        }
        Loader {
            id: page_Loader
            anchors {
                top: mainItm.top
                bottom: mainItm.bottom
                left: leftMenue.right
                right: mainItm.right
                margins: 2
            }
        }
    }
}
