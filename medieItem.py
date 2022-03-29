import os
from turtle import width

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi


class MedieItem(QtWidgets.QWidget):
    def __init__(self, main_window, mediaPath):
        super().__init__()
        loadUi('qt_assets/item.ui', self)

        self.path = os.path.normpath(mediaPath)
        self.name = self.path.split(os.sep)[-1]

        self.main_window = main_window
        self.init_ui()

    
    def init_ui(self):
        self.setMinimumHeight(self.geometry().height())   
        self.setMinimumWidth(self.geometry().width())   

        self.itemlabel.setText(self.name)

        #signals
        self.deleteButton.clicked.connect(self.deleteLater) 

