import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: introPage
    width: 1280
    height: 960
    objectName: "introPage"
    anchors.fill: parent

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

    Text {
        id: pageTitle
        objectName: "pageTitle"
        x: 536
        y: 17
        text: qsTr("Drone Analysis App")
        font.pixelSize: 24
    }

    Text {
        id: text1
        x: 488
        y: 261
        width: 305
        height: 31
        text: qsTr("Welcome to our drone analysis app. ")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
        minimumPixelSize: 12
        clip: false

        Text {
            id: text3
            x: -188
            y: 64
            text: qsTr("This app works by taking in several parameters pertaining to a drone provided by the user. ")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }
    }

    Text {
        id: text2
        x: 613
        y: 191
        text: qsTr("Hello!")
        font.pixelSize: 22
    }

    Text {
        id: text4
        x: 259
        y: 387
        width: 764
        height: 59
        text: qsTr("The application will then run calculations based on these parameters in order to provide the user with an estimate of certain performance parameters pertaining to their drone.")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
    }

    Text {
        id: text5
        x: 459
        y: 488
        width: 362
        height: 83
        text: qsTr("Some parameters are still Work In Progress and have been marked as such. Although they appear on the user interface, they have no actual function at the moment (or are hardcoded in the actural program).")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
    }

    Button {
        id: startButton
        objectName: "startButton"
        x: 528
        y: 716
        width: 225
        height: 50
        text: qsTr("Get Started")
        icon.color: "#000000"
        font.pixelSize: 18
    }


}
