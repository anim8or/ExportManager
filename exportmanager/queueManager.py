from .ExportJobs import*
from .ExportLibrary import *
from PyQt5.QtWidgets  import*
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class exportTaskListItem(QListWidgetItem):
    exportjob = None
    
class TaskQueue():
    EL=ExportLibrary()
    IconList = EL.collectIcons()
    window =None
    tasklist = [] #a list of all the jobs in the queue
    def __init__(self):
        pass

    def MoveTaskUp(self):
        currentRow = self.window.currentRow()
        currentItem=self.window.takeItem(currentRow)
        self.window.insertItem(currentRow - 1, currentItem)

    def MoveTaskDown(self):
        currentRow = self.window.currentRow()
        currentItem=self.window.takeItem(currentRow)
        self.window.insertItem(currentRow + 1, currentItem)
    def DeleteTask(self):
        listItems=self.window.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.window.takeItem(self.window.row(item))
    def runTasks(self):
        for f in self.tasklist:
            f.doJob()
    def addTask(self,Jobname,jobform):
        #QMessageBox.information(QWidget(),"Adding Task", str(jobform[0]))
        task =ExportFactory(jobform[1])
        task.setName(Jobname)
        task.JobIcon = self.IconList[jobform[0]]
        self.tasklist.append(task)
        icon = QIcon(task.JobIcon)
        size = QSize(20, 20)
        newitem = exportTaskListItem(Jobname, self.window)
        newitem.exportjob = task
        newitem.setIcon(icon)
    def refreshTasks(self):
        for i in range(self.window.count()):
            self.window.item(i).setText(self.window.item(i).exportjob.JobName)
        
    def listTasks(self):
        for l in self.tasklist:
            print(l.JobIcon)
      

    def processQueue(self,count) :
        for i in range(self.window.count()):
            self.window.item(i).exportjob.doJob(count)
        





