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
        width: 506
        height: 466
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
            text: qsTr("Lift (N)")
            font.pixelSize: 18
        }
        Text {
            id: liftOutput
            objectName: "liftOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: liftInducedDragLabel
            objectName: "liftInducedDragLabel"
            text: qsTr("Lift Induced Drag (N)")
            font.pixelSize: 18
        }
        Text {
            id: liftInducedDragOutput
            objectName: "liftInducedDragOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: parasiticDragLabel
            objectName: "parasiticDragLabel"
            text: "Parasitic Drag (N)"
            textFormat: Text.RichText
            font.pixelSize: 18
        }
        Text {
            id: parasiticDragOutput
            objectName: "parasiticDragOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: totalDragLabel
            objectName: "totalDragLabel"
            text: qsTr("Total Drag (N)")
            font.pixelSize: 18
        }
        Text {
            id: totalDragOutput
            objectName: "totalDragOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: stallSpeedLabel
            objectName: "stallSpeedLabel"
            height: 20
            text: "Stall Speed (m/s)"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText
        }
        Text {
            id: stallSpeedOutput
            objectName: "stallSpeedOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: maxSpeedLabel
            objectName: "maxSpeedLabel"
            text: qsTr("Maximum Speed (m/s)")
            font.pixelSize: 18
        }
        Text {
            id: maxSpeedOutput
            objectName: "maxSpeedOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: totalRangeLabel
            objectName: "totalRangeLabel"
            text: qsTr("Total Range (m)")
            font.pixelSize: 18
        }
        Text {
            id: totalRangeOutput
            objectName: "totalRangeOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
        }

    }
}
