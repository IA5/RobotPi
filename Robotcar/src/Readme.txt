Please use the follwoing #startup args --display ssd1322 --interface spi --width 256 --height 64  if you wish to attach a display to your robot.

This project requires a RaspberryPi ARM Processor.

Built orignally on a RPI4, using Python 3.

Remote control via a bluetooth Xbox controller, allows switching from manual to semi-autonomous mode.
The bluetooth controller must first be paired with the Pi to allow control from boot up.

Semi autonomous mode uses the 4 sonar sensors on the robot to detect obstacles and move around the area in a random pattern. 
The objective being to not bump into anything.

Manual mode allows for remote operation of the Robot and together with the motion daemon a live feed is provided which allows the Robot to 
be controlled remotely.

Next steps:

Add a AI capabaility for Image Recognition, allow family members to be identified and greeted on identification.
        
Tests

Runtests.py for running the supplied tests.