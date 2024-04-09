from PySide6.QtCore import QObject

class PopupController:
    def __init__(self, window):
        self.window = window
        self.connectConfirmButton()

    def connectConfirmButton(self):
        confirmButton = self.window.findChild(QObject, "popupPage").findChild(QObject, "confirmButton")
        confirmButton.clicked.connect(self.hidePopup)
    
    def hidePopup(self):
        popupWindow = self.window.findChild(QObject, "popupPage")
        popupWindow.close()
