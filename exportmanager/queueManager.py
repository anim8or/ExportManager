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
    #IconList ={"FOO":"bmplocatioN"}
    window =None
    tasklist = [] #a list of all the jobs in the queue
    def __init__(self):
        pass

                #self.Combobox = window
    def MoveTaskUp(self,initialIndex):
        if initialIndex >0:
            element = self.tasklist.pop(initialIndex)        
            new_position = initialIndex-1
            self.tasklist.insert(new_position, element)

    def MoveTaskDown(self,initialIndex):
        if initialIndex < len(self.tasklist):
            element = self.tasklist.pop(initialIndex)        
            new_position = initialIndex+1
            self.tasklist.insert(new_position, element)
    def DeleteTask(self,initialIndex):
        self.tasklist.pop(initialIndex)
    def runTasks(self):
        for f in self.tasklist:
            f.doJob()
    def addTask(self,Jobname,jobform):
        ef =ExportFactory()
        task = ef.getjob(jobform)
        task.JobName = Jobname
        task.JobFormat = jobform
        task.JobIcon = self.IconList[jobform]
        self.tasklist.append(task)
        icon = QIcon(task.JobIcon)
        size = QSize(20, 20)
        newitem = exportTaskListItem(Jobname, self.window)
        newitem.exportjob = task
        newitem.setIcon(icon)
    def listTasks(self):
        for l in self.tasklist:
            print(l.JobIcon)
      






test = TaskQueue()

#test.addTask("TESTjob","bmp","bmp")


