import os
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from converter import *


class MediaItem(QWidget):
    def __init__(self, main_window, mediaPath):
        super().__init__()
        loadUi('qt_assets/item.ui', self)
        self.path = os.path.normpath(mediaPath)
        self.main_window = main_window
        self.converted = False
        self.conversionError = None

        self.completedPixMap = QPixmap("icons/ok.png")
        self.completedIcon = QIcon(self.completedPixMap)
        self.idleIcon = QIcon()
        self.errorIcon = QIcon(QPixmap("icons/error.png"))
        self.convertingIcon = QIcon(QPixmap("icons/clock.png"))
        
        self.processPath()
        self.init_ui()

    def getMediaPixmap(self):
        mediaType = formatType(self.format)
        if mediaType == "Image":
            return QPixmap("icons/image.png")
        elif mediaType == "Audio":
            return QPixmap("icons/audio.png")
        elif mediaType == "Video":
            return QPixmap("icons/video.png")
        else:
            return QPixmap("icons/image.png") # default icon to not crash the app

    def getDir(self, splittedPath):
        dir = ""
        for p in splittedPath:
            dir += p + "\\"
        return dir

    def processPath(self):
        splittedPath = self.path.split(os.sep)
        self.dir = self.getDir(splittedPath[:-1])
        mediaName = splittedPath[-1]
        self.format = mediaName.split(".")[-1]
        self.name = mediaName.split(".")[0]

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

        self.statusIconButton.setEnabled(False)
        self.statusIconButton.setIcon(self.idleIcon)
        self.statusIconButton.setFixedSize(self.completedPixMap.rect().size()/3)
        self.mediaIconLabel.setPixmap(self.getMediaPixmap())
        self.formatLabel.setText(self.getSizeInfo())

        #signals
        self.deleteButton.clicked.connect(self.deleteLater) 
        self.statusIconButton.clicked.connect(self.showError)
    
    def getSizeInfo(self):
        mb = os.path.getsize(self.path) / 1048576
        return str(round(mb, 2)) + " MB" 
    
    def onBeginConversion(self):
        self.statusIconButton.setIcon(self.convertingIcon)

    def showError(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(self.conversionError)
        msg.setWindowTitle("Failed :(")
        msg.exec_()

    def onConverted(self, result, error):
        if result == COMPLETED:
            self.statusIconButton.setEnabled(False)
            self.statusIconButton.setIcon(self.completedIcon)
        else: # in case of error
            self.statusIconButton.setIcon(self.errorIcon)
            self.statusIconButton.setEnabled(True)
            self.conversionError = error

    def setTargetFormat(self, targetFormat):
        self.targetFormat = targetFormat
        

class FormatMenu(QMenu):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        data = formats
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
        self.mediaItem.onBeginConversion()
        result, error = convert(self.mediaItem)
        self.mediaItem.onConverted(result, error)
