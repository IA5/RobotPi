import sys
import src.lib.UltraBorg3 as UltraBorg
from src.utils.Utils import CompareUtils  
from src.lib.Display import Terminal

class SonicSensor:
    def __init__(self, range, display, debug):
        
        self.Range = range
        self.Debug = debug
        self.Display = display
        self.Utils = CompareUtils()

        # Create a new UltraBorg object
        self.UB = UltraBorg.UltraBorg()
        self.UB.i2cAddress = 36
        self.UB.Init() 

    def __del__(self):
            self.UB = None
            print("Deleted - SonicSensor")

    @property
    def Range(self):
        return self.__Range

    @Range.setter
    def Range(self, val):
        if val < 0:
            self.__Range = 0
        elif val > 1500:
            self.__Range = 1500
        else:
            self.__Range = val

    @property
    def Debug(self):
        return self.__Debug

    @Debug.setter
    def Debug(self, val):
        if (val is None):
            val = False
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

    def IsSensorHot(self,sensor, range):
        
        if (isinstance(sensor, int) != True):
            return False
        
        if (sensor == 0):
            return False

        if (sensor < range):
            return True
        else:
            return False

    def GetSensorReading(self):

        #  #Read all four ultrasonic values
        usm1 = self.UB.GetDistance1() #Front
        usm2 = self.UB.GetDistance2() #Left
        usm3 = self.UB.GetDistance3() #Right
        usm4 = self.UB.GetDistance4() #Back

        SonicSensorRead = [usm1, usm2, usm3, usm4]

        return SonicSensorRead

    def GetDistanceCode(self, sensorReading):

        f = 0
        l = 0
        r = 0
        b = 0

        if (isinstance(sensorReading[0], float)):
            f = int(sensorReading[0])
            if (self.Debug):
                self.Display.print('#1 -F % 4d mm' % (sensorReading[0]))
                
        if (isinstance(sensorReading[1], float)):
            l = int(sensorReading[1])
            if (self.Debug):
                self.Display.print('#2 - L % 4d mm' % (sensorReading[1]))

        if (isinstance(sensorReading[2], float)):
            r = int(sensorReading[2])
            if (self.Debug):
                self.Display.print('#3 - R % 4d mm' % (sensorReading[2]))

        if (isinstance(sensorReading[3], float)):
            b = int(sensorReading[3])
            if (self.Debug):
                self.Display.print('#4 - B % 4d mm' % (sensorReading[3]))
            
        if (f==0):
                return 'FF'
        if (l==0):
                return 'LL' 
        if (r==0):
                return 'RR'
        if (b==0):
                return 'BB'

        if (self.IsSensorHot(f, self.Range) and self.IsSensorHot(b, self.Range) 
            and self.IsSensorHot(l, self.Range) and not self.Utils.equals(self.IsSensorHot(r, self.Range), True)):
                return 'FBL'

        if (self.IsSensorHot(f, self.Range) and self.IsSensorHot(b, self.Range) 
            and not self.Utils.equals(self.IsSensorHot(l, self.Range), True) and not self.Utils.equals(self.IsSensorHot(r, self.Range), True)):
                return 'FB'

        if (self.IsSensorHot(f, self.Range) and self.IsSensorHot(r, self.Range) 
            and not self.Utils.equals(self.IsSensorHot(l, self.Range), True) and not self.Utils.equals(self.IsSensorHot(b, self.Range), True)):
                return 'FR'

        if (self.IsSensorHot(f, self.Range) and self.IsSensorHot(l, self.Range) 
            and self.IsSensorHot(r, self.Range) and not self.Utils.equals(self.IsSensorHot(b, self.Range), True)):
                return 'FLR'
            
        if (self.IsSensorHot(f, self.Range) and not self.Utils.equals(self.IsSensorHot(l, self.Range), True) 
            and not self.Utils.equals(self.IsSensorHot(r, self.Range), True) and not self.Utils.equals(self.IsSensorHot(b, self.Range), True)):
                return 'F'

        if (self.IsSensorHot(b, self.Range) and self.IsSensorHot(l, self.Range) 
            and not self.Utils.equals(self.IsSensorHot(f, self.Range), True) and not self.Utils.equals(self.IsSensorHot(r, self.Range), True)):
                return 'BL'

        if (self.IsSensorHot(b, self.Range) and self.IsSensorHot(l, self.Range) 
            and self.IsSensorHot(r, self.Range) and not self.Utils.equals(self.IsSensorHot(f, self.Range), True)):
                return 'BLR'

        if (self.IsSensorHot(r, self.Range) and self.IsSensorHot(l, self.Range) 
            and not self.Utils.equals(self.IsSensorHot(f, self.Range), True) and not self.Utils.equals(self.IsSensorHot(b, self.Range), True)):
                return 'RL'   

        if (self.IsSensorHot(l, self.Range) and not self.Utils.equals(self.IsSensorHot(r, self.Range), True) 
            and not self.Utils.equals(self.IsSensorHot(b, self.Range), True) and not self.Utils.equals(self.IsSensorHot(f, self.Range), True)):
                return 'L'   

        if (self.IsSensorHot(f, self.Range) and self.IsSensorHot(l, self.Range) 
            and not self.Utils.equals(self.IsSensorHot(r, self.Range), True) and not self.Utils.equals(self.IsSensorHot(b, self.Range), True)):
                return 'FL'    

        if (self.IsSensorHot(b, self.Range) and self.IsSensorHot(r, self.Range) 
            and not self.Utils.equals(self.IsSensorHot(f, self.Range), True) and not self.Utils.equals(self.IsSensorHot(l, self.Range), True)):
                return 'BR'     

        if (self.IsSensorHot(r, self.Range) and not self.Utils.equals(self.IsSensorHot(l, self.Range), True) 
            and not self.Utils.equals(self.IsSensorHot(b, self.Range), True) and not self.Utils.equals(self.IsSensorHot(f, self.Range), True)):
                return 'R'    

        if (self.IsSensorHot(r, self.Range) and self.IsSensorHot(b, self.Range) 
            and self.IsSensorHot(f, self.Range) and not self.Utils.equals(self.IsSensorHot(l, self.Range), True)):
                return 'RBF'   

        if (self.IsSensorHot(b, self.Range) and not self.Utils.equals(self.IsSensorHot(l, self.Range), True) 
            and not self.Utils.equals(self.IsSensorHot(r, self.Range), True) and not self.Utils.equals(self.IsSensorHot(f, self.Range), True)):
                return 'B'   

        if (self.IsSensorHot(f, self.Range) and self.IsSensorHot(l, self.Range) 
            and self.IsSensorHot(r, self.Range) and self.IsSensorHot(b, self.Range)):
                return 'FBLR'
            
        if (not self.Utils.equals(self.IsSensorHot(f, self.Range), True) and not self.Utils.equals(self.IsSensorHot(l, self.Range), True)
            and not self.Utils.equals(self.IsSensorHot(r, self.Range), True) and not self.Utils.equals(self.IsSensorHot(b, self.Range), True)):
                return 'FREE'

              