from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone

class DroneParameterController:
    def __init__(self, window, resultSignal, getMission):
        self.window = window
        self.resultSignal = resultSignal
        self.results = {}
        self.params = {}
        self.getMission = getMission

        self.modelLayer = None

        self.connectButtons()
    
    def connectButtons(self):
        estimateButton = self.window.findChild(QObject, "droneParametersPage").findChild(QObject, "generateResultsButton")
        estimateButton.clicked.connect(self.collectParameters)
        estimateButton.clicked.connect(self.runSimulations)
        estimateButton.clicked.connect(self.goToResults)

        returnButton = self.window.findChild(QObject, "droneParametersPage").findChild(QObject, "returnButton")
        returnButton.clicked.connect(self.goBack)
    
    def collectParameters(self):
        for child in self.window.findChildren(QObject, "droneParametersPage")[0].children():
            for grandchild in child.children():
                if "Input" in grandchild.objectName():
                    name = grandchild.objectName()[ : -1 * len("Input")]

                    if grandchild.property("text") != None: # generic QObject
                        try:
                            self.params[name] = float(grandchild.property("text"))
                        except ValueError:
                            self.params[name] = grandchild.property("text")
                    elif grandchild.property("currentText") != None: # QComboBox
                        try:
                            self.params[name] = float(grandchild.property("currentText"))
                        except ValueError:
                            self.params[name] = grandchild.property("currentText")
                    elif grandchild.property("selectedFile") != None: # FileDialog
                        self.params[name] = grandchild.property("selectedFile").toString()[len("file:///") : ]
                    else:
                        raise Exception("Unrecognized QObject used")
                    
        self.modelLayer = Drone(self.params["wingSpan"], self.params["wingArea"],
                                self.params["airFoil"],
                                self.params["fuselageRadius"], self.params["fuselageLength"],
                                self.params["droneWeight"],
                                self.params["angleOfAttack"],
                                self.params["reynoldsNum"],
                                self.params["batteryWeight"], self.params["batteryCapacity"], self.params["batteryVoltage"],
                                self.params["cruiseMotorTablePath"], self.params["vtolMotorTablePath"],
                                self.params["auxPowerCon"],
                                self.params["ascentDescentSpeed"],
                                self.getMission())

        print(self.params)

    def runSimulations(self):
        self.results["stallSpeed"] = self.modelLayer.calcStallSpeed()
        self.results["maxSpeed"] = self.modelLayer.calcMaxSpeed()
        self.results["lift"] = self.modelLayer.calcLift()
        self.results["liftInducedDrag"] = self.modelLayer.calcLiftInducedDrag()
        self.results["parasiticDrag"] = self.modelLayer.calcParasiticDrag()
        self.results["totalDrag"] = self.modelLayer.calcDrag()
        self.results["totalRange"] = self.modelLayer.calcMaxRange()
    
    def getResults(self):
        return self.results

    def goToResults(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        resultsWindow = self.window.findChild(QObject, "resultsPage")

        paramWindow.setProperty("visible", False)
        resultsWindow.setProperty("visible", True)
        self.resultSignal.emit()
    
    def goBack(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        profileWindow = self.window.findChild(QObject, "missionProfilePage")

        profileWindow.setProperty("visible", True)
        paramWindow.setProperty("visible", False)

        
