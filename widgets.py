import os
from turtle import width

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMenu, QAction
from PyQt5.uic import loadUi

from converter import Converter

class MedieItem(QWidget):
    def __init__(self, main_window, mediaPath):
        super().__init__()
        loadUi('qt_assets/item.ui', self)
        self.path = os.path.normpath(mediaPath)
        self.main_window = main_window
        self.processPath()
        self.init_ui()
        self.converted = False
    
    def processPath(self):
        self.name = self.path.split(os.sep)[-1]
        self.format = None
        self.targetFormat = None

    def init_ui(self):
        self.setMinimumHeight(self.geometry().height())   
        self.setMinimumWidth(self.geometry().width())   

        self.itemlabel.setText(self.name)

        #signals
        self.deleteButton.clicked.connect(self.deleteLater) 
    
    def setTargetFormat(self, targetFormat):
        self.targetFormat = targetFormat
        print(self.targetFormat)


class FormatMenu(QMenu):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        data = {"Audio":["mp3", "wav"], "image":["png", "jpeg"]}
        self.setup_menu(data, self)
        self.triggered[QAction].connect(mainWindow.setTargetFormat)

    def setup_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.setup_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.setup_menu(element, menu_obj)
        else:
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)


class Worker(QObject):
    def __init__(self, mediaItem):
        super().__init__()
        self.mediaItem = mediaItem
    def doWork():
        Converter.convert()