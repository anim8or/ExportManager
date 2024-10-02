from .ExportLibrary import *
from krita import *

class ExportJob:
    def __init__(self):
        
        # These should be instance attributes
        self.JobName = ""  # a unique identifier for the job
        self.JobFormat = ""  # output format
        self.jobType = ""  # identifier for the format
        self.jobtitle = ""  # a description of the job (export to .bmp, etc.)
        self.JobIcon = None  # a reference to the icon to be displayed in the queue
        self.JobOptions = None  # all the export options required for the job
        self.Job = None  # a function that executes as part of the job
        self.testval = "letsRock!"
        self.EL = ExportLibrary()
        self.Iconlist = self.EL.collectIcons()  # calling EL method
        self.ExportFilename = ""  # override export filename
        self.ExportLocation = ""  # override default export location
        self.exportoptions = {
            "fileName": "",
            "filePath": ""
        }  # This is now an instance-specific dictionary
        def __new__(cls, *args, **kwargs):
            instance = super(ExportJob, cls).__new__(cls)
            return instance
        def __init__(self):
            pass
    def setName(self,name):
        self.JobName =name
    def setIcon(self,iconpath):
        self.JobIcon = iconpath
        pass # we cant pecify a blankj icon by default
    def doJob(self,index):
        raise NotImplementedError("doJob must be implemented in the subclass")



class ExportBMP (ExportJob):
    
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "bmp"
        self.jobtitle ="Export to .bmp"
        self.JobFormat = "bmp"
    def doJob(self, index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject()) 

