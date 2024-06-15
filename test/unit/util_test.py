import unittest
import pytest

from unittest.mock import patch
from app import util


@pytest.mark.unit
class TestUtil(unittest.TestCase):
    def test_convert_to_number_correct_param(self):
        self.assertEqual(4, util.convert_to_number("4"))
        self.assertEqual(0, util.convert_to_number("0"))
        self.assertEqual(0, util.convert_to_number("-0"))
        self.assertEqual(-1, util.convert_to_number("-1"))
        self.assertAlmostEqual(4.0, util.convert_to_number("4.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("0.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("-0.0"), delta=0.0000001)
        self.assertAlmostEqual(-1.0, util.convert_to_number("-1.0"), delta=0.0000001)

    def test_convert_to_number_invalid_type(self):
        self.assertRaises(TypeError, util.convert_to_number, "")
        self.assertRaises(TypeError, util.convert_to_number, "3.h")
        self.assertRaises(TypeError, util.convert_to_number, "s")
        self.assertRaises(TypeError, util.convert_to_number, None)
        self.assertRaises(TypeError, util.convert_to_number, object())

    def test_InvalidConvertToNumber_with_valid_input(self):
        self.assertEqual(util.InvalidConvertToNumber("1.23"), 1.23)
        self.assertEqual(util.InvalidConvertToNumber("123"), 123)

    def test_InvalidConvertToNumber_with_invalid_input(self):
        with self.assertRaises(TypeError):
            util.InvalidConvertToNumber("abc")

    def test_validate_permissions_with_user1(self):
        self.assertTrue(util.validate_permissions("operation", "user1"))

    def test_validate_permissions_with_other_user(self):
        self.assertFalse(util.validate_permissions("operation", "user2"))

if __name__ == '__main__':
    unittest.main()
