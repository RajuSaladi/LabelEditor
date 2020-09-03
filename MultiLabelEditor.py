import os
import cv2
import pdb
import pandas as pd
from tkinter import *

SAVEAFTERSTEPS = 1
WIDTHTHRESHOLD = 2
HEIGHTTHRESHOLD = 2
mainFolder = os.getcwd()

varList = []

def assignAndCreateFolder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    return folderPath

class GUIFunctions:

    def CreateMainWindow(self,LabelsList,objectIDNum):
        self.firstWindow = Tk()
        self.currentRowNumber = 0
        Label(self.firstWindow, text='Select Label for this ObjectID {}'.format(objectIDNum)).grid(row=self.currentRowNumber)
        self.currentRowNumber = self.currentRowNumber + 1
        
        """
        self.varList = []
        for i in range(0,len(LabelsList)):
            eachLabel = LabelsList[i]
            self.varList.append(IntVar())
            Checkbutton(self.firstWindow, text=eachLabel, variable=self.varList[i]).grid(row=self.currentRowNumber, sticky=W)
            self.currentRowNumber = self.currentRowNumber + 1
        """
        
        self.labelChooser = IntVar()
        for i in range(0,len(LabelsList)):
            eachLabel = LabelsList[i]
            Radiobutton(self.firstWindow, text=eachLabel, variable=self.labelChooser,value=i+1,command=self.CloseAllWindows).grid(row=self.currentRowNumber,sticky=W)
            self.currentRowNumber = self.currentRowNumber + 1
        mainloop()

    def GetLabelFromWindow(self,LabelsList,objectIDNum):
        self.CreateMainWindow(LabelsList,objectIDNum)
        selectedLabel = LabelsList[int(self.labelChooser.get())-1]
        #print("Selected Label is {}".format(selectedLabel))
        return selectedLabel
    
    def CloseAllWindows(self):
        self.firstWindow.destroy()
    
