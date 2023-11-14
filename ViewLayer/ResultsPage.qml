import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: resultsPage
    width: 1280
    height: 960
    objectName: "resultsPage"
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
        x: 536
        y: 17
        text: qsTr("Drone Analysis App")
        font.pixelSize: 24
    }

    Grid {
        id: resultsGrid
        objectName: "resultsGrid"
        x: 44
        y: 106
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 50

        Text {
            id: liftLabel
            objectName: "liftLabel"
            text: qsTr("Wing Span (m)")
            font.pixelSize: 18
        }
        TextField {
            id: liftInput
            objectName: "liftInput"
            width: 80
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: liftInducedDragLabel
            objectName: "liftInducedDragLabel"
            text: qsTr("Wing Thickness (m)")
            font.pixelSize: 18
        }
        TextField {
            id: liftInducedDragInput
            objectName: "liftInducedDragInput"
            width: 80
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: parasiticDragLabel
            objectName: "parasiticDragLabel"
            text: "Weight of the Drone (kg)"
            textFormat: Text.RichText
            font.pixelSize: 18
        }
        TextField {
            id: parasiticDragInput
            objectName: "parasiticDragInput"
            width: 80
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: totalDragLabel
            objectName: "totalDragLabel"
            text: qsTr("Weight of the Load (kg)")
            font.pixelSize: 18
        }
        TextField {
            id: totalDragInput
            objectName: "totalDragInput"
            width: 80
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: stallSpeedLabel
            objectName: "stallSpeedLabel"
            height: 20
            text: "Area of the Wings (m<sup>2</sup>)"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText
        }
        TextField {
            id: stallSpeedInput
            objectName: "stallSpeedInput"
            width: 80
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: maxSpeedLabel
            objectName: "maxSpeedLabel"
            text: qsTr("Angle of Attack (degrees)")
            font.pixelSize: 18
        }
        TextField {
            id: maxSpeedInput
            objectName: "maxSpeedInput"
            width: 80
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

    }
}
