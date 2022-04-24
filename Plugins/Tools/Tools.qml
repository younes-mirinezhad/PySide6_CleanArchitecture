import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../../Core/Controls" as Ctrl
import plugins.Tools 1.0

Pane {
    padding: height*0.1

    Ctrl.Pane {
        anchors.fill: parent

        Tools { id: toolsPlugin }

        ColumnLayout {
            anchors.centerIn: parent

            RowLayout {
                Label {
                    Layout.preferredWidth: 100
                    text: "Project Name:"
                }
                TextField {
                    id: prjName_txt
                    Layout.preferredWidth: 200
                    placeholderText: qsTr("Enter project name")
                }
            }
            RowLayout {
                Label {
                    Layout.preferredWidth: 100
                    text: "Description:"
                }
                ScrollView {
                    Layout.preferredWidth: 200
                    Layout.preferredHeight: 100

                    TextArea {
                        id: prjDescription_txt
                        selectByKeyboard: true
                        selectByMouse: true
                        placeholderText: qsTr("Enter description")
                    }
                }
            }
            Ctrl.IconButton {
                text_btn: "Create"
                text_visible: true
                Layout.fillWidth: true
                height: 40
                onClicked: {
                    if(prjName_txt.text.length > 0){
                        toolsPlugin.createProject(prjName_txt.text, prjDescription_txt.text)
                        prjName_txt.text = ""
                        prjDescription_txt.text = ""
                    }
                    else
                        console.log("------ Enter name and description fields")
                }
            }
        }
    }
}
