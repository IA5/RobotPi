from src.lib.SonicSensor import SonicSensor
from time import sleep
import random

class ObstacleAvoidance:

    codeList = []

    directionCode_count =  3
    retry_obs_count = 2 #2
    obstruction_buffer = 20
    sensor = None

    def __init__(self, motor, display, range, debug):
        self.Motor = motor
        self.Display = display
        self.Debug = debug

        self.Range = range
        self.sensor = SonicSensor(range,self.Display,debug)

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
    def Motor(self):
        return self.__Motor

    @Motor.setter
    def Motor(self, val):
        if (val is None):
            self.__Motor = MotorControl(None, None, None, None, None, self.Debug)
        else:
            self.__Motor = val 

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
    def Range(self):
        return self.__Range

    @Range.setter
    def Range(self, val):
        if (val is None):
            self.__Range = 450
        else:
            self.__Range = val 

    def selfDrive(self):
        sleep(2)
        sensorReading = self.sensor.GetSensorReading()
        directionCode = self.sensor.GetDistanceCode(sensorReading)
        self.navigate(sensorReading, directionCode)

   
    def navigate(self,sensorReading, directionCode):
        if ((sensorReading.count(0) >= 1) or (sensorReading[0] is not None and sensorReading[0] <= self.obstruction_buffer) 
            or (sensorReading[1] is not None and sensorReading[1] <= self.obstruction_buffer) or (sensorReading[2] is not None and sensorReading[2] <= self.obstruction_buffer) 
                or (sensorReading[3] is not None and sensorReading[3] <= self.obstruction_buffer)):
            self.logDirectionCode(directionCode)
            if (directionCode != "Free"):
                if (self.codeList.count(directionCode) >= self.retry_obs_count):
                    directionCode = self.swapBlockedCode(directionCode)
                    self.Display.consolePrint('Codeswap - % s' % (directionCode))
            
        self.detectObstacles(directionCode, self.Motor, self.Display)
              
    def logDirectionCode(self, code):
        print(self.codeList)
        if len(self.codeList) >= self.directionCode_count:
            self.codeList.clear()
        
        self.codeList.append(code)
    
    def countDirectionCode(self,code):
        self.codeList.count(code)

    def swapBlockedCode(self,odCode):        
        if odCode == "FF":
            return "BB"
        elif odCode == "RR":
            return "LL"           
        elif odCode == "LL":
            return "RR"            
        elif odCode == "BB":
            return "FF"
        elif odCode == None:
            return "BB" 
        elif odCode == "FBL":
            return "RBF"    
        elif odCode == "FR":
            dcodes = ["B", "L"]
            code = random.choice(dcodes)
            return code
        elif odCode == "FLR":
            return "F"
        elif odCode == "F":
            return "B"
        elif odCode == "BL":
            dcodes = ["F", "R"]
            code = random.choice(dcodes)
            return code
        elif odCode == "BLR":
            return "R"
        elif odCode == "RL":
            dcodes = ["B", "LL"]
            code = random.choice(dcodes)
            return code
        elif odCode == "L":
            return "R"
        elif odCode == "FL":
            dcodes = ["RR", "R"]
            code = random.choice(dcodes)
            return code
        elif odCode == "BR":
            dcodes = ["F", "L"]
            code = random.choice(dcodes)
            return code
        elif odCode == "R":
            return "F"
        elif odCode == "RBF":
            return "FBL"
        elif odCode == "B":
            return "F"
        elif odCode == "FBLR":
            return "F"
        elif odCode == "FREE":
            return "B"
       
    def detectObstacles(self,directionCode, motor, display):
        motor.startMotors()
        if (directionCode == "FBL"):
            display.print("rightShift")
            motor.turnRight(motor.Speed + motor.ShiftOffset)  
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FB"):
            dcodes = ["RS", "LS"]
            rc = random.choice(dcodes) 
            if rc == "RS":
                display.print("rightShift")
                motor.turnRight(motor.Speed + motor.ShiftOffset)
            elif rc == "LS":
                display.print("leftShift")
                motor.turnLeft(motor.Speed + motor.TurnOffset)  
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FR"):
            dcodes = ["RR", "L"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FLR"):
            motor.reverse(motor.Speed)
            display.print("reverse")    
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FF"):
            dcodes = ["RR", "F", "L", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "RR"):
            dcodes = ["RS", "RR"]
            rc = random.choice(dcodes) 
            if rc == "RS":
                display.print("rightShift")
                motor.turnRight(motor.Speed + motor.ShiftOffset)
            elif rc == "RR":
                display.print("right")
                motor.turnRight(motor.Speed)
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "LL"):
            dcodes = ["LS", "LL"]
            rc = random.choice(dcodes) 
            if rc == "LS":
                display.print("leftShift")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "LL":
                display.print("left")
                motor.turnLeft(motor.Speed)
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "BB"):
            dcodes = ["RR", "F", "L", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.ShiftOffset)
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "F"):
            dcodes = ["RR", "L", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "BL"):
            dcodes = ["F", "R"]
            rc = random.choice(dcodes) 
            if rc == "F":
                display.print("forward")
                motor.forward(motor.Speed)  
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "BLR"):
            display.print("forward")
            motor.forward(motor.Speed)   
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "RL"):
            dcodes = ["F", "RR"]
            rc = random.choice(dcodes) 
            if rc == "F":
                display.print("forward")
                motor.forward(motor.Speed)  
            elif rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "L"):
            dcodes = ["RR", "F", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FL")  :
            dcodes = ["RR", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "BR"):
            dcodes = ["F", "L"]
            rc = random.choice(dcodes) 
            if rc == "F":
                display.print("forward")
                motor.forward(motor.Speed)  
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "R"):
            dcodes = ["RR", "F", "L"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "F":
                display.print("reverse")
                motor.forward(motor.Speed) 
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "RBF"):
            display.print("leftShift") 
            motor.turnLeft(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "B"):
            dcodes = ["F", "L", "R"]
            rc = random.choice(dcodes) 
            if rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FBLR"):
            dcodes = ["RR", "F", "L", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
            sleep(motor.DriveCycleSleep)
        elif (directionCode == "FREE"):
            dcodes = ["RR", "F", "L", "R"]
            rc = random.choice(dcodes) 
            if rc == "RR":
                display.print("reverse")
                motor.reverse(motor.Speed)  
            elif rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "L":
                display.print("left")
                motor.turnLeft(motor.Speed + motor.TurnOffset) 
            elif rc == "R":
                display.print("right")
                motor.turnRight(motor.Speed + motor.TurnOffset) 
        elif (directionCode == None):
            dcodes = ["RR", "F"]
            rc = random.choice(dcodes) 
            if rc == "F":
                display.print("forward")
                motor.forward(motor.Speed) 
            elif rc == "R":
                display.print("reverse")
                motor.reverse(motor.Speed) 
 