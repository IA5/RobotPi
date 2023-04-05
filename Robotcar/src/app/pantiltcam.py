import sys
sys.path.append('/home/pi/git/pantilt-sandbox')
from RemoteControl import RemoteControl
from Display import Terminal
import time
import os
import datetime

from time import sleep
import RPi.GPIO as GPIO

#pantilthat
import pantilthat
from sys import exit

from decimal import Decimal
from timer import Timer

class pantiltControl:
    t = Timer()

    debug = True
    device = '/dev/input/event0'

    display = Terminal(debug)
    remote = RemoteControl(display,device,debug)

    def measure_temp():
            temp = os.popen("vcgencmd measure_temp").readline()
            return (temp.replace("temp=",""))
        
    def measure_time():
        timezone_aware_dt = datetime.datetime.now(datetime.timezone.utc)
        return(str(timezone_aware_dt))


    def panTiltApi(self,direction, angle):
        
        #if angle < 0 or angle > 180:
         #   return "{'error':'out of range'}"

        #angle -= 180

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
            for x in range(180):
                panTiltApi('pan', x)
                #raspistill -vf -o image.jpg
                sleep(0.20)
                
        #      for i in range(90,-1,-1):
        #         panTiltApi('tilt', i)
        #         sleep(0.20)
                panTiltApi('tilt', 75)
                    
                
        #         for y in range(30,56):
        #             panTiltApi('tilt', y)
        #             sleep(0.07)

    ##Main
    ####################### 

    def main2(self):
            
        gamePad = -1
        pan_angle = -10
        tilt_angle = -10

        while gamePad == -1:
            gamePad = self.remote.GetInputDevice()

            if (gamePad == -1):
                continue
            else:
                break

        while True:

            remoteCode = self.remote.gamePadCode(gamePad)   
            
            if remoteCode == "F":
                #self.motor.forward(self.motor.Speed)
                tilt_angle= tilt_angle - 1
                self.panTiltApi('tilt', tilt_angle)
            elif remoteCode == "RR":
                tilt_angle= tilt_angle + 1
                self.panTiltApi('tilt', tilt_angle)
                #self.motor.reverse(self.motor.Speed)
            elif remoteCode == "L":
                pan_angle= pan_angle - 1
                self.panTiltApi('pan', pan_angle)
                #self.motor.turnLeft(self.motor.Speed + self.motor.TurnOffset)
            elif remoteCode == "R":
                pan_angle= pan_angle + 1
                self.panTiltApi('pan', pan_angle)
            elif remoteCode == "DUP":
                #self.motor.forward(self.motor.Speed)
                tilt_angle= tilt_angle - 10
                tilt_angle = self.angleGuard(tilt_angle, 'tilt')
                self.panTiltApi('tilt', tilt_angle)
            elif remoteCode == "DDOWN":
                tilt_angle= tilt_angle + 10
                tilt_angle = self.angleGuard(tilt_angle, 'tilt')
                self.panTiltApi('tilt', tilt_angle)
                #self.motor.reverse(self.motor.Speed)
            elif remoteCode == "DLEFT":
                pan_angle= pan_angle - 10
                pan_angle = self.angleGuard(pan_angle, 'pan')
                self.panTiltApi('pan', pan_angle)
                #self.motor.turnLeft(self.motor.Speed + self.motor.TurnOffset)
            elif remoteCode == "DRIGHT":
                pan_angle= pan_angle + 10
                pan_angle = self.angleGuard(pan_angle, 'pan')
                self.panTiltApi('pan', pan_angle)
            #    self.panTiltApi('tilt', tilt_angle + 5)
                #self.motor.turnRight(self.motor.Speed + self.motor.TurnOffset)
            #elif remoteCode == "RR":
                #self.motor.reverse(self.motor.Speed)
            #elif remoteCode == "RRR":
                #self.motor.rightShift(self.motor.Speed + self.motor.ShiftOffset)
            #elif remoteCode == "LLL":
                #self.motor.leftShift(self.motor.Speed + self.motor.ShiftOffset)
            #elif remoteCode == "start":
                #self.stop_autonomous_thread = False
                #self.t = threading.Thread(target=self.auto)
                #self.t.daemon = True
                #self.t.start()
            #elif remoteCode == "select":
                #self.stop_autonomous_thread= True 
            #    sleep(1) 
                ##self.t.join()  
            #elif remoteCode == "X":
                #self.motor.stop()
            else:
                #self.motor.stop()
                continue

    def angleGuard(self, tangle, direction):    
        angle = tangle
        if direction == 'pan':
            if tangle > 90:
                angle = 90 
            if tangle < -90:
                angle = -90

        if direction == 'tilt':
            if tangle > 60:
                angle = 60 
            if tangle < -80:
                angle = -80

        return angle
      

    def main(args=None):
        t.start()

        while True:
            recon()
                         
if __name__ == "__main__":
    try:
        #set Camera to default position
        #panTiltApi('pan', 90)
        #panTiltApi('tilt', 75)
        from pantiltcam import pantiltControl
        p = pantiltControl()
        p.main2()
        
    except KeyboardInterrupt:
        GPIO.cleanup()
      




