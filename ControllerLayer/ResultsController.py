from PySide6.QtCore import QObject

from ModelLayer.Mission import *

class ResultsController:
    def __init__(self, window, getModelLayer):
        self.window = window
        self.resultsWindow = window.findChild(QObject, "resultsPage")

        backButton = self.resultsWindow.findChild(QObject, "backButton")
        backButton.clicked.connect(self.goBack)
        csvButton = self.resultsWindow.findChild(QObject, "csvButton")
        csvButton.clicked.connect(self.exportAllResults)

        self.getModelLayer = getModelLayer
    
    def populateResults(self, results, mission):
        #WARNING: mission is passed as a function since enums act funny in Pyside6 and lose their value
        mission = mission()

        for child in self.resultsWindow.children():
            for grandchild in child.children():
                if "Output" in grandchild.objectName():
                    name = grandchild.objectName()[ : -1 * len("Output")]
                    print(name, grandchild.objectName())
                    result = f"{results[name]:.3e}"
                    if result[-4 : ] == "e+00":
                        result = result[ : -4]
                    grandchild.setProperty("text", result)
        

        self.resultsWindow.findChild(QObject, "typeSummary").setProperty("text", str(mission.missionType))
        self.resultsWindow.findChild(QObject, "performanceSummary").setProperty("text", str(mission.performance))
        self.resultsWindow.findChild(QObject, "profileSummary").setProperty("text", str(mission.profile))
        self.resultsWindow.findChild(QObject, "missionDistanceSummary").setProperty("text", str(mission.parameters["missionDistance"]))
        self.resultsWindow.findChild(QObject, "cruiseAltitudeSummary").setProperty("text", str(mission.parameters["cruiseAltitude"]))
        

    def goBack(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        self.resultsWindow

        paramWindow.setProperty("visible", True)
        self.resultsWindow.setProperty("visible", False)

    def exportAllResults(self):
        try:
            modelLayer = self.getModelLayer()
            modelLayer.resultsWriter.exportToCSV("./")
        except:
            self.popupError("An error occured during simulated flight.")

    def popupError(self, e):
        errorWindow = self.window.findChild(QObject, "popupPage")
        errorWindow.findChild(QObject, "popupLabel").setProperty("text", f"{e}")
        errorWindow.open()
