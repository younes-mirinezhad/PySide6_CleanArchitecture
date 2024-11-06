import Qt.labs.platform
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ViewPortModule 1.0

Pane {
    anchors.fill: parent
    padding: 5

    Connections {
        target: Qt.application
        function onAboutToQuit() { VideoPlayer_Plugin.exit() }
    }

    ColumnLayout {
        anchors.fill: parent

        ViewPort {
            id: viewPortItm
            Layout.fillWidth: true
            Layout.fillHeight: true

            Component.onCompleted: {
                VideoPlayer_Plugin.setViewPort(viewPortItm)
            }
        }
        Item {
            id: controlBoxItm
            Layout.fillWidth: true
            Layout.preferredHeight: 30

            ColumnLayout {
                anchors.fill: parent

                ProgressBar {
                    id: streamerProgressBar
                    Layout.fillWidth: true
                    Layout.preferredHeight: 8
                    from: 0
                    to: VideoPlayer_Plugin ? VideoPlayer_Plugin.framesCount : 0
                    value: VideoPlayer_Plugin ? VideoPlayer_Plugin.frameNumber : 0

                    // MouseArea {
                    //     anchors.fill: parent
                        
                    //     onClicked: {
                    //         var p = Math.round(mouse.x / width * streamerProgressBar.to)
                    //     }
                    // }
                }
                RowLayout {
                    id: buttonBoxItm
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Button {
                        id: selectVideoFileItm
                        Layout.fillHeight: true
                        Layout.preferredWidth: height

                        ToolTip.text: "Select video"
                        onHoveredChanged: ToolTip.visible = hovered

                        onClicked: videoSelector.open()

                        background: Rectangle {
                            radius: parent.width/4
                            Image {
                                anchors.fill: parent
                                source: "./Icons/VideoFile.png"
                                fillMode: Image.PreserveAspectCrop
                            }
                        }
                    }

                    Item { Layout.fillWidth: true }

                    Button {
                        id: playItm
                        Layout.fillHeight: true
                        Layout.preferredWidth: height

                        ToolTip.text: (VideoPlayer_Plugin && VideoPlayer_Plugin.playbackStatus) ? "Pause" : "Play"
                        onHoveredChanged: ToolTip.visible = hovered

                        onClicked: VideoPlayer_Plugin.changeStreamerStatus()

                        background: Rectangle {
                            radius: parent.width/4
                            Image {
                                anchors.fill: parent
                                source: (VideoPlayer_Plugin && VideoPlayer_Plugin.playbackStatus) ? "./Icons/Pause.png" : "./Icons/Play.png"
                                fillMode: Image.PreserveAspectCrop
                            }
                        }
                    }

                    Item { Layout.fillWidth: true }
                }
            }
        }
    }
    FileDialog {
        id: videoSelector
        title: "Select a Video File"
        nameFilters: ["Video files (*.mp4 *.avi *.mkv *.mov *.wmv)"]
        
        onAccepted: {
            // Remove "file://"
            var filePath = videoSelector.currentFile.toString().replace("file://", "")
            VideoPlayer_Plugin.setStreamerPath(filePath)
            VideoPlayer_Plugin.init()
        }
    }
}
