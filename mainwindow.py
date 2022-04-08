import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QThread
from PyQt5.uic import loadUi

from widgets import *


# icons by <aS target="_blank" href="https://icons8.com/icon/KPhFC2OwpbWV/delete">Delete</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('qt_assets/mainwindow.ui', self)
        self.n_convertedItems = 0
        self.setup_ui() 
        self.TEST_CASE() # test case 
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
        # format menu
        self.formatButton.setMenu(FormatMenu(self))
        # thread
        self.converterThread = ConverterThread(self)

        # signals
        self.convertButton.clicked.connect(self.conversionState)
        self.converterThread.finished.connect(self.pickItemToConvert)
        self.converterThread.finished.connect(self.updateProgressBar)
        self.cancelButton.clicked.connect(self.abortConversion)

    def addItem(self, path):
        widget = MediaItem(self, path)
        self.vbox.addWidget(widget)    

    def updateProgressBar(self):
        self.n_convertedItems = self.n_convertedItems+1
        self.conversionProgressBar.setValue(self.n_convertedItems)

    def pickItemToConvert(self):
        for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i).widget()
            if not item.converted:
                item.converted = True
                self.converterThread.startConvertItem(item)
                break # abort after picking
        
        """ for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i).widget()
            print(item.converted) """
        
        # if couldnt find anything we reset the state
        pass # for now

    def abortConversion(self):
        self.converterThread.quit()
        self.idleState()

    # program has two states
    # one is "idle" state user can interact with app normally 
    # on the other hand other state is "conversion" step,
    # this state activates after user starts the conversion process
    # during this state some changes on ui is expected
    def conversionState(self):
        self.convertButton.setEnabled(False)
        self.conversionProgressBar.setMaximum(self.vbox.count())
        self.pickItemToConvert()
    
    # this reverts every changes conversion state does
    def idleState(self):
        self.convertButton.setEnabled(True)
        self.conversionProgressBar.setValue(0)
        self.n_convertedItems = 0
        
    def setTargetFormat(self, targetFormatAction):
        self.setTargetFormatByText(targetFormatAction.text())
    
    def setTargetFormatByText(self, targetFormat):
        self.formatButton.setText(targetFormat)

        # set global tf
        self.globalTargetFormat = targetFormat

        # set all items tf 
        for i in range(self.vbox.count()):
            item = self.vbox.itemAt(i).widget()
            item.setTargetFormat(targetFormat)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.addItem(url.toLocalFile())

    def closeEvent(self, event):
        self.converterThread.quit() # quit worker thread
        return super().closeEvent(event)

    # uitlity function to generate test senario
    # add 3 music files and set target to wav
    def TEST_CASE(self):
        self.addItem("C:\Berke\Portal 2 OST\Portal2-03-FrankenTurrets.mp3")
        self.addItem("C:\Berke\Portal 2 OST\Portal2-05-Excursion_Funnel.mp3")
        self.addItem("C:\Berke\Portal 2 OST\Portal2-06-Overgrowth.mp3")
        self.setTargetFormatByText("wav")
           

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
