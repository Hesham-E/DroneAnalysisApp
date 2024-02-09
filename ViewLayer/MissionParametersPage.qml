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
        x: 113
        y: 167
        objectName: "missionDistanceLabel"
        text: qsTr("Total Mission Distance (m)")
        font.pixelSize: 18

        property string tip: "The total distance between the start and finish points of the mission."
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
        y: 161
        objectName: "missionDistanceInput"
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: temperatureLabel
        x: 826
        y: 167
        objectName: "temperatureLabel"
        text: qsTr("Temperature (K)")
        font.pixelSize: 18

        property string tip: "The current air temperature at the base station."
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
        x: 998
        y: 161
        objectName: "temperatureInput"
        width: 80
        height: 36
        text: qsTr("288.15")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }
    
    Text {
        id: pressureLabel
        x: 824
        y: 267
        objectName: "pressureLabel"
        text: qsTr("Air Pressure (Pa)")
        font.pixelSize: 18

        property string tip: "The current air pressure at the base station."
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
        x: 998
        y: 261
        objectName: "pressureInput"
        width: 80
        height: 36
        text: qsTr("101325")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: cruiseAltitudeLabel
        x: 174
        y: 367
        objectName: "cruiseAltitudeLabel"
        text: qsTr("Cruise Altitude (m)")
        font.pixelSize: 18

        property string tip: "The cruise altitude of the mission."
        ToolTip.visible: tip ? cruiseAltitudeMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: cruiseAltitudeMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: cruiseAltitudeInput
        x: 362
        y: 361
        objectName: "cruiseAltitudeInput"
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: baseStationAltitudeLabel
        x: 126
        y: 267
        text: qsTr("Base Station Altitude (m)")
        font.pixelSize: 18
        objectName: "baseStationAltitudeLabel"
        
        property string tip: "The base station altitude. Used as a reference point for the takeoff altitude and atmosphereic conditions in the air."
        ToolTip.visible: tip ? baseStationAltitudeMA.containsMouse && baseStationAltitudeLabel.visible : false
        ToolTip.text: tip
        MouseArea {
            id: baseStationAltitudeMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: baseStationAltitudeInput
        x: 362
        y: 261
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        objectName: "baseStationAltitudeInput"
    }

    Text {
        id: vtolClimbLabel
        x: 128
        y: 468
        text: qsTr("VTOL Climb Altitude (m)")
        font.pixelSize: 18
        objectName: "vtolClimbLabel"
        visible: false
        
        property string tip: "The altitude to climb to after take off in VTOL mode. The drone will switch to fixed wing ascent after reaching this altitude."
        ToolTip.visible: tip ? vtolClimbMA.containsMouse && vtolClimbLabel.visible : false
        ToolTip.text: tip
        MouseArea {
            id: vtolClimbMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: vtolClimbInput
        x: 362
        y: 462
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        objectName: "vtolClimbInput"
        visible: false
    }

    Text {
        id: vtolDescentLabel
        x: 111
        y: 552
        text: qsTr("VTOL Descent Altitude (m)")
        font.pixelSize: 18
        objectName: "vtolDescentLabel"
        visible: false

        property string tip: "The altitude to begin VTOL landing from. The drone will have descended to this altitude in fixed wing mode from the cruise altitude."
        ToolTip.visible: tip ? vtolDescentMA.containsMouse && vtolDescentLabel.visible : false
        ToolTip.text: tip
        MouseArea {
            id: vtolDescentMA
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    TextField {
        id: vtolDescentInput
        x: 362
        y: 546
        width: 80
        height: 36
        text: qsTr("1")
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        objectName: "vtolDescentInput"
        visible: false
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
