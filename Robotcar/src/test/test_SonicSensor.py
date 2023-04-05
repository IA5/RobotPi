import sys
sys.path.append('/home/pi/git/Robotcar')

import unittest
from src.lib.SonicSensor import SonicSensor
from src.test.constants import *

class test_UltraSonicSensors(unittest.TestCase):

    def test_IsSensorHot_SonicSensor(self):

        range = 550
        Sensor = SonicSensor(0, False)

        #check for valid sensor variable as a integer value '
        self.assertFalse(Sensor.IsSensorHot(0.1, range))
        
        #check if sensor is 0 return false'
        self.assertFalse(Sensor.IsSensorHot(0, range))
        
        #check sensor reading is less than range value return True
        self.assertTrue(Sensor.IsSensorHot(300, range))

        #check sensor readimg is greater than range return false
        self.assertFalse(Sensor.IsSensorHot(700, range))

    def test_Range_SonicSensor(self):

        
        Sensor = SonicSensor(0, False)

        self.inputval = -1
        #negative number returns 0
        Sensor.Range = self.inputval
        self.assertEqual(Sensor.Range, 0)
        
        self.inputval = 1600
        #val greater than 1500 returns 1500
        Sensor.Range = self.inputval
        self.assertEqual(Sensor.Range, 1500)

        self.inputval = 1000
        #val greater than 1500 returns 1500
        Sensor.Range = self.inputval
        self.assertEqual(Sensor.Range,1000)

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


    def test_GetDirectionCode_SonicSensor_FBL(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_FBL), "FBL")

    def test_GetDirectionCode_SonicSensor_FB(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_FB), "FB")

    def test_GetDirectionCode_SonicSensor_FR(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_FR), "FR")

    def test_GetDirectionCode_SonicSensor_FLR(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_FLR), "FLR")
    
    def test_GetDirectionCode_SonicSensor_F(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_F), "F")

    def test_GetDirectionCode_SonicSensor_BL(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_BL), "BL")

    def test_GetDirectionCode_SonicSensor_BLR(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_BLR), "BLR")
    
    def test_GetDirectionCode_SonicSensor_RL(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_RL), "RL")

    def test_GetDirectionCode_SonicSensor_L(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_L), "L")
  
    def test_GetDirectionCode_SonicSensor_FL(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_FL), "FL")

    def test_GetDirectionCode_SonicSensor_BR(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_BR), "BR")

    def test_GetDirectionCode_SonicSensor_R(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_R), "R")

    def test_GetDirectionCode_SonicSensor_RBF(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_RBF), "RBF")

    def test_GetDirectionCode_SonicSensor_B(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_B), "B")

    def test_GetDirectionCode_SonicSensor_FBLR(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_FBLR), "FBLR")

    def test_GetDirectionCode_SonicSensor_0_1(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_1),None)

    def test_GetDirectionCode_SonicSensor_0_2(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_2),None)

    def test_GetDirectionCode_SonicSensor_0_3(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_3),None)

    def test_GetDirectionCode_SonicSensor_0_4(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_4),None)

    def test_GetDirectionCode_SonicSensor_0_5(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_5),None)

    def test_GetDirectionCode_SonicSensor_0_6(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_6),None)

    def test_GetDirectionCode_SonicSensor_0_7(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_7),None)

    def test_GetDirectionCode_SonicSensor_0_8(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_8),None)

    def test_GetDirectionCode_SonicSensor_0_9(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_9),None)

    def test_GetDirectionCode_SonicSensor_0_10(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_10),None)

    def test_GetDirectionCode_SonicSensor_0_11(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_11),None)

    def test_GetDirectionCode_SonicSensor_0_12(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_12),None)

    def test_GetDirectionCode_SonicSensor_0_13(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_13),None)

    def test_GetDirectionCode_SonicSensor_0_14(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_14),None)

    def test_GetDirectionCode_SonicSensor_0_15(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_15),None)

    def test_GetDirectionCode_SonicSensor_0_16(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_0_16),None)

    def test_GetDirectionCode_SonicSensor_Freeway(self):
        sensor = SonicSensor(range, False)
        self.assertEqual(sensor.GetDistanceCode(sonicSensorRead_Freeway),None)        


#     sonicSensorRead_0_1 = [0, 1500.00, 1500.00, 1500.00]
# sonicSensorRead_0_2 = [0, 0, 1500.00, 1500.00]
# sonicSensorRead_0_3 = [0, 0, 0, 1500.00]
# sonicSensorRead_0_4 = [0, 0, 0, 0]

# sonicSensorRead_0_5 = [1500.00, 0, 0, 0]
# sonicSensorRead_0_6 = [1500.00, 1500.00, 0, 0]
# sonicSensorRead_0_7 = [1500.00, 1500.00, 1500.00, 0]
# sonicSensorRead_0_8 = [0, 1500.00, 1500.00, 1500.00]

# sonicSensorRead_0_9 = [1500.00, 1500.00, 0, 0]
# sonicSensorRead_0_10 = [0, 1500.00,1500.00, 0]
# sonicSensorRead_0_11 = [1500.00, 0, 1500.00, 1500.00]
# sonicSensorRead_0_12 = [1500.00, 1500.00, 0, 1500.00]

# sonicSensorRead_0_13 = [0, 1500.00, 0, 0]
# sonicSensorRead_0_14 = [0, 0,1500.00, 0]
# sonicSensorRead_0_15 = [1500.00, 0, 1500.00, 0]
# sonicSensorRead_0_16 = [0, 1500.00, 0, 1500.00]

# sonicSensorRead_Freeway = [1500.00, 1500.00, 1500.00, 1500.00]

if __name__ == '__main__':
    unittest.main(exit=False)
