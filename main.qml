import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Universal
import "ViewLayer"


Window {
    width: 1280
    height: 960
    visible: true
    id: appWindow
    objectName: "appWindow"

    DroneParametersPage {
        id: droneParametersPage 
        objectName: "droneParametersPage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: true
    }

    ResultsPage {
        id: resultsPage
        objectName: "resultsPage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: false
    }

}
