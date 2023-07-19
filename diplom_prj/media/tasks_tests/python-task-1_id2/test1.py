import unittest
class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        result = add(-5, -7)
        self.assertEqual(result, -12)

    def test_add_positive_and_negative_numbers(self):
        result = add(10, -3)
        self.assertEqual(result, 7)

    def test_add_zero_to_number(self):
        result = add(10, 0)
        self.assertEqual(result, 10)

if __name__ == '__main__':
    unittest.main()
