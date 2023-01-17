# ROS2 simple pyqt publisher 
# pip install pyqtgraph (or pip3)

import pyqtgraph as pg
import pyqtgraph.Qt as qtgqt
import pyqtgraph.dockarea as darea
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
#import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from rclpy.clock import Clock

class PlotHandler(object):
    def __init__(self):
        super(PlotHandler, self).__init__()
        pg.setConfigOptions(antialias=True)
        self.app = QApplication([])

    def initializePlot(self):
        self.win = QtWidgets.QMainWindow()
        rclpy.init()
        node = Node("demo_node")
        self.stringPub = node.create_publisher(String, "demo_string", 10)
        self.floatPub = node.create_publisher(Float32, "demo_float", 10)
        area = darea.DockArea()
        white = (200, 200, 200)
        red = (200, 66, 66); redB = pg.mkBrush(200, 66, 66, 200)
        blue = (6, 106, 166); blueB = pg.mkBrush(6, 106, 166, 200)
        green = (16, 200, 166); greenB = pg.mkBrush(16, 200, 166, 200)
        yellow = (244, 244, 160); yellowB = pg.mkBrush(244, 244, 160, 200)
        self.win.setWindowTitle("Simple ROS pub")
        self.win.resize(500, 300)
        self.win.move(400, 400)
        self.win.setCentralWidget(area)
        dock1 = darea.Dock("", size = (1,1))  # give this dock minimum possible size
        area.addDock(dock1, "left")
        widg1 = pg.LayoutWidget()
        self.timeBtn = QtWidgets.QPushButton("Publish time")
        self.steerSlid = QtWidgets.QSlider(Qt.Horizontal)
        widg1.addWidget(self.timeBtn, row=0, col=0)
        widg1.addWidget(self.steerSlid, row=1, col=0)
        widg1.setStyleSheet("background-color: rgb(40, 44, 52); color: rgb(171, 178, 191);")
        dock1.setStyleSheet("background-color: rgb(18, 20, 23);")
        dock1.addWidget(widg1)
        self.state = None
        self.timeBtn.clicked.connect(self.time)
        self.steerSlid.valueChanged.connect(self.update)
        self.steerSlid.setMinimum(-20)
        self.steerSlid.setMaximum(20)
        self.steerSlid.setValue(0)
        self.update()
        self.win.show()

    def update(self):
        msg = Float32()
        msg.data = float(self.steerSlid.value()) / 10
        self.floatPub.publish(msg)        
        print(self.steerSlid.value())

    def time(self):
        msg = String()
        msg.data = "Current time: %s" % Clock().now()
        self.stringPub.publish(msg)         


if __name__ == "__main__":
    import sys
    print(__file__, "- started ")
    ph = PlotHandler()
    ph.initializePlot()
    QApplication.instance().exec_()