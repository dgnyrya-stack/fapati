"""Модульные и интеграционные тесты калькулятора."""
import unittest
import calculator as c


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        c.memory_clear()

    def test_add(self):
        self.assertEqual(c.add(2, 3), 5)
        self.assertEqual(c.add(-2, 1), -1)

    def test_subtract(self):
        self.assertEqual(c.subtract(7, 3), 4)
        self.assertEqual(c.subtract(2, 5), -3)

    def test_multiply(self):
        self.assertEqual(c.multiply(4, 3), 12)
        self.assertEqual(c.multiply(-2, 0), 0)

    def test_divide(self):
        self.assertEqual(c.divide(8, 2), 4)
        with self.assertRaises(ValueError):
            c.divide(8, 0)

    def test_power(self):
        self.assertEqual(c.power(2, 3), 8)
        self.assertEqual(c.power(4, 0), 1)
        with self.assertRaises(ValueError):
            c.power(0, -1)
        with self.assertRaises(ValueError):
            c.power(-1, 0.5)

    def test_square_root(self):
        self.assertEqual(c.square_root(9), 3)
        self.assertEqual(c.square_root(0), 0)
        with self.assertRaises(ValueError):
            c.square_root(-1)

    def test_factorial(self):
        self.assertEqual(c.factorial(5), 120)
        self.assertEqual(c.factorial(0), 1)
        for value in [-1, 1.5, 171]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                c.factorial(value)

    def test_memory_save_and_read(self):
        c.memory_save(7)
        self.assertEqual(c.memory_read(), 7)

    def test_memory_add(self):
        c.memory_save(7)
        c.memory_add(3)
        self.assertEqual(c.memory_read(), 10)

    def test_memory_clear(self):
        c.memory_save(7)
        c.memory_clear()
        self.assertEqual(c.memory_read(), 0)

    def test_operations_and_memory_together(self):
        # Интеграционная проверка: результат вычисления сохраняется в память.
        c.memory_save(c.multiply(c.add(2, 3), 4))
        c.memory_add(c.square_root(9))
        self.assertEqual(c.memory_read(), 23)


if __name__ == '__main__':
    unittest.main(verbosity=2)
