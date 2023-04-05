import UltraBorg3 as UltraBorg
import time
import os
from demo_opts import get_device
from luma.core.virtual import terminal
from PIL import ImageFont
import datetime

from time import sleep
import RPi.GPIO as GPIO

#pantilthat
import pantilthat
from sys import exit

from decimal import Decimal
from timer import Timer
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False);

sonicSensorRangeMm = 550
pwmFreq = 100
speed = 30
motor_delay_time = 0.5
t = Timer()

#Motor 1
GPIO.setup(18,GPIO.OUT) #PWMA
GPIO.setup(4,GPIO.OUT) #AIN2
GPIO.setup(23,GPIO.OUT) #AIN1
GPIO.setup(9,GPIO.OUT) #STBY
GPIO.setup(22,GPIO.OUT) #BIN1
GPIO.setup(27,GPIO.OUT) #BIN2
GPIO.setup(17,GPIO.OUT) #PWMB

#Motor 2
GPIO.setup(21,GPIO.OUT) #PWMA
GPIO.setup(20,GPIO.OUT) #AIN2
GPIO.setup(26,GPIO.OUT) #AIN1
GPIO.setup(16,GPIO.OUT) #STBY
GPIO.setup(19,GPIO.OUT) #BIN1
GPIO.setup(13,GPIO.OUT) #BIN2
GPIO.setup(12,GPIO.OUT) #PWMB

pwm1a = GPIO.PWM(18, pwmFreq) # pin 12 to PWM 
pwm1b = GPIO.PWM(17, pwmFreq) # pin 11 to PWM -- front right 

pwm2a = GPIO.PWM(21, pwmFreq) # pin 40 to PWM
pwm2b = GPIO.PWM(12, pwmFreq) # pin 32 to PWM

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))
    
def measure_time():
    timezone_aware_dt = datetime.datetime.now(datetime.timezone.utc)
    return(str(timezone_aware_dt))

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

def printToDisplay(text):
        for fontname, size in [(None, None), ("tiny.ttf", 6), ("ProggyTiny.ttf", 16), ("creep.bdf", 16), ("miscfs_.ttf", 12), ("FreePixel.ttf", 12), ('ChiKareGo.ttf', 16)]:
            font = make_font(fontname, size) if fontname else None
            term = terminal(device, font)

            term.println(text)
            term.clear()

def left(spd):
    runMotor(1, spd, 0) 
    runMotor(2, spd, 0)
    runMotor(3, spd, 0)
    runMotor(4, spd, 0)
    
def right(spd):
    runMotor(1, spd, 1)
    runMotor(2, spd, 1)
    runMotor(3, spd, 1)
    runMotor(4, spd, 1)
    
def reverse(spd):
    runMotor(1, spd, 0)
    runMotor(2, spd, 0)
    runMotor(3, spd, 1)
    runMotor(4, spd, 1)

def forward(spd):
    runMotor(1, spd, 1)
    runMotor(2, spd, 1)
    runMotor(3, spd, 0)
    runMotor(4, spd, 0)

def runMotor(motor, spd, direction):
    in1 = GPIO.HIGH
    in2 = GPIO.LOW
    #Motor 1
    GPIO.output(9, GPIO.HIGH);
    #Motor 2
    GPIO.output(16, GPIO.HIGH);
    
    if (direction == 1):
        in1 = GPIO.LOW
        in2 = GPIO.HIGH
    if (motor == 1):
        #Motor 1
        GPIO.output(23, in1)
        GPIO.output(4, in2)
        pwm1a.ChangeDutyCycle(spd)
    elif(motor == 2):
        #Motor 2
        GPIO.output(22, in1)
        GPIO.output(27, in2)
        pwm1b.ChangeDutyCycle(spd)
    elif (motor == 3):
        #Motor 3
        GPIO.output(26, in1)
        GPIO.output(20, in2)
        pwm2a.ChangeDutyCycle(spd)
    elif(motor == 4):
        #Motor 4
        GPIO.output(19, in1)
        GPIO.output(13, in2)
        pwm2b.ChangeDutyCycle(spd)
    
def motorStop():
    #Motor 1
    GPIO.output(9, GPIO.LOW)
     #Motor 2
    GPIO.output(16, GPIO.LOW);


def panTiltApi(direction, angle):
    
    if angle < 0 or angle > 180:
        return "{'error':'out of range'}"

    angle -= 90

    if direction == 'pan':
        pantilthat.pan(angle)
        print("{{'pan':{}}}".format(angle))
        return

    elif direction == 'tilt':
        pantilthat.tilt(angle)
        print("{{'tilt':{}}}".format(angle))
        return

    print("{'error':'invalid direction'}")
    return

def recon():
    elapsedTime = t.stop()
    print(str(round(elapsedTime) % 20))
    
    if (round(elapsedTime) % 20 == 0):
        motorStop()
        for x in range(181):
            panTiltApi('pan', x)
            sleep(0.07)
        
        for y in range(30,56):
            panTiltApi('tilt', y)
            sleep(0.07)

##Main
####################### 
    
