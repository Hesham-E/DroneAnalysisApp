import QtQuick
import QtQuick.Controls

import "."

Popup {
    id: popupPage
    width: Style.screenWidth / 3
    height: Style.screenHeight / 3
    objectName: "popupPage"

    property var labelSize: 18
    property var outputWidth: 200
    property var outputHeight: 36

    Text {
        id: popupTitle
        x: 160
        y: 8
        width: 106
        height: 39
        objectName: "popupTitle"
        text: qsTr("ERROR")
        font.pixelSize: 24
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
    }

    Text {
        id: popupLabel
        anchors.centerIn: parent
        width: 380
        height: 165
        objectName: "popupLabel"
        text: qsTr("Hello this is a sample message")
        font.pixelSize: 24
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
    }

    Button {
        id: confirmButton
        x: 113
        y: 281
        objectName: "confirmButton"
        width: 200
        height: 31
        text: qsTr("Confirm")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 500 }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 500 }
    }

}
