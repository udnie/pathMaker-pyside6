from PySide6.QtCore    import Qt

### --------------------- dotsShared.py --------------------
''' dotsShared: common and paths dictionaries shared across classes and files '''
### --------------------------------------------------------
common = {
    "factor": 0.35,
    "tagZ":   20.0,    
    "gridZ": -50.0, 
    "pathZ": -25.0,  
    "bkgZ":  -99.0,
    "DotsW":  1460,  # app width 
    "DotsH":   825,  # app height
    "ViewW":  1080,  # canvas width  30 X 36
    "ViewH":   720,  # canvas height 30 X 24
    "gridSize": 30,
    "ScrollW": 152,  
    "ScrollH": 685,  
    "LabelW":  133,
    "LabelH":  112,    
    "MaxW":    110,
    "MaxH":     85,  
    "Star":    .70,
    "Type":    106,
    "Margin":   13,
}
            
PathStr = "F,S,C,D,N,T,P,R,W,V,{,},/,!,cmd,left,right,up,down,del,opt,<,>,:,\",_,+,-,="

paths = {
    "image":   "./",
    "paths":   "./paths/",
}

pathMenu = (
    ('C', 'Center Path'),
    ("D", "Delete Screen"), 
    ("F", "Files"),
    ("N", "New Path"),
    ("P", "Path Chooser"),
    ("R", "Reverse Path"),
    ("S", "Save Path"),
    ("T", "Test"),
    ("W", "Way Points"),
    ("V", "..View Points"),
    ("/", "Path Color"),
    ("cmd", "Closes Path"),
    ('_/+', "Rotate 1 deg"),
    ('<,>', 'Toggle Size'),
    ("} ", "Flop Path"),
    ("{ ", "Flip Path"),  
    (':/\"', "Scale X"),
    ('-,=', 'Scale Y'),
    ('U/D', 'Arrow Keys'),
    ('L/R', 'Arrow Keys'),
    ("opt", "Add a Point"),
    ("del", "Delete a Point"),
    (">", "  Shift Pts +5%"),
    ("<", "  Shift Pts -5%"),
    ("! ","  Half Path Size"))

pathcolors = (
    "DODGERBLUE",    
    "AQUAMARINE", 
    "CORAL",         
    "CYAN",        
    "DEEPSKYBLUE",   
    "LAWNGREEN", 
    "GREEN",    
    "HOTPINK",  
    "WHITESMOKE",
    "LIGHTCORAL", 
    "LIGHTGREEN",    
    "LIGHTSALMON", 
    "LIGHTSKYBLUE",
    "LIGHTSEAGREEN", 
    "MAGENTA",     
    "TOMATO",
    "ORANGERED", 
    "RED",    
    "YELLOW")       

singleKeys = {  ## wish I had done this earlier
    Qt.Key.Key_Up: 'up',          
    Qt.Key.Key_Down: 'down',
    Qt.Key.Key_Left: 'left',      
    Qt.Key.Key_Right:'right',
    Qt.Key.Key_Alt: 'opt',    
    Qt.Key.Key_Shift: 'shift',
    Qt.Key.Key_Control: 'cmd',
    Qt.Key.Key_Enter: 'enter',
    Qt.Key.Key_Return: 'return',
    Qt.Key.Key_Space: 'space',             
    Qt.Key.Key_C: 'C',  
    Qt.Key.Key_L: 'L',   
    Qt.Key.Key_N: 'N', 
    Qt.Key.Key_O: 'O',  
    Qt.Key.Key_P: 'P',
    Qt.Key.Key_R: 'R',
    Qt.Key.Key_S: 'S', 
    Qt.Key.Key_T: 'T',
    Qt.Key.Key_V: 'V', 
    Qt.Key.Key_W: 'W',  
    Qt.Key.Key_Plus: '+',         
    Qt.Key.Key_Equal: '=',    
    Qt.Key.Key_Minus: '-',  
    Qt.Key.Key_Less: '<',     
    Qt.Key.Key_Greater: '>',
    Qt.Key.Key_Colon: ':',   
    Qt.Key.Key_Apostrophe: '\'',      
    Qt.Key.Key_QuoteDbl: '"', 
    Qt.Key.Key_Slash: '/',
    Qt.Key.Key_Underscore: '_', 
    Qt.Key.Key_BraceLeft: '{',
    Qt.Key.Key_BraceRight: '}',   
    Qt.Key.Key_BracketLeft: '[',
    Qt.Key.Key_BracketRight: ']', 
}
### --------------------- dotsShared.py --------------------

