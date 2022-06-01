import os
from turtle import width

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QMenu, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from sympy import Q

from converter import Converter



class MediaItem(QWidget):
    def __init__(self, main_window, mediaPath):
        super().__init__()
        loadUi('qt_assets/item.ui', self)
        self.path = os.path.normpath(mediaPath)
        self.main_window = main_window
        self.converted = False

        self.completedPixMap = QPixmap("icons/ok.png")
        self.completedIcon = QIcon(self.completedPixMap)
        self.idleIcon = QIcon()
        
        self.processPath()
        self.init_ui()

    def getMediaPixmap(self):
        return QPixmap("icons/image.png")

    def processPath(self):
        self.name = self.path.split(os.sep)[-1]
        self.format = None
        self.targetFormat = None

    def init_ui(self):
        self.setMinimumHeight(self.geometry().height())   
        self.setMinimumWidth(self.geometry().width())   

        self.itemlabel.setText(self.name)

        #buttons
        pixmap = QPixmap("icons\\trash.png")
        icon = QIcon(pixmap)
        size = pixmap.rect().size()/3
        self.deleteButton.setIcon(icon)
        self.deleteButton.setIconSize(size)
        self.deleteButton.setFixedSize(size)

        self.statusIconButton.setEnabled(True)
        self.statusIconButton.setIcon(self.idleIcon)
        self.statusIconButton.setFixedSize(self.completedPixMap.rect().size()/3)

        self.mediaIconLabel.setPixmap(self.getMediaPixmap())

        self.formatLabel.setText(self.getSizeInfo())

        #signals
        self.deleteButton.clicked.connect(self.deleteLater) 
    
    def getSizeInfo(self):
        mb = os.path.getsize(self.path) / 1048576
        return str(round(mb, 2)) + " MB" 

    def completed(self):
        self.statusIconButton.setIcon(self.completedIcon)

    def setTargetFormat(self, targetFormat):
        self.targetFormat = targetFormat
        

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


class ConverterThread(QThread):
    def __init__(self, mainWindow):
        super().__init__(parent=mainWindow)

    def startConvertItem(self, mediaItem):
        self.mediaItem = mediaItem
        self.start()

    def run(self):
        Converter.convert(self.mediaItem)
        self.mediaItem.completed()
