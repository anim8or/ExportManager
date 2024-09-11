### ExportManager

ExportManager is a tool to allow batching of multiple operations that can be run upon a directory of rita .kra files.

### Usage

You select a number of predefined jobs from the available list: you assign the job a name (name can be anything).

<<IMAGE 1 here>>
You click the add job to queue to add the jobs to the queue. You can move selected tasks up and down the list, allowing you to re-order the list, should you require it.  
You can also delete selected jobs from the list.  
  
Double-clicking a list in the queue opens up the edit window. Here you can rename the job, set job specific overrides like a file name or new location and change settings associated with the export file type.
<<IMAGE 2>>


Overriding the file name with a new file will result in an index appended to the end of the filename. It is recommended to add a separator character like an underscore or minus sign (_ -) to separate the filename from the index.

As well as export operations, there are a number of utility jobs that will perform specific functions, switch color spaces, crop or resize a document, save to a new file. These have a spanner icon and can be added. You will need to edit these jobs to make sure they work.  
Once your queue is assembled, you can then specify a directory of kra files to operate on by clicking the get files button.  
You then run through the queue by clicking the Run Job queue button.

### Job Types
Export manager uses 2 job types:
### Image exports
these allow export to  .bmp, .gif, .jpg, .pdf, .png, .psd, .tga, .tif and webp
### Utilities
thes perform an operation on the opened document:
**Convert Colour space**
will convert between RGB and CYMK. and also convert to Grayscale  or convert to different bitdepths
**resize Image**
will resize image to specific size
**Toggle groups On/Off**
will toggle named layer on or off
**crop image**
will crop image to new size, using a rectangle, where top left of the rectangle is 0,0

