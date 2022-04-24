import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.12
import QtQuick.Controls.Material 2.15

MouseArea {
    id: control
    width: 40
    height: 40
    property string icon_btn
    property bool icon_visible: false
    property string text_btn
    property bool text_visible: true
    property bool clicked: false
    property int radius: width/5

    Rectangle {
        anchors.fill: parent
        anchors{
            topMargin: 5
            leftMargin: 5
            rightMargin: 5
            bottomMargin: 0
        }
        radius: control.radius

        RowLayout{
            anchors.fill: parent

            Item { Layout.fillWidth: (txt.visible && img.visible) ? false : true }
            Image{
                id: img
                visible: control.icon_visible
                source: control.icon_btn
                Layout.preferredWidth: control.height-10
                Layout.preferredHeight: control.height-10
                Layout.leftMargin: (txt.visible && img.visible) ? 5 : 0
            }
            Text{
                id: txt
                visible: control.text_visible ? x + width + 15 < control.width : 0
                text: control.text_btn
            }
            Item { Layout.fillWidth: true }
        }
    }
}

//RoundButton{
//    id: control
//    property string icon_btn
//    property bool icon_visible: false
//    property string text_btn
//    property bool text_visible: true
//    radius: width/5

//    contentItem: RowLayout{
//        anchors.fill: parent

//        Image{
//            id: img
//            visible: control.icon_visible
//            source: control.icon_btn
//            Layout.preferredWidth: control.height-10
//            Layout.preferredHeight: control.height-10
//            Layout.leftMargin: 5
//        }
//        Text{
//            id: txt
//            visible: control.text_visible ? x + width + 10 < control.width : 0
//            text: control.text_btn
//            Layout.leftMargin: img.visible ? 0 : (control.width-width)/2
//        }
//        Item { Layout.fillWidth: true }
//    }
//}
