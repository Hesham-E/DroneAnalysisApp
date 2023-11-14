from PySide6.QtCore import QObject

import sys
import os
sys.path.append(os.path.abspath('../ModelLayer'))
from ModelLayer.Drone import Drone

class ResultsController:
    def __init__(self, window, results):
        self.window = window
        self.modelLayer = None
        self.results = results
        print(self.results)
        self.populateResults()
    
    def populateResults(self):
        for child in self.window.findChildren(QObject, "resultsPage")[0].children():
            for grandchild in child.children():
                if "Output" in grandchild.objectName():
                    name = grandchild.objectName()[ : -1 * len("Output")]
                    print(name, grandchild.objectName())
                    grandchild.setProperty("text", str(self.results[name]))
