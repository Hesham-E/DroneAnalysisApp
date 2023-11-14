from .ParameterController import ParameterController
from .ResultsController import ResultsController
from .IntroController import IntroController

class ControllerContainer:
    def __init__(self, window):
        self.introController = IntroController(window)
        self.parameterController = ParameterController(window)

#    def changeButtonText(self, text):
#        estimateButton = self.appWindow.findChild(QObject, "DronePage").findChild(QObject, "estimateButton")
#        x = lambda obj: obj.setProperty("text", text)
#        estimateButton.clicked.connect(partial(x, estimateButton))
