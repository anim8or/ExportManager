from PyQt5.QtWidgets  import*
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgRenderer
import os

class FontSelectorWidget(QWidget):
    def __init__(self,fontname):
        super().__init__()
        # Create a combobox and a button
        self.combo_box = QComboBox()
        # Populate the combobox with system fonts
        self.populate_fonts()
        # Set up the layout
        self.combo_boxSelectedIndex = self.getFontindex(fontname)
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        self.setLayout(layout)
        self.Font = ""
        # Connect the button to a method to print the selected font
        self.combo_box.currentIndexChanged.connect(self.updateFont)
        
    def populate_fonts(self):
        # Get the list of system fonts
        font_db = QFontDatabase()
        fonts = font_db.families()
        self.combo_box.addItems(fonts)
        
    def getFontindex(self,Fontname):
        for i in range( self.combo_box.count()):
            if  self.combo_box.itemText(i) == Fontname:
                return (i)
        return(0)
        # Add fonts to the combobox
    def selectIndex (self,index):
        self.combo_box.setCurrentIndex(index)
    
    def updateFont(self):
        self.Font = self.combo_box.currentText()
        #QMessageBox.information(QWidget(),"adding job type:", self.Font)
        
    def print_selected_font(self):
        # Print the selected font from the combobox
        selected_font = self.combo_box.currentText()
        print(f"Selected Font: {selected_font}")
        
class NamedHBoxLayout(QHBoxLayout):
    def __init__(self, name="",attribute=""):
        super().__init__()
        self.name = name
        self.attribute = attribute
        
class Qddlist(QComboBox):
    def __init__(self, color=[0, 0, 255], parent=None):
        super().__init__(parent)
        self.ddl= True
        
    def setItem(self,item):
        if type(item) == str:
            for i in range( self.count()):
                if  self.itemText(i) == item:
                    self.setCurrentIndex(i)
        else:
            self.setCurrentIndex(index)
            
