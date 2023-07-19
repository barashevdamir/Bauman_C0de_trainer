import unittest
import sys
import io

class DivideTestCase(unittest.TestCase):

    def test_divide(self):
        # Тестирование деления с ненулевым делителем
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(5, 2), 2.5)
        self.assertEqual(divide(100, 10), 10)

    def test_divide_by_zero(self):
        # Тестирование деления на ноль и проверка вывода сообщения об ошибке
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        divide(10, 0)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Error: Division by zero is not allowed.")

        sys.stdout = original_stdout

if __name__ == '__main__':
    unittest.main()