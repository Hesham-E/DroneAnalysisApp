from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone
from .ResultsController import ResultsController

class ParameterController:
    def __init__(self, window):
        self.window = window
        self.params = {}
        self.results = {}

        self.modelLayer = None

        self.connectEstimationButton()
    
    def connectEstimationButton(self):
        estimateButton = self.window.findChild(QObject, "droneParametersPage").findChild(QObject, "estimateButton")
        estimateButton.clicked.connect(self.collectParameters)
        estimateButton.clicked.connect(self.runSimulations)
        estimateButton.clicked.connect(self.goToResults)
    
    def collectParameters(self):
        for child in self.window.findChildren(QObject, "droneParametersPage")[0].children():
            for grandchild in child.children():
                if "Input" in grandchild.objectName():
                    name = grandchild.objectName()[ : -1 * len("Input")]
                    try:
                        self.params[name] = float(grandchild.property("text"))
                    except ValueError:
                        self.params[name] = grandchild.property("text")
        
        self.modelLayer = Drone(self.params["wingSpan"], self.params["wingArea"], self.params["wingThickness"],
                                self.params["vStabilizerLength"], self.params["vStabilizerThickness"],
                                self.params["fuselageRadius"],
                                self.params["droneWeight"], self.params["loadWeight"],
                                self.params["angleOfAttack"],
                                self.params["batteryWeight"], self.params["batteryCapacity"], self.params["batteryVoltage"],
                                self.params["targetAltitude"],
                                self.params["motorTablePath"])

        print(self.params)

    def runSimulations(self):
        temp = self.params['temperature']
        pressure = self.params['pressure']

        self.results['stallSpeed'] = self.modelLayer.calcStallSpeed(pressure, temp)
        self.results['maxSpeed'] = self.modelLayer.calcMaxSpeed(pressure, temp)
        self.results['lift'] = self.modelLayer.calcLift(pressure, temp)
        self.results['liftInducedDrag'] = self.modelLayer.calcLiftInducedDrag(pressure, temp)
        self.results['parasiticDrag'] = self.modelLayer.calcParasiticDrag(pressure, temp)
        self.results['totalDrag'] = self.modelLayer.calcDrag(pressure, temp)

    def goToResults(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        resultsWindow = self.window.findChild(QObject, "resultsPage")

        paramWindow.setProperty("visible", False)
        resultsWindow.setProperty("visible", True)

        self.resultsController = ResultsController(self.window, self.results)
