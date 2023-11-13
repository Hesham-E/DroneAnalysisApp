import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: droneParametersPage
    anchors.fill: parent

    Grid {
        id: leftParameterGrid
        x: 43
        y: 173
        width: 431
        height: 586
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 50

        Text {
            id: wingSpanLabel
            text: qsTr("Wing Span (m)")
            font.pixelSize: 18
        }
        TextField {
            id: wingSpanInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: wingThicknessLabel
            text: qsTr("Wing Thickness (m)")
            font.pixelSize: 18
        }
        TextField {
            id: wingThicknessInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: droneWeightLabel
            text: "Weight of the Drone (kg)"
            textFormat: Text.RichText
            font.pixelSize: 18
        }
        TextField {
            id: droneWeightInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: loadWeightLabel
            text: qsTr("Weight of the Load (kg)")
            font.pixelSize: 18
        }
        TextField {
            id: loadWeightInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: wingAreaLabel
            height: 20
            text: "Area of the Wings (m<sup>2</sup>)"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText
        }
        TextField {
            id: wingAreaInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: angleOfAttackLabel
            text: qsTr("Angle of Attack (degrees)")
            font.pixelSize: 18
        }
        TextField {
            id: angleOfAttackInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryWeightLabel
            text: qsTr("Weight of the Battery (kg)")
            font.pixelSize: 18
        }
        TextField {
            id: batteryWeightInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryCapctiyLabel
            text: qsTr("Battery Capacity (Wh)")
            font.pixelSize: 18
        }
        TextField {
            id: batteryCapacityInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

    }

    Grid {
        id: rightParameterGrid
        x: 724
        y: 173
        width: 515
        height: 558
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 40

        Text {
            id: reynoldsNumLabel
            text: qsTr("Reynolds Number")
            font.pixelSize: 18
        }
        TextField {
            id: reynoldsNumInput
            width: 100
            height: 36
            text: qsTr("1000000")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: pressureLabel
            text: qsTr("Air Pressure (Pa)")
            font.pixelSize: 18
        }
        TextField {
            id: pressureInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: temperatureLabel
            text: qsTr("Temperature (K)")
            font.pixelSize: 18
        }
        TextField {
            id: temperatureInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: vStabilizerLengthLabel
            text: qsTr("Vertical Stabilizer Length (m)")
            font.pixelSize: 18
        }
        TextField {
            id: vStabilizerLengthInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: vStabilizerThicknessLabel
            text: qsTr("Vertical Stabilizer Thickness (m)")
            font.pixelSize: 18
        }
        TextField {
            id: vStabilizerThicknessInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: fuselageRadiusLabel
            text: qsTr("Fuselage Radius (m)")
            font.pixelSize: 18
        }
        TextField {
            id: fuselageRadiusInput
            width: 80
            height: 36
            text: qsTr("0")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: motorTableLabel
            text: qsTr("File Path to Motor Table")
            font.pixelSize: 18
        }
        TextField {
            id: motorTableInput
            width: 220
            height: 36
            text: qsTr("/path/to/MotorTable.csv")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        CheckBox {
            id: checkBox
            text: qsTr("Use Non-Ideal Conditions?")
            font.pixelSize: 18
            leftPadding: 0
        }

      }

    Image {
        id: epJrE5C6_400x400
        x: 0
        y: 0
        width: 150
        height: 150
        source: "images/EpJrE5C6_400x400.png"
        fillMode: Image.PreserveAspectFit
    }

    Button {
        id: estimateButton
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
        x: 555
        y: 13
        text: qsTr("Drone Analysis App")
        font.pixelSize: 24
    }




}
