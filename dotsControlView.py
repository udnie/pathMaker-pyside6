import os
import sys


from PySide6.QtCore    import Signal
from PySide6.QtCore    import Qt
from PySide6.QtGui     import QPainter
from PySide6.QtWidgets import QGraphicsView

from dotsSideGig     import MsgBox
from dotsShared      import common, singleKeys

MixKeys   = (Qt.Key.Key_D, Qt.Key.Key_F, Qt.Key.Key_T)
ExitKeys  = (Qt.Key.Key_X, Qt.Key.Key_Q, Qt.Key.Key_Escape)

### ------------------ dotsControlView ---------------------
''' dotsControlView: Base class to create the control view 
    adds drag and drop ''' 
### --------------------------------------------------------
class ControlView(QGraphicsView):
### --------------------------------------------------------
    ## adds drag and drop to a QGraphicsView instance and 
    ## keyboard capture 
    keysSignal = Signal([str])

    def __init__(self, parent):
        super().__init__(parent)

        self.pathMaker = parent       
    
        self.setObjectName('ControlView')
        self.setScene(parent.scene)
      
        self.dragOver = False
    
        self.setRenderHints(QPainter.RenderHint.Antialiasing | 
            QPainter.RenderHint.TextAntialiasing | 
            QPainter.RenderHint.SmoothPixmapTransform)

        self.setStyleSheet("border: 1px solid rgb(100,100,100)")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setAcceptDrops(False)  
      
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.grabKeyboard()  ## happy days
      
### --------------------------------------------------------
    def dragMoveEvent(self, e):
        pass

    def dragEnterEvent(self, e):
        pass

    def dropEvent(self, e):
        pass
   
### -------------------------------------------------------
    ## best location for reading keys - especially arrow keys
    def keyPressEvent(self, e):
        key = e.key() 
        if e.key() == 33:  ## '!' on a mac
            self.setKey('!')
        elif key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):  ## can vary
            self.setKey('del')
        elif key in MixKeys:
            if key == Qt.Key.Key_D:    
                self.setKey('D') 
            elif key == Qt.Key.Key_F:
                self.setKey('F')    
            elif key == Qt.Key.Key_T:
                self.setKey('T')    
        elif key in singleKeys: ## in dotsShared.py   
                self.setKey(singleKeys[key]) 
        elif e.key() in ExitKeys:
            self.pathMaker.scene.clear()
            self.pathMaker.close()

    def setKey(self, key):  ## sending key to dropCanvas
        self.key = key
        self.keysSignal[str].emit(self.key)

    def keyReleaseEvent(self, e):   
        self.keysSignal[str].emit('')

### ------------------ dotsControlView ---------------------