import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Material.impl 2.12
import "./Controls" as Ctrl

Ctrl.Pane {
    id: control
    property string selectedPage: ""
    property variant pagesList: []
    onPagesListChanged: {
        if(pagesList.length > 0){
            for(var i=0; i<pagesList.length; i++){
                pagesListModel.append({
                                          pageUrl: pagesList[i].pageUrl,
                                          iconUrl: pagesList[i].iconUrl,
                                          btnText: pagesList[i].btnText
                                      })
            }
            selectedPage = pagesList[0].pageUrl
        }
    }

    ListModel{ id: pagesListModel }
    ListView{
        id: pagesList_lv
        anchors.fill: parent
        model: pagesListModel

        delegate: Ctrl.IconButton {
            width: pagesList_lv.width
            height: 30
            text_btn: btnText
            text_visible: true
            icon_btn: "../../" + iconUrl
            icon_visible: true

            onClicked: { selectedPage = model.pageUrl }
        }
    }
}
