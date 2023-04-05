import sys
sys.path.append('/home/pi/git/Robotcar')
import unittest
loader = unittest.TestLoader()
tests = loader.discover('src/test')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)