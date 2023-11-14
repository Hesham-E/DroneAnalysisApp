# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtCore import QObject
from functools import partial
from ControllerLayer.ControllerContainer import ControllerContainer

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]

#    estimateButton = window.findChild(QObject, "DronePage").findChild(QObject, "estimateButton")
#    x = lambda obj: obj.setProperty("text", "hi")
#    estimateButton.clicked.connect(partial(x, estimateButton))
#    print(window.findChild(QObject, "DronePage").findChild(QObject, "estimateButton"))
#    for child in window.findChildren(QObject, "DronePage")[0].children():
#        for grandchild in child.children():
#            if "Input" in grandchild.objectName():
#                print(grandchild.objectName())


    controller = ControllerContainer(window)
#    cont.changeButtonText("hello")


    sys.exit(app.exec())