def main(args=None):
    t.start()

    echoCountBL = 0
    echoCountBR = 0
    echoCountFL = 0
    echoCountFR = 0
    
    echoCountBLErr = 0
    echoCountBRErr = 0
    echoCountFLErr = 0
    echoCountFRErr = 0
    while True:
        for fontname, size in [(None, None), ("tiny.ttf", 6), ("ProggyTiny.ttf", 16), ("creep.bdf", 16), ("miscfs_.ttf", 12), ("FreePixel.ttf", 12), ('ChiKareGo.ttf', 16)]:
            font = make_font(fontname, size) if fontname else None
            term = terminal(device, font)
         
        usm1 = UB.GetDistance1()
        usm2 = UB.GetDistance2()
        usm3 = UB.GetDistance3()
        usm4 = UB.GetDistance4()

        # Convert to the nearest millimeter
        usm1 = int(usm1)
        usm2 = int(usm2)
        usm3 = int(usm3)
        usm4 = int(usm4)
        
        if (usm1 < sonicSensorRangeMm and usm2 < sonicSensorRangeMm and usm3 < sonicSensorRangeMm and usm4 < sonicSensorRangeMm):
            left(speed)
            left(speed)
            reverse(speed)
            right(speed)
            right(speed)
            forward(speed)
        else:
        # Display the readings
            if usm1 == 0:
                print('#1 No reading')
                term.println('#1 No reading')
            else:
                print('#1 % 4d mm' % (usm1))
                term.println('#1 % 4d mm' % (usm1))
                
                if (usm1 < sonicSensorRangeMm):
                    echoCountFL += 1
                    sleep(motor_delay_time)
                    recon()
                    if echoCountFL > 1:
                        reverse(speed) 
                        sleep(motor_delay_time)
                        right(speed)
                        sleep(motor_delay_time) 
                        echoCountFLErr += 1
                        if echoCountFLErr > 2:
                            forward(speed)
                            print('FLErr-fwd')
                            right(speed)
                            right(speed)
                            print('right-right')
                        echoCountFL = 1
                    else:
                        forward(speed)
                        echoCountFLErr = 0 
                else:
                    echoCountFL = 1
                    forward(speed)
            
            if usm2 == 0:
                print('#2 No reading')
                term.println('#2 No reading')
            else:
                print('#2 % 4d mm' % (usm2))
                term.println('#2 % 4d mm' % (usm2))
                
                if (usm2 < sonicSensorRangeMm):
                    echoCountFR += 1
                    sleep(motor_delay_time)
                    recon()
                    if echoCountFR > 1:
                        reverse(speed) 
                        sleep(motor_delay_time)
                        left(speed)
                        sleep(motor_delay_time)
                        echoCountFRErr += 1
                        if echoCountFRErr > 2:
                            reverse(speed)
                            print('FRErr-rev')
                            left(speed)
                            left(speed)
                            print('Left-Left')
                        echoCountFR = 1
                    else:
                        forward(speed)
                        echoCountFRErr = 0
                else:
                    echoCountFR = 1
                    forward(speed)

            if usm3 == 0:
                print ('#3 No reading')
                term.println('#3 No reading')
            else:
                print('#3 % 4d mm' % (usm3))
                term.println('#3 % 4d mm' % (usm3))
                
                if (usm3 < sonicSensorRangeMm):
                    echoCountBR += 1
                    sleep(motor_delay_time)
    #               
                    recon()
                    if echoCountBR > 1:
                        forward(speed) 
                        sleep(motor_delay_time)
                        left(speed)
                        sleep(motor_delay_time)
                        echoCountBRErr += 1
                        if echoCountBRErr > 2:
                            forward(speed)
                            left(speed)
                            left(speed)
                        echoCountBR = 1
                    else:
                        reverse(speed)
                        echoCountBRErr = 0
                else:
                    echoCountBR = 1
                    reverse(speed)
            
            if usm4 == 0:
                print ('#4 No reading')
                term.println('#4 No reading')
            else:
                print ('#4 % 4d mm' % (usm4))
                term.println('#4 % 4d mm' % (usm4))
                    
                if (usm4 < sonicSensorRangeMm):
                    echoCountBL += 1
                    sleep(motor_delay_time)
                    recon()
                    if echoCountBL > 1:
                        forward(speed) 
                        sleep(motor_delay_time)
                        right(speed)
                        sleep(motor_delay_time)
                        echoCountBLErr += 1
                        if echoCountBLErr > 2:
                            forward(speed)
                            left(speed)
                            left(speed)
                        echoCountBL = 1
                    else:
                        reverse(speed)
                        echoCountBLErr = 0
                        
                else:
                    echoCountBL = 1
                    reverse(speed)                      
        term.println(measure_temp())
        term.println(measure_time())
       # time.sleep(.1)
        print(measure_temp())
        
if __name__ == "__main__":
    try:
        device = get_device()
        printToDisplay("Start the UltraBorg")
        printToDisplay(measure_time())
        UB = UltraBorg.UltraBorg()
        UB.i2cAddress = 36
        # Create a new UltraBorg object
        UB.Init()
        panTiltApi('pan', 0)
        panTiltApi('tilt', 90)
        main()
        
    except KeyboardInterrupt:
        #Motor 1
        GPIO.output(9, GPIO.LOW)
        #Motor 2
        GPIO.output(16, GPIO.LOW);
        GPIO.cleanup()






