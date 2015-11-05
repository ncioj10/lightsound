import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *
import serial

suppState = 0
an = 0
peakSize = 200
limiter = 60

def plotSomething():
    global suppState, an, peakSize, limiter
    if SR.newAudio==False: 
        return
    xs,ys=SR.fft()
    try:
	ser = serial.Serial('COM9', 9600)
	for a in range(5,limiter,3):
		if ys[a] > peakSize:
			suppState= 1
			break

	if suppState == 1:
		if an == 0:
				
			    ser.write('1');
                            an = 1
	else:
		if an == 1:
			    ser.write('0');
                            an = 0
	suppState = 0
    except serial.SerialException,e:
        z=e
        print z
        
        
        
    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    SR.newAudio=False

def setPeakSize(ps):
    global peakSize
    peakSize = ps
    print "PeakSize set to "+str(ps)

def increaseLimiter():
    global limiter
    limiter= limiter+5
    print str(limiter)

if __name__ == "__main__":

    
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    uiplot.btnA.clicked.connect(plotSomething)
    uiplot.btnB.clicked.connect(lambda: self.setPeakSize(200))
    uiplot.btnC.clicked.connect(lambda: self.setPeakSize(400))
    uiplot.btnD.clicked.connect(lambda: self.increaseLimiter())
    #uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    #uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
    #uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 1000)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    SR=SwhRecorder()
    SR.setup()
    SR.continuousStart()

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SR.close()
    sys.exit(code)
