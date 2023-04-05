import sys
import random
sys.path.append('/home/pi/git/Robotcar')

import threading
from time import sleep
from src.lib.MotorControl import MotorControl
from src.lib.Display import Terminal
from time import sleep
from src.lib.ObstacleAvoidance import ObstacleAvoidance
from src.lib.RemoteControl import RemoteControl
from src.lib.ProximitySensor import ProximitySensor

class RobotController:

    speed = 35
    shift_offset = 10
    turn_offset = 10
    drivecycle_sleep = 0.9

    range = 200

    debug = True
    device = '/dev/input/event0'

    display = Terminal(debug)
    motor = MotorControl(speed, turn_offset, shift_offset, drivecycle_sleep, debug)
    obsAvoidance = ObstacleAvoidance(motor, display, range, debug)
    remote = RemoteControl(display,device,debug)

    t = None
    global stop_autonomous_thread


    def __del__(self):
        self.motor.GPIOCleanUp()
        print("Deleted - RobotController")
    
    def auto(self):
        
        try:
        
          while True:
            
                if (self.stop_autonomous_thread): 
                    break

                self.obsAvoidance.selfDrive()
    
        except KeyboardInterrupt:
           print("Thread Exception Ignored")
           self.motor.stop()
           self.motor.GPIOCleanUp()

        except:
            self.motor.stop()
            self.motor.GPIOCleanUp()

    def main(self):
        try:

            gamePad = -1
            while gamePad == -1:
                gamePad = self.remote.GetInputDevice()

                if (gamePad == -1):
                    continue
                else:
                    break

            self.motor.startMotors()
        
            while True:
       
                remoteCode = self.remote.gamePadCode(gamePad)   
                
                if remoteCode == "F":
                    self.motor.forward(self.motor.Speed)
                elif remoteCode == "RR":
                    self.motor.reverse(self.motor.Speed)
                elif remoteCode == "L":
                    self.motor.turnLeft(self.motor.Speed + self.motor.TurnOffset)
                elif remoteCode == "R":
                    self.motor.turnRight(self.motor.Speed + self.motor.TurnOffset)
                elif remoteCode == "RR":
                    self.motor.reverse(self.motor.Speed)
                elif remoteCode == "RRR":
                    self.motor.rightShift(self.motor.Speed + self.motor.ShiftOffset)
                elif remoteCode == "LLL":
                    self.motor.leftShift(self.motor.Speed + self.motor.ShiftOffset)
                elif remoteCode == "start":
                    self.stop_autonomous_thread = False
                    self.t = threading.Thread(target=self.auto)
                    self.t.daemon = True
                    self.t.start()
                elif remoteCode == "select":
                    self.stop_autonomous_thread= True 
                    sleep(1) 
                    self.t.join()  
                elif remoteCode == "X":
                    self.motor.stop()
                else:
                    self.motor.stop()
                    continue
        except:
            self.motor.stop()
            self.motor.GPIOCleanUp()
        
if __name__ == "__main__":
    try:
      
        r = RobotController()
        r.main()
        
    except KeyboardInterrupt:
        print("Interupted")
    


        
 