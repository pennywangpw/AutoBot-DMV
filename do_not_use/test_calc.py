import unittest
import calc

class TestCalc(unittest.TestCase):

    def test_add(self):
        result = calc.add(10,5)
        self.assertEqual(result,15)

        self.assertEqual(calc.add(10,3),13)
        self.assertEqual(calc.add(0,0),0)
        self.assertEqual(calc.add(-1,3),2)
        self.assertEqual(calc.add(-1,-2),-3)


    def test_subtract(self):
        result = calc.subtract(10,5)
        self.assertEqual(result,5)
        self.assertEqual(calc.subtract(0,5),-5)
        self.assertEqual(calc.subtract(-1,-2),1)
        self.assertEqual(calc.subtract(0,-2),2)
        self.assertEqual(calc.subtract(-3,5),-8)


    def test_multiply(self):
        result = calc.multiply(10,5)
        self.assertEqual(result,50)
        self.assertEqual(calc.multiply(0,5),0)
        self.assertEqual(calc.multiply(-5,5),-25)
        self.assertEqual(calc.multiply(-5,-5),25)


    def test_divide(self):
        result = calc.divide(10,5)
        self.assertEqual(result,2)
        self.assertEqual(calc.divide(10,-5),-2)
        self.assertEqual(calc.divide(-10,-5),2)
        self.assertEqual(calc.divide(-10,10),-1)




if __name__ == '__main__':
    unittest.main()
