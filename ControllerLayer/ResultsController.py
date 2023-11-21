from PySide6.QtCore import QObject

class ResultsController:
    def __init__(self, window):
        self.window = window
        backButton = self.window.findChild(QObject, "resultsPage").findChild(QObject, "backButton")
        backButton.clicked.connect(self.goBack)
    
    def populateResults(self, results):
        for child in self.window.findChildren(QObject, "resultsPage")[0].children():
            for grandchild in child.children():
                if "Output" in grandchild.objectName():
                    name = grandchild.objectName()[ : -1 * len("Output")]
                    print(name, grandchild.objectName())
                    grandchild.setProperty("text", str(results[name]))

    def goBack(self):
        paramWindow = self.window.findChild(QObject, "droneParametersPage")
        resultsWindow = self.window.findChild(QObject, "resultsPage")

        paramWindow.setProperty("visible", True)
        resultsWindow.setProperty("visible", False)
