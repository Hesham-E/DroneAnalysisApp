from PySide6.QtCore import Signal, QObject
from functools import partial

from .ParameterController import ParameterController
from .ResultsController import ResultsController
from .IntroController import IntroController

class ControllerContainer(QObject):
    resultsReady = Signal()
    
    def __init__(self, window):
        super().__init__()
        self.introController = IntroController(window)
        self.parameterController = ParameterController(window, self.resultsReady)
        self.resultsController = ResultsController(window)
        
        self.resultsReady.connect(partial(self.resultsController.populateResults, self.parameterController.getResults()))
#    def changeButtonText(self, text):
#        estimateButton = self.appWindow.findChild(QObject, "DronePage").findChild(QObject, "estimateButton")
#        x = lambda obj: obj.setProperty("text", text)
#        estimateButton.clicked.connect(partial(x, estimateButton))
