from PySide6.QtCore import QObject

class IntroController:
    def __init__(self, window):
        self.window = window
        self.connectStartButton()
    
    def connectStartButton(self):
        startButton = self.window.findChild(QObject, "introPage").findChild(QObject, "startButton")
        startButton.clicked.connect(self.goToParameters)
    
    def goToParameters(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        introWindow = self.window.findChild(QObject, "introPage")

        paramWindow.setProperty("visible", True)
        introWindow.setProperty("visible", False)
