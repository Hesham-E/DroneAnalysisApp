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
        x: 603
        y: 17
        text: qsTr("Results")
        font.pixelSize: 24
    }

    Text {
        id: resultsTitle
        x: 178
        y: 107
        text: qsTr("Cruising Performance")
        font.pixelSize: 20
    }

    Grid {
        id: resultsGrid
        objectName: "resultsGrid"
        x: 44
        y: 150
        width: 494
        height: 573
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 50

        Text {
            id: minimumCruiseThrustSpeedLabel
            objectName: "minimumCruiseThrustSpeedLabel"
            text: qsTr("Minimum Cruise Thrust Speed (m/s)")
            font.pixelSize: 18
        }
        Text {
            id: minimumCruiseThrustSpeedOutput
            objectName: "minimumCruiseThrustSpeedOutput"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
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
            verticalAlignment: Text.AlignVCenter
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
            verticalAlignment: Text.AlignVCenter
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
            verticalAlignment: Text.AlignVCenter
        }

    }

    Button {
        id: backButton
        objectName: "backButton"
        x: 536
        y: 874
        width: 208
        height: 36
        text: qsTr("Go Back")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Text {
        id: summaryTitle
        x: 928
        y: 107
        text: qsTr("Mission Summary")
        font.pixelSize: 20
    }

    Grid {
        id: summaryGrid
        objectName: "summaryGrid"
        x: 790
        y: 150
        width: 444
        height: 397
        verticalItemAlignment: Grid.AlignVCenter
        horizontalItemAlignment: Grid.AlignLeft
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        columns: 2
        spacing: 50
        columnSpacing: 50


        Text {
            id: typeLabel
            objectName: "typeLabel"
            text: qsTr("Mission Type")
            font.pixelSize: 18
        }
        Text {
            id: typeSummary
            objectName: "typeSummary"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: performanceLabel
            objectName: "performanceLabel"
            text: qsTr("Performance Profile")
            font.pixelSize: 18
        }
        Text {
            id: performanceSummary
            objectName: "performanceSummary"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }


        Text {
            id: profileLabel
            objectName: "profileLabel"
            text: qsTr("Mission Profile")
            font.pixelSize: 18
        }
        Text {
            id: profileSummary
            objectName: "profileSummary"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: missionDistanceLabel
            objectName: "missionDistanceLabel"
            text: qsTr("Target Distance (m)")
            font.pixelSize: 18
        }
        Text {
            id: missionDistanceSummary
            objectName: "missionDistanceSummary"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: cruiseHeightLabel
            objectName: "cruiseHeightLabel"
            text: qsTr("Cruise Height (m)")
            font.pixelSize: 18
        }
        Text {
            id: cruiseHeightSummary
            objectName: "cruiseHeightSummary"
            width: 200
            height: 36
            text: qsTr("NA")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Button {
        id: button
        x: 161
        y: 513
        width: 231
        height: 34
        text: qsTr("(WIP) Export Detailed Results")
    }
}
