import unittest
import pytest

from unittest.mock import patch
from app.calc import Calculator, InvalidPermissions


def mocked_validation(*args, **kwargs):
    return True
def mocked_validation_invalidUser(*args, **kwargs):
    return False

@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    def test_substract_method_returns_correct_result(self):
        self.assertEqual(0, self.calc.substract(2, 2))
        self.assertEqual(4, self.calc.substract(2, -2))
        self.assertEqual(-4, self.calc.substract(-2, 2))
        self.assertEqual(1, self.calc.substract(1, 0))
        self.assertEqual(0, self.calc.substract(0, 0))

    def test_divide_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))

    def test_add_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())

    def test_divide_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_divide_method_fails_with_division_by_zero(self):
        self.assertRaises(TypeError, self.calc.divide, 2, 0)
        self.assertRaises(TypeError, self.calc.divide, 2, -0)
        self.assertRaises(TypeError, self.calc.divide, 0, 0)
        self.assertRaises(TypeError, self.calc.divide, "0", 0)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))
        self.assertEqual(4, self.calc.multiply(-2, -2))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_with_invalid_parameters(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.multiply, 2, "2")
        self.assertRaises(TypeError, self.calc.multiply, "2", "2")
        self.assertRaises(TypeError, self.calc.multiply, None, 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, None)
        self.assertRaises(TypeError, self.calc.multiply, object(), 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, object())

    @patch('app.util.validate_permissions', side_effect=mocked_validation_invalidUser, create=True)
    def test_multiply_method_invalid_permissions(self, _validate_permissions):
        self.assertRaises(InvalidPermissions, self.calc.multiply, "2", 2)

    def test_power_method_returns_correct_result(self):
        self.assertEqual(0, self.calc.power(0, 2))
        self.assertEqual(1, self.calc.power(2, 0))
        self.assertEqual(-1, self.calc.power(-1, 3))
        self.assertEqual(1, self.calc.power(-1, 4))
        self.assertEqual(4, self.calc.power(2, 2))
        self.assertEqual(8, self.calc.power(2, 3))

    def test_log_base_10_positive(self):
        self.assertAlmostEqual(3.0, self.calc.log_base_10(1000), delta=0.0000001)
        self.assertAlmostEqual(2.0, self.calc.log_base_10(100), delta=0.0000001)
        self.assertAlmostEqual(1.0, self.calc.log_base_10(10), delta=0.0000001)
        self.assertAlmostEqual(0.0, self.calc.log_base_10(1), delta=0.0000001)

    def test_log_base_10_negative_or_zero(self):
        with self.assertRaises(ValueError):
            self.calc.log_base_10(-10)
        with self.assertRaises(ValueError):
            self.calc.log_base_10(0)

    def test_log_base_10_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.log_base_10("abc")

    def test_square_root_positive(self):
        self.assertAlmostEqual(5.0, self.calc.square_root(25), delta=0.0000001)
        self.assertAlmostEqual(0.5, self.calc.square_root(0.25), delta=0.0000001)
        self.assertAlmostEqual(0.0, self.calc.square_root(0), delta=0.0000001)

    def test_square_root_negative(self):
        with self.assertRaises(ValueError):
            self.calc.square_root(-25)

    def test_square_root_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.square_root("abc")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