class mouseClickFunctions:
    guiF = GUIFunctions()

    def initializeParams(self):
        self.refPt = {}
        self.done = {}
        self.DISPLAYNAME = "LabelEditor"
        self.boxStart= {}
        self.labels = {}
        self.noOfobjectIDs = 0

    def clickAndDraw(self,event, x, y, flags, param):
        
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if(event == cv2.EVENT_LBUTTONDOWN):
            self.noOfobjectIDs = self.noOfobjectIDs + 1
            self.refPt[self.noOfobjectIDs] = [(x, y)]
            self.boxStart[self.noOfobjectIDs]= True
            self.done[self.noOfobjectIDs] = False
        # check to see if the left mouse button was released
        elif(event == cv2.EVENT_LBUTTONUP):
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished

            try:
                self.refPt[self.noOfobjectIDs][1] = (x, y)
            except:
                self.refPt[self.noOfobjectIDs].append((x, y))
            self.done[self.noOfobjectIDs] = True
            self.boxStart[self.noOfobjectIDs] = False
            self.labels[self.noOfobjectIDs] = guiF.GetLabelFromWindow(self.labelsToChooseFromList,self.noOfobjectIDs)
        elif (self.noOfobjectIDs in self.boxStart.keys()):
            if(self.boxStart[self.noOfobjectIDs]== True):
                try:
                    self.refPt[self.noOfobjectIDs][1] = (x, y)
                except:
                    self.refPt[self.noOfobjectIDs].append((x, y))
        self.imageForDisplay = self.imageCopy.copy()
        for eachBox in range(1,self.noOfobjectIDs+1):
            if(len(self.refPt[eachBox]) == 2):
                cv2.rectangle(self.imageForDisplay, self.refPt[eachBox][0], self.refPt[eachBox][1], (0, 255, 0), 2)
                if not (self.noOfobjectIDs in self.labels.keys()):
                    labelNameToDisplay = "ObjectID"
                else:
                    labelNameToDisplay = self.labels[self.noOfobjectIDs]
                cv2.putText(self.imageForDisplay, "{0}:{1}".format(labelNameToDisplay,eachBox), (int(self.refPt[eachBox][0][0]),int(self.refPt[eachBox][0][1]-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0),1)
        
        cv2.imshow(self.DISPLAYNAME, self.imageForDisplay)

    def GetBBoxValues(self):
        return self.refPt,self.labels,self.done
    
    def getBBoxFromMouseOnCaptureWindow(self,imageFrame,labelsList):
        self.imageCopy = imageFrame.copy()
        self.imageForDisplay = self.imageCopy.copy()
        self.labelsToChooseFromList = labelsList

        self.initializeParams()
        cv2.namedWindow(self.DISPLAYNAME)
        cv2.setMouseCallback(self.DISPLAYNAME, self.clickAndDraw)

        #self.imageForDisplay = cv2.resize(self.imageForDisplay, (640,480), interpolation = cv2.INTER_AREA)
        while True:
            # display the image and wait for a keypress
            
            cv2.imshow(self.DISPLAYNAME, self.imageForDisplay)
            key = cv2.waitKey(1) & 0xFF

            # if the 'r' key is pressed, reset the bbox region
            if key == ord("r"):
                self.imageForDisplay = imageFrame.copy()
                self.initializeParams()
         
            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                self.done = {}
                return self.GetBBoxValues()
                break
            
            elif key == ord("d"):
                return self.GetBBoxValues()
                break


if __name__ == "__main__":

    mcF = mouseClickFunctions()
    guiF = GUIFunctions()
    
    imageFolder = os.path.join(mainFolder,"Data")
    outputFolder = assignAndCreateFolder(os.path.join(mainFolder,"GroundTruth"))
    groundTruthCSVPath = os.path.join(outputFolder,"GroundTruthInfoMutliLabel.csv")
    labelListTextFilePath = os.path.join(outputFolder,"Labels.txt")
    
    f = open(labelListTextFilePath,'r')
    labelsList = f.read().splitlines()
    f.close()

    if not os.path.exists(groundTruthCSVPath):
        groundTruthDataFrame = pd.DataFrame(columns = ["Imagepath","ObjectID","ObjectType","x","y","w","h"])
        prevGroundTruthDataFrame = pd.DataFrame(columns = ["Imagepath","ObjectID","ObjectType","x","y","w","h"])
        with open(groundTruthCSVPath, 'w',newline='') as f:
            groundTruthDataFrame.to_csv(f,index = False)
    else:
        groundTruthDataFrame = pd.DataFrame()
        prevGroundTruthDataFrame = pd.read_csv(groundTruthCSVPath)

    i = 0
    for eachImage in os.listdir(imageFolder):

        thisImageFullPath = os.path.join(imageFolder,eachImage)
        if(thisImageFullPath in prevGroundTruthDataFrame["Imagepath"]):
            print("Skiping Image as Labels already exists for this image {}".format(eachImage))
            continue

        i = i + 1
        if(i>SAVEAFTERSTEPS):
            groundTruthDataFrame.reset_index(drop=True,inplace= True)
            #groundTruthDataFrame.columns = ["Imagepath","ObjectID","ObjectType","x","y","w","h"]
            with open(groundTruthCSVPath, 'a',newline='') as f:
                groundTruthDataFrame.to_csv(f,index = False,header=False)
            i = 0
            groundTruthDataFrame = pd.DataFrame()
        frame = cv2.imread(thisImageFullPath)
        frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
        
        #guiF.CreateMainWindow(labelsList)    
        bboxesCollection,labelsCollection,doneBBoxStatusCollection = mcF.getBBoxFromMouseOnCaptureWindow(frame,labelsList)
        #guiF.CloseAllWindows()

        for thisObjectID in doneBBoxStatusCollection.keys():
            thisBBox = bboxesCollection[thisObjectID]
            thisLabel = labelsCollection[thisObjectID]
            if ((doneBBoxStatusCollection[thisObjectID] is True) and (len(thisBBox) ==2)):
                x = min(thisBBox[0][0],thisBBox[1][0])
                y = min(thisBBox[0][1],thisBBox[1][1])
                w = abs(thisBBox[1][0] - thisBBox[0][0])
                h = abs(thisBBox[1][1] - thisBBox[0][1])
                if((w >= WIDTHTHRESHOLD)&(h >= HEIGHTTHRESHOLD)):
                    groundTruthDataFrame = groundTruthDataFrame.append([[thisImageFullPath,thisObjectID,thisLabel,x,y,w,h]])
