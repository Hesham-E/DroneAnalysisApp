import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: droneParametersPage
    objectName: "droneParametersPage"
    anchors.fill: parent

    Grid {
        id: leftParameterGrid
        objectName: "leftParameterGrid"
        x: 7
        y: 106
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 30

        Text {
            id: wingSpanLabel
            objectName: "wingSpanLabel"
            text: qsTr("Wing Span (m)")
            font.pixelSize: 18
        }
        TextField {
            id: wingSpanInput
            objectName: "wingSpanInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: wingThicknessLabel
            objectName: "wingThicknessLabel"
            text: qsTr("Wing Thickness (m)")
            font.pixelSize: 18
        }
        TextField {
            id: wingThicknessInput
            objectName: "wingThicknessInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: droneWeightLabel
            objectName: "droneWeightLabel"
            text: "Weight of the Drone (kg)"
            textFormat: Text.RichText
            font.pixelSize: 18
        }
        TextField {
            id: droneWeightInput
            objectName: "droneWeightInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: loadWeightLabel
            objectName: "loadWeightLabel"
            text: qsTr("Weight of the Load (kg)")
            font.pixelSize: 18
        }
        TextField {
            id: loadWeightInput
            objectName: "loadWeightInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: wingAreaLabel
            objectName: "wingAreaLabel"
            height: 20
            text: "Area of the Wings (m<sup>2</sup>)"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText
        }
        TextField {
            id: wingAreaInput
            objectName: "wingAreaInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: angleOfAttackLabel
            objectName: "angleOfAttackLabel"
            text: qsTr("Angle of Attack (degrees)")
            font.pixelSize: 18
        }
        TextField {
            id: angleOfAttackInput
            objectName: "angleOfAttackInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryWeightLabel
            objectName: "batteryWeightLabel"
            text: qsTr("Weight of the Battery (kg)")
            font.pixelSize: 18
        }
        TextField {
            id: batteryWeightInput
            objectName: "batteryWeightInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryCapactiyLabel
            objectName: "batteryCapactiyLabel"
            text: qsTr("Battery Capacity (mAh)")
            font.pixelSize: 18
        }
        TextField {
            id: batteryCapacityInput
            objectName: "batteryCapacityInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryVoltageLabel
            objectName: "batteryVoltageLabel"
            text: qsTr("Battery Voltage (V)")
            font.pixelSize: 18
        }
        TextField {
            id: batteryVoltageInput
            objectName: "batteryVoltageInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

    }

    Grid {
        id: middleParameterGrid
        objectName: "middleParameterGrid"
        x: 351
        y: 106
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 30

        Text {
            id: reynoldsNumLabel
            objectName: "reynoldsNumLabel"
            text: qsTr("Reynolds Number")
            font.pixelSize: 18
        }
        TextField {
            id: reynoldsNumInput
            objectName: "reynoldsNumInput"
            width: 100
            height: 36
            text: qsTr("500000")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: pressureLabel
            objectName: "pressureLabel"
            text: qsTr("Air Pressure (Pa)")
            font.pixelSize: 18
        }
        TextField {
            id: pressureInput
            objectName: "pressureInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: temperatureLabel
            objectName: "temperatureLabel"
            text: qsTr("Temperature (K)")
            font.pixelSize: 18
        }
        TextField {
            id: temperatureInput
            objectName: "temperatureInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: vStabilizerLengthLabel
            objectName: "vStabilizerLengthLabel"
            text: qsTr("Vertical Stabilizer Length (m)")
            font.pixelSize: 18
        }
        TextField {
            id: vStabilizerLengthInput
            objectName: "vStabilizerLengthInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: vStabilizerThicknessLabel
            objectName: "vStabilizerThicknessLabel"
            text: qsTr("Vertical Stabilizer Thickness (m)")
            font.pixelSize: 18
        }
        TextField {
            id: vStabilizerThicknessInput
            objectName: "vStabilizerThicknessInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: fuselageRadiusLabel
            objectName: "fuselageRadiusLabel"
            text: qsTr("Fuselage Radius (m)")
            font.pixelSize: 18
        }
        TextField {
            id: fuselageRadiusInput
            objectName: "fuselageRadiusInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: targetAltitudeLabel
            objectName: "targetAltitudeLabel"
            text: qsTr("Target Altitude (m)")
            font.pixelSize: 18
        }
        TextField {
            id: targetAltitudeInput
            objectName: "targetAltitudeInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: cruiseMotorTableLabel
            objectName: "cruiseMotorTableLabel"
            text: qsTr("File Path to Cruise Motor Table")
            font.pixelSize: 18
        }
        TextField {
            id: cruiseMotorTablePathInput
            objectName: "cruiseMotorTablePathInput"
            width: 220
            height: 36
//            text: qsTr("/path/to/MotorTable.csv")
            text: qsTr("./ModelLayer/T-motor AT2814 KV900 Cam-Carbon Z 10X8 25X20 test - alipoviy.csv")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: vtolMotorTableLabel
            objectName: "vtolMotorTableLabel"
            text: qsTr("File Path to VTOL Motor Table")
            font.pixelSize: 18
        }
        TextField {
            id: vtolMotorTablePathInput
            objectName: "vtolMotorTablePathInput"
            width: 220
            height: 36
//            text: qsTr("/path/to/MotorTable.csv")
            text: qsTr("./ModelLayer/T-motor AT2814 KV900 Cam-Carbon Z 10X8 25X20 test - alipoviy.csv")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }




      }

    Grid {
        id: rightParameterGrid
        objectName: "rightParameterGrid"
        x: 847
        y: 106
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 30

        Text {
            id: auxPowerConLabel
            objectName: "auxPowerConLabel"
            text: qsTr("Auxiliary Power Consumed (W)")
            font.pixelSize: 18
        }
        TextField {
            id: auxPowerConInput
            objectName: "auxPowerConInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: ascentDecentSpeedLabel
            objectName: "ascentDecentSpeedLabel"
            text: qsTr("Desired Ascent and Decent Speed (m/s)")
            font.pixelSize: 18
        }
        TextField {
            id: ascentDecentSpeedInput
            objectName: "ascentDecentSpeedInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        CheckBox {
            id: nonIdealInput
            text: "Use Non-Ideal Conditions?"
            objectName: "nonIdealConditionsInput"
            font.pixelSize: 18
            leftPadding: 0
        }
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
        id: estimateButton
        objectName: "estimateButton"
        x: 536
        y: 874
        width: 208
        height: 36
        text: qsTr("Estimate Parameters")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Text {
        id: pageTitle
        objectName: "pageTitle"
        x: 536
        y: 17
        text: qsTr("Drone Analysis App")
        font.pixelSize: 24
    }
}
