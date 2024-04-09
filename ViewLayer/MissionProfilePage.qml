import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

import "."

Item {
    id: missionProfilePage
    width: Style.screenWidth
    height: Style.screenHeight
    objectName: "missionProfilePage"
    anchors.fill: parent

    Text {
        id: pageTitle
        objectName: "pageTitle"
        x: 526
        y: 8
        text: qsTr("Select Mission Profile")
        font.pixelSize: 24
    }

    Image {
        id: imageProfile1
        objectName: "imageProfile1"
        x: 53
        y: 337
        width: 345
        height: 190
        source: "images/MissionProfile1.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectOneButton
        objectName: "selectOneButton"
        x: 121
        y: 531
        width: 208
        height: 36
        text: qsTr("Select Profile #1")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Image {
        id: imageProfile2
        objectName: "imageProfile2"
        x: 474
        y: 342
        width: 333
        height: 180
        source: "images/MissionProfile2.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectTwoButton
        objectName: "selectTwoButton"
        x: 536
        y: 531
        width: 208
        height: 36
        text: qsTr("Select Profile #2")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Image {
        id: imageProfile3
        objectName: "imageProfile3"
        x: 850
        y: 374
        width: 400
        source: "images/MissionProfile3.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectThreeButton
        objectName: "selectThreeButton"
        x: 946
        y: 531
        width: 208
        height: 36
        text: qsTr("Select Profile #3")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Image {
        id: imageProfile4
        objectName: "imageProfile4"
        x: 459
        y: 612
        width: 363
        height: 185
        source: "images/MissionProfile4.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectFourButton
        objectName: "selectFourButton"
        x: 536
        y: 811
        width: 208
        height: 36
        text: qsTr("Select Profile #4")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: returnButton
        objectName: "returnButton"
        x: 37
        y: 899
        width: 241
        height: 36
        text: qsTr("Go Back")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Text {
        id: selectPerformanceLabel
        x: 412
        y: 156
        objectName: "selectPerformanceLabel"
        text: qsTr("Desired Performance Profile")
        font.pixelSize: 18
    }
    ComboBox {
        id: selectPerformanceInput
        objectName: "selectPerformanceInput"
        x: 651
        y: 152
        width: 142
        height: 32
        model: ["Performance", "Efficient"]
    }
}
