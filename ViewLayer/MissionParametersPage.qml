import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal
import "."

Item {
    id: missionParametersPage
    width: Style.screenWidth
    height: Style.screenHeight
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
        x: 104
        y: 379
        objectName: "missionDistanceLabel"
        text: qsTr("Total Mission Distance (m)")
        font.pixelSize: 18

        property string tip: "The total distance between each point of the mission."
        ToolTip.visible: tip ? missionDistanceMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: missionDistanceMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: missionDistanceInput
        x: 362
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

        property string tip: "The current air temperature."
        ToolTip.visible: tip ? temperatureMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: temperatureMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: temperatureInput
        x: 985
        y: 373
        objectName: "temperatureInput"
        width: 80
        height: 36
        text: qsTr("288.15")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: cruiseHeightLabel
        x: 183
        y: 530
        objectName: "cruiseHeightLabel"
        text: qsTr("Cruise Height (m)")
        font.pixelSize: 18

        property string tip: "The maximum cruise height of the mission."
        ToolTip.visible: tip ? cruiseHeightMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: cruiseHeightMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: cruiseHeightInput
        x: 362
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

        property string tip: "The current air pressure."
        ToolTip.visible: tip ? pressureMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: pressureMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: pressureInput
        x: 985
        y: 530
        objectName: "pressureInput"
        width: 80
        height: 36
        text: qsTr("101325")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: loadWeightLabel
        x: 489
        y: 668
        objectName: "loadWeightLabel"
        text: qsTr("Payload Weight (kg)")
        font.pixelSize: 18
        visible: false

        property string tip: "The weight of the payload transported."
        ToolTip.visible: tip ? loadWeightMA.containsMouse && loadWeightLabel.visible : false
        ToolTip.text: tip
        MouseArea {
            id: loadWeightMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: loadWeightInput
        x: 691
        y: 662
        objectName: "loadWeightInput"
        width: 80
        height: 36
        text: qsTr("0")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        visible: false
    }

    Button {
        id: returnButton
        objectName: "returnButton"
        x: 389
        y: 855
        width: 208
        height: 36
        text: qsTr("Go Back")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: continueButton
        objectName: "continueButton"
        x: 706
        y: 855
        width: 208
        height: 36
        text: qsTr("Continue")
        icon.color: "#000000"
        font.pixelSize: 18
    }

}
