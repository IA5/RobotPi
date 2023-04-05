import RPi.GPIO as GPIO
import time

class ProximitySensor:
    
    sensorFront = 6
    sensorBack = 14

    def __init__(self, debug):
        self.Debug = debug

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensorFront,GPIO.IN)
        GPIO.setup(self.sensorBack,GPIO.IN)

    @property
    def Debug(self):
        return self.__Debug

    @Debug.setter
    def Debug(self, val):
        if (val is None):
            val = False
        else:
            self.__Debug = val

    def IsSensorHot(self,sensor):
        if GPIO.input(sensor):
            return False
        else: 
            return True
    
    def IsFrontSensorOn(self):
         s = self.IsSensorHot(self.sensorFront)
         if self.Debug:
                if s:
                    print("Front sensor on")

         return s
        
    def IsBackSensorOn(self):
        s = self.IsSensorHot(self.sensorBack)
        if self.Debug:
                if s:
                    print("Back sensor on")

        return s

    if __name__ == "__main__":
        try:
            import ProximitySensor
            infrared = ProximitySensor.ProximitySensor(True)
       
        except KeyboardInterrupt:
            GPIO.cleanup()
