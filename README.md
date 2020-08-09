## Image Quality Labeling Tool
Author: Litao Hu (hu430@purdue.edu)

## Requirements:
1. Python 3.5+
2. Numpy
3. PyQt5
4. lxml
5. imageio

## General Steps:
0. Read "Charge_to_Observer.pdf".
1. Install all required packages indicated above; or type "pip3 install -r requirements.txt"/"pip install -r requirements.txt" in terminal at root directory of the labeling tool (Note below for MacOS users).
2. Download the datasets from the given link. Put the folders "imageFiles" and "GroundTruthRecordAnnotation" in the root directory of the experiment.
3. Open the terminal at the root directory of the experiment and run "python3 annotateApp.py"/"python annotateApp.py" from the terminal to open the GUI.
4. Assign region types and quality grades for image regions in the scanned documents. Click "save" when you finish grading a document. Then click "Next Image" or "Prev Image" to go the the next or the previous image.
5. To zoom in, hold and drag the left mouse button to select an area to zoom. Double-click left mouse button to return to the whole document view.
6. After grading all images, close the GUI and zip the "Outputs" folder. Then send the compressed folder to hu430@purdue.edu.

## For MacOS Users (IMPORTANT):
1. If the GUI is not displayed entirely, go to System Preference->Displays, choose "Scaled" for resolution, and select "More Space".
2. Please use PyQt5 5.9.2 version instead of the latest 5.15.0 version. Install the correct version by typing "pip3 install PyQt5==5.9.2" in the terminal.
