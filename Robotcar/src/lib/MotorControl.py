from time import sleep
import RPi.GPIO as GPIO

class MotorControl:

    def __init__(self, speed, turnOffset, shiftOffset, driveCycleSleep, debug):
       
        self.Debug = debug

        if self.Debug:
                print(f'Init - Class MotorControl')

        self.Speed = speed
        self.TurnOffset = turnOffset
        self.ShiftOffset = shiftOffset
        self.DriveCycleSleep = driveCycleSleep

        if self.Debug:
                print(f'Speed: {self.Speed}')
                print(f'Turn offsset: {self.TurnOffset}')
                print(f'Shift offset: {self.ShiftOffset}')
                print(f'Drive cycle sleep: {self.DriveCycleSleep}')

        self.gpioInit()

    def __del__(self):
        self.stop()
        self.GPIOCleanUp()

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
    def Speed(self):
        return self.__Speed

    @Speed.setter
    def Speed(self, val):
        if (val is None):
            self.__Speed = 45
        else:
            self.__Speed = val 
            
    @property
    def ShiftOffset(self):
        return self.__ShiftOffset

    @ShiftOffset.setter
    def ShiftOffset(self, val):
        if (val is None):
            self.__ShiftOffset = 35
        else:
            self.__ShiftOffset = val 
    
    @property
    def TurnOffset(self):
        return self.__TurnOffset

    @TurnOffset.setter
    def TurnOffset(self, val):
        if (val is None):
            self.__TurnOffset = 25
        else:
            self.__TurnOffset = val 

    @property
    def DriveCycleSleep(self):
        return self.__DriveCycleSleep

    @DriveCycleSleep.setter
    def DriveCycleSleep(self, val):
        if (val is None):
            self.__DriveCycleSleep = 0.9
        else:
            self.__DriveCycleSleep = val 
    
    def gpioInit(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        pwmFreq = 40

        #BCM Board - MotorController 1
        GPIO.setup(18,GPIO.OUT) #PWMA
        GPIO.setup(4,GPIO.OUT) #AIN2
        GPIO.setup(23,GPIO.OUT) #AIN1
        GPIO.setup(9,GPIO.OUT) #STBY
        GPIO.setup(22,GPIO.OUT) #BIN1
        GPIO.setup(27,GPIO.OUT) #BIN2
        GPIO.setup(17,GPIO.OUT) #PWMB

        #BCM Board - MotorController 2
        GPIO.setup(21,GPIO.OUT) #PWMA
        GPIO.setup(20,GPIO.OUT) #AIN2
        GPIO.setup(26,GPIO.OUT) #AIN1
        GPIO.setup(16,GPIO.OUT) #STBY
        GPIO.setup(19,GPIO.OUT) #BIN1
        GPIO.setup(13,GPIO.OUT) #BIN2
        GPIO.setup(12,GPIO.OUT) #PWMB

        self.pwma = GPIO.PWM(18, pwmFreq)
        self.pwmb = GPIO.PWM(17, pwmFreq)
        self.pwmc = GPIO.PWM(21, pwmFreq) 
        self.pwmd = GPIO.PWM(12, pwmFreq)

        #initialise with pins to low - no motor activity.
        self.stop()

    def startMotors(self):
        if self.Debug:
                print(f'Start motors - speed: {self.Speed}')
        self.pwma.start(self.Speed)
        self.pwmb.start(self.Speed)
        self.pwmc.start(self.Speed)
        self.pwmd.start(self.Speed)

    def rightShift(self,spd):
        if self.Debug:
            print(f'Motors - rightshift: {spd}')
        self.runMotor(0, spd, 0)
        self.runMotor(1, spd, 0)
        
        self.runMotor(2, spd, 1)
        self.runMotor(3, spd, 1)

    def leftShift(self,spd):
        if self.Debug:
            print(f'Motors - leftshift: {spd}')
        self.runMotor(0, spd, 1)
        self.runMotor(1, spd, 1)
        
        self.runMotor(2, spd, 0)
        self.runMotor(3, spd, 0)

    def reverse(self,spd):
        if self.Debug:
            print(f'Motors - reverse: {spd}')
        self.runMotor(0, spd, 0)
        self.runMotor(1, spd, 1)
        
        self.runMotor(2, spd, 0)
        self.runMotor(3, spd, 1)
        
    def forward(self,spd):
        if self.Debug:
            print(f'Motors - forward: {spd}')
        self.runMotor(0, spd, 1)
        self.runMotor(1, spd, 0)
        
        self.runMotor(2, spd, 1)
        self.runMotor(3, spd, 0)
        
    def turnLeft(self,spd):
        if self.Debug:
            print(f'Motors - turnLeft: {spd}')
        self.runMotor(0, spd, 0)
        self.runMotor(1, spd, 0)
        
        self.runMotor(2, spd, 0)
        self.runMotor(3, spd, 0)

    def turnRight(self,spd):
        if self.Debug:
            print(f'Motors - turnRight: {spd}')
        self.runMotor(0, spd, 1)
        self.runMotor(1, spd, 1)
        
        self.runMotor(2, spd, 1)
        self.runMotor(3, spd,1)

    def runMotor(self,motor, spd, direction):
        in1 = GPIO.HIGH
        in2 = GPIO.LOW
        GPIO.output(9, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        
        if (direction == 1):
            in1 = GPIO.LOW
            in2 = GPIO.HIGH

        if (motor == 0):
            GPIO.output(23, in1)
            GPIO.output(4, in2)
            self.pwma.ChangeDutyCycle(spd)
        elif(motor == 1):
            GPIO.output(22, in1)
            GPIO.output(27, in2)
            self.pwmb.ChangeDutyCycle(spd)
        elif(motor == 2):
            GPIO.output(26, in1)
            GPIO.output(20, in2)
            self.pwmc.ChangeDutyCycle(spd)
        elif(motor == 3):
            GPIO.output(19, in1)
            GPIO.output(13, in2)
            self.pwmd.ChangeDutyCycle(spd)
        
    def stop(self):
        if self.Debug:
            print(f'Motors - stop')
        GPIO.output(9, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)

    def GPIOCleanUp(self):
        GPIO.cleanup()
        

    ##Main
    ####################### 
    def main(self):
        self.startMotors()
        
        i = 1
        while i < 2:
            i += 1
            
            self.forward(100)
            sleep(2)
            self.stop()
            sleep(.25)
            
            self.reverse(100)
            sleep(2)
            self.stop()
            sleep(.25)
        
            self.turnLeft(100)
            sleep(2)
            self.stop()
            sleep(.25)
            
            self.turnRight(100)
            sleep(2)
            self.stop()
            sleep(.25)
            
            self.rightShift(100)
            sleep(2)
            self.stop()
            sleep(.25)
                
            self.leftShift(100)
            sleep(2)
            self.stop()
            sleep(2)
            
    if __name__ == "__main__":
        try:
            import MotorControl
            #motor = MotorControl.MotorControl(5,25,35,0.9, True)
            motor = MotorControl.MotorControl(True)
            motor.main()
            del motor
        except KeyboardInterrupt:
            GPIO.output(9, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            GPIO.cleanup()

        
        


