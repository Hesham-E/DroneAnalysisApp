from PySide6.QtCore import QObject

class IntroController:
    def __init__(self, window):
        self.window = window
        self.connectStartButton()
    
    def getStartButton(self):
        startButton = self.window.findChild(QObject, "introPage").findChild(QObject, "startButton")
        return startButton

    def connectStartButton(self):
        startButton = self.window.findChild(QObject, "introPage").findChild(QObject, "startButton")
        startButton.clicked.connect(self.goToParameters)
    
    def goToParameters(self):
        typeWindow = self.window.findChild(QObject, "missionTypePage")
        introWindow = self.window.findChild(QObject, "introPage")

        typeWindow.setProperty("visible", True)
        introWindow.setProperty("visible", False)
