import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal
import "."

Item {
    id: resultsPage
    width: Style.screenWidth
    height: Style.screenHeight
    objectName: "resultsPage"
    anchors.fill: parent

    property var labelSize: 18
    property var outputWidth: 200
    property var outputHeight: 36

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
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: minimumCruiseThrustSpeedOutput
            objectName: "minimumCruiseThrustSpeedOutput"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: stallSpeedLabel
            objectName: "stallSpeedLabel"
            height: 20
            text: "Stall Speed (m/s)"
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText
        }
        Text {
            id: stallSpeedOutput
            objectName: "stallSpeedOutput"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: maxSpeedLabel
            objectName: "maxSpeedLabel"
            text: qsTr("Maximum Speed (m/s)")
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: maxSpeedOutput
            objectName: "maxSpeedOutput"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: totalRangeLabel
            objectName: "totalRangeLabel"
            text: qsTr("Total Range (m)")
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: totalRangeOutput
            objectName: "totalRangeOutput"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
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
        height: resultsPage.outputHeight
        text: qsTr("Go Back")
        icon.color: "#000000"
        font.pixelSize: resultsPage.labelSize
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
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: typeSummary
            objectName: "typeSummary"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: performanceLabel
            objectName: "performanceLabel"
            text: qsTr("Performance Profile")
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: performanceSummary
            objectName: "performanceSummary"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }


        Text {
            id: profileLabel
            objectName: "profileLabel"
            text: qsTr("Mission Profile")
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: profileSummary
            objectName: "profileSummary"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: missionDistanceLabel
            objectName: "missionDistanceLabel"
            text: qsTr("Target Distance (m)")
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: missionDistanceSummary
            objectName: "missionDistanceSummary"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: cruiseAltitudeLabel
            objectName: "cruiseAltitudeLabel"
            text: qsTr("Cruise Altitude (m)")
            font.pixelSize: resultsPage.labelSize
        }
        Text {
            id: cruiseAltitudeSummary
            objectName: "cruiseAltitudeSummary"
            width: resultsPage.outputWidth
            height: resultsPage.outputHeight
            text: qsTr("NA")
            font.pixelSize: resultsPage.labelSize
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
