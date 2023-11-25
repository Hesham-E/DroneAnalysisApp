import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: missionParametersPage
    width: 1280
    height: 960
    objectName: "missionParametersPage"
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
        x: 501
        y: 8
        text: qsTr("Select Mission Parameters")
        font.pixelSize: 24
    }

    Text {
        id: missionDistanceLabel
        x: 155
        y: 379
        objectName: "missionDistanceLabel"
        text: qsTr("Total Mission Distance (km)")
        font.pixelSize: 18
    }
    TextField {
        id: missionDistanceInput
        x: 413
        y: 373
        objectName: "missionDistanceInput"
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: temperatureLabel
        x: 818
        y: 379
        objectName: "temperatureLabel"
        text: qsTr("Temperature (K)")
        font.pixelSize: 18
    }
    TextField {
        id: temperatureInput
        x: 985
        y: 373
        objectName: "temperatureInput"
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: cruiseHeightLabel
        x: 234
        y: 530
        objectName: "cruiseHeightLabel"
        text: qsTr("Cruise Height (m)")
        font.pixelSize: 18
    }
    TextField {
        id: cruiseHeightInput
        x: 413
        y: 530
        objectName: "cruiseHeightInput"
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: pressureLabel
        x: 816
        y: 530
        objectName: "pressureLabel"
        text: qsTr("Air Pressure (Pa)")
        font.pixelSize: 18
    }
    TextField {
        id: pressureInput
        x: 985
        y: 530
        objectName: "pressureInput"
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Button {
        id: continueButton
        objectName: "continueButton"
        x: 536
        y: 855
        width: 208
        height: 36
        text: qsTr("Continue")
        icon.color: "#000000"
        font.pixelSize: 18
    }

}
