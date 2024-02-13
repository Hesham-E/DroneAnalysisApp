from PySide6.QtCore import Signal, QObject
from functools import partial

from .DroneParameterController import DroneParameterController
from .ResultsController import ResultsController
from .IntroController import IntroController
from .MissionController import MissionController

class ControllerContainer(QObject):
    resultsReady = Signal()
    
    def __init__(self, window):
        super().__init__() #Calls the QObject constructor such that we can use Signal()
        self.introController = IntroController(window)
        self.missionController = MissionController(window)
        self.droneParameterController = DroneParameterController(window, self.resultsReady, self.missionController.getMission)
        self.resultsController = ResultsController(window, self.droneParameterController.getModelLayer)

        self.resultsReady.connect(partial(self.resultsController.populateResults, self.droneParameterController.getResults(), self.missionController.getMission))

