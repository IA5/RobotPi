import sys
sys.path.append('/home/pi/git/Robotcar')
import evdev
from evdev import InputDevice, categorize, ecodes
from time import sleep
from src.lib.Display import Terminal
import random

class RemoteControl:
  
    aBtn = 304
    bBtn = 305
    xBtn = 307
    yBtn = 308

    up = 46
    down = 32
    left = 18
    right = 33

    start = 158
    select = 315

    lTrig = 310
    rTrig = 311

    ljoy = 317
    rjoy = 318

    t = None

    global stop_autonomous_thread

    def __init__(self, display, device, debug):
        self.Display = display
        self.Debug = debug
        self.Device = device
   
    @property
    def Debug(self):
        return self.__Debug

    @Debug.setter
    def Debug(self, val):
        if (val is None):
            self.__Debug = False
        else:
            self.__Debug = val 

    @property
    def Display(self):
        return self.__Display

    @Display.setter
    def Display(self, val):
        if (val is None):
            self.__Display = Terminal(self.Debug)
        else:
            self.__Display = val 
    
    @property
    def Device(self):
        return self.__Device

    @Device.setter
    def Device(self, val):
        if (val is None):
            self.__Device = "/dev/input/event0"
        else:
            self.__Device = val 

    def GetInputDevice(self):
        try:
            if self.Debug:
                print("Path to monitor for remote device")
                print(self.Device)

            gamePad = InputDevice(self.Device)
            return gamePad
        except:
            if self.Debug:
                self.Display.print("PLEASE CONNECT BLUETOOTH CONTROLLER")
                sleep(3)
            return -1
       
    def gamePadCode(self, gamepad):
                          
        for event in gamepad.read_loop():
            if self.Debug:
                self.Display,print(event)
            if event.type == ecodes.EV_KEY:
                #self.Display,print(str(event.value))
                if event.value == 1:
                    if event.code == self.yBtn:
                        if self.Debug:
                            self.Display,print("Y")
                        return "F"
                    elif event.code == self.bBtn:
                        if self.Debug:
                            self.Display,print("B")
                        return "R"
                    elif event.code == self.aBtn:
                        if self.Debug:
                            self.Display,print("A")
                        return "RR"
                    elif event.code == self.xBtn:
                        if self.Debug:
                            self.Display,print("X")
                        return "L"
                    elif event.code == self.up:
                        if self.Debug:
                            self.Display,print("up")
                    elif event.code == self.down:
                        if self.Debug:
                            self.Display,print("down")
                    elif event.code == self.left:
                        if self.Debug:
                            self.Display,print("left")
                    elif event.code == self.right:
                        if self.Debug:
                            self.Display,print("right")
                    elif event.code == self.start:
                        if self.Debug:
                            self.Display,print("start - autonomous mode")
                        return "start"
                    elif event.code == self.select:
                        if self.Debug:
                            self.Display,print("select - stop autonomous mode") 
                        return "select"        
                    elif event.code == self.lTrig:
                        if self.Debug:
                            self.Display,print("left bumper")
                        return "X"
                    elif event.code == self.rTrig:
                        if self.Debug:
                            self.Display,print("right bumper")  
                        return "X" 
                    elif event.code == self.ljoy:
                        if self.Debug:
                            self.Display,print("left joy - left shift") 
                        return "LLL"   
                    elif event.code == self.rjoy:
                        if self.Debug:
                            self.Display,print("right joy - right shift") 
                        return "RRR"
                    else: 
                        if self.Debug:
                            self.Display,print("Stop Stop Stop")
                        return "XX" 
                else:
                    break