class Compresslist(QComboBox):
    def __init__(self, color=[0, 0, 255], parent=None):
        super().__init__(parent)
        self.ddl= True
        self.activeSecondaryAttributes=[] # all secondary attributes currntly being displayed
        self.secondaryAttributes = {}
        self.AttributeHolder = []
        self.extraAttributes = []
        self.parentWindow = None
        self.SecondaryLayout =NamedHBoxLayout("secondary items")

    def setItem(self,item):
        if type(item) == str:
            for i in range( self.count()):
                if  self.itemText(i) == item:
                    self.setCurrentIndex(i)
        else:
            self.setCurrentIndex(index)
            
    def clear_layout(self, layout):
        """Helper function to remove widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
                
    # Function to hide all widgets in the layout
    def hide_layout_widgets(self,layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()
                
    # Function to show all widgets in the layout
    def show_layout_widgets(self,layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.show()    
                
    def index_changed(self, index):
        #QMessageBox.information(QWidget(),"adding job type:","index changed")  
        #clear secondary attribute widgets
        
        while self.activeSecondaryAttributes:
            layout_to_remove = self.activeSecondaryAttributes.pop(0)
            self.hide_layout_widgets(layout_to_remove)
            # Remove the layout from main layout
            self.parentWindow.removeItem(layout_to_remove)
            # Move layout to the removed list
            self.AttributeHolder.append(layout_to_remove)
        #populate secondary attribute widgets
        for f in range(len(self.AttributeHolder)-1, -1, -1):
            #QMessageBox.information(QWidget(),"adding job type:",self.AttributeHolder[f].attribute) 
            if self.AttributeHolder[f].attribute == str(self.currentText()):
                item = self.AttributeHolder.pop(f)
                self.parentWindow.addLayout(item)
                self.activeSecondaryAttributes.append(item)
                self.show_layout_widgets(item)
    def getListValues(self):
        x = self.currentIndex()

        # Get a list of all items in the combobox
        y = [self.itemText(i) for i in range(self.count())]

        # Output the result in the desired format
        result = [x, y]
        return (result)

    
class ColorSwatchButton(QPushButton):
    def __init__(self, color=[0, 0, 255], parent=None):
        super().__init__(parent)
        # Initialize the button with the passed RGB list
        self.current_color = QColor(*color)  # Unpack the list of RGB values into QColor
        # Set the initial icon color
        self.update_icon()
        pixmap = QPixmap(self.size())
        # Connect the button click to open the color dialog
        self.clicked.connect(self.open_color_dialog)

    def update_icon(self):
        """Updates the button icon with the current color."""
        pixmap = QPixmap(self.size())
        pixmap.fill(self.current_color)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        
    def getRGB (self):
        return([self.current_color.red(),self.current_color.green(),self.current_color.blue()])
    def open_color_dialog(self):
        """Opens a QColorDialog to choose a new color."""
        color = QColorDialog.getColor(self.current_color, self, "Select Color")
        if color.isValid():
            self.current_color = color
            t = str(self.getRGB())
            self.update_icon()  # Update the button with the new color

class EditScreen(QMainWindow):
    Editjob = None
    QueueMan = None
    filepathLineEdit =None #add it in here for scope and so we can set the lineEdit thats created dynamically
    
    def __init__(self,Job):
        self.jobedits=[]
        super(EditScreen,self).__init__()
        self.ui = uic.loadUi(os.path.dirname(__file__)+"/Krita_exporter_Editjob.ui", self) # Load the .ui file
        self.Editjob = Job.currentItem().exportjob
        self.show()
        self.loadExportData()
        #connect UI elements
        self.btn_EditJob.clicked.connect(self.writeOutExportData)
    def setListView(self,Listwidget):
        self.ListWindow = Listwidget
        
    def getflatvalues(self,dict):
        result = []
        optvars = list(dict.values())
        for o in optvars:
            for p in o:
                result.append(p)
        return result

    def setQueueManager(self,qman):
        self.QueueMan = qman
       
    def setsaveLocation(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file:
            self.Editjob.exportoptions["filePath"] = file
            self.filepathLineEdit.setText(file)
            
    def writeOutExportData(self):
        #write out the export job name
        exportoptions ={}
        if self.lineEdit.text()!= self.Editjob.JobName:
            self.Editjob.JobName = self.lineEdit.text()
        
        layerchildren = self.verticalLayout_5.children()
        for l in layerchildren:
            #check to see if there are any secondary attributes assigned to the widget
            # if there are  then write out these wid
            widgets = []

            for i in range(l.count()):
                item = l.itemAt(i)
                widget = item.widget()

                if widget is not None:
                    widgets.append(widget)
            #performs a quick check here to see if there are an secondary attributes associated with the control.
            #if there are write them all out  
            for w in widgets:
                #QMessageBox.information(QWidget(),"111:", str(w))
                if hasattr(w,'secondaryAttributes'):
                    
                    #get all the ui objects in the scondray attributes list
                    for x in w.AttributeHolder:
                        secondaryAttributes = []
                        for i in range(x.count()):
                            item = l.itemAt(i)
                            widget = item.widget()
                            if widget is not None:
                                secondaryAttributes.append(widget)
                        QMessageBox.information(QWidget(),"SECONDARY INFO:", str(len(secondaryAttributes)))
                        if hasattr(secondaryAttributes[1], 'text'):
                            exportoptions[ secondaryAttributes[0].text()]=secondaryAttributes[1].text()
                        if hasattr(secondaryAttributes[1], 'value'):
                            exportoptions[ secondaryAttributes[0].text()]=secondaryAttributes[1].value()
                        if hasattr(secondaryAttributes[1], 'current_color'):
                            exportoptions[ "transparencyFillcolor" ]=secondaryAttributes[1].getRGB()
                        if hasattr(secondaryAttributes[1], 'Font'):
                            exportoptions[ secondaryAttributes[0].text()]=secondaryAttributes[1].Font
                        for x in w.activeSecondaryAttributes:
                            secondaryAttributes = []
                            for i in range(x.count()):
                                item = l.itemAt(i)
                                widget = item.widget()
                                if widget is not None:
                                    secondaryAttributes.append(widget)
                            QMessageBox.information(QWidget(),"SECONDARY INFO:", str(len(secondaryAttributes)))
                            if hasattr(secondaryAttributes[1], 'text'):
                                exportoptions[ secondaryAttributes[0].text()]=secondaryAttributes[1].text()
                            if hasattr(secondaryAttributes[1], 'value'):
                                exportoptions[ secondaryAttributes[0].text()]=secondaryAttributes[1].value()
                            if hasattr(secondaryAttributes[1], 'current_color'):
                                exportoptions[ "transparencyFillcolor" ]=secondaryAttributes[1].getRGB()
                            if hasattr(secondaryAttributes[1], 'Font'):
                                exportoptions[ secondaryAttributes[0].text()]=secondaryAttributes[1].Font
                                
            ##QMessageBox.information(QWidget(),"222:", str(w))            
            if len(widgets) == 1:
                if hasattr(widgets[0], 'isChecked'):
                    key = widgets[0].text().replace('&', '')  # Remove ampersand
                    value = widgets[0].isChecked()  # Get checkbox state
                    exportoptions[key] = False 

            if len(widgets) == 2:
                if isinstance(widgets[1], QCheckBox):
                    # this section reads in any check box from the front end. a 'check box' is a layout with 2 widgets inside.
                    #widget 0 is a label that will serve as the key for the dict
                    #widget 1 is th check box itself, we need only ready the checked() state of the button to retrn a boolean value that can be written straight into the dict.
                    # at the moment I am writing to a new dict and then comparing the 2 to validate the data before writing it back out.
                    # it currently doesnt add the econdary attributes, that can be fixed. what IS concerning is that even though it read the check state of the button 
                    # and it will return debug messages confirming the state and type of checked state, when writing it out, the value is '' ( check line 329)
                    QMessageBox.information(QWidget(),"CHECKBOX DEBUG",(f"Widget 1: {widgets[1]}")) # Debug to check the checkbox
                    QMessageBox.information(QWidget(),"CHECKBOX DEBUG",(f"Is checked: {widgets[1].isChecked()}"))  # Debug to check its state

                    key = widgets[0].text().replace('&', '')  # Clean key from the label
                    value = True#widgets[1].isChecked()  # Directly assign the checkbox state
                    QMessageBox.information(QWidget(),"KEY DEBUG",(f"Key: '{key}'"))
                    QMessageBox.information(QWidget(),"KEY DEBUG",(f"Key: '{widgets[0].text()}'"))
                    QMessageBox.information(QWidget(),"Value Type Check", (f"value: '{value}', type: {type(value)}"))
                    

                    exportoptions[key] = value  # Update the dictionary with key-value pair
                    QMessageBox.information(QWidget(),"**Value Type Check", (f"value: '{value}', type: {type(exportoptions[key])}"))
                    
                    
                    
                    if widgets[1].isTristate():
                        QMessageBox.information(QWidget(), "button is tri state")
                    # Debugging: Show QMessageBox to confirm correct behavior
                    QMessageBox.information(QWidget(), "Key", f"Key: '{key}'")
                    QMessageBox.information(QWidget(), "Value", f"Value: {value}")


                if hasattr(widgets[1], 'ddl'):
                    # we need the current selection then an array of all the items in the list 
                    exportoptions[ widgets[0].text()]=(widgets[1].getListValues())
                    #self.Editjob.exportoptions[ widgets[0].text()]=widgets[1].currentText()
                if hasattr(widgets[1], 'text'):
                    exportoptions[ widgets[0].text()]=widgets[1].text()
                if hasattr(widgets[1], 'value'):
                    #QMessageBox.information(QWidget(),"adding job type:", widgets[0].text()) ## should be a spin box yalue
                    exportoptions[ widgets[0].text()]=widgets[1].value()
                if hasattr(widgets[1], 'current_color'):
                    exportoptions[ "transparencyFillcolor" ]=widgets[1].getRGB()
                if hasattr(widgets[1], 'Font'):
                    exportoptions[ widgets[0].text()]=widgets[1].Font
            if len(widgets) == 3:
                if hasattr(widgets[1], 'isChecked'):
                    key = widgets[0].text().replace('&', '')  # Remove ampersand
                    value = widgets[1].isChecked()  # Get checkbox state
                    exportoptions[key] = False 
                if hasattr(widgets[1], 'ddl'):
                    QMessageBox.information(QWidget(),"adding job type:", "dropdown list foundBBBB")
                    exportoptions[ widgets[0].text()]=(widgets[1].getListValues())
                if hasattr(widgets[1], 'text'):
                    exportoptions[ widgets[0].text()]=widgets[1].text()
                if hasattr(widgets[1], 'value'):
                    exportoptions[ widgets[0].text()]=widgets[1].value()  
        #save data validation
        matchedKeys =0
        for k in self.Editjob.exportoptions.keys():
            for m in exportoptions.keys():
                #ok check the value type against the original value
                if type (self.Editjob.exportoptions[k]) ==  type (exportoptions[m]):       
                    matchedKeys += 1
        QMessageBox.information(QWidget(),"number of keys matched:", str(exportoptions))
        QMessageBox.information(QWidget(),"number of keys in original data:", str((self.Editjob.exportoptions)))
        #output
"""
 new output    {'fileName': '', 'filePath': '', 'compressiontype': [3, ['NONE', 'JPEG DCT compression', 'Deflate(ZIP)', 'Lempel-Ziv & Welch', 'Pixar Log']], 'alpha': '', 'flatten': '', 'saveProfile': '', 'predictor': 0, 'bitdepth': [1, ['8', '16']]}
