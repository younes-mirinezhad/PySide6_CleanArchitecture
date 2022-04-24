import QtQuick 2.15
import QtQuick.Controls 2.15 as Qctrl
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Material.impl 2.12

Qctrl.Pane{
    id: control
    Material.elevation: 10
    property int radius: 10
    property color color: "#585858"
    padding: 0

    background: Rectangle {
        color: control.color
//        color: control.Material.backgroundColor
//        color: Qt.rgba(control.Material.backgroundColor.r/2,
//                       control.Material.backgroundColor.g/2,
//                       control.Material.backgroundColor.b/2,
//                       control.Material.backgroundColor.a<0.5?0.25:0.75)

//        radius: control.Material.elevation > 0 ? control.radius : 0
        radius: control.radius
//        layer.enabled: control.enabled && control.Material.elevation > 0
//        layer.effect: ElevationEffect { elevation: control.Material.elevation }
    }
}
