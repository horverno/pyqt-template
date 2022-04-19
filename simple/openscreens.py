#!/usr/bin/env python

# this script uses screen and the default gnome-terminal if not installed, please install with:
# sudo apt install screen gnome-terminal
# sudo apt install libcanberra-gtk-module libcanberra-gtk3-module
# pip install pyqtgraph

from __future__ import print_function
import subprocess
import pyqtgraph as pg
import pyqtgraph.Qt as qtgqt
import pyqtgraph.dockarea as darea
#import numpy as np

class PlotHandler(object):
    def __init__(self):
        super(PlotHandler, self).__init__()
        pg.setConfigOptions(antialias=True)
        self.app = qtgqt.QtGui.QApplication([])

    def initializePlot(self):
        self.win = qtgqt.QtGui.QMainWindow()
        area = darea.DockArea()
        white = (200, 200, 200)
        red = (200, 66, 66); redB = pg.mkBrush(200, 66, 66, 200)
        blue = (6, 106, 166); blueB = pg.mkBrush(6, 106, 166, 200)
        green = (16, 200, 166); greenB = pg.mkBrush(16, 200, 166, 200)
        yellow = (244, 244, 160); yellowB = pg.mkBrush(244, 244, 160, 200)
        self.win.setWindowTitle("Screen handler")
        #self.win.resize(1000, 400)
        self.win.move(400, 400)
        self.win.setCentralWidget(area)
        dock1 = darea.Dock("", size = (1,1))  # give this dock minimum possible size
        area.addDock(dock1, "left")
        widg1 = pg.LayoutWidget()
        self.roscoreBtn = qtgqt.QtGui.QPushButton("roscore")
        self.rvizBtn = qtgqt.QtGui.QPushButton("rviz")
        self.tftreeBtn = qtgqt.QtGui.QPushButton("tftree")
        self.updateBtn = qtgqt.QtGui.QPushButton("update screen list")
        widg1.addWidget(self.updateBtn, row=1, col=2)
        widg1.addWidget(self.roscoreBtn, row=2, col=0)
        widg1.addWidget(self.rvizBtn, row=2, col=1)
        widg1.addWidget(self.tftreeBtn, row=2, col=2)
        widg1.setStyleSheet("background-color: rgb(40, 44, 52); color: rgb(171, 178, 191);")
        dock1.setStyleSheet("background-color: rgb(18, 20, 23);")
        dock1.addWidget(widg1)
        self.state = None
        self.rvizBtn.clicked.connect(self.rviz1)
        self.roscoreBtn.clicked.connect(self.roscore1)
        self.tftreeBtn.clicked.connect(self.tftree1)
        self.updateBtn.clicked.connect(self.update)
        self.listwidget = qtgqt.QtGui.QListWidget()
        self.listwidget.setStyleSheet("""QListWidget{ color: rgb(171, 178, 191);}""")
        self.listwidget.clicked.connect(self.listclick)
        self.listwidget.itemDoubleClicked.connect(self.openscreen)
        self.listwidget
        dock1.addWidget(self.listwidget)
        self.update()
        self.win.show()

    def update(self):
        self.listwidget.clear()
        p = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
        output, err = p.communicate()
        lines = output.splitlines()
        #print(len(lines))
        if len(lines) > 2:
            for line in lines:
                if line[0] == '\t':
                    self.listwidget.insertItem(0, line.split()[0].strip().split('.')[1])

    def openscreen(self):
        item = self.listwidget.currentItem()
        print(item.text() + " >> double click")        
        toexec = ''.join(['screen -r ', str(item.text()), '; exec bash'])
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', toexec])

    def listclick(self, qmodelindex):
        item = self.listwidget.currentItem()
        print("single click: " + item.text())

    def tftree1(self):
        cmd = ['screen', '-mdS', 'tftree1', 'bash', '-c', 'rosrun rqt_tf_tree rqt_tf_tree']
        p = subprocess.Popen(cmd)
        print(cmd)
        self.update()

    def rviz1(self):
        cmd = ['screen', '-mdS', 'rviz1', 'bash', '-c', 'rosrun rviz rviz']
        p = subprocess.Popen(cmd)
        print(cmd)
        self.update()

    def roscore1(self):
        cmd = ['screen', '-mdS', 'roscore1', 'bash', '-c', 'roscore']
        p = subprocess.Popen(cmd)
        print(cmd)
        self.update()
        #subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'ls; exec bash'])
        #gnome-terminal -- bash -c "ls; exec bash"


if __name__ == "__main__":
    import sys
    print(__file__, "- started ")
    ph = PlotHandler()
    ph.initializePlot()
    if (sys.flags.interactive != 1) or not hasattr(qtgqt.QtCore, "PYQT_VERSION"):
        qtgqt.QtGui.QApplication.instance().exec_()