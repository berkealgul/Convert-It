import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QThread
from PyQt5.uic import loadUi

from widgets import *
from converter import Converter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('qt_assets/mainwindow.ui', self)
        self.n_threads = 4
        self.threads = self.createThreads()
        self.setup_ui()   
        self.show()
        
    def setup_ui(self):
        self.setAcceptDrops(True)

        # setting up scroll bar
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)
        self.itemScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.itemScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.itemScrollArea.setWidgetResizable(True)
        self.itemScrollArea.setWidget(self.widget)
        
        self.formatButton.setMenu(FormatMenu(self))

        # signals
        self.convertButton.clicked.connect(self.convert)

    def startConversion(self):
        pass
        #lol

    def assingItemToIdleThread(self):
        for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i).widget()
            if item.converted is False:
                for thread in self.threads:
                    if not thread.isRunning():
                        item.converted = True
                        worker = Worker(item)
                        return

    def convert(self):
        for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i).widget()
            Converter.convert(item)
    
    def setTargetFormat(self, targetFormatAction):
        targetFormat = targetFormatAction.text()
        self.formatButton.setText(targetFormat)
        
        # set global tf
        self.globalTargetFormat = targetFormat

        # set all items tf 
        for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i).widget()
            item.setTargetFormat(targetFormat)
    
    def createThreads(self):
        threads = []
        for i in range(self.n_threads):
            threads.append(QThread())
        return threads

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            widget = MedieItem(self, url.toLocalFile())
            self.vbox.addWidget(widget)    

           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
