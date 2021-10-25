import sys
import os

from PySide6.QtCore     import Slot, Property, QVariantAnimation
from PySide6.QtCore     import Qt, QEvent, QObject, QTimer, QPointF, QPoint, \
                               QPropertyAnimation
from PySide6.QtGui      import QPainterPath, QColor, QPen, QPixmap, QFont
from PySide6.QtWidgets  import QFileDialog, QGraphicsPathItem, QGraphicsPixmapItem, \
                               QWidget, QGraphicsItemGroup, QGraphicsScene, QApplication, \
                               QPushButton 

from dotsSideGig     import Node, DoodleMaker, MsgBox, TagIt, getColorStr
from dotsShared      import common, paths, PathStr

from dotsSideWays    import SideWays
from dotsDrawsPaths  import DrawsPaths
from dotsControlView import ControlView

ScaleRotateKeys = ('+','_','<','>',':','\"','=','-')
Tick = 3  ## points to move using arrow keys

### -------------------- dotsPathMaker ---------------------
''' dotsPathMaker: contains load, save, addPath, pathChooser,
    pathlist, and path modifier functions...'''
''' moved all scene references from sideWays to pathMaker '''
### --------------------------------------------------------
class PathMaker(QWidget):
### --------------------------------------------------------
    def __init__(self, parent=None):  
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.view  = ControlView(self)
      
        self.chooser = None ## placeholder for popup_widget 
 
        self.sideWays = SideWays(self)  ## extends pathMaker
        self.drawing  = DrawsPaths(self) 

        self.doFirst = {
            'D':   self.delete,
            '/':   self.changePathColor,
            'cmd': self.drawing.closeNewPath,
        }

        self.direct = {
            'F': self.sideWays.openFiles,
            'C': self.sideWays.centerPath,
            'P': self.pathChooser,
            '{': self.sideWays.flipPath,
            '}': self.sideWays.flopPath,
        }

        self.noPathKeysSet = {
            'R': self.sideWays.reversePath,
            'S': self.sideWays.savePath,
            'T': self.pathTest,
            'W': self.addWayPtTags,
            'N': self.toggleNewPath,
        }

        self.WayPtsKeys = {
            '!': self.sideWays.halfPath,
            'V': self.drawing.togglePointItems,
            '<': self.sideWays.shiftWayPtsLeft,
            '>': self.sideWays.shiftWayPtsRight,
        }

        self.moveKeys = {
            "right": (Tick, 0),
            "left":  (-Tick, 0),
            "up":    (0, -Tick),
            "down":  (0, Tick),
        }

        self.scene.setSceneRect(0, 0,
            common["ViewW"],
            common["ViewH"])

        self.setFixedSize(common["ViewW"]+2,
            common["ViewH"]+2)

        self.move(350,75)
        self.view.keysSignal[str].connect(self.pathKeys) 

        ''' doesn't matter here or drawingWidget '''
        self.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)

        self.initThis()
     
### --------------------------------------------------------
    def initThis(self):
        self.pts = []
        self.key = ""

        self.npts = 0  ## counter used by addNewPathPts
        self.newPath = None
        self.addingNewPath = False

        self.color = "DODGERBLUE"
        self.openPathFile = '' 
        self.tag = ''
 
        self.pathSet = False
        self.pathChooserSet = False
       
        self.ball = None
        self.path = None                 
 
        self.pathTestNode = QPropertyAnimation()
        self.tagGroup = None        

        self.pathTestSet = False
     
        # from PySide6.QtCore import QT_VERSION_STR
        # from PySide6.QtCore import PYQT_VERSION_STR

        # print("PyQt version:", PYQT_VERSION_STR) 
        # print("Python version:", QT_VERSION_STR)

### ---------------------- key handler ---------------------
    @Slot(str)
    def pathKeys(self, key):
        self.key = key
        if key in PathStr:
            if key in self.doFirst:
                self.doFirst[key]()  ## run the function
            elif key in self.noPathKeysSet:
                self.noPathKeysSet[key]()  
            elif self.tagCount() == 0 and not self.addingNewPath:
                if key in self.direct: 
                    self.direct[key]()  
                elif len(self.pts) > 0:
                    if key in self.moveKeys: 
                        self.sideWays.movePath(self.moveKeys[key])
                    elif key in ScaleRotateKeys:
                        self.sideWays.scaleRotate(key)
            elif key in self.WayPtsKeys:
                self.WayPtsKeys[key]() 

### --------------------- event filter ----------------------                
    def eventFilter(self, source, e):       
        if self.addingNewPath:
            if e.type() == QEvent.Type.MouseButtonPress and \
                e.button() == Qt.MouseButton.LeftButton:
                    self.npts = 0  
                    self.drawing.addNewPathPts(e.scenePosition()) 

            elif e.type() == QEvent.Type.MouseMove and \
                e.buttons() == Qt.MouseButton.LeftButton:
                    self.drawing.addNewPathPts(e.scenePosition())
           
            elif e.type() == QEvent.Type.MouseButtonRelease and \
                e.button() == Qt.MouseButton.LeftButton:
                    self.drawing.addNewPathPts(e.scenePosition())
                    self.drawing.updateNewPath()  
   
        return QWidget.eventFilter(self, source, e)

### --------------------------------------------------------
    def delete(self):
        self.stopPathTest()
        self.drawing.removePointItems()
        self.removeWayPtTags()
        self.removePath()
        self.drawing.removeNewPath()
        self.pathChooserOff() 
        self.scene.clear()
        self.initThis()
      
    def pathChooser(self): 
        if not self.pathChooserSet and not self.addingNewPath:
            self.chooser = DoodleMaker(self)  
            self.chooser.move(600,200)
            self.chooser.show()
            self.pathChooserSet = True
        else:  
            self.pathChooserOff()

    def pathChooserOff(self):
        self.chooser = None
        self.pathChooserSet = False
          
