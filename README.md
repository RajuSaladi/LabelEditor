# LabelEditor
This Python code works as a label editor through which you can draw bounding boxes and label them. CSV file shall be generated from this tool which contains information about your labelling.

Setup folders in this folder sturcture:
  MainFolder
  |--->Data
  |--->GroundTruth
       |--->GroundTruthInfoMutliLabel.csv
       |--->Labels.txt

Data: This folder should contain images to be labelled
GroundTruth: This Folder to save the outputs of label tool
Labels.txt: This text file should contain the label names for the data
GroundTruthInfoMutliLabel.csv : Generated .csv file contains the Image Path , Object ID,ObjectType,x,y,w,h


Instructions:
  * Reads image from imagedir
  * displays image on screen
  * User can draw bounding box on image using mouse left buttoni.e., Click and hold left mouse button where user want to start bounding     box.move mouse towards the end of object. user can see the bounding box being drawn. when the user satisfies with bounding box drawn, release mouse left button.
  * A Popup will appear from which user can chose label for that bounding box
  * User can draw multiple bounding boxes
  * Once, labeling for the frame is done, Press 'd' on Keyboard.
  * If user wants to reset the bounding boxes for this frame, press 'r'
  * If user wants to skip the frame, press 'c'
