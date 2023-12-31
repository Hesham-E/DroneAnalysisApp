from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Mission import *

class MissionController:
    def __init__(self, window):
        self.missionType = 0
        self.missionParameters = {}
        self.missionProfile = 0
        self.missionPerformance = 0

        self.window = window
        self.parameterWindow = window.findChild(QObject, "missionParamtersPage")
        self.profileWindow = window.findChild(QObject, "missionProfilePage")
        self.typeWindow = window.findChild(QObject, "missionTypePage")

        # Start mission type window configuration
        surveillanceButton = self.typeWindow.findChild(QObject, "surveillanceButton")
        payloadButton = self.typeWindow.findChild(QObject, "payloadDeliveryButton")
        allButton = self.typeWindow.findChild(QObject, "allButton")
        payloadButton.clicked.connect(self.selectPayloadDelivery)
        surveillanceButton.clicked.connect(self.selectSurveillance)
        # End mission type window configuration

        # Start mission parameter window configuration
        parameterContinueButton = self.parameterWindow.findChild(QObject, "continueButton")
        parameterReturnButton = self.parameterWindow.findChild(QObject, "returnButton")
        parameterContinueButton.clicked.connect(self.confirmParameters)
        parameterReturnButton.clicked.connect(self.goBackParameters)
        # End mission parameter window configuration

        # Start mission profile window configuration
        profileOneButton = self.profileWindow.findChild(QObject, "selectOneButton")
        profileReturnButton = self.profileWindow.findChild(QObject, "returnButton")
        profileReturnButton.clicked.connect(self.goBackProfile)
        profileOneButton.clicked.connect(self.selectProfileOne)
        # End mission profile window configuration

    def getMission(self):
        mission = Mission(self.missionType, self.missionParameters, self.missionProfile, self.missionPerformance)
        return mission
    
    def selectProfileOne(self):
        self.missionProfile = MissionProfile.VTOL_STRAIGHT
        comboBox = self.profileWindow.findChild(QObject, "selectPerformanceInput")
        
        if comboBox.property("currentText") == "Performance":
            self.missionPerformance = MissionPerformance.PERFORMANCE
        else:
            self.missionPerformance = MissionPerformance.EFFICIENT
        
        self.profileWindow.setProperty("visible", False)
        self.window.findChild(QObject, "droneParametersPage").setProperty("visible", True)

    def goBackProfile(self):
        self.parameterWindow.setProperty("visible", True)
        self.profileWindow.setProperty("visible", False)
    
    def goBackParameters(self):
        self.typeWindow.setProperty("visible", True)
        self.parameterWindow.setProperty("visible", False)

        self.parameterWindow.findChild(QObject, "loadWeightLabel").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "loadWeightInput").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "loadWeightInput").setProperty("text", "0")

    def confirmParameters(self):
        for child in self.parameterWindow.children():
            if "Input" in child.objectName():
                name = child.objectName()[ : -1 * len("Input")]
                try:
                    self.missionParameters[name] = float(child.property("text"))
                except ValueError:
                    self.missionParameters[name] = child.property("text")
        
        self.parameterWindow.setProperty("visible", False)
        self.profileWindow.setProperty("visible", True)
    
    def selectPayloadDelivery(self):
        self.missionType = MissonType.PAYLOAD_DELIVERY

        self.typeWindow.setProperty("visible", False)

        self.parameterWindow.findChild(QObject, "loadWeightLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "loadWeightInput").setProperty("visible", True)
        self.parameterWindow.setProperty("visible", True)
    
    def selectSurveillance(self):
        self.missionType = MissonType.SURVEILLANCE

        self.typeWindow.setProperty("visible", False)
        self.parameterWindow.setProperty("visible", True)