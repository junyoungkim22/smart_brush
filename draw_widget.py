from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line

import serial


class DrawWidget(Widget):
    def __init__(self, **kwargs):
        super(DrawWidget, self).__init__(**kwargs)
        self.comPort = 'COM10'
        self.comPortBaud = 9600

        self.x, self.y = 0, 0
        self.first = True
        self.startx, self.starty = self.width / 4, self.height / 4
        self.lastx, self.lasty = 0, 0
        self.initx, self.inity = 0, 0
        self.ser = serial.Serial()
        self.sensitivity = 3
        self.past_dz = 150

        self.x_list = []
        self.y_list = []
        self.thick_list = []
        self.smooth = False

    def open_serial(self):
        if(self.ser.isOpen()):
            try:
               self.ser.close()
            except:
               i=i
        try:
            self.ser = serial.Serial(port=self.comPort, baudrate=self.comPortBaud, timeout=1)
            print("serial port '" + self.comPort + "' opened!")
            #self.calibrate()
        except:
            print("failed to open serial port '" + self.comPort + "'")


    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]