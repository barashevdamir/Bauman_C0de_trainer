import unittest

class TestFactorial(unittest.TestCase):
    def test_factorial_of_zero(self):
        result = factorial(0)
        self.assertEqual(result, 1)

    def test_factorial_of_positive_number(self):
        result = factorial(5)
        self.assertEqual(result, 120)

    def test_factorial_of_negative_number(self):
        with self.assertRaises(ValueError):
            factorial(-5)

if __name__ == '__main__':
    unittest.main()
