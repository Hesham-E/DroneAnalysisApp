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
        minCruiseSpeed = float( self.paramWindow.findChild(QObject, "minCruiseSpeedInput").property("text") )
        stallSpeed = float( self.paramWindow.findChild(QObject, "stallSpeedInput").property("text") )
        aspectRatio = float( self.paramWindow.findChild(QObject, "aspectRatioInput").property("text") )
        cruisePropellorDiameter = float( self.paramWindow.findChild(QObject, "cruisePropellorDiameterInput").property("text") )
        vtolPropellorDiameter = float( self.paramWindow.findChild(QObject, "vtolPropellorDiameterInput").property("text") )
        numberOfVTOLPropellors = float( self.paramWindow.findChild(QObject, "vtolPropellorNumberInput").property("text") )
        vtolMotorHeight = float( self.paramWindow.findChild(QObject, "vtolMotorHeightInput").property("text") )
        vtolMotorDiameter = float( self.paramWindow.findChild(QObject, "vtolMotorDiameterInput").property("text") )

        droneMass = float( self.paramWindow.findChild(QObject, "droneWeightInput").property("text") )
        batteryMass = float( self.paramWindow.findChild(QObject, "batteryWeightInput").property("text") )
        loadMass = self.getMission().parameters["loadWeight"]
        mass = droneMass + batteryMass + loadMass

        wingSpan = self.reverseCalculator.calcWingSpan(aspectRatio, stallSpeed, mass)
        wingArea = self.reverseCalculator.calcWingArea(stallSpeed, mass)

        fuselageLength = float( self.paramWindow.findChild(QObject, "fuselageLengthInput").property("text") )
        fuselageRadius = float( self.paramWindow.findChild(QObject, "fuselageRadiusInput").property("text") )
        maxThrust = self.reverseCalculator.calcMaxStaticThrust(maxSpeed, stallSpeed, mass, aspectRatio, cruisePropellorDiameter, numberOfVTOLPropellors, vtolPropellorDiameter, vtolMotorHeight, vtolMotorDiameter, fuselageLength, fuselageRadius)
        if fuselageLength == 0 or fuselageRadius == 0:
            fuselageLength, fuselageRadius = self.reverseCalculator.calcFuselageDimensions(mass, wingArea, aspectRatio, minCruiseSpeed, numberOfVTOLPropellors, vtolPropellorDiameter, vtolMotorHeight, vtolMotorDiameter)

        self.paramWindow.findChild(QObject, "wingSpanInput").setProperty("text", round( wingSpan, 2 ) )
        self.paramWindow.findChild(QObject, "wingAreaInput").setProperty("text", round( wingArea, 2 ) )
        self.paramWindow.findChild(QObject, "fuselageRadiusInput").setProperty("text", round( fuselageRadius, 2 ) )
        self.paramWindow.findChild(QObject, "fuselageLengthInput").setProperty("text", round( fuselageLength, 2 ) )

        maxStaticThrustLabel = self.paramWindow.findChild(QObject, "maxStaticThrustLabel")
        maxStaticThrustOutput = self.paramWindow.findChild(QObject, "maxStaticThrustOutput")
        maxStaticThrustLabel.setProperty("visible", True)
        maxStaticThrustOutput.setProperty("visible", True)
        maxStaticThrustOutput.setProperty("text", round( maxThrust, 2 ) )

    def toggleDesign(self):
        self.designToggled = not self.designToggled
        self.paramWindow.findChild(QObject, "rightParameterGrid").setProperty("visible", self.designToggled)
        self.paramWindow.findChild(QObject, "legendColumn").setProperty("visible", self.designToggled)

        leftChildren = self.paramWindow.findChild(QObject, "leftParameterGrid").findChildren(QObject)
        if self.designToggled:

            # components to turn different colors
            # green for must input/will predict
            # yellow for optional input, must input both if one is selected though
            self.paramWindow.findChild(QObject, "wingSpanLabel").setProperty("color", "#3f7a23")
            self.paramWindow.findChild(QObject, "wingAreaLabel").setProperty("color", "#3f7a23")
            self.paramWindow.findChild(QObject, "fuselageRadiusLabel").setProperty("color", "#e6bf40")
            self.paramWindow.findChild(QObject, "fuselageLengthLabel").setProperty("color", "#e6bf40")
        else:
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
                    
        # try:
        self.drone = Drone(self.params["wingSpan"], self.params["wingArea"],
                                self.params["airFoil"],
                                self.params["fuselageRadius"], self.params["fuselageLength"],
                                self.params["cruisePropellorDiameter"], self.params["vtolPropellorDiameter"],
                                self.params["droneWeight"],
                                self.params["angleOfAttack"],
                                self.params["batteryWeight"], self.params["batteryCapacity"], self.params["batteryVoltage"],
                                self.params["vtolMotorHeight"], self.params["vtolMotorDiameter"], self.params["vtolPropellorNumber"],
                                self.params["cruiseMotorTablePath"], self.params["vtolMotorTablePath"],
                                self.params["auxPowerCon"],
                                self.params["vtolSpeed"],
                                self.getMission())
        # except Exception as e:
        #     self.popupError("A critical parameter is missing or impossible.")


        print(self.params)

    def runSimulations(self):
        self.results["stallSpeed"] = self.drone.calcStallSpeed()
        self.results["minimumCruiseThrustSpeed"] = self.drone.calcEfficientSpeed()
        self.results["maxSpeed"] = self.drone.calcMaxSpeed()
        self.results["lift"] = self.drone.calcLift()
        self.results["liftInducedDrag"] = self.drone.calcLiftInducedDrag()
        self.results["parasiticDrag"] = self.drone.calcParasiticDrag()
        self.results["totalDrag"] = self.drone.calcDrag()
        self.results["maxTakeOffWeight"] = self.drone.calcMaxTakeOffWeight()

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

        
