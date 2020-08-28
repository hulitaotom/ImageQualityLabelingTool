import os
import sys
import re
import glob
import PyQt5
import imageio
from PIL import Image
import PyQt5.QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QGraphicsView, QGraphicsScene
from annotateGUI import *
import numpy as np
from PIL import Image,ImageQt
from PyQt5.QtCore import Qt, QT_VERSION_STR
import xml.etree.ElementTree as ET
#from xml.dom import minidom
from lxml import etree
import platform

version = "0726.2020"

class annotateApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(annotateApp, self).__init__(parent)
        self.setupUi(self)
        self.imagePixmap = 0
        self.imageScene = QGraphicsScene()
        #self.imageView.mouseReleaseEvent = self.imgClickedFunc
        self.btnNextImage.clicked.connect(self.nextImg)
        self.btnPrevImage.clicked.connect(self.prevImg)
        self.cboFileList.currentIndexChanged.connect(self.cboIndexChangedFunc)
        self.btnSave.clicked.connect(self.save)
        #self.btnUndo.clicked.connect(self.initialize)
        #Self instance defination
        self.ratio = 1 #image scale ratio
        self.rowIndex = 0 # row index in the table
        self.columnIndex = 0 #column index in the table
        self.fileIndex = 0 #the index of the image list
        self.ROILen = 0 #the number of region of interest in an image(Read from the txt file)
        self.ROI = [] #the rectangle ROI information
        self.ROI_poly = []
        self.ROI_type = []
        self.nameList = [] #nameList is the list of image names without file extention.
        self.fileList = [] #fileList  is the list of all files in the imageFiles datapath.
        self.imageList = [] #this is the image file list
        self.checkBoxes = []
        self.ROIcheckBoxes = []
        self.comboBoxes = {}
        self.quality_factors = ["r300DPI", "r200DPI", "r150DPI", "r100DPI", "r75DPI"]
        self.windowSize = 1800
        self.update = False
        self.labelVersion.setText("Ver. "+version)
        self.startup()
    def nextImg(self):
        if self.fileIndex < len(self.imageList)-1:
            self.cboFileList.setCurrentIndex(self.cboFileList.currentIndex()+1)
        else:
            self.cboFileList.setCurrentIndex(0)
    def prevImg(self):
        if self.fileIndex == 0:
            self.cboFileList.setCurrentIndex(len(self.imageList)-1)
        else:
            self.cboFileList.setCurrentIndex(self.cboFileList.currentIndex()-1)
    def cboIndexChangedFunc(self):
        self.fileIndex = self.cboFileList.currentIndex()
        self.initialize()

    def createPoly(self, poly, ratio):
        polygon = QtGui.QPolygonF()                          
        for x,y in poly:
            polygon.append(QtCore.QPointF(int((x+2)/ratio), int((y+2)/ratio)))
        return polygon

    def chkBoxClickedFuncQuality(self,event):
        #tempImg = QtGui.QPixmap(self.leftPicturePath).scaled(400, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        checked_res = None
        res = [300,200,150,100,75]
        filePath = self.imageList[self.fileIndex]
        imread = Image.open(filePath)

        if self.sender() == self.tableWidget.cellWidget(0,0):
            checked = self.tableWidget.cellWidget(0,0).isChecked()
            for i in range(1, self.ROILen):
                self.tableWidget.cellWidget(i,0).setChecked(checked)

        if self.sender() in self.checkBoxes:
            for i in range(len(self.checkBoxes)):
                if self.sender() != self.checkBoxes[i]:
                    self.checkBoxes[i].setChecked(False)

        for i in range(len(self.checkBoxes)):
            if self.checkBoxes[i].isChecked():
                checked_res = res[i]

        if checked_res:
            for i in range(1, self.ROILen):
                if self.tableWidget.cellWidget(i,0).isChecked():
                    list1 = self.tableWidget.item(i,1).text()
                    roi = [int(x) for x in list1.split(',')]
                    #qp.drawRect(int(roi[0]/self.ratio),int(roi[2]/self.ratio),int((roi[1]-roi[0])/self.ratio),int((roi[3]-roi[2])/self.ratio))
                    patch = imread.crop((roi[0], roi[2], roi[1], roi[3]))
                    height = roi[3]-roi[2]
                    width = roi[1]-roi[0]
                    if checked_res != 300:
                        ratio = 300/checked_res
                        patch = patch.resize((int(width/ratio), int(height/ratio)), Image.BILINEAR)
                        patch = patch.resize((width, height), Image.BILINEAR)
                        imread.paste(patch, (roi[0], roi[2]))

        qim = ImageQt.ImageQt(imread)
        imagePixmap = QtGui.QPixmap.fromImage(qim).scaled(self.windowSize, self.windowSize, aspectRatioMode=QtCore.Qt.KeepAspectRatio)

        qp = QtGui.QPainter(imagePixmap)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(255, 0, 0))
        pen.setWidth(5)
        qp.setPen(pen)
        for i in range(1, self.ROILen):
            if self.tableWidget.cellWidget(i,0).isChecked():
                if self.tableWidget.cellWidget(0,1).isChecked():
                    pen.setColor(QtGui.QColor(0, 255, 0))
                    qp.setPen(pen)
                    qp.drawPolygon(self.createPoly(self.ROI_poly[i-1], self.ratio))
                else:
                    list1 = self.tableWidget.item(i,1).text()
                    roi = [int(x)+2 for x in list1.split(',')]
                    qp.drawRect(int(roi[0]/self.ratio),int(roi[2]/self.ratio),int((roi[1]-roi[0])/self.ratio),int((roi[3]-roi[2])/self.ratio))

        qp.end()
        self.imageScene.clear()
        self.imageScene.addPixmap(imagePixmap)
        self.imageView.setImage(imagePixmap)
    '''
    def chkBoxClickedFunc(self,event):
        #tempImg = QtGui.QPixmap(self.leftPicturePath).scaled(400, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        filePath = os.path.join("imageFiles", self.imageList[self.fileIndex])
        imagePixmap = QtGui.QPixmap(filePath).scaled(self.windowSize, self.windowSize, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        qp = QtGui.QPainter(imagePixmap)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(255, 0, 0))
        pen.setWidth(5)
        qp.setPen(pen)
        #qp.setPen(QtGui.QColor(255,0,0))
        for i in range(self.ROILen):
            if self.tableWidget.cellWidget(i,0).isChecked():
                list1 = self.tableWidget.item(i,1).text()
                roi = [int(x)+2 for x in list1.split(',')]
                qp.drawRect(int(roi[0]/self.ratio),int(roi[2]/self.ratio),int((roi[1]-roi[0])/self.ratio),int((roi[3]-roi[2])/self.ratio))
        qp.end()
        self.imageScene.clear()
        self.imageScene.addPixmap(imagePixmap)
        self.imageView.setImage(imagePixmap)
    '''
    def selectionChange(self, selection):
        if self.update: return
        selected_row, selected_col = self.comboBoxes[self.sender()]
        if selected_col > 2:
            for col in range(3,8):
                currIdx = self.tableWidget.cellWidget(selected_row, col).currentIndex()
                if (col < selected_col):
                    self.tableWidget.cellWidget(selected_row, col).setCurrentIndex(min(currIdx, selection))
                else:
                    self.tableWidget.cellWidget(selected_row, col).setCurrentIndex(max(currIdx, selection))
                if self.tableWidget.cellWidget(selected_row,0).isChecked():
                    for row in range(1, self.ROILen):
                        if self.tableWidget.cellWidget(row,0).isChecked():
                            currIdx = self.tableWidget.cellWidget(row, col).currentIndex()
                            if (col < selected_col):
                                self.tableWidget.cellWidget(row, col).setCurrentIndex(min(currIdx, selection))
                            else:
                                self.tableWidget.cellWidget(row, col).setCurrentIndex(max(currIdx, selection))
        
        if self.tableWidget.cellWidget(selected_row,0).isChecked():
            for row in range(1, self.ROILen):
                if self.tableWidget.cellWidget(row,0).isChecked():
                    self.tableWidget.cellWidget(row, selected_col).setCurrentIndex(selection)


    def save(self):
        output_dir = 'Outputs'
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        #print(self.nameList[self.fileIndex])
        save_path = os.path.join(output_dir, self.nameList[self.fileIndex]+".xml")  # create a new xml file with all keys and empty item
        #f = open(save_path, 'w')
        data = etree.Element('Data')

        #Go through the table
        for rowIndex in range(1, self.ROILen):
            ROIType = self.tableWidget.cellWidget(rowIndex, 2).currentText()
            #fill in the ROI coordinates
            coords = self.tableWidget.item(rowIndex,1).text().split(',')

            ranks = []
            for i in range(len(self.quality_factors)):
                ranks.append(self.tableWidget.cellWidget(rowIndex, 3+i).currentText())
            region = etree.SubElement(data, 'Region')
            #data.append(region)
            #items = ET.SubElement(data, 'Region')
            subItem1 = etree.SubElement(region, 'Coords')
            subItem1.set('Left', coords[0])
            subItem1.set('Right', coords[1])
            subItem1.set('Top', coords[2])
            subItem1.set('Bottom', coords[3])
            subItem2 = etree.SubElement(region, 'Type')
            subItem2.text = ROIType
            subItem3 = etree.SubElement(region, 'Ranks')
            for i in range(len(self.quality_factors)):
                rank = etree.SubElement(subItem3, self.quality_factors[i])
                rank.text = ranks[i]
            subItem4 = etree.SubElement(region, 'Polygon')
            for x,y in self.ROI_poly[rowIndex-1]:
                point = etree.SubElement(subItem4, 'Point')
                point.set('x', str(x))
                point.set('y', str(y))

        #tree = ET.ElementTree(data)
        xml_object = etree.tostring(data, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        with open(save_path, 'wb') as f:
            f.write(xml_object)
        #f.close()
        self.lineSaveStatus.setText("Success")

    def readFromSavedXML(self, xml_path):
        if os.stat(xml_path).st_size == 0:
            return None
        tree = ET.parse(xml_path)
        if not tree:
            return None
        root = tree.getroot()
        ret = []
        if not root:
            return None
        for obj in root:
            region_dict = dict()
            region_dict['Type'] = obj[1].text
            region_dict['Ranks'] = [obj[2][i].text for i in range(len(self.quality_factors))]
            ret.append(region_dict)
        return ret


    def imgClickedFunc(self):
        pass
    def initialize(self):  #this function should be called when change to a new image
        xml_path = os.path.join("Outputs", self.nameList[self.fileIndex] + ".xml")
        self.update = os.path.isfile(xml_path) #this variable tells if this is the first time we update the xml file
        if self.update:
            self.lineSaveStatus.setText("Labeled")
        else:
            self.lineSaveStatus.setText("Unsaved")
        #1. set the image
        filePath = self.imageList[self.fileIndex]
        print(self.nameList[self.fileIndex])
        imread = Image.open(filePath)

        if (imread.size[1] / imread.size[0]) > (self.windowSize / self.windowSize):
            self.ratio =  imread.size[1] / self.windowSize
        else:
            self.ratio = imread.size[0] / self.windowSize
        #print(imread.size)
        #imagePixmap = QtGui.QPixmap(filePath)
        imagePixmap = QtGui.QPixmap(filePath).scaled(self.windowSize,self.windowSize,aspectRatioMode= QtCore.Qt.KeepAspectRatio)
        self.imageScene.addPixmap(imagePixmap)
        self.imageView.setImage(imagePixmap)
        self.imageView.aspectRatioMode = Qt.KeepAspectRatio
        self.imageView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.imageView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.imageView.show()

        # Read XML data
        gt_xml_path = os.path.join("GroundTruthRecordAnnotation", 'pc-'+self.nameList[self.fileIndex]+'.xml')
        tree = ET.parse(gt_xml_path)
        root = tree.getroot()
        self.ROI = []
        self.ROI_poly = []
        self.ROI_type = []

        for obj in root[1]:
            if len(obj[0]) <= 0:
                continue

            if obj.tag.split('}')[-1] not in ('TextRegion', 'ImageRegion'): 
                continue

            if obj.tag.split('}')[-1] == 'TextRegion':
                self.ROI_type.append(0)
            elif obj.tag.split('}')[-1] == 'ImageRegion':
                self.ROI_type.append(1)
            else:
                self.ROI_type.append(2)

            left, right, top, bot = float('inf'), 0, float('inf'), 0
            #print(obj.tag.split('}')[-1])
            poly = []
            for pt in obj[0]:
                poly.append([int(pt.attrib['x']), int(pt.attrib['y'])])
                left = min(left, int(pt.attrib['x']))
                right = max(right, int(pt.attrib['x']))
                top = min(top, int(pt.attrib['y']))
                bot = max(bot, int(pt.attrib['y']))
                
            # filter out small regions
            threH, threW, threA = 40, 40, 2000
            if (right-left <= threW or bot-top <= threH) and (right-left)*(bot-top) <= threA:
                continue
                
            self.ROI_poly.append(poly)

            self.ROI.append([int(left), int(right), int(top), int(bot)])
        self.ROILen = len(self.ROI)

        
        self.ROILen += 1
        self.tableWidget.setRowCount(self.ROILen)#set table rows
        self.ROIcheckBoxes = []
        newWidget = QtWidgets.QCheckBox()
        newWidget.clicked.connect(self.chkBoxClickedFuncQuality)
        self.tableWidget.setCellWidget(0,0,newWidget)
        self.tableWidget.setItem(0,0,QtWidgets.QTableWidgetItem('    All'))
        for rowIndex in range(1, self.ROILen):
            #set ROIs
            ROI = self.ROI[rowIndex-1]
            #print(ROI[0]+','+ROI[1]+','+ROI[2]+','+ROI[3])
            self.tableWidget.setItem(rowIndex,1,QtWidgets.QTableWidgetItem(','.join([str(x) for x in ROI])))#coordinates
            newWidget = QtWidgets.QCheckBox()
            newWidget.clicked.connect(self.chkBoxClickedFuncQuality)
            self.tableWidget.setCellWidget(rowIndex,0,newWidget)
            self.ROIcheckBoxes.append(newWidget)
            newWidget = QtWidgets.QComboBox()
            newWidget.addItem("symbol")
            newWidget.addItem("raster")
            newWidget.addItem("vector")
            newWidget.activated.connect(self.selectionChange)
            #newWidget.addItem("background")
            self.tableWidget.setCellWidget(rowIndex, 2, newWidget)
            self.comboBoxes[newWidget] = [rowIndex, 2]
            self.tableWidget.cellWidget(rowIndex, 2).setCurrentIndex(self.ROI_type[rowIndex-1])
            #self.tableWidget.cellWidget(rowIndex, 2).setCurrentIndex(int(ROI[4])-1)

            for i in range(3,8):
                newWidget = QtWidgets.QComboBox()
                newWidget.addItem("A")
                newWidget.addItem("B")
                newWidget.addItem("C")
                newWidget.addItem("D")
                newWidget.activated.connect(self.selectionChange)
                self.tableWidget.setCellWidget(rowIndex, i, newWidget)
                self.comboBoxes[newWidget] = [rowIndex, i]
            self.tableWidget.setItem(rowIndex, 8, QtWidgets.QTableWidgetItem("None"))
           
        newWidget = QtWidgets.QCheckBox()
        newWidget.clicked.connect(self.chkBoxClickedFuncQuality)
        self.tableWidget.setCellWidget(0,1,newWidget)
        self.tableWidget.setItem(0,1,QtWidgets.QTableWidgetItem('    Show Polygons'))
        self.checkBoxes = []
        for columnIndex in range(3, 8):
            newWidget = QtWidgets.QCheckBox()
            newWidget.clicked.connect(self.chkBoxClickedFuncQuality)
            self.tableWidget.setCellWidget(0,columnIndex,newWidget)
            self.checkBoxes.append(newWidget)

        self.checkBoxes[0].setChecked(True)

        category = {'symbol':0, 'raster':1, 'vector':2}
        rank = {'A':0, 'B':1, 'C':2, 'D':3}
        #5 fill the table
        if self.update:
            saved_data = self.readFromSavedXML(xml_path)
            if not saved_data:
                return
            for rowIndex in range(1, self.ROILen):
                region_data = saved_data[rowIndex-1]
                self.tableWidget.cellWidget(rowIndex, 2).setCurrentIndex(category[region_data['Type']])
                for i in range(len(self.quality_factors)):
                    self.tableWidget.cellWidget(rowIndex, 3+i).setCurrentIndex(rank[region_data['Ranks'][i]])

        self.update = False

    def startup(self):
        #header = self.tableWidget.horizontalHeader()
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 100)
        self.tableWidget.setColumnWidth(7, 100)
        self.tableWidget.setColumnWidth(8, 100)
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        path = "imageFiles"
        try:
            self.fileList = glob.glob(os.path.join(path, '*.tif'))
        except:
            os.mkdir(path)
        for file in self.fileList: #get all image file names
            name = file[len(path)+1:].split('.')[0]
            gt_xml_path = os.path.join("GroundTruthRecordAnnotation", 'pc-'+name+'.xml')
            if os.path.isfile(gt_xml_path):
                self.imageList.append(file)
                self.nameList.append(name)
            else:
                os.remove(file)

        for file in self.nameList:
            self.cboFileList.addItem(file)
        self.rowIndex = 0
        self.columnIndex = 0
        self.fileIndex = 0

        #self.initialize()  #When the program is started, the comboBox will triger the initialize() function with index 0
if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = annotateApp()

    currentForm.show()
    currentApp.exec_()
