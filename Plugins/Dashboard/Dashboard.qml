import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../../Core/Controls" as Ctrl
import plugins.Dashboard 1.0

Ctrl.Pane {
    id: root

    Dashboard { id: dashboardPlugin }
    Ctrl.MessageDialog { id: msg }

    ColumnLayout {
        id: listPart_clm
        anchors {
            top: parent.top
            left: parent.left
            bottom: parent.bottom
            margins: 10
        }
        width: 150

        Ctrl.IconButton {
            Layout.fillWidth: true
            height: 40
            text_btn: "Load Project List"
            radius: 10
            Layout.alignment: Qt.AlignCenter

            onClicked: {
                var _prjList = dashboardPlugin.getProjectsList()
                for(var i=0; i<_prjList.length; i++)
                {
                    prjList.append({
                                       id: _prjList[i].id,
                                       name: _prjList[i].name,
                                       description: _prjList[i].description
                                   })
                }
            }
        }
        Item { Layout.preferredHeight: 20 }
        Label { Layout.alignment: Qt.AlignCenter; text: "Projects list" }
        Item { Layout.preferredHeight: 5 }
        ListModel { id: prjList }
        ListView {
            id: prjList_lv
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            spacing: 5
//            ScrollBar.vertical: ScrollBar {
//                id: sb
//                active: prjList.length > 0 ? true : false
//                Component.onCompleted: { x = prjList_lv.width-width/2; width = 10 }
//            }

            model: prjList
            delegate: MouseArea {
                width: prjList_lv.width
                height: 40
                Rectangle {
                    anchors.fill: parent
                    border.width: 1
                    color: "transparent"

                    ColumnLayout {
                        anchors.fill: parent
                        RowLayout {
                            Item { Layout.preferredWidth: 5 }
                            Label { text: id + " : "}
                            Item { Layout.fillWidth: true }
                            Label { text: name }
                            Item { Layout.fillWidth: true }
                        }
                    }
                }
                onClicked: {
                    msg.title = "Project Name: " + name
                    msg.text = "Description:\n" + description
                    msg.visible = true
                }
            }
        }
    }
}
