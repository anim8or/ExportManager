#BBD's Krita Script Starter Feb 2018
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase
from PyQt5.QtWidgets  import*
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from .queueManager import *
from .editExportJob import EditScreen
from .ExportJobs import *
from .ExportLibrary import *
import time
DOCKER_NAME = 'ExportManager'
DOCKER_ID = 'pykrita_exportmanager'
   

class QtUI(QMainWindow):
    iconlist = {}
    def openEditWindow(self,item):
        self.editWindow = QMainWindow()
        self.ui = EditScreen(item)
        #self.ui.setupUi(self.editWindow)
        #self.editWindow.show()
        #EditScreen(item)
        self.ui.setQueueManager(self.QM)
    def setKraDirectoy (self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file:
            self.kra_directory = file
            self.label.setText(file)

    def popup(self):
        QMessageBox.information(QWidget(),"popup example", "Get files")
    def AddJob(self):
        if self.lineEdit.text():
            #QMessageBox.information(QWidget(),"adding job type:", self.comboBox.itemData(self.comboBox.currentIndex()))
            self.QM.addTask(self.lineEdit.text(),self.comboBox.itemData(self.comboBox.currentIndex()))
            self.lineEdit.clear()
    def MoveJobUp(self):
        self.QM.MoveTaskUp()
    def MoveJobDown(self):
        self.QM.MoveTaskDown()
    def DeleteJob(self):
        self.QM.DeleteTask()
    def RunQueue(self):
        #QMessageBox.information(QWidget(),"popup example", "Run Queue")
        if self.kra_directory:
            print(" Processing ",self.kra_directory)
            filecount =len(os.listdir(self.kra_directory))
            start = time.time()
            for count, kra_file  in enumerate(os.listdir(self.kra_directory), start=1 ):
                print ("processing file : " , count , "of ",filecount)
                if kra_file.endswith('.kra'):
                    #process the job queue here
                    kra_path = os.path.join(self.kra_directory, kra_file)
                    newDocument= Krita.instance().openDocument(kra_path)
                    Krita.instance().activeWindow().addView(newDocument)    
                    image= Krita.instance().activeDocument()
                    image.setBatchmode(True) # do not display export dialog box
                    self.QM.processQueue(count)
                    image.setModified(False)
                    image.close() 
        #post running queue, clean up the directory
        test = os.listdir(self.kra_directory)
        for item in test:
            if item.endswith(".kra~"):
                os.remove(os.path.join(self.kra_directory, item))
        end = time.time()
        print('Done. Process took ' + str(end - start) + 'seconds')

    def populateJobTypes(self):
        iconpath = os.path.dirname(__file__)+"/icons/"
        filelist = os.listdir(iconpath)
        availableExport= ExportFactory('list')
        el =ExportLibrary()
        self.iconlist= el.collectIcons()
        for a in availableExport :
            icon= QIcon(self.iconlist[a[1][0]])
            self.comboBox.addItem( icon, a[0],a[1])
   # icon1 = QIcon("/home/parisa/ListWidget/check.png");
    #QListWidgetItem(icon1,"Item 1")
    #listWidget.addItem(newitem)
        #self.comboBox.setIconSize(size) 
       # self.comboBox.addItems(formatList)
       # size = QSize(30, 30) 
       # self.comboBox.setItemIcon(i, icon)
##        for i in range(0,self.comboBox.count()):
##        icon = QIcon(self.iconlist[self.comboBox.itemText(i)] )
##        size = QSize(30, 30) 
##        self.comboBox.setItemIcon(i, icon)
        #formatList = ["bmp", "gif","ico","jpg","pdf","png","psd","tga","tif","tiff","webp","Convert to CYMK"]
        #iconpath = os.path.dirname(__file__)+"/icons/"
        #filelist = os.listdir(iconpath)
        #iconlist = {}
        #for f in filelist:
        #    self.iconlist[(os.path.splitext((os.path.basename(iconpath+ f)))[0])] =iconpath+ f
        # icon = QIcon(os.path.dirname(__file__)+"/icons/pdf.svg")
        #size = QSize(20, 20) 
        # setting icon size 
        #self.comboBox.setIconSize(size) 
        #self.comboBox.addItems(formatList)
        #for i in range(0,self.comboBox.count()):
        #    icon = QIcon(self.iconlist[self.comboBox.itemText(i)] )
        #    size = QSize(30, 30) 
        #    self.comboBox.setItemIcon(i, icon)



            
    def showItem(self,item):
        self.openEditWindow(self.listWidget)

        
    def __init__(self):
        super(QtUI,self).__init__()
        self.kra_directory = ""
        self.file_path = os.path.realpath(__file__)
        uic.loadUi(os.path.dirname(__file__)+"/Krita_exporter.ui", self) # Load the .ui file
        #connect UI elements
        self.populateJobTypes()
        self.QM=TaskQueue()
        self.QM.window=self.listWidget
        self.pushButton.clicked.connect(self.setKraDirectoy)
        self.commandLinkButton.clicked.connect(self.AddJob)
        self.pushButton_2.clicked.connect(self.MoveJobUp)
        self.pushButton_3.clicked.connect(self.DeleteJob)
        self.pushButton_4.clicked.connect(self.MoveJobDown)
        self.commandLinkButton_2.clicked.connect(self.RunQueue)
        self.listWidget.itemDoubleClicked.connect(self.showItem)                      

class Exportmanager(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)
        #mainWidget = QWidget(self)
        mainWidget = QtUI()
        self.setWidget(mainWidget)

    def popup(self):
        QMessageBox.information(QWidget(),"popup example", "hi")
        
    def canvasChanged(self, canvas):
        pass


instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        Exportmanager)

instance.addDockWidgetFactory(dock_widget_factory)
