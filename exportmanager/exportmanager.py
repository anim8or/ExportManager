#BBD's Krita Script Starter Feb 2018
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase
from PyQt5.QtWidgets  import*
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from .queueManager import *
from .editExportJob import EditScreen
#from .ExportLibrary import *
DOCKER_NAME = 'ExportManager'
DOCKER_ID = 'pykrita_exportmanager'



class QtUI(QMainWindow):
    iconlist = {}
    def openEditWindow(self):
        self.editWindow = QMainWindow()
        self.ui = EditScreen()
        #self.ui.setupUi(self.editWindow)
        #self.editWindow.show()
        EditScreen()

        
    def popup(self):
        QMessageBox.information(QWidget(),"popup example", "Get files")
    def AddJob(self):
        if self.lineEdit.text():
            self.QM.addTask(self.lineEdit.text(),self.comboBox.currentText())
            self.lineEdit.clear()
    def MoveJobUp(self):
        QMessageBox.information(QWidget(),"popup example", "move Job up")
    def MoveJobDown(self):
        QMessageBox.information(QWidget(),"popup example", "move Job down")
    def DeleteJob(self):
        QMessageBox.information(QWidget(),"popup example", "Delete Job")
    def RunQueue(self):
        QMessageBox.information(QWidget(),"popup example", "Run Queue")
    def populateJobTypes(self):
        #reads the icons and
        pass
        formatList = ["bmp", "gif","ico","jpg","pdf","png","psd","tga","tif","tiff","webp"]
        iconpath = os.path.dirname(__file__)+"/icons/"
        filelist = os.listdir(iconpath)
        #iconlist = {}
        for f in filelist:
            self.iconlist[(os.path.splitext((os.path.basename(iconpath+ f)))[0])] =iconpath+ f
  
        icon = QIcon(os.path.dirname(__file__)+"/icons/pdf.svg")
        size = QSize(20, 20) 
        # setting icon size 
        self.comboBox.setIconSize(size) 
        self.comboBox.addItems(formatList)
        for i in range(0,self.comboBox.count()):
            icon = QIcon(self.iconlist[self.comboBox.itemText(i)] )
            size = QSize(30, 30) 
            self.comboBox.setItemIcon(i, icon)
    def showItem(self,item):
        #try an open the edit window here
        
        self.statusbar.showMessage(item.exportjob.testval)
        self.openEditWindow()
    def __init__(self):
        super(QtUI,self).__init__()
  
        self.file_path = os.path.realpath(__file__)
        uic.loadUi(os.path.dirname(__file__)+"/Krita_exporter.ui", self) # Load the .ui file
        #self.show()
        #connect UI elements
        self.populateJobTypes()
        self.QM=TaskQueue()
        self.QM.window=self.listWidget
        self.pushButton.clicked.connect(self.popup)
        self.commandLinkButton.clicked.connect(self.AddJob)
        self.pushButton_2.clicked.connect(self.MoveJobUp)
        self.pushButton_3.clicked.connect(self.DeleteJob)
        self.pushButton_4.clicked.connect(self.MoveJobDown)
        self.commandLinkButton_2.clicked.connect(self.RunQueue)
        #self.statusbar.showMessage(str(type(self.QM.IconList)));  
        self.listWidget.itemDoubleClicked.connect(self.showItem)                      

class Exportmanager(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)
        #mainWidget = QWidget(self)
        mainWidget = QtUI()
        self.setWidget(mainWidget)
        #uic.loadUi('basic.ui', mainWidget) # Load the .ui file
                   
        #mainWidget.show()
        #examplebutton = QPushButton("show popup",mainWidget)
        #examplebutton.clicked.connect(self.popup)
        #mainWidget.setLayout(QVBoxLayout())
        #mainWidget.layout().addWidget(examplebutton)
    def popup(self):
        QMessageBox.information(QWidget(),"popup example", "hi")
        
    def canvasChanged(self, canvas):
        pass

#comment when deploying to krita
#newui = QtUI()



#un comment when deploying to krita

instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        Exportmanager)

instance.addDockWidgetFactory(dock_widget_factory)
