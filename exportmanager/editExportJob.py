from PyQt5.QtWidgets  import*
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
class EditScreen(QMainWindow):
    def __init__(self):
        super(EditScreen,self).__init__()
        self.setWindowTitle("EDIT JOB")
        self.file_path = os.path.realpath(__file__)
        uic.loadUi(os.path.dirname(__file__)+"/Krita_exporter_Editjob.ui", self) # Load the .ui file
        #mainWidget = EditScreen()
        #self.setWidget(mainWidget)
        self.show()
        #connect UI elements
                   

