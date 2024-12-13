from PyQt5.QtWidgets  import*
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QTimer

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
    def getListValues(self):
        return([self.itemText(i) for i in range(self.count())])
    def getSelected(self):
        return (self.currentIndex())
            
    def setItem(self,item):
        if type(item) == str:
            for i in range( self.count()):
                if  self.itemText(i) == item:
                    self.setCurrentIndex(i)
        else:
            self.setCurrentIndex(index)
      

class Compresslist(QComboBox):
    def __init__(self):
        super().__init__()
        self.ddl= True
        self.secondaryControls = {}  # Map compression type -> associated widgets
        self.secondaryAttributes ={}
        QTimer.singleShot(0, self.register_secondary_controls)
        QTimer.singleShot(0, self.setUpConnections)
    def getListValues(self):
        return([self.itemText(i) for i in range(self.count())])
    def getSelected(self):
        return (self.currentIndex())
        
        
        
        
    def setUpConnections (self):
        self.currentIndexChanged.connect(self.toggle_secondary_controls)
        
    def register_secondary_controls(self):
        """
        Register a dictionary mapping combobox items to the widgets that should be toggled.
        Example: {"None": [widget1, widget2], "LZW": [widget3, widget4]}
        """
        #self.secondaryControls = mapping
        parent = self.parentWidget()  # Get the parent widget
        layout = parent.layout()  # Get the layout of the parent widget
        name = parent.objectName()
        MainLayout = layout.itemAt(0)
        for i in range(MainLayout.count()):
            for key, value in self.secondaryAttributes.attributes.items():
                for v in value:
                    if MainLayout.itemAt(i).name ==str(v):
                        self.secondaryControls[key] = MainLayout.itemAt(i)
        #QMessageBox.information(QWidget(),"COMPRESSLIST",str(self.secondaryControls))
        self.toggle_secondary_controls()

    def refresh_seconday_controls(self):
        for layout in self.secondaryControls[self.currentText()]:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if widget:
                    widget.show()
        
    def toggle_secondary_controls(self):
        """
        Toggle the visibility of secondary controls based on the selected combobox item.
        """
        #selected_item = self.itemText(index)
        # Hide all widgets
        for layout in self.secondaryControls.values():
 
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if widget:
                    try:
                        widget.hide()
                    except:
                        pass
        try:  
            #get the ui to show, ising current text as the key for the self.secondaryAttributes.attributes.  
            if self.currentText() in  self.secondaryAttributes.attributes.keys():
                layoutlist= self.secondaryAttributes.attributes[self.currentText()]
                for layoutToShow in layoutlist: 
                    for layouts in self.secondaryControls.values():
                        if str(layouts.name) == str(layoutToShow):
                            for i in range(layouts.count()):
                                item = layouts.itemAt(i)
                                widget = item.widget()
                                if widget:
                                    widget.show()

        except:
            pass            


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
            widgets = []
            for i in range(l.count()):
                item = l.itemAt(i)
                widget = item.widget()

                if widget is not None:
                    widgets.append(widget)
           
            if len(widgets) == 1:
                if hasattr(widgets[0], 'isChecked'):
                    key = widgets[0].text().replace('&', '')  # Remove ampersand
                    value = widgets[0].isChecked()  # Get checkbox state
                    exportoptions[key] = False 
                    continue 
            if len(widgets) == 2:
                
                if isinstance(widgets[1], QCheckBox):
                    self.Editjob.exportoptions[widgets[0].text()] = widgets[1].isChecked()
                    continue 
                if hasattr(widgets[1], 'ddl'):
                    # we need the current selection then an array of all the items in the list 
                    self.Editjob.exportoptions[ widgets[0].text()]=[widgets[1].getSelected(),(widgets[1].getListValues())]
                    continue 
                    #self.Editjob.exportoptions[ widgets[0].text()]=widgets[1].currentText()


                if isinstance(widgets[1], QLineEdit):
                    #QMessageBox.information(QWidget(),"saving:",str("writing out text"))
                    self.Editjob.exportoptions[ widgets[0].text()]=widgets[1].text()
                    continue 
                if isinstance(widgets[1], QSpinBox):
                    #QMessageBox.information(QWidget(),"saving:",str("writing out value"))
                    self.Editjob.exportoptions[ widgets[0].text()]=widgets[1].value()
                    continue 
                if hasattr(widgets[1], 'current_color'):
                    self.Editjob.exportoptions[ "transparencyFillcolor" ]=widgets[1].getRGB()
                    continue 
                if hasattr(widgets[1], 'Font'):
                    self.Editjob.exportoptions[ widgets[0].text()]=widgets[1].Font
                    continue 

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
            else:
                if len(value[1]) >3:

                    #add a compress list
                    layout = NamedHBoxLayout(key)
                    ddl = Compresslist()
                    ddl.addItems(self.Editjob.exportoptions[key][1])
                    ddl.setCurrentIndex(self.Editjob.exportoptions[key][0])
                    #ddl.currentIndexChanged.connect(ddl.index_changed)
                    ddl.parentWindow = layout
                    label = QLabel(key)
                    ddl.secondaryAttributes = self.Editjob.secondaryAttributes 
                    layout.addWidget(label)
                    layout.addWidget(ddl)
                    secondarylayout = NamedHBoxLayout("secondaryAttributes")
                    layout.addLayout(secondarylayout)
                    return([layout,ddl])
                else:
                    layout = NamedHBoxLayout(key)
                    ddl = Qddlist() # HERE! CHANGE THE OBJECT HERE TO A QDDL!!!!!
                    ddl.addItems(self.Editjob.exportoptions[key][1])
                    ddl.setCurrentIndex(self.Editjob.exportoptions[key][0])
                    label = QLabel(key)
                    layout.addWidget(label)
                    layout.addWidget(ddl)
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
        
        #QMessageBox.information(QWidget(),"loading export jobs:",str(self.Editjob.exportoptions))
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
        if self.Editjob.hasSecondaryAttrib:
            self.secondarylist = self.getflatvalues(self.Editjob.secondaryAttributes.attributes)
        for f in self.Editjob.exportoptions.keys():
            #if f not in self.secondarylist:
            ctrl =self.getControl(f,self.Editjob.exportoptions[f])
            if type(self.Editjob.exportoptions[f]) is str:
                if f == "filePath":
                    newButton =QPushButton("Set location/filename")
                    newButton.clicked.connect(self.setsaveLocation)
                    ctrl[0].addWidget(newButton)
                if f == self.Editjob.secondaryAttributes:
                    ctrl[1].parentWindow = ctrl[1]
                    ctrl[1].secondaryAttributes = self.Editjob.secondaryAttributes
                    attribs = QWidget()    
                    ctrl[0].addWidget(newButton)

            self.verticalLayout_5.addLayout(ctrl[0])
