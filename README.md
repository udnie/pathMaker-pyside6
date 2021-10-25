## pathMaker 
This app is a stand-alone portion of pathmaker from my dotsQt program here to illustrate a possible bug I'm experiencing with pyside6 and pyqt6 on a Mac.

I'm programming on a mid-2015 MacBookPro running
BigSur, python 3.9.6, and don't use a mouse. This wasn't a problem in pyqt5.

You can launch pathmaker from the command line by typing python(3) dotsPathMaker.py. Once the screen is up you should be able to trigger the 
problem, warnings written to the standard output or such, by moving the mouse pointer around - off the screen and back.

To exit enter X, Q, or Escape.

Sorry for so much code but the problem doesn't seem to appear running single file apps and may not when using a mouse.

Thanks in advance.

Mel Tearle

**The Bug**		
qt.pointer.dispatch: delivering touch release to same window QWindow(0x0) not QWidgetWindow(0x7f92d2bc83a0, name="PathMakerClassWindow")  
qt.pointer.dispatch: skipping QEventPoint(id=1 ts=0 pos=0,0 scn=568.752,647.051 gbl=568.752,647.051 Released ellipse=(1x1 ∡ 0) vel=0,0 press=-568.752,-647.051 last=-568.752,-647.051 Δ 568.752,647.051) : no target window

