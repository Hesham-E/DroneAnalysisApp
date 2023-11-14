from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone

class ParameterController:
    def __init__(self, window):
        self.window = window
        self.params = {}

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
        results = {}

        temp = self.params['temperature']
        pressure = self.params['pressure']

        results['stallSpeed'] = self.modelLayer.calcStallSpeed(pressure, temp)
        results['maxSpeed'] = self.modelLayer.calcMaxSpeed(pressure, temp)
        results['lift'] = self.modelLayer.calcLift(pressure, temp)
        results['liftInducedDrag'] = self.modelLayer.calcLiftInducedDrag(pressure, temp)
        results['parasiticDrag'] = self.modelLayer.calcParasiticDrag(pressure, temp)
        results['totalDrag'] = self.modelLayer.calcDrag(pressure, temp)

        print(results)

    def goToResults(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        resultsWindow = self.window.findChild(QObject, "resultsPage")

        paramWindow.setProperty("visible", False)
        resultsWindow.setProperty("visible", True)
