# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_main import Ui_Dialog
import json


from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
        

class RenderArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent)

        self.penWidth = 1
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.rects = []
        
    def clear(self):
        self.rects = []
        self.update()
        
    def setRects(self, array):
        self.rects = []
        for d in array:
            self.rects.append(QtCore.QRect(d['left']/2, d['top']/2, (d['right']-d['left'])/2, (d['bottom']-d['top'])/2))
        self.update()
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #painter.scale(self.width() / 100.0, self.height() / 100.0)


        painter.setPen(QtGui.QPen(QtCore.Qt.black, self.penWidth,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, QtCore.Qt.red)
        gradient.setColorAt(1.0, QtCore.Qt.green)
        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawRects(self.rects)


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.renderView = RenderArea( self.background)
        self.renderView.setGeometry(QtCore.QRect(0, 0, 320, 320))
        self.array = []
        



    @pyqtSignature("")
    def on_btndel_clicked(self):
        row = self.listWidget.currentRow()
        if row == -1:
            return
        self.listWidget.takeItem(row)
        del self.array[row]
        print len(self.array)
        self.renderView.setRects(self.array)
    
    @pyqtSignature("")
    def on_pushButton_3_clicked(self):
        d = {}
        d['left'] = int(self.left.text())
        d['right'] = int(self.right.text())
        d['top'] = int(self.top.text())
        d['bottom'] = int(self.bottom.text())
        d['type']= str(self.type.currentText())
        d['description'] = str(self.description.toPlainText())

        if(d['type'] == 'text'):
            d['textsize'] = int(self.textsize.value())
            d['textcolor']= str(self.textcolor.text())
        #
        
        row =  self.listWidget.currentRow()
        
        if row is not -1:
            item = self.listWidget.item(row)
            s = "(%d,%d)*(%d,%d)"%(d['left'], d['top'], d['right'], d['bottom'])
            item.setText(s)
            self.array[row] = d
        
        self.renderView.setRects(self.array)

        
    
    @pyqtSignature("")
    def on_pushButton_4_clicked(self):
        options = QtGui.QFileDialog.Options()
        fileName = QtGui.QFileDialog.getSaveFileName(parent = self,
                filter = "Text Files (*.txt)", options = options)
        if fileName:
            text = json.dumps(self.array, indent=4)
            
            f = open(fileName, 'w')
            f.write(text)
            f.close()
            print fileName
        

    
    @pyqtSignature("")
    def on_btnadd_clicked(self):
        d={}
        d['left'] = 0
        d['right'] =0
        d['top'] = 0
        d['bottom'] = 0
        d['type'] = 'text'
        d['textsize'] = 1
        d['textcolor'] = 'ffffff'
        d['description'] = ''

        self.array.append(d)
        self.listWidget.addItem("[%d,%d]*[%d,%d]"%(d['left'], d['top'], d['right'], d['bottom']))
        self.listWidget.setCurrentRow(len(self.array)-1)

    
    @pyqtSignature("int")
    def on_listWidget_currentRowChanged(self, currentRow):
        self.left.setValue(self.array[currentRow]['left'])
        self.top.setValue(self.array[currentRow]['top'])
        self.right.setValue(self.array[currentRow]['right'])
        self.bottom.setValue(self.array[currentRow]['bottom'])
        self.description.setPlainText(self.array[currentRow]['description'])
        type = self.array[currentRow]['type']
        i = self.type.findText(type)
        self.type.setCurrentIndex(i)
        if type == 'text':
            self.textsize.setValue(self.array[currentRow]['textsize'])
            self.textcolor.setText(self.array[currentRow]['textcolor'])
        else:
            self.textsize.setValue(1)
            self.textcolor.clear()
        
        
    @pyqtSignature("QString")
    def on_textcolor_textChanged(self, text):
        if len(text) == 6:
            red = str("0x"+text[0:2])
            red = int(red, 0)
            green = str("0x"+text[2:4])
            green = int(green, 0)
            blue = str("0x"+text[4:6])
            blue =  int(blue, 0)
            color = QtGui.QColor(red, green, blue)
            if color.isValid(): 
                self.labelcolor.setPalette(QtGui.QPalette(color))
                self.labelcolor.setAutoFillBackground(True)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
    

