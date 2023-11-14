from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone

class ResultsController:
    def __init__(self, window):
        self.parameterWindow = window
        self.params = {}

        self.modelLayer = None
