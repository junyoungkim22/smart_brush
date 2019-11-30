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

        self.color = (100, 100, 100)

    def open_serial(self):
        if(self.ser.isOpen()):
            try:
               self.ser.close()
            except:
                pass
        try:
            self.ser = serial.Serial(port=self.comPort, baudrate=self.comPortBaud, timeout=1)
            print("serial port '" + self.comPort + "' opened!")
        except:
            print("failed to open serial port '" + self.comPort + "'")
        if(self.ser.isOpen()):
            self.calibrate()

    def parse_line(self, line):
        pos = line.split('\t')
        return (int(float(pos[0])), int(float(pos[1])), int(float(pos[2])))


    def start_draw(self):
        print("start")
        while(self.ser.isOpen()):
            while(self.ser.inWaiting() > 0):
                line = self.ser.readline().decode().rstrip()
                print(line)
                (disx, disy, disz) = self.parse_line(line)

                if(disx == 0 or disy == 0 or disz == 0):
                    break
                corx = disx - self.initx
                cory = disy - self.inity
                diffx = corx - self.lastx
                diffy = cory - self.lasty

                if(abs(diffx) > 30 or abs(diffy) > 30):
                    break

                diffy = diffy * (-1)

                drawx = self.startx + (corx*self.sensitivity)
                drawy = self.starty + (cory*self.sensitivity)

                with self.canvas:
                    Color(*self.color)
                    d = 30.
                    Ellipse(pos=(drawx - d / 2, drawy - d / 2), size=(d, d))
        print("end")



    def calibrate(self):
        calibrated = False
        print("Calibrating...")
        times = 0
        disx = 1000
        disy = 1000
        color = (random(), random(), random())
        if( self.ser.isOpen() ):
            while( calibrated is False ):
                line = self.ser.readline().decode().rstrip()
                try:
                    (disx, disy, disz) = self.parse_line(line)
                except:
                    continue
                if(times == 0):
                    if(disx == 0 or disy == 0):
                        continue
                    times += 1
                    print("init")
                    continue

                new_disx = disx
                new_disy = disy
                if(new_disx == 0 or new_disy == 0):
                    continue
                if(abs(new_disx - disx) > 100):
                    print("XXX")
                    times = 0
                    continue
                if(abs(new_disy - disy) > 100):
                    print("YYY")
                    times = 0
                    continue
                print("go")
                times += 1

                if(times == 5):
                    calibrated = True
                    self.initx = disx
                    self.inity = disy
                    print(self.initx)
                    print(self.inity)
                    break
            print("Done Calibrating!")
            self.start_draw()


    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            print("touch")
            print(touch.x)
            print(touch.y)
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]