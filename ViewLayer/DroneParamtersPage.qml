import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: droneParametersPage
    anchors.fill: parent

    Grid {
        id: leftParameterGrid
        x: 8
        y: 119
        width: 296
        height: 354
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 30
        columnSpacing: 50

        Text {
            id: wingSpanLabel
            text: qsTr("Wing Span (m)")
            font.pixelSize: 12
        }
        TextField {
            id: wingSpanInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: droneWeightLabel
            text: "Weight of the Drone (kg)"
            textFormat: Text.RichText
            font.pixelSize: 12
        }
        TextField {
            id: droneWeightInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: loadWeightLabel
            text: qsTr("Weight of the Load (kg)")
            font.pixelSize: 12
        }
        TextField {
            id: loadWeightInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: wingAreaLabel
            height: 20
            text: "Area of the Wings (m<sup>2</sup>)"
            font.pixelSize: 12
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText
        }
        TextField {
            id: wingAreaInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: angleOfAttackLabel
            text: qsTr("Angle of Attack (degrees)")
            font.pixelSize: 12
        }
        TextField {
            id: angleOfAttackInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryWeightLabel
            text: qsTr("Weight of the Battery (kg)")
            font.pixelSize: 12
        }
        TextField {
            id: batteryWeightInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: batteryCapctiyLabel
            text: qsTr("Battery Capacity (Wh)")
            font.pixelSize: 12
        }
        TextField {
            id: batteryCapacityInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }



    }

    Grid {
        id: rightParameterGrid
        x: 322
        y: 119
        width: 300
        height: 91
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 30
        columnSpacing: 40

        Text {
            id: reynoldsNumLabel
            text: qsTr("Reynolds Number")
            font.pixelSize: 12
        }
        TextField {
            id: reynoldsNumInput
            width: 80
            height: 24
            text: qsTr("1000000")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        CheckBox {
            id: checkBox
            text: qsTr("Use Non-Ideal Conditions?")
            font.pixelSize: 12
            leftPadding: 0
        }

      }

    Image {
        id: epJrE5C6_400x400
        x: 0
        y: 0
        width: 109
        height: 113
        source: "images/EpJrE5C6_400x400.png"
        fillMode: Image.PreserveAspectFit
    }

    Button {
        id: estimateButton
        x: 480
        y: 448
        width: 147
        height: 24
        text: qsTr("Estimate Parameters")
        icon.color: "#000000"
    }

    Text {
        id: pageTitle
        x: 235
        y: 18
        text: qsTr("Drone Analysis App")
        font.pixelSize: 20
    }




}
