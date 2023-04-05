import sys
sys.path.append('/home/pi/git/Robotcar')
import os
from PIL import ImageFont

class Terminal:
    
    def __init__(self, debug):
        self.Debug = debug

    def __del__(self):
        self.device = None
        print("Deleted - Terminal")

    def consolePrint(self, s):
        if (self.Debug):
            print(s)
    
    
    def print(self,a):
        if (self.Debug):
            print(a)
    
    @property
    def Term(self):
        return self.__Term

    @Term.setter
    def Term(self, val):
        self.__Term = val

    @property
    def Debug(self):
        return self.__Debug

    @Debug.setter
    def Debug(self, val):
        self.__Debug = val
