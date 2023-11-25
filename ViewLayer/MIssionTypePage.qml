import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: missionTypePage
    width: 1280
    height: 960
    objectName: "missionTypePage"
    anchors.fill: parent

    Text {
        id: pageTitle
        objectName: "pageTitle"
        x: 536
        y: 17
        text: qsTr("Select Mission Type")
        font.pixelSize: 24
    }

    Image {
        id: epJrE5C6_400x400
        objectName: "epJrE5C6_400x400"
        x: 0
        y: 0
        width: 100
        height: 100
        source: "images/EpJrE5C6_400x400.png"
        fillMode: Image.PreserveAspectFit
    }

    Button {
        id: surveillanceButton
        objectName: "surveillanceButton"
        x: 536
        y: 374
        width: 208
        height: 36
        text: qsTr("Surveillance")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: payloadDeliveryButton
        objectName: "payloadDeliveryButton"
        x: 536
        y: 462
        width: 208
        height: 36
        text: qsTr("Payload Delivery")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: allButton
        objectName: "allButton"
        x: 536
        y: 562
        width: 208
        height: 36
        text: qsTr("All")
        icon.color: "#000000"
        font.pixelSize: 18
    }


}
