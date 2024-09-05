from ExportLibrary import *



                                                         
class ExportJob():
    JobName ="" # a unique identifier for the job
    JobFormat ="" # on output format
    JobIcon =None # an reference to the icon to be displayed in the Queue
    JobOptions = None #all the export options that are required for the job
    Job =None # a function that executes as part of the job
    testval = "letsRock!"
    EL=ExportLibrary()
    Iconlist = EL.collectIcons()


    ExportFilename= ""# a string to override export filename
    ExportLocation= "" # an override to the default export location
    alpha =  False
    compression= 3
    downsample=False
    forceSRGB=True
    indexed= False
    interlaced= False
    saveAsHDR= False
    saveSRGBProfile= False
    storeAuthor= False
    storeMetaData= False
    transparencyFillcolor=[255,255,255]
    quality= 85
    smoothing= 5
    subsampling= 2
    optimize= True
    saveProfile=True
    exportoptions = []
    def __init__(self,name,form,):
    
        self.JobName =name # a unique identifier for the job
        self.JobFormat =form # on output format
        #set up a bunch of export options - we wont need them for every job
        self.exportFilename = "file.name"
        self.ExportLocation = "file.path"
        self.exportoptions.append(self.exportFilename)
        self.exportoptions.append(self.ExportLocation)
        self.alpha =  False
        self.compression= 3
        self.downsample=False
        self.forceSRGB=True
        self.indexed= False
        self.interlaced= False
        self.saveAsHDR= False
        self.saveSRGBProfile= False
        self.storeAuthor= False
        self.storeMetaData= False
        self.transparencyFillcolor=[255,255,255]
        self.quality= 85
        self.smoothing= 5
        self.subsampling= 2
        self.optimize= True
        self.saveProfile=True
        
        self.PopulateExportOptions()
    def setIcon(self,iconpath):
        self.JobIcon = iconpath
        pass # we cant pecify a blankj icon by default
    def doJob(self):
        #perform the export job here
        pass
    def PopulateExportOptions(self):
        pass
class ExportBMP (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOBMP")

class ExportGIF (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOGIF")
class ExportICO (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOICO")
class ExportJPG (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOJPG")
    def PopulateExportOptions(self):
        #jpg unique options
        #self.exportoptions=
        self.exportoptions.append(self.quality)
        self.exportoptions.append(self.smoothing)
        self.exportoptions.append(self.optimize)
        self.exportoptions.append(self.saveProfile)
        self.exportoptions.append(self.transparencyFillcolor)

class ExportPDF (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOPDF")
class ExportPNG (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOPNG")
    def PopulateExportOptions(self):

        self.exportoptions.append(self.alpha)
        self.exportoptions.append(self.downsample)
        self.exportoptions.append(self.forceSRGB)
        self.exportoptions.append(self.indexed)
        self.exportoptions.append(self.interlaced)
        self.exportoptions.append(self.saveAsHDR)
        self.exportoptions.append(self.storeAuthor)
        self.exportoptions.append(self.storeMetaData)
        self.exportoptions.append(self.transparencyFillcolor)
        #png unique options
        #self.exportoptions.extend([self.alpha,self.downsample,self.forceSRGB,self.indexed,self.interlaced,self.saveAsHDR,self.storeAuthor,self.storeMetaData,self.transparencyFillcolor])
        #set some defaults    
class ExportPSD (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOPSD")
class ExportTGA (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOTGA")
class ExportTIF (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOTIF")
class ExportWEBP (ExportJob):
    def doJob(self):
        #perform the export job here
        print("FOOWEBP")


class ExportFactory ():
    joblist={"bmp":ExportBMP("",""),
    "gif":ExportGIF("",""),
    "ico":ExportICO("",""),
    "jpg":ExportJPG("",""),
    "pdf":ExportPDF("",""),
    "png":ExportPNG("",""),
    "psd":ExportPSD("",""),
    "tga":ExportTGA("",""),
    "tif":ExportTIF("",""),
    "webp":ExportWEBP("","")
    }
    def __init__(self):
        pass
    def getjob(self,job):
        return (self.joblist[job])
    
test= ExportBMP("testname","bmp")
test2= ExportICO("testname","ico")
test2.exportFilename = "foooo"
print (test2.exportoptions )
print
print (test.exportoptions)

