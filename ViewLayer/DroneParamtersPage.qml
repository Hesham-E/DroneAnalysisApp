import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: droneParametersPage
    anchors.fill: parent

    Grid {
        id: parameterGrid
        x: 151
        y: 88
        width: 338
        height: 354
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 30
        columnSpacing: 100

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
            id: dragCoefficientLabel
            textFormat: Text.RichText
            text: qsTr("Drag Coeffcient (C<sub>d</sub>)")
            font.pixelSize: 12
        }
        TextField {
            id: dragCoefficientInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: verticalThrustLabel
            text: qsTr("Total Vertical Thrust (N)")
            font.pixelSize: 12
        }
        TextField {
            id: verticalThrustInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: horizontalThrustLabel
            text: qsTr("Total Horizontal Thrust (N)")
            font.pixelSize: 12
        }
        TextField {
            id: horizontalThrustInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: propVTOLDLabel
            text: qsTr("VTOL Propeller Diameter (cm)")
            font.pixelSize: 12
        }
        TextField {
            id: propVTOLDInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: propVTOLSizeLabel
            text: qsTr("VTOL Propeller Size (cm)")
            font.pixelSize: 12
        }
        TextField {
            id: propVTOLSizeInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: propVTOLPitchLabel
            text: qsTr("VTOL Propeller Pitch (cm)")
            font.pixelSize: 12
        }
        TextField {
            id: propVTOLPitchInput
            width: 80
            height: 24
            text: qsTr("0")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
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
