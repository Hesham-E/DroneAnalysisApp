import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Universal

Item {
    id: missionProfilePage
    width: 1280
    height: 960
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
        x: 25
        y: 338
        width: 400
        source: "images/MissionProfile1.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectOneButton
        objectName: "selectOneButton"
        x: 121
        y: 529
        width: 208
        height: 36
        text: qsTr("Select Profile #1")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Image {
        id: imageProfile2
        objectName: "imageProfile2"
        x: 440
        y: 338
        width: 400
        source: "images/MissionProfile2.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectTwoButton
        objectName: "selectTwoButton"
        x: 536
        y: 529
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
        y: 342
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
        x: 231
        y: 625
        width: 400
        source: "images/MissionProfile4.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectFourButton
        objectName: "selectFourButton"
        x: 327
        y: 822
        width: 208
        height: 36
        text: qsTr("Select Profile #4")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Image {
        id: imageProfile5
        objectName: "imageProfile5"
        x: 646
        y: 625
        width: 400
        source: "images/MissionProfile5.png"
        fillMode: Image.PreserveAspectFit
    }
    Button {
        id: selectFiveButton
        objectName: "selectFiveButton"
        x: 742
        y: 822
        width: 208
        height: 36
        text: qsTr("Select Profile #5")
        icon.color: "#000000"
        font.pixelSize: 18
    }

    Button {
        id: createOwnButton
        objectName: "createOwnButton"
        x: 1006
        y: 899
        width: 241
        height: 36
        text: qsTr("Create Own Mission Profile")
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
        model: ["Performance", "Efficicent", "Minimum"]
    }
}
