import unittest
from calculations import *

Test1_Planet1 = Planet(300, 10, 30)
Test1_Planet2 = Planet(200, 20, 400)

Test2_Planet1 = Planet(90000, 0, 0)
Test2_Planet2 = Planet(0, 1000, 1000)

Test3_Planet1 = Planet(0, -50, -20)
Test3_Planet2 = Planet(0, -300, -230)


class TestCalculations(unittest.TestCase):
    def test_calculate_distance(self):
        self.assertEqual(calculate_distance(Test1_Planet1, Test1_Planet2)[0], 370.1351105)
        self.assertEqual(calculate_distance(Test2_Planet1, Test2_Planet2)[0], 1414.2135624)
        self.assertEqual(calculate_distance(Test3_Planet1, Test3_Planet2)[0], 326.4965543)

    def test_calculate_force(self):
        self.assertEqual(calculate_force(Test1_Planet1, Test1_Planet2, 6.67428e-11)[3], 2.9230423e-11)
        self.assertEqual(calculate_force(Test2_Planet1, Test2_Planet2, 6.67428e-11)[3], 0.0000000)
        self.assertEqual(calculate_force(Test3_Planet1, Test3_Planet2, 6.67428e-11)[3], 0.0000000)


if __name__ == "__main__":
    unittest.main()
