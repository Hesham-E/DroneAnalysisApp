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

    IntroductionPage {
        id: introPage
        objectName: "introPage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: true
    }

    MissionTypePage {
        id: missionTypePage
        objectName: "missionTypePage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: false
    }

    MissionParametersPage {
        id: missionParamtersPage
        objectName: "missionParamtersPage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: false
    }

    MissionProfilePage {
        id: missionProfilePage
        objectName: "missionProfilePage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: false
    }

    DroneParametersPage {
        id: droneParametersPage
        objectName: "droneParametersPage"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        visible: false
    }

    PopupPage {
        id: popupPage
        objectName: "popupPage"
        anchors.centerIn: parent
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
