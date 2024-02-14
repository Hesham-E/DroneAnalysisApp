from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone

class DroneParameterController:
    def __init__(self, window, resultSignal, getMission):
        self.window = window
        self.paramWindow = self.window.findChild(QObject, "droneParametersPage")
        self.resultSignal = resultSignal
        self.results = {}
        self.params = {}
        self.getMission = getMission
        self.designToggled = False

        self.modelLayer = None

        self.connectButtons()
    
    def connectButtons(self):
        estimateButton = self.paramWindow.findChild(QObject, "generateResultsButton")
        estimateButton.clicked.connect(self.collectParameters)
        estimateButton.clicked.connect(self.runSimulations)
        estimateButton.clicked.connect(self.goToResults)

        returnButton = self.paramWindow.findChild(QObject, "returnButton")
        returnButton.clicked.connect(self.goBack)

        predictDesignSwitch = self.paramWindow.findChild(QObject, "predictDesignSwitch")
        predictDesignSwitch.clicked.connect(self.toggleDesign)
    
    def toggleDesign(self):
        self.designToggled = not self.designToggled
        self.paramWindow.findChild(QObject, "rightParameterGrid").setProperty("visible", self.designToggled)

        leftChildren = self.paramWindow.findChild(QObject, "leftParameterGrid").findChildren(QObject)
        if self.designToggled:
            self.paramWindow.findChild(QObject, "batteryCapacityLabel").setProperty("color", "#AD3A1A")

            for child in leftChildren:
                if "Label" in child.property("objectName"):
                    child.setProperty("color", "#AD3A1A")
        else:
            self.paramWindow.findChild(QObject, "batteryCapacityLabel").setProperty("color", "black")

            for child in leftChildren:
                if "Label" in child.property("objectName"):
                    child.setProperty("color", "black")

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
                                self.params["vtolSpeed"],
                                self.getMission())

        print(self.params)

    def runSimulations(self):
        self.results["stallSpeed"] = self.modelLayer.calcStallSpeed()
        self.results["minimumCruiseThrustSpeed"] = self.modelLayer.calcEfficientSpeed()
        self.results["maxSpeed"] = self.modelLayer.calcMaxSpeed()
        self.results["lift"] = self.modelLayer.calcLift()
        self.results["liftInducedDrag"] = self.modelLayer.calcLiftInducedDrag()
        self.results["parasiticDrag"] = self.modelLayer.calcParasiticDrag()
        self.results["totalDrag"] = self.modelLayer.calcDrag()
        self.results["totalRange"] = self.modelLayer.calcMaxRange()
    
    def getResults(self):
        return self.results

    def goToResults(self):
        resultsWindow = self.window.findChild(QObject, "resultsPage")

        self.paramWindow.setProperty("visible", False)
        resultsWindow.setProperty("visible", True)
        self.resultSignal.emit()
    
    def getModelLayer(self):
        # TODO: move "self.modelLayer out of this class and pass a reference originating from ControllerContainer"
        # Might not be feasible considering we create the object based on data from this page, though

        return self.modelLayer 
    
    def goBack(self):
        profileWindow = self.window.findChild(QObject, "missionParamtersPage")

        profileWindow.setProperty("visible", True)
        self.paramWindow.setProperty("visible", False)

        
