from tkinter import Canvas, Tk
from tkinter import N, W, E, S
from tkinter import ttk
from tkinter import Frame, StringVar, Entry, END
from tkinter import Button
from threading import Timer
from PIL import Image
import io, os
import serial
import numpy

comPort = 'COM4'
comPortBaud = 9600

class App:

    def __init__(self, master):

        self.width = 800
        self.height = 800
        self.x, self.y = 0, 0
        self.first = True
        self.startx, self.starty = self.width / 4, self.height / 4
        self.lastx, self.lasty = 0, 0
        self.initx, self.inity = 0, 0
        self.ser = serial.Serial()
        self.sensitivity = 3

        self.x_list = []
        self.y_list = []
        self.smooth = False

        # set main window's title
        master.title("Draw")

        frame = Frame(master)
        frame.grid(row=0,column=0)

        self.comPortStr = StringVar()
        self.comPort = Entry(frame,textvariable=self.comPortStr)
        self.comPort.grid(row=0,column=0)
        self.comPort.delete(0, END)
        self.comPort.insert(0,comPort)

        self.button = Button(frame, text="Open", fg="red", command=self.open_serial)
        self.button.grid(row=0,column=1)

        '''
        self.entryStr = StringVar()
        self.entry = Entry(frame,textvariable=self.entryStr)
        self.entry.grid(row=0,column=2)
        self.entry.delete(0, END)
        self.entry.insert(0,"I")

        self.send_button = Button(frame, text="Send", command=self.send_to_serial)
        self.send_button.grid(row=0,column=3)
        '''
        self.submit_button = Button(frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=0, column=2)

        self.canvas = Canvas(master, width=self.width, height=self.height)
        #self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas.grid(row=1)

        ## start attempts to read from serial port
        #self.read_loop()

    def __del__(self):
        self.stop_read_loop()

    def open_serial(self):
        # close the serial port
        if( self.ser.isOpen() ):
            try:
                self.ser.close()
            except:
                i=i  # do nothing
        # open the serial port
        try:
            self.ser = serial.Serial(port=self.comPortStr.get(),baudrate=comPortBaud, timeout=1)
            print("serial port '" + self.comPortStr.get() + "' opened!")
            self.calibrate()
        except:
            print("failed to open serial port '" + self.comPortStr.get() + "'")

    def read_loop(self):
        try:
            self.t.cancel()
        except:
            aVar = 1  # do nothing
        #print("reading")
        if( self.ser.isOpen() ) :
            self.read_from_serial();

        self.t = Timer(0.0,self.read_loop)
        self.t.start()

    def smoothListTriangle(self, y_list, strippedXs=False, degree=5):
        weight = []
        window = degree*2 - 1
        smoothed = [0.0]*(len(y_list) - window)
        for x in range(1, 2*degree):
            weight.append(degree-abs(degree - x))
        w = numpy.array(weight)
        for i in range(len(smoothed)):
            smoothed[i] = sum(numpy.array(y_list[i:i+window] * w)/float(sum(w)))
        return smoothed

    def read_from_serial(self):
        if( self.ser.isOpen() ):
            while( self.ser.inWaiting() > 0 ):

                line = self.ser.readline().decode().rstrip()

                pos = line.split('\t')
                disx = int(float(pos[0]))
                disy = int(float(pos[1]))
                disz = int(float(pos[2]))

                '''
                print(disx)
                print(self.x)
                print(disy)
                print(self.y)
                '''

                #print(str(disx) + '\t' + str(disy) + '\t' + str(disz))  

                if(disx == 0):
                    break
                if(disy == 0):
                    break
                if(disz == 0):
                    break

                '''
                if(self.first):
                    if(disx < 200):
                        break
                    if(disy > 1000):
                        break
                    self.x = disx
                    self.lastx = self.x
                    self.y = disy
                    self.lasty = self.y
                    self.first = False
                    break
                '''
                corx = disx - self.initx
                cory = disy - self.inity
                diffx = corx - self.lastx
                diffy = cory - self.lasty
                '''
                print(corx)
                print(cory)
                '''
                '''
                print("***")
                print(diffx)
                print(diffy)
                print("---")
                '''

                #ignore erratic output from sensor
                #if(abs(diffx) > 30 or abs(diffx) < 2):
                
                if(abs(diffx) > 30):
                    break
                if(abs(diffy) > 30):
                    break
                

                #print("No BREAK")
                diffy = diffy * (-1)

                '''
                self.lastx = corx
                self.lasty = self.y
                self.x = disx
                self.y = disy
                '''
                drawx = self.startx + (corx*self.sensitivity)
                drawy = self.starty + (cory*self.sensitivity)
                '''
                print("DRAW")
                print(drawx)
                print(drawy)
                '''

                #self.canvas.create_oval(self.corx, self.cory, self.corx + diffx, self.cory + diffy, width=30)
                if(disz < 150):
                    self.smooth = True
                    self.x_list.append(drawx)
                    self.y_list.append(drawy)
                    self.canvas.create_oval(drawx, drawy, drawx + 10, drawy + 10, width=1, fill='#0000ff')
                    '''
                    self.canvas.create_oval(drawx, drawy, drawx + 10, drawy + 10, width=15, fill='#fb0')
                    self.canvas.update()
                    '''
                if(disy > 200):
                    if self.smooth:
                        print("smooth")
                        print(len(self.y_list))
                        if (len(self.y_list) > 1):
                            print("smooth draw")
                            self.y_list = self.smoothListTriangle(self.y_list)
                            for drawx, drawy in zip(self.x_list, self.y_list):
                                self.canvas.create_oval(drawx, drawy, drawx + 10, drawy + 1, width=15, fill='#ffffff')
                        self.smooth = False
                        self.x_list = []
                        self.y_list = []

                self.lastx = corx
                self.lasty = cory

                '''
                self.corx = self.corx + diffx
                self.cory = self.cory + diffy
                '''

                #self.lastx = self.x
                #self.x = int(float(pos[0]*10))
                #print(x)

    def stop_read_loop(self):
        try:
            self.t.excancel()
        except:
            pass
            #print("failed to cancel timer")
            # do nothing

    def calibrate(self):
        calibrated = False
        print("Calibrating...")
        times = 0
        disx = 1000
        disy = 1000
        if( self.ser.isOpen() ):
            #while( calibrated is False ):
            #while(self.ser.inWaiting() > 0):
            while( calibrated is False ):
                line = self.ser.readline().decode().rstrip()
                pos = line.split('\t')
                print(disx)
                print(disy)
                if(times == 0):
                    disx = int(float(pos[0]))
                    disy = int(float(pos[1]))
                    if(disx == 0 or disy == 0):
                        continue
                    times += 1
                    print("init")
                    continue

                new_disx = int(float(pos[0]))
                new_disy = int(float(pos[1]))
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

                '''

                line = self.ser.readline().decode().rstrip()
                print("cal loop")

                pos = line.split('\t')
                disx = int(float(pos[0]))
                disy = int(float(pos[1]))
                '''

                '''
                print(disx)
                print(self.x)
                print(disy)
                print(self.y)
                '''
                '''
                if(disx == 0):
                    continue
                if(disy == 0):
                    continue

                for i in range(5):
                    line = self.ser.readline().decode().rstrip()
                    pos = line.split('\t')
                    new_disx = int(float(pos[0]))
                    new_disy = int(float(pos[1]))
                    if(abs(new_disx - disx) > 0.5):
                        continue
                    if(abs(new_disy - disy) > 0.5):
                        continue
                    if i == 4:
                        calibrated = True
                        self.initx = disx
                        self.inity = disy
                        print(self.initx)
                        print(self.inity)
                '''
            print("Done Calibrating!")
            self.read_loop()

    def display_image(self):
        img = Image.open("images/gul.PNG")
        img = img.resize((self.width, self.height), Image.ANTIALIAS)
        p = img.getdata()
        black_thresh = 500
        for y in range(0, self.height - 1):
            for x in range(0, self.width - 1):
                pixel = p[y * self.width + x]
                if(sum(pixel) < black_thresh):
                    pass
                    #self.canvas.create_rectangle(self.width - x, self.height - y, self.width - x + 20, self.height - y + 20, outline='#fb0', fill='#00f')
                    self.display_pixel(x, y, 0)
                else:
                    pass
                    #self.display_pixel(self.width - x, self.height - y, 200)

    def display_pixel(self, x, y, colour):
        if( x >= 0 and x < self.width and y >= 0 and y < self.height ) :
            colour = int(colour)
                
            fillColour = "#%02x%02x%02x" % (colour, colour, 255)
            #draw a new pixel and add to pixel_array
            self.canvas.create_rectangle(x, y, x+1, y, outline=fillColour, fill=fillColour)

    def submit(self):
        self.display_image()

root = Tk()

app = App(root)
#app.display_image()
#print("entering main loop!")
root.mainloop()

app.stop_read_loop()

print("exiting")

'''
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root, width=500, height=500)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)
canvas.bind("<Button-3>", save)
canvas.pack()
#ps = canvas.postscript(colormode='color')

root.mainloop()

compare("test.jpg", "ga_3.PNG")
'''
#ps = canvas.postscript(colormode='color')
#img = Image.open(io.BytesIO(ps.encode('utf-8')))
#img.save('test.jpg')