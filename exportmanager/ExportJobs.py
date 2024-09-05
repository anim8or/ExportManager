from ExportLibrary import *
import pprint
                                                         
class ExportJob():
    exportoptions = {}
    def __init__(self,name,form,):
        self.PopulateExportOptions()
    def setIcon(self,iconpath):
        self.JobIcon = iconpath
        pass # we cant pecify a blankj icon by default
    def doJob(self):
        raise NotImplementedError("doJob must be implemented in the subclass")
    def PopulateExportOptions(self):
        self.exportoptions = {
            "fileName": "file.name",
            "filePath": "file.path"
        }

class ExportPNG (ExportJob):
    def __init__(self,name,form):
        super().__init__(name,form)
    def doJob(self):
        #perform the export job here
        print("FOOPNG")
    def PopulateExportOptions(self):
        self.exportoptions["alpha"]=True

class ExportSVG (ExportJob):
    def __init__(self,name,form):
        super().__init__(name,form)    
    def doJob(self):
        #perform the export job here
        print("FOOSVG")

test= ExportPNG("testname","png")
test2= ExportSVG("testname","svg")
 
pprint.pprint (test.exportoptions)
pprint.pprint (test2.exportoptions)


test.doJob()
test2.doJob()

