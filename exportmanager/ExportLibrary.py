import os
class ExportLibrary():
    #a collection of functions used by export job and task list
    def __init__(self):
    
        pass
 
    def collectIcons(self):
        #returns a dict of icon name and location
        iconpath = os.path.dirname(__file__)+"/icons/"
        iconpath = iconpath.replace('\\', '/')
        filelist = os.listdir(iconpath)
        iconlist = {}
        for f in filelist:
            iconlist[(os.path.splitext((os.path.basename(iconpath+ f)))[0])] =iconpath+ f
        return(iconlist)
        
