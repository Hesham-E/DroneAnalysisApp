//import QtQuick
//import QtQuick.Window
//import QtQuick.Controls
//import QtQuick.Controls.Universal

//Grid {
//    id: grid
//    x: 151
//    y: 88
//    width: 338
//    height: 354
//    verticalItemAlignment: Grid.AlignVCenter
//    horizontalItemAlignment: Grid.AlignLeft
//    layoutDirection: Qt.LeftToRight
//    flow: Grid.LeftToRight
//    columns: 2
//    spacing: 30
//    columnSpacing: 100

//    Text {
//        id: text1
//        text: qsTr("Wing Span (m)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput1
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//    Text {
//        id: text2
//        textFormat: Text.RichText
//        text: qsTr("Drag Coeffcient (C<sub>d</sub>)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput2
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//    Text {
//        id: text3
//        text: qsTr("Total Vertical Thrust (N)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput3
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//    Text {
//        id: text4
//        text: qsTr("Total Horizontal Thrust (N)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput4
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//    Text {
//        id: text5
//        text: qsTr("VTOL Propeller Diameter (cm)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput5
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//    Text {
//        id: text6
//        text: qsTr("VTOL Propeller Size (cm)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput6
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//    Text {
//        id: text7
//        text: qsTr("VTOL Propeller Pitch (cm)")
//        font.pixelSize: 12
//    }
//    TextField {
//        id: textInput7
//        width: 80
//        height: 24
//        text: qsTr("0")
//        font.pixelSize: 12
//        horizontalAlignment: Text.AlignHCenter
//    }

//}

//Image {
//    id: epJrE5C6_400x400
//    x: 0
//    y: 0
//    width: 109
//    height: 113
//    source: "images/EpJrE5C6_400x400.png"
//    fillMode: Image.PreserveAspectFit
//}

//Button {
//    id: button
//    x: 480
//    y: 448
//    width: 147
//    height: 24
//    text: qsTr("Estimate Parameters")
//    icon.color: "#000000"
//}

//Text {
//    id: text8
//    x: 235
//    y: 18
//    text: qsTr("Drone Analysis App")
//    font.pixelSize: 20
//}
