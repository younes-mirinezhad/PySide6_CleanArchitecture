import QtQuick 2.15
import QtQuick.Controls 2.15

Popup {
    id: popup
    anchors.centerIn: parent
    width: 350
    height: 200
    modal: true
    focus: true
//    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    closePolicy: Popup.NoAutoClose

    property string title: ""
    property string text: ""

    Label {
        id: title_lbl
        anchors{
            top: parent.top
            left: parent.left
            leftMargin: 2
            topMargin: 2
        }
        font.bold: true
        text: popup.title
    }
    ScrollView {
        anchors{
            top: title_lbl.bottom
            left: parent.left
            right: parent.right
            bottom: okBtn.top
            margins: 2
            topMargin: 5
        }
        TextArea {
            id: text_lbl
            anchors.fill: parent
            enabled: false
            text: popup.text
        }
    }
    IconButton {
        id: okBtn
        width: 75
        height: 30
        anchors{
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }
        text_btn: "OK"
        onClicked: popup.close()
    }
}