### -------------------- path stuff ------------------------
    def toggleNewPath(self):  ## add/delete new drawn path
        if self.addingNewPath: 
            self.drawing.delNewPath()  ## changed your mind
            self.delete()
        elif not self.pathSet and self.tagCount() == 0:
            self.drawing.addNewPath()

    def addPath(self):  ## make a path from pathMaker pts
        self.removePath() 
        self.path = QGraphicsPathItem(self.setPaintPath(True))
        self.path.setPen(QPen(QColor(self.color), 3, Qt.PenStyle.DashDotLine))
        self.path.setZValue(common['pathZ']) 
        self.scene.addItem(self.path)
        self.pathSet = True
 
    def removePath(self):       
        if self.pathSet:
            self.scene.removeItem(self.path)
            self.pathSet = False
            self.path = None
    
    def redrawPathsAndTags(self):
        self.removeWayPtTags()
        self.removePath()
        self.addPath()
        self.addWayPtTags()

    def findTop(self):
        for itm in self.scene.items():
            return itm.zValue()
        return 0

    def changePathColor(self):
        self.color = getColorStr()
        if self.addingNewPath:
            self.drawing.updateNewPath()
        else:
            self.addPath()

    def setPaintPath(self, bool=False):  ## also used by waypts
        path = QPainterPath()
        for pt in self.pts:  ## pts on the screen 
            if not path.elementCount():
                path.moveTo(QPointF(pt))
            path.lineTo(QPointF(pt)) 
        if bool: path.closeSubpath()
        return path

    def redrawPoints(self, bool=True):  ## pointItems points
        self.drawing.removePointItems()
        self.redrawPathsAndTags()
        if bool: self.drawing.addPointItems()

### --------------------- wayPtTags ------------------------
    def addWayPtTags(self):
        if self.addingNewPath:
            return
        if self.tagCount() > 0:  ## toggle it off
            self.removeWayPtTags()
            self.drawing.removePointItems()
            return 
        lnn = len(self.pts)
        if lnn > 0: 
            self.addSomeTags(lnn)

    def addSomeTags(self, lnn):
        self.addWayPtTagsGroup()
        inc = int(lnn/10)  ## approximate a 10% increment
        list = (x*inc for x in range(0,10))  ## get the indexes
        for idx in list:  ## add wayPointTags to tagGroup
            pt = self.pts[idx]
            pct = (idx/lnn)*100
            if pct == 0.0: 
                idx = lnn
            tag = self.makePtsTag(pt, idx, pct)
            self.addWayPtTag(tag, pt)
        if self.openPathFile:  ## filename top left corner
            self.addWayPtTag(self.openPathFile, QPointF(5.0,5.0))
   
    def addWayPtTag(self, tag, pt):
        self.tag = TagIt('pathMaker', tag, QColor("TOMATO")) 
        self.tag.setPos(pt)
        self.tag.setZValue(common["tagZ"]+5) 
        self.tagGroup.addToGroup(self.tag)
   
    def addWayPtTagsGroup(self):
        self.tagGroup = QGraphicsItemGroup()
        self.tagGroup.setZValue(common["tagZ"]+5)
        self.scene.addItem(self.tagGroup)

    def removeWayPtTags(self):   
        if self.tagCount() > 0:  ## don't change
            self.scene.removeItem(self.tagGroup) 
            self.tagGroup = None
        
    def makePtsTag(self, pt, idx, pct):  ## used by pointItem as well
        s = "(" + "{:2d}".format(int(pt.x()))
        s = s + ", " + "{:2d}".format(int(pt.y())) + ")"
        s = s + "  " + "{0:.2f}%".format(pct)
        s = s + "  " + "{0:2d}".format(idx)
        return s

    def tagCount(self):  
        return sum(
            pix.type == 'tag' 
            for pix in self.scene.items()
        )

### ---------------------- pathTest ------------------------
    def pathTest(self):
        if self.pts and self.pathSet:
            if not self.pathTestSet:
    
                self.ball = QGraphicsPixmapItem(QPixmap(paths['image'] + 'ball.png'))
                node = Node(self.ball)
                self.ball.setZValue(self.findTop()+10)
       
                self.pathTestNode = QPropertyAnimation(node, b'pos')
                self.pathTestNode.setDuration(10000)  ## 10 seconds

                waypts = self.setPaintPath(True)  ## close subpath
                pt = getOffSet(self.ball)

                self.pathTestNode.setStartValue(waypts.pointAtPercent(0.0)-pt)
                for i in range(1, 99):   
                    self.pathTestNode.setKeyValueAt(i/100.0, waypts.pointAtPercent(i/100.0)-pt
                        )
                self.pathTestNode.setEndValue(waypts.pointAtPercent(1.0)-pt)  
                self.pathTestNode.setLoopCount(-1)
  
                self.startPathTest()
            else:
                self.stopPathTest()

    def startPathTest(self):
        self.scene.addItem(self.ball)
        self.pathTestNode.start()
        self.pathTestSet = True

    def stopPathTest(self): 
        if self.pathTestSet:  
            self.pathTestNode.stop()
            self.scene.removeItem(self.ball)
            self.ball = None
            self.pathTestNode = None
            self.pathTestSet = False

def getOffSet(pix):
    b = pix.boundingRect()
    w = (b.width()*.5)
    h = (b.height()*.5)
    return QPointF(w,h)

### --------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    apath = PathMaker()
    apath.show()
    sys.exit(app.exec())

### -------------------- dotsPathMaker ---------------------


