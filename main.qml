import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Universal
import "ViewLayer"


Window {
    width: 1280
    height: 960
    visible: true

    StackView {
        id: stack
        initialItem: droneParametersPage
        anchors.fill: parent
    }

    DroneParamtersPage {
        id: droneParamtersPage
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
    }
}
