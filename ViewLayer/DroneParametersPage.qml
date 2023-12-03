import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal
import QtQuick.Dialogs
import QtCore


Item {
    id: droneParametersPage
    width: 1280
    height: 960
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
        spacing: 35
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
            id: airFoilLabel
            objectName: "airFoilLabel"
            text: qsTr("Airfoil Shape (NACA Shape)")
            font.pixelSize: 18
        }
        ComboBox {
            id: airFoilInput
            objectName: "airFoilInput"
            width: 90
            height: 36
            font.pixelSize: 18
            model: ["2408", "23012", "23018"]
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
            id: fuselageLengthLabel
            objectName: "fuselageLengthLabel"
            text: qsTr("Fuselage Length (m)")
            font.pixelSize: 18
        }
        TextField {
            id: fuselageLengthInput
            objectName: "fuselageLengthInput"
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



    }

    Grid {
        id: middleParameterGrid
        objectName: "middleParameterGrid"
        x: 403
        y: 106
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 35
        columnSpacing: 30

        Text {
            id: reynoldsNumLabel
            objectName: "reynoldsNumLabel"
            text: qsTr("Reynolds Number")
            font.pixelSize: 18
        }
        ComboBox {
            id: reynoldsNumInput
            objectName: "reynoldsNumInput"
            width: 125
            height: 36
            font.pixelSize: 18
            model: ["50000", "100000", "200000", "500000", "1000000"]
        }

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

        Text {
            id: ascentDescentSpeedLabel
            objectName: "ascentDescentSpeedLabel"
            text: qsTr("Desired Ascent and Descent Speed (m/s)")
            font.pixelSize: 18
        }
        TextField {
            id: ascentDescentSpeedInput
            objectName: "ascentDescentSpeedInput"
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
        Button {
            id: cruiseMotorTableButton
            text: qsTr("Choose Table...")
            width: 100
            font.pixelSize: 12
            onClicked: cruiseMotorTablePathInput.open()
        }
        FileDialog {
            id: cruiseMotorTablePathInput
            objectName: "cruiseMotorTablePathInput"
//            currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
            onAccepted: {
                cruiseMotorTableButton.text = selectedFile
            }
        }

        Text {
            id: vtolMotorTableLabel
            objectName: "vtolMotorTableLabel"
            text: qsTr("File Path to VTOL Motor Table")
            font.pixelSize: 18
        }
        Button {
            id: vtolMotorTableButton
            text: qsTr("Choose Table...")
            width: 100
            font.pixelSize: 12
            onClicked: vtolMotorTablePathInput.open()
        }
        FileDialog {
            id: vtolMotorTablePathInput
            objectName: "vtolMotorTablePathInput"
//            currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
            onAccepted: {
                vtolMotorTableButton.text = selectedFile
            }
        }

      }

    Grid {
        id: rightParameterGrid
        objectName: "rightParameterGrid"
        x: 848
        y: 364
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 35
        columnSpacing: 30


        Text {
            id: maxSpeedLabel
            objectName: "maxSpeedLabel"
            text: qsTr("(WIP) Desired Max Speed (m/s)")
            font.pixelSize: 18
        }
        TextField {
            id: maxSpeedInput
            objectName: "maxSpeedInput"
            width: 80
            height: 36
            text: qsTr("1")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

    }
    Switch {
        id: switch1
        x: 1003
        y: 297
        text: qsTr("(WIP) Predict Design")
        font.pixelSize: 18
    }

    Label {
        id: label
        x: 893
        y: 300
        width: 110
        height: 31
        text: qsTr("Predict Speed")
        font.pixelSize: 18
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
        id: generateResultsButton
        objectName: "generateResultsButton"
        x: 643
        y: 896
        width: 214
        height: 36
        text: qsTr("Generate Results")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: updateButton
        objectName: "updateButton"
        x: 406
        y: 896
        width: 219
        height: 36
        text: qsTr("(WIP) Update Parameters")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: returnButton
        objectName: "returnButton"
        x: 17
        y: 896
        width: 208
        height: 36
        text: qsTr("Go Back")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Text {
        id: pageTitle
        objectName: "pageTitle"
        x: 545
        y: 8
        text: qsTr("Drone Parameters")
        font.pixelSize: 24
    }
}
