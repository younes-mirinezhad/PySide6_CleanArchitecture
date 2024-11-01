import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: root
    visible: true
    width: 1280
    height: 720
    title: qsTr("PySide6")

    property string currentPage: ""
    onCurrentPageChanged: { loader_content.source = currentPage }
    Component.onCompleted: {}

    SplitView {
        anchors.fill: parent
        orientation: Qt.Horizontal

        Pane {
            id: pluginsItem
            SplitView.preferredWidth: 40
            SplitView.minimumWidth: 40
            SplitView.maximumWidth: 60
            SplitView.fillHeight: true
            padding: 5

            ListView {
                id: pluginListView
                anchors.fill: parent
                model: pluginsList
                spacing: 5

                delegate: Item {
                    width: pluginListView.width
                    height: width

                    Button {
                        width: parent.width
                        height: parent.height
                        anchors.centerIn: parent
                        ToolTip.text: modelData.name

                        background: Rectangle {
                            radius: parent.width/4
                            Image {
                                source: modelData.iconUrl
                                fillMode: Image.PreserveAspectCrop
                                anchors.fill: parent
                            }
                        }

                        onHoveredChanged: ToolTip.visible = hovered
                        onClicked: root.currentPage = modelData.uiUrl
                        Component.onCompleted: {
                            if (root.currentPage == "")
                                root.currentPage = modelData.uiUrl
                        }
                    }
                }
            }
        }
        Loader {
            id: loader_content
            SplitView.fillWidth: true
            SplitView.fillHeight: true
        }
    }
}
