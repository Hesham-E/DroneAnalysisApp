from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone
from ModelLayer.ReverseCalculator import ReverseCalculator

class DroneParameterController:
    def __init__(self, window, resultSignal, getMission):
        self.window = window
        self.paramWindow = self.window.findChild(QObject, "droneParametersPage")
        self.resultSignal = resultSignal
        self.results = {}
        self.params = {}
        self.getMission = getMission
        self.designToggled = False

        self.drone = None
        self.reverseCalculator = ReverseCalculator(getMission())

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

        updateButton = self.paramWindow.findChild(QObject, "updateButton")
        updateButton.clicked.connect(self.predictParamteers)
    
    def predictParamteers(self):
        maxSpeed = float( self.paramWindow.findChild(QObject, "maxSpeedInput").property("text") )
        stallSpeed = float( self.paramWindow.findChild(QObject, "stallSpeedInput").property("text") )
        aspectRatio = float( self.paramWindow.findChild(QObject, "aspectRatioInput").property("text") )
        droneMass = float( self.paramWindow.findChild(QObject, "droneWeightInput").property("text") )
        batteryMass = float( self.paramWindow.findChild(QObject, "batteryWeightInput").property("text") )
        loadMass = self.getMission().parameters["loadWeight"]
        mass = droneMass + batteryMass + loadMass

        wingSpan = self.reverseCalculator.calcWingSpan(aspectRatio, stallSpeed, mass)
        wingArea = self.reverseCalculator.calcWingArea(stallSpeed, mass)

        self.paramWindow.findChild(QObject, "wingSpanInput").setProperty("text", round( wingSpan, 2 ) )
        self.paramWindow.findChild(QObject, "wingAreaInput").setProperty("text", round( wingArea, 2 ) )

    def toggleDesign(self):
        self.designToggled = not self.designToggled
        self.paramWindow.findChild(QObject, "rightParameterGrid").setProperty("visible", self.designToggled)

        leftChildren = self.paramWindow.findChild(QObject, "leftParameterGrid").findChildren(QObject)
        if self.designToggled:
            for child in leftChildren:
                if "Label" in child.property("objectName"):
                    child.setProperty("color", "#3f7a23")

            # components that we don't want to be green / we want them to be a special color
            self.paramWindow.findChild(QObject, "droneWeightLabel").setProperty("color", "black")
            self.paramWindow.findChild(QObject, "cruisePropellorDiameterLabel").setProperty("color", "black")
            self.paramWindow.findChild(QObject, "airFoilLabel").setProperty("color", "black")
            self.paramWindow.findChild(QObject, "fuselageRadiusLabel").setProperty("color", "#e6bf40")
            self.paramWindow.findChild(QObject, "fuselageLengthLabel").setProperty("color", "#e6bf40")
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
                    
        try:
            self.drone = Drone(self.params["wingSpan"], self.params["wingArea"],
                                    self.params["airFoil"],
                                    self.params["fuselageRadius"], self.params["fuselageLength"],
                                    self.params["propellorDiameter"],
                                    self.params["droneWeight"],
                                    self.params["angleOfAttack"],
                                    self.params["batteryWeight"], self.params["batteryCapacity"], self.params["batteryVoltage"],
                                    self.params["vtolMotorHeight"], self.params["vtolMotorDiameter"], self.params["vtolPropellorNumber"],
                                    self.params["cruiseMotorTablePath"], self.params["vtolMotorTablePath"],
                                    self.params["auxPowerCon"],
                                    self.params["vtolSpeed"],
                                    self.getMission())
        except Exception as e:
            self.popupError("A critical parameter is missing or incorrect.")


        print(self.params)

    def runSimulations(self):
        self.results["stallSpeed"] = self.drone.calcStallSpeed()
        self.results["minimumCruiseThrustSpeed"] = self.drone.calcEfficientSpeed()
        self.results["maxSpeed"] = self.drone.calcMaxSpeed()
        self.results["lift"] = self.drone.calcLift()
        self.results["liftInducedDrag"] = self.drone.calcLiftInducedDrag()
        self.results["parasiticDrag"] = self.drone.calcParasiticDrag()
        self.results["totalDrag"] = self.drone.calcDrag()

        try:
            self.results["totalRange"] = self.drone.calcMaxRange()
        except Exception as e:
            self.popupError(e)
    
    def getResults(self):
        return self.results

    def goToResults(self):
        resultsWindow = self.window.findChild(QObject, "resultsPage")

        self.paramWindow.setProperty("visible", False)
        resultsWindow.setProperty("visible", True)
        self.resultSignal.emit()
    
    def getModelLayer(self):
        # TODO: move "self.drone out of this class and pass a reference originating from ControllerContainer"
        # Might not be feasible considering we create the object based on data from this page, though

        return self.drone 
    
    def goBack(self):
        profileWindow = self.window.findChild(QObject, "missionParamtersPage")

        profileWindow.setProperty("visible", True)
        self.paramWindow.setProperty("visible", False)
    
    def popupError(self, e):
        errorWindow = self.window.findChild(QObject, "popupPage")
        errorWindow.findChild(QObject, "popupLabel").setProperty("text", f"{e}")
        errorWindow.open()

        
