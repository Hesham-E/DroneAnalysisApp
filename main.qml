import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Universal
import "ViewLayer"


Window {
    width: 640
    height: 480
    visible: true

    StackView {
        id: stack
        initialItem: droneParametersPage
        anchors.fill: parent
    }

    DroneParamtersPage {
        id: droneParamtersPage
    }
}
