import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal
import QtQuick.Dialogs
import QtCore
import "."


Item {
    id: droneParametersPage
    width: Style.screenWidth
    height: Style.screenHeight
    objectName: "droneParametersPage"
    anchors.fill: parent

    property var inputWidth: 90
    property var inputHeight: 36
    property var bodyFontSize: 18

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
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The total wing span from tip to tip."
            ToolTip.visible: tip ? wingSpanMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: wingSpanMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: wingSpanInput
            objectName: "wingSpanInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: droneWeightLabel
            objectName: "droneWeightLabel"
            text: "Weight of the Drone (kg)"
            textFormat: Text.RichText
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The dry weight of the drone (excluding the battery and payload)."
            ToolTip.visible: tip ? droneWeightMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: droneWeightMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: droneWeightInput
            objectName: "droneWeightInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: wingAreaLabel
            objectName: "wingAreaLabel"
            height: 20
            text: "Area of the Wings (m<sup>2</sup>)"
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText

            property string tip: "The surface area of the wings as viewed from above."
            ToolTip.visible: tip ? wingAreaMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: wingAreaMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: wingAreaInput
            objectName: "wingAreaInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: airFoilLabel
            objectName: "airFoilLabel"
            text: qsTr("Airfoil Shape (NACA Shape)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The shape of the airfoil based on the available NACA database shapes."
            ToolTip.visible: tip ? airFoilMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: airFoilMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        ComboBox {
            id: airFoilInput
            objectName: "airFoilInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            font.pixelSize: droneParametersPage.bodyFontSize
            model: ["2408", "23012", "23018"]
        }

        Text {
            id: fuselageRadiusLabel
            objectName: "fuselageRadiusLabel"
            text: qsTr("Fuselage Radius (m)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The radius of the fuselage at its widest point."
            ToolTip.visible: tip ? fuselageRadiusMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: fuselageRadiusMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: fuselageRadiusInput
            objectName: "fuselageRadiusInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: fuselageLengthLabel
            objectName: "fuselageLengthLabel"
            text: qsTr("Fuselage Length (m)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The length of the fuselage from tip to tail."
            ToolTip.visible: tip ? fuselageLengthMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: fuselageLengthMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: fuselageLengthInput
            objectName: "fuselageLengthInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: angleOfAttackLabel
            objectName: "angleOfAttackLabel"
            text: qsTr("Angle of Attack (degrees)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The angle of attack during cruising."
            ToolTip.visible: tip ? angleOfAttackMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: angleOfAttackMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: angleOfAttackInput
            objectName: "angleOfAttackInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
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
            font.pixelSize: droneParametersPage.bodyFontSize
        }
        TextField {
            id: reynoldsNumInput
            objectName: "reynoldsNumInput"
            width: 100
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: auxPowerConLabel
            objectName: "auxPowerConLabel"
            text: qsTr("Auxiliary Power Consumed (W)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The power consumed by peripheral systems (ICs, boards, etc.) that are not the motors."
            ToolTip.visible: tip ? auxPowerConMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: auxPowerConMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: auxPowerConInput
            objectName: "auxPowerConInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryWeightLabel
            objectName: "batteryWeightLabel"
            text: qsTr("Weight of the Battery (kg)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The weight of the battery used to power the drone."
            ToolTip.visible: tip ? batteryWeightMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: batteryWeightMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: batteryWeightInput
            objectName: "batteryWeightInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryCapacityLabel
            objectName: "batteryCapacityLabel"
            text: qsTr("Battery Capacity (mAh)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The capacity of the battery used to power the drone."
            ToolTip.visible: tip ? batteryCapacityMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: batteryCapacityMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: batteryCapacityInput
            objectName: "batteryCapacityInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryVoltageLabel
            objectName: "batteryVoltageLabel"
            text: qsTr("Battery Voltage (V)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The voltage of the battery used to power the drone."
            ToolTip.visible: tip ? batteryVoltageMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: batteryVoltageMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: batteryVoltageInput
            objectName: "batteryVoltageInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: ascentDescentSpeedLabel
            objectName: "ascentDescentSpeedLabel"
            text: qsTr("Desired Ascent and Descent Speed (m/s)")
            font.pixelSize: droneParametersPage.bodyFontSize
        }
        TextField {
            id: ascentDescentSpeedInput
            objectName: "ascentDescentSpeedInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: cruiseMotorTableLabel
            objectName: "cruiseMotorTableLabel"
            text: qsTr("File Path to Cruise Motor Table")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The table containing thrust and power details of the motor / propellor combination to be used."
            ToolTip.visible: tip ? cruiseMotorTableMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: cruiseMotorTableMA
                anchors.fill: parent
                hoverEnabled: true
            }
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
            onAccepted: {
                cruiseMotorTableButton.text = selectedFile
            }
        }

        Text {
            id: vtolMotorTableLabel
            objectName: "vtolMotorTableLabel"
            text: qsTr("File Path to VTOL Motor Table")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The table containing thrust and power details of the motor / propellor combination to be used."
            ToolTip.visible: tip ? vtolMotorTableMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: vtolMotorTableMA
                anchors.fill: parent
                hoverEnabled: true
            }
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
            onAccepted: {
                vtolMotorTableButton.text = selectedFile
            }
        }

      }

    Grid {
        id: rightParameterGrid
        objectName: "rightParameterGrid"
        x: 879
        y: 361
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
            font.pixelSize: droneParametersPage.bodyFontSize
        }
        TextField {
            id: maxSpeedInput
            objectName: "maxSpeedInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

    }
    Switch {
        id: switch1
        x: 1003
        y: 297
        text: qsTr("(WIP) Predict Design")
        font.pixelSize: droneParametersPage.bodyFontSize
    }

    Label {
        id: label
        x: 893
        y: 300
        width: 110
        height: 31
        text: qsTr("Predict Speed")
        font.pixelSize: droneParametersPage.bodyFontSize
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
        height: droneParametersPage.inputHeight
        text: qsTr("Generate Results")
        icon.color: "#000000"
        font.pixelSize: droneParametersPage.bodyFontSize
    }

    Button {
        id: updateButton
        objectName: "updateButton"
        x: 406
        y: 896
        width: 219
        height: droneParametersPage.inputHeight
        text: qsTr("(WIP) Update Parameters")
        icon.color: "#000000"
        font.pixelSize: droneParametersPage.bodyFontSize
    }

    Button {
        id: returnButton
        objectName: "returnButton"
        x: 17
        y: 896
        width: 208
        height: droneParametersPage.inputHeight
        text: qsTr("Go Back")
        icon.color: "#000000"
        font.pixelSize: droneParametersPage.bodyFontSize
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
