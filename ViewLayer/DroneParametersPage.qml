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

            property string tip: "The total wing span from tip to tip. Used in drag, lift, and various other calculations."
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
            text: qsTr("2.2")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: droneWeightLabel
            objectName: "droneWeightLabel"
            text: "Weight of the Drone (kg)"
            textFormat: Text.RichText
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The dry weight of the drone (excluding the battery and payload). Used in thrust and a variety of mechanical calculations."
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
            text: qsTr("6")
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

            property string tip: "The surface area of the wings as viewed from above. Used in drag, lift, and various other calculations."
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
            text: qsTr("0.53")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: airFoilLabel
            objectName: "airFoilLabel"
            text: qsTr("Airfoil Shape (NACA Shape)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The shape of the airfoil based on the available NACA database shapes. Used in drag, lift, and various other calculations."
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

            property string tip: "The radius of the fuselage at its widest point. Used in drag and various other calculations."
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
            text: qsTr("0.1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: fuselageLengthLabel
            objectName: "fuselageLengthLabel"
            text: qsTr("Fuselage Length (m)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The length of the fuselage from tip to tail. Used in drag and various other calculations."
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
            text: qsTr("1.1")
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
            visible: false
        }
        TextField {
            id: angleOfAttackInput
            objectName: "angleOfAttackInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
            visible: false
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
            id: auxPowerConLabel
            objectName: "auxPowerConLabel"
            text: qsTr("Auxiliary Power Consumed (W)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The power consumed by peripheral systems (ICs, boards, etc.) that are not the motors. Used in power calculations."
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
            text: qsTr("10")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryWeightLabel
            objectName: "batteryWeightLabel"
            text: qsTr("Weight of the Battery (kg)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The weight of the battery used to power the drone. Used in thrust and a variety of mechanical calculations."
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

            property string tip: "The capacity of the battery used to power the drone. Used in power and max range calculations."
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
            text: qsTr("6000")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryVoltageLabel
            objectName: "batteryVoltageLabel"
            text: qsTr("Battery Voltage (V)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The voltage of the battery used to power the drone. Used in power and max range calculations."
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
            text: qsTr("22.2")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: vtolSpeedLabel
            objectName: "vtolSpeedLabel"
            text: qsTr("Desired VTOL Speed (m/s)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The desired VTOL ascent/descent speed. Used in flight calculations."
            ToolTip.visible: tip ? vtolSpeedMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: vtolSpeedMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: vtolSpeedInput
            objectName: "vtolSpeedInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("5")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: cruiseMotorTableLabel
            objectName: "cruiseMotorTableLabel"
            text: qsTr("File Path to Cruise Motor Table")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The table containing thrust and power details of the motor / propellor combination to be used. Used in power and thrust calculations."
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

            property string tip: "The table containing thrust and power details of the motor / propellor combination to be used. Used in power and thrust calculations."
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
        x: 901
        y: 319
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 35
        columnSpacing: 30
        visible: false


        Text {
            id: maxSpeedLabel
            objectName: "maxSpeedLabel"
            text: qsTr("Desired Max Speed (m/s)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The desired max speed of the drone. Will be used to predict drone specification parameters in red."
            ToolTip.visible: tip ? maxSpeedMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: maxSpeedMA
                anchors.fill: parent
                hoverEnabled: true
            }
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

        Text {
            id: stallSpeedLabel
            objectName: "stallSpeedLabel"
            text: qsTr("Desired Stall Speed (m/s)")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The desired stall speed of the drone. Will be used to predict drone specification parameters in red."
            ToolTip.visible: tip ? stallSpeedMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: stallSpeedMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: stallSpeedInput
            objectName: "stallSpeedInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: aspectRatioLabel
            objectName: "aspectRatioLabel"
            text: qsTr("Desired Aspect Ratio")
            font.pixelSize: droneParametersPage.bodyFontSize

            property string tip: "The desired aspect ratio of the drone. Will be used to predict drone specification parameters in red."
            ToolTip.visible: tip ? aspectRatioMA.containsMouse : false
            ToolTip.text: tip
            MouseArea {
                id: aspectRatioMA
                anchors.fill: parent
                hoverEnabled: true
            }
        }
        TextField {
            id: aspectRatioInput
            objectName: "aspectRatioInput"
            width: droneParametersPage.inputWidth
            height: droneParametersPage.inputHeight
            text: qsTr("1")
            font.pixelSize: droneParametersPage.bodyFontSize
            horizontalAlignment: Text.AlignHCenter
        }

    }
    Switch {
        id: predictDesignSwitch
        objectName: "predictDesignSwitch"
        x: 1052
        y: 261
        width: 176
        height: 20
        text: qsTr("Predict Design")
        font.pixelSize: droneParametersPage.bodyFontSize

        property string tip: "Switch used to toggle between using drone parameters to predict performance metrics, or vice versa. When predicting parameters, the applicable ones will be in red."
        ToolTip.visible: tip ? predictDesignMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: predictDesignMA
            anchors.fill: parent
            anchors.rightMargin: -40
            anchors.bottomMargin: 2
            anchors.leftMargin: 40
            anchors.topMargin: -2
            hoverEnabled: true
        }
    }

    Label {
        id: predictPerformanceLabel
        objectName: "predictPerformanceLabel"
        x: 893
        y: 259
        width: 110
        height: 24
        text: qsTr("Predict Performance")
        font.pixelSize: droneParametersPage.bodyFontSize

        property string tip: "Switch used to toggle between using drone parameters to predict performance metrics, or vice versa. When predicting parameters, the applicable ones will be in red."
        ToolTip.visible: tip ? predictPerformanceMA.containsMouse : false
        ToolTip.text: tip
        MouseArea {
            id: predictPerformanceMA
            anchors.fill: parent
            anchors.rightMargin: -48
            hoverEnabled: true
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
        text: qsTr("Update Parameters")
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