class ExportGIF (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "gif"
        self.jobtitle ="Export to .gif"
        self.JobFormat = "gif"
    def doJob(self, index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject()) 

class ExportICO (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "ico"
        self.jobtitle ="Export to .ico"
        self.JobFormat = "ico"
    def doJob(self, index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject())
        
class ExportJPG (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "jpg"
        self.jobtitle ="Export to .jpg"
        self.JobFormat = "jpg"
        self.exportoptions.update({
        "quality":85,
        "smoothing":5,
        "optimize":True,
        "saveProfile":True,
        "transparencyFillcolor":[255,255,255]
        })
    def doJob(self, index):
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        jpgOptions=InfoObject()
        #populate an export options using the objects dict
        for opt in self.exportoptions.keys():
            # validate the key - we dont want the filename or filepath at this time
            if opt !=  "fileName" or opt != "filePath":
                jpgOptions.setProperty(opt, self.exportoptions[opt])
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] !="":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + index +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,jpgOptions)                                  
            


class ExportPDF(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "pdf"
        self.jobtitle ="Export to .pdf"
        self.JobFormat = "pdf"
    def doJob(self,index):
        #perform the export job here
        print("FOOPDF")
        
class ExportPNG (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "png"
        self.jobtitle = "Export to .png"
        self.JobFormat = "png"
        self.exportoptions.update({
            "compression": 3,
            "indexed": False,
            "interlaced": False,
            "saveSRGBProfile": False,
            "forceSRGB": False,
            "alpha": True,
            "transparencyFillcolor": [255, 255, 255],
            "downsample": False,
            "saveAsHDR": False,
            "storeAuthor": False,
            "storeMetaData": 85
        })
    def doJob(self, index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        pngOptions=InfoObject()
        #populate an export options using the objects dict
        for opt in self.exportoptions.keys():
            # validate the key - we dont want the filename or filepath at this time
            if opt != "fileName" or opt != "filePath":
                pngOptions.setProperty(opt, self.exportoptions[opt])
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] !="":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + index +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,pngOptions)                                  

class ExportPSD (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "psd"
        self.jobtitle ="Export to .psd"
        self.JobFormat = "psd"
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject()) 
        
class ExportTGA (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "tga"
        self.jobtitle ="Export to .tga"
        self.JobFormat = "tga"
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject())
        
class ExportTIF (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.secondaryAttribute = "compressiontype" # all seconday attributes are assigned to this widget
        self.jobType = "tif"
        self.jobtitle ="Export to .tif"
        self.JobFormat = "tif"
        self.compressionTypes=["NONE","JPEG DCT compression","Deflate(ZIP)","Lempel-Ziv & Welch","Pixar Log"]
        self.PredictorTypes = ["None","Horizontal Diferencing"]
        self.BitDepths=["8","16"]
        self.optionToggle ={"NONE":["alpha","flatten","saveProfile"],
                            "JPEG DCT compression":["alpha","flatten","saveProfile","quality"],
                            "Deflate(ZIP)":["alpha","flatten","saveProfile","deflate"],
                            "Lempel-Ziv & Welch":["alpha","flatten","saveProfile"],
                            "Pixar Log":["alpha","flatten","saveProfile""pixarlog"]
                            }
        self.exportoptions.update({
            "compressiontype":[3,["NONE","JPEG DCT compression","Deflate(ZIP)","Lempel-Ziv & Welch","Pixar Log"]],
            "alpha": True,
            "flatten":True,
            "saveProfile":True, 
            "predictor":0,
            "bitdepth": [1,["8","16"]],
            "deflate":6,
            "pixarlog":6,
            "quality":80
            })
        self.secondaryAttributes ={
            "JPEG DCT compression":["quality"],
            "Deflate(ZIP)":["deflate"],
            "Pixar Log":["pixarlog"]
            }
        
    #OK so the export options enabled/disabled depending on what opitons are selected
    #for example, setting export to jpg will show jpg compression setting,
    #setting deflate will show deflate value
    #setting lzw only show base settings
    # setting pixar show pixar log setting
    
        
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject())
        
class ExportWEBP (ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "webp"
        self.jobtitle ="Export to .webp"
        self.JobFormat = "webp"
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        outputlocation = os.path.dirname(image.fileName())
        outputFilename = os.path.splitext(os.path.basename(image.fileName()))[0]+"."+self.JobFormat 
        # vlidate the filne name. if there is one then we append the index to it and prep for output
        if self.exportoptions["filePath"] != "":
            outputlocation = self.exportoptions["filePath"]
        if self.exportoptions["fileName"] !="":
            outputFilename = self.exportoptions["fileName"] +"_" + str(index) +"."+self.JobFormat 
        image.setBatchmode(True)
        outputName =outputlocation + "/"+ outputFilename
        newDocument = image.exportImage(outputName,InfoObject()) 


class ConvertCYMK(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "palette" #name of the icon used
        self.jobtitle = "Convert image to CYMK colorspace"
        self.JobFormat = "cymk"
        self.exportoptions ={}
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        doc = application.activeDocument()
        cmyk_profile = "CMYK/USWebCoatedSWOP.icc"
        doc.setColorSpace(cmyk_profile)
        
class ConvertRGB(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "palette" #name of the icon used
        self.jobtitle = "Convert image to RGB colorspace"
        self.JobFormat = "RGB"
        self.exportoptions={}
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        doc = application.activeDocument()
        rgb_profile = "RGB/sRGB-elle-V2-srgbtrc.icc"
        doc.setColorSpace(rgb_profile)
        
        
class ConvertGreyscale(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "palette" #name of the icon used
        self.jobtitle = "Convert image to greyscale"
        self.JobFormat = "grey"
        self.exportoptions={}
    def doJob(self,index):
        #perform the export job here
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        doc = application.activeDocument()
        grayscale_profile = "GRAYA/sRGB-elle-V2-g10.icc"  # A common grayscale ICC profile
        doc.setColorSpace(grayscale_profile)
        

class ToggleGroup(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "utility" #name of the icon used
        self.jobtitle = "Toggle Group on/off"
        self.JobFormat = "toggle"
        self.exportoptions={
            "Layer Name": "",
            "Visible":True
        }
    def doJob(self,index):
        pass
        application = Krita.instance()
        # Get the current active document
        doc = application.activeDocument()
        layer_name = self.exportoptions["Layer Name"] # Replace with your layer or folder name
        layer = doc.nodeByName(layer_name)
         # Check if the layer or folder exists
        if layer:
            # Make the layer or folder visible
            layer.setVisible(self.exportoptions["Visible"])
            doc.refreshProjection()
        
class ResizeImage(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "utility" #name of the icon used
        self.jobtitle = "Resize Image"
        self.JobFormat = "Resize"
        self.exportoptions={
            "width": 0,
            "height": 0
        }
    def doJob(self,index):
        #perform the export job here
        print("resize")
        new_width = self.exportoptions["width"]  # Replace with your desired width
        new_height = self.exportoptions["height"]  # Replace with your desired height
        #perform the export job here
        application = Krita.instance()
        # Get the current active document
        image = application.activeDocument()
        # Optionally specify the resolution (DPI)
        resolution = image.resolution()# Keep the current X resolution (DPI)
        # Resize the image
        image.resizeImage(0, 0, new_width, new_height)
        # Scale all layers
        root = image.rootNode()
        for node in root.childNodes():
            if node.type() == "paintlayer":
                node.scaleNode(QPointF(), new_width, new_height, "Bicubic")


class CropImage(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "utility" #name of the icon used
        self.jobtitle = "crop Image"
        self.JobFormat = "crop"
        self.exportoptions={
            "left": 0,
            "top": 0,
            "width":0,
            "height":0
        }
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        doc = application.activeDocument()
        left = 100   # X coordinate of the top-left corner of the crop region
        top = 100    # Y coordinate of the top-left corner of the crop region
        width = 800  # Width of the crop region
        height = 600 # Height of the crop region
        doc.crop(left, top, width, height)
        
class replaceFont(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.fontSelector = True # an attribute to check to make sure you are looking at fonts and not colours
        self.jobType = "utility" #name of the icon used
        self.jobtitle = "replace all instances of a font in a document with another"
        self.JobFormat = "fontswap"
        self.exportoptions={
            "Old Font": "",
            "New Font": ""
        }
    def doJob(self,index):
        pass
        # Get the current Krita instance
        application = Krita.instance()
        doc = application.activeDocument()
        if doc is None:
            print("No document is open!")
        else:
            # Specify the new font you want to apply
            new_font = "Arial"  # Replace with your desired font name

            # Iterate over all layers
            for node in doc.topLevelNodes():
                # Check if the node is a vector layer (text objects are inside vector layers)
                if node.type() == "vectorlayer":
                    print(f"Processing vector layer: {node.name()}")

                    # Iterate over all vector objects in the layer
                    for shape in node.shapes():
                        # Check if the shape is a text shape
                        if shape.type() == "TextShape":
                            print(f"Found text object in layer: {node.name()}")
                            
                            # Get the text shape content
                            text_shape = shape

                            # Get the text document inside the shape
                            text_document = text_shape.textDocument()

                            # Access the current font of the text object
                            current_font = text_document.defaultFont()

                            # Print current font info
                            print(f"Current font: {current_font.family()}")

                            # Set the new font family
                            new_font_object = current_font
                            new_font_object.setFamily(new_font)

                            # Apply the new font to the text shape
                            text_document.setDefaultFont(new_font_object)
                            print(f"Replaced with new font: {new_font}")

            # Refresh the document view to reflect the changes
            doc.refreshProjection()


class undoOperation(ExportJob):
    def __init__(self):
        super().__init__()  # Initialize parent class attributes
        self.jobType = "utility" #name of the icon used
        self.jobtitle = "Undo previous operation"
        self.JobFormat = "undo"
    def doJob(self,index):
        #perform the export job here
        application = Krita.instance()
        doc = application.activeDocument()
        application = Krita.instance()
        #Perform an undo operation
        application.action('edit_undo').trigger()
        doc.refreshProjection()
                
def listClasses():
    joblist = [ExportBMP(),ExportGIF(),ExportICO(),ExportJPG(),ExportPDF(),ExportPNG(),ExportPSD(),ExportTGA(),ExportTIF(),ExportWEBP(),ConvertCYMK(),ConvertRGB(),ConvertGreyscale(),CropImage(),ToggleGroup(),ResizeImage(),replaceFont()]
    result = []
    for j in joblist:
        result.append([j.jobtitle,[j.jobType,j.JobFormat]])
    return (result)

class ExportFactory():
    def __new__(cls, job):
        if job == "bmp":
            return ExportBMP()
        if job == "gif":
            return ExportGIF()
        
        if job == "ico":
            return ExportGIF()
        if job == "jpg":
            return ExportJPG()
        if job == "pdf":
            return ExportPDF()
        if job == "png":
            return ExportPNG()
        if job == "psd":
            return ExportPSD()
        if job == "tga":
            return ExportTGA()
        if job == "tif":
            return ExportTIF()
        if job == "webp":
            return ExportWEBP()
        if job == "cymk":
            return ConvertCYMK()
        if job == "rgb":
            return ConvertRGB()
        if job == "grey":
            return ConvertGreyscale()
        if job == "crop":
            return CropImage()
        if job == "toggle":
            return ToggleGroup()
        if job == "Resize":
            return ResizeImage()
        if job == "crop":
            return CropImage()
        if job == "fontswap":
            return replaceFont()
        if job =="undo":
            return undoOperation()
        if job == "list":
            return listClasses()





##test = ExportFactory("tif")
##print(hasattr(test,'secondaryAttributes'))

