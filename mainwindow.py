import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.uic import loadUi
from sympy import true

from medieItem import MedieItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('qt_assets/mainwindow.ui', self)
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
        # self.itemScrollArea.installEventFilter(self) 
        # self.itemScrollArea.setAcceptDrops(True)

        # signals
        self.pushButton.clicked.connect(self.addItem) 

    # def eventFilter(self, o, e):
    #     if (o.objectName() == "itemScrollArea"):
    #         if e.type() == QtCore.QEvent.DragEnter:
    #             self.itemDragEnterEvent(e)
    #             return True
    #         if e.type() == QtCore.QEvent.Drop:
    #             self.itemDropEvent(e)
    #             return True

    #     return super().eventFilter(o, e)

    # def itemDragEnterEvent(self, event):
    #     print("drag")
    #     if event.mimeData().hasUrls():
    #         event.accept()
    #     else:
    #         event.ignore()
    
    # def itemDropEvent(self, event):
    #     print("drop")
    #     print(event.mimeData.urls().path())


    def dragEnterEvent(self, event):
        print("drag")
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        print("drop")
        print(event.mimeData.urls().path())

    def addItem(self, b):
        widget = MedieItem(self)
        self.vbox.addWidget(widget)
           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
