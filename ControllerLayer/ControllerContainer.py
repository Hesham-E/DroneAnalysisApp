from PySide6.QtCore import QObject
from functools import partial
from .ParameterController import ParameterController

class ControllerContainer:
    def __init__(self, window):
        self.parameterController = ParameterController(window)

#    def changeButtonText(self, text):
#        estimateButton = self.appWindow.findChild(QObject, "DronePage").findChild(QObject, "estimateButton")
#        x = lambda obj: obj.setProperty("text", text)
#        estimateButton.clicked.connect(partial(x, estimateButton))