old output    {'fileName': '', 'filePath': '', 'compressiontype': [3, ['NONE', 'JPEG DCT compression', 'Deflate(ZIP)', 'Lempel-Ziv & Welch', 'Pixar Log']], 'alpha': True, 'flatten': True, 'saveProfile': True, 'predictor': 0, 'bitdepth': [1, ['8', '16']], 'deflate': 6, 'pixarlog': 6, 'quality': 80}

"""      
        if matchedKeys == len(self.Editjob.exportoptions.keys()) :
            QMessageBox.information(QWidget(),"validating save data:", "VALIDATION PASSED")
            self.Editjob.exportoptions = exportoptions

            """
       # self.reportexportData()            
        self.QueueMan.refreshTasks()
        self.close()
        
    def getControl(self,key,value):   
       #QMessageBox.information(QWidget(),"adding job type:",str(value))
        if type (value) is str:
            layout = NamedHBoxLayout(key)
            layout.addWidget(QLabel(key))
            EditLine = QLineEdit()
            layout.addWidget(EditLine)
            return([layout,EditLine])
        if type (value) is int:
            queryLayout = NamedHBoxLayout(key)
            spin_box= QSpinBox()
            label = QLabel(key)
            spin_box.setMaximum(2147483647) 
            spin_box.setMinimum(-2147483648)
            spin_box.setValue(value)
            queryLayout.addWidget(label)
            queryLayout.addWidget(spin_box)
            return([queryLayout,spin_box])
        if type (value) is bool:

            queryLayout = NamedHBoxLayout(key)
            checkbox= QCheckBox()
            checkbox.setChecked(value)
            label = QLabel(key)
            queryLayout.addWidget(label)
            queryLayout.addWidget(checkbox)
            return([queryLayout,checkbox])
        if type (value) is list:
            if len(value) ==3:
                layout = NamedHBoxLayout(key)
                colorButton = ColorSwatchButton(color=value)
                # Add the label and color button to the layout
                label = QLabel(key)
                layout.addWidget(label)
                layout.addWidget(colorButton)
                spacer_expanding = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                layout.addSpacerItem(spacer_expanding)
                return([layout,colorButton])
            if len(value) ==2:
                layout = NamedHBoxLayout(key)
                ddl = Compresslist()
                ddl.addItems(self.Editjob.exportoptions[key][1])
                ddl.setCurrentIndex(self.Editjob.exportoptions[key][0])
                ddl.currentIndexChanged.connect(ddl.index_changed)
                ddl.parentWindow = layout
                label = QLabel(key)
                ddl.secondaryAttributes = self.Editjob.secondaryAttributes 
                layout.addWidget(label)
                layout.addWidget(ddl)
                secondarylayout = NamedHBoxLayout("secondaryAttributes")
                layout.addLayout(secondarylayout)
                return([layout,ddl])
        if value == "Font":
            layout = NamedHBoxLayout(key)
            layout.addWidget(QLabel(key))
            fontlist = FontSelectorWidget(self.Editjob.exportoptions[key])
            fontlist.selectIndex(fontlist.getFontindex(self.Editjob.exportoptions[key]))
            #widget.setWindowTitle("Font Selector")
            layout.addWidget(fontlist)
            spacer_expanding = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addSpacerItem(spacer_expanding)
            return([layout,fontlist])
    def reportexportData(self):
        for opt in self.Editjob.exportoptions:
            QMessageBox.information(QWidget(),"Reporting EXport data",opt + ": "+str(self.Editjob.exportoptions[opt]) )
    def loadExportData(self):
        #load in the icon from the job and resize/apply it here
        pixmap = QPixmap(60, 60)
        pixmap.fill(Qt.transparent)  # Make the pixmap transparent
        # Create an SVG renderer
        svg_renderer = QSvgRenderer(self.Editjob.Iconlist[self.Editjob.jobType])
        # Calculate the aspect ratio
        svg_size = svg_renderer.defaultSize()
        aspect_ratio = svg_size.width() / svg_size.height()
        # Determine new width and height based on the aspect ratio, fitting in 60x60
        if aspect_ratio > 1:
            # Width is greater than height, scale width to 60 and adjust height
            new_width = 60
            new_height = 60 / aspect_ratio
        else:
            # Height is greater than or equal to width, scale height to 60 and adjust width
            new_height = 60
            new_width = 60 * aspect_ratio
        # Create a QRectF for positioning and scaling the SVG
        target_rect = QRectF(0, 0, new_width, new_height)
        # Use a QPainter to paint the SVG onto the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter, target_rect)
        painter.end()  # Always end the painter after painting
        # Set the QPixmap as the content of the QLabel
        self.JOBICON.setPixmap(pixmap)
        testval = type(self.Editjob.exportoptions)
        self.lineEdit.setText(self.Editjob.JobName)
        self.label_4.setText(self.Editjob.jobType)
        self.hasSecondaryAttrib = hasattr(self.Editjob,'secondaryAttributes')# sets a flag to be true  if there are selection sensitive attributes or false if not
        self.secondarylist = []
        #self.reportexportData()
        if self.hasSecondaryAttrib:
            self.secondarylist = self.getflatvalues(self.Editjob.secondaryAttributes)
        for f in self.Editjob.exportoptions.keys():
            
            if f not in self.secondarylist:
                ctrl =self.getControl(f,self.Editjob.exportoptions[f])
                if type(self.Editjob.exportoptions[f]) is str:
                    if f == "filePath":
                        newButton =QPushButton("Set location/filename")
                        newButton.clicked.connect(self.setsaveLocation)
                        ctrl[0].addWidget(newButton)
                    if f == self.Editjob.secondaryAttributes:
                        ctrl[1].parentWindow = ctrl[1]
                        ctrl[1].secondaryAttributes = self.Editjob.secondaryAttribute
                        attribs = QWidget()    
                        ctrl[0].addWidget(newButton)
                        
                if f == self.Editjob.secondaryAttribute:  
                    for key in self.Editjob.secondaryAttributes.keys() :
                        test= self.Editjob.secondaryAttributes[key]
                        for n in self.Editjob.secondaryAttributes[key]:
                            newCtrl = self.getControl(n,self.Editjob.exportoptions[n])[0]
                            newCtrl.attribute = key
                            ctrl[1].AttributeHolder.append(newCtrl)
                self.verticalLayout_5.addLayout(ctrl[0])
