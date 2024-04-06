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
        typeBackButton = self.typeWindow.findChild(QObject, "returnButton")
        payloadButton.clicked.connect(self.selectPayloadDelivery)
        surveillanceButton.clicked.connect(self.selectSurveillance)
        typeBackButton.clicked.connect(self.goBackType)
        # End mission type window configuration

        # Start mission parameter window configuration
        parameterContinueButton = self.parameterWindow.findChild(QObject, "continueButton")
        parameterReturnButton = self.parameterWindow.findChild(QObject, "returnButton")
        parameterContinueButton.clicked.connect(self.confirmParameters)
        parameterReturnButton.clicked.connect(self.goBackParameters)
        # End mission parameter window configuration

        # Start mission profile window configuration
        profileReturnButton = self.profileWindow.findChild(QObject, "returnButton")
        profileReturnButton.clicked.connect(self.goBackProfile)
        profileOneButton = self.profileWindow.findChild(QObject, "selectOneButton")
        profileOneButton.clicked.connect(self.selectProfileOne)
        profileTwoButton = self.profileWindow.findChild(QObject, "selectTwoButton")
        profileTwoButton.clicked.connect(self.selectProfileTwo)
        profileThreeButton = self.profileWindow.findChild(QObject, "selectThreeButton")
        profileThreeButton.clicked.connect(self.selectProfileThree)
        profileFourButton = self.profileWindow.findChild(QObject, "selectFourButton")
        profileFourButton.clicked.connect(self.selectProfileFour)
        # End mission profile window configuration

    def getMission(self):
        mission = Mission(self.missionType, self.missionParameters, self.missionProfile, self.missionPerformance)
        return mission
    
    def selectProfileOne(self):
        self.missionProfile = MissionProfile.VTOL_STRAIGHT
        self.selectProfileHelper()
    
    def selectProfileTwo(self):
        self.missionProfile = MissionProfile.BASIC_FIXED_WING
        
        self.parameterWindow.findChild(QObject, "vtolClimbLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "vtolDescentLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("text", "0")

        self.selectProfileHelper()
    
    def selectProfileThree(self):
        self.missionProfile = MissionProfile.SWEEP
        
        self.parameterWindow.findChild(QObject, "vtolClimbLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "vtolDescentLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("text", "0")

        self.selectProfileHelper()

    def selectProfileFour(self):
        self.missionProfile = MissionProfile.DOUBLE_CRUISE

        self.parameterWindow.findChild(QObject, "vtolDescentLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "cruiseAltitude2Label").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "cruiseAltitude2Input").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "cruiseAltitude2Input").setProperty("text", "0")

        self.selectProfileHelper()

    def selectProfileHelper(self):
        comboBox = self.profileWindow.findChild(QObject, "selectPerformanceInput")
        if comboBox.property("currentText") == "Performance":
            self.missionPerformance = MissionPerformance.PERFORMANCE
        else:
            self.missionPerformance = MissionPerformance.EFFICIENT

        self.profileWindow.setProperty("visible", False)
        self.parameterWindow.setProperty("visible", True)
    
    def goBackProfile(self):
        self.typeWindow.setProperty("visible", True)
        self.profileWindow.setProperty("visible", False)
    
    def goBackParameters(self):
        self.profileWindow.setProperty("visible", True)
        self.parameterWindow.setProperty("visible", False)

        self.parameterWindow.findChild(QObject, "vtolClimbLabel").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "vtolDescentLabel").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "vtolDescentInput").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "vtolClimbLabel").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "vtolClimbInput").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "cruiseAltitude2Label").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "cruiseAltitude2Input").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "cruiseAltitude2Input").setProperty("text", "0")

        self.parameterWindow.findChild(QObject, "loadWeightLabel").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "loadWeightInput").setProperty("visible", False)
        self.parameterWindow.findChild(QObject, "loadWeightInput").setProperty("text", "0")
    
    def goBackType(self):
        introWindow = self.window.findChild(QObject, "introPage")

        self.typeWindow.setProperty("visible", False)
        introWindow.setProperty("visible", True)

    def confirmParameters(self):
        for child in self.parameterWindow.children():
            if "Input" in child.objectName():
                name = child.objectName()[ : -1 * len("Input")]
                try:
                    self.missionParameters[name] = float(child.property("text"))
                except ValueError:
                    self.missionParameters[name] = child.property("text")
        
        self.parameterWindow.setProperty("visible", False)
        self.window.findChild(QObject, "droneParametersPage").setProperty("visible", True)
    
    def selectPayloadDelivery(self):
        self.missionType = MissonType.PAYLOAD_DELIVERY

        self.typeWindow.setProperty("visible", False)

        self.parameterWindow.findChild(QObject, "loadWeightLabel").setProperty("visible", True)
        self.parameterWindow.findChild(QObject, "loadWeightInput").setProperty("visible", True)
        self.profileWindow.setProperty("visible", True)
    
    def selectSurveillance(self):
        self.missionType = MissonType.SURVEILLANCE

        self.typeWindow.setProperty("visible", False)
        self.profileWindow.setProperty("visible", True)