import unittest
import pytest
import http.client

from unittest.mock import patch
from flask import Flask
from app import util
from app.calc import Calculator
from app.api import api_application

@pytest.mark.unit
class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = api_application.test_client()
        self.app.testing = True

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello from The Calculator!\n")

    def test_add_correct_params(self):
        response = self.app.get('/calc/add/4/5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '9')

        response = self.app.get('/calc/add/4.5/5.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '10.0')

    def test_add_invalid_params(self):
        response = self.app.get('/calc/add/4/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))

    def test_substract_correct_params(self):
        response = self.app.get('/calc/substract/10/5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '5')

        response = self.app.get('/calc/substract/10.5/5.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '5.0')

    def test_substract_invalid_params(self):
        response = self.app.get('/calc/substract/10/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))

    def test_power_correct_params(self):
        response = self.app.get('/calc/power/2/3')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 8.0)

        response = self.app.get('/calc/power/4/0.5')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 2.0)

    def test_power_invalid_params(self):
        response = self.app.get('/calc/power/2/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))

    def test_multiply_correct_params(self):
        response = self.app.get('/calc/multiply/2/3')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 6.0)

        response = self.app.get('/calc/multiply/4.5/2')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 9.0)

    def test_multiply_invalid_params(self):
        response = self.app.get('/calc/multiply/2/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))

    @patch('app.util.validate_permissions')
    def test_multiply_without_permissions_params(self, mock_validate_permissions):
        mock_validate_permissions.side_effect = lambda x, y: False

        response = self.app.get('/calc/multiply/2/1')
        self.assertEqual(response.status_code, 403)
        self.assertIn("User has no permissions", response.data.decode('utf-8'))

    def test_divide_correct_params(self):
        response = self.app.get('/calc/divide/6/3')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 2.0)

        response = self.app.get('/calc/divide/7.5/2.5')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 3.0)

    def test_divide_invalid_params(self):
        response = self.app.get('/calc/divide/6/0')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Division by zero is not possible", response.data.decode('utf-8'))

        response = self.app.get('/calc/divide/6/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))

        response = self.app.get('/calc/divide/6/0')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Division by zero is not possible", response.data.decode('utf-8'))

    @patch('app.util.convert_to_number')
    def test_divide_with_raw_params(self, mock_convert_to_number):
        mock_convert_to_number.side_effect = lambda x: x

        response = self.app.get('/calc/divide/6/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Parameters must be numbers", response.data.decode('utf-8'))

        response = self.app.get('/calc/divide/abc/6')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Parameters must be numbers", response.data.decode('utf-8'))

        response = self.app.get('/calc/divide/abc/cba')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Parameters must be numbers", response.data.decode('utf-8'))

    def test_log10_correct_params(self):
        response = self.app.get('/calc/log10/100')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 2.0)

        response = self.app.get('/calc/log10/1000')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 3.0)

    def test_log10_invalid_params(self):
        response = self.app.get('/calc/log10/-10')
        self.assertEqual(response.status_code, 400)
        self.assertIn("El logaritmo en base 10 solo está definido para números positivos", response.data.decode('utf-8'))

        response = self.app.get('/calc/log10/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))

    def test_sqrt_correct_params(self):
        response = self.app.get('/calc/sqrt/25')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 5.0)

        response = self.app.get('/calc/sqrt/0.25')
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(float(response.data.decode('utf-8')), 0.5)

    @patch('app.util.InvalidConvertToNumber')
    def test_sqrt_invalid_string_params(self, mock_invalid_convert_to_number):
        mock_invalid_convert_to_number.side_effect = lambda x: x

        response = self.app.get('/calc/sqrt/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Parameters must be numbers", response.data.decode('utf-8'))

    def test_sqrt_invalid_params(self):
        response = self.app.get('/calc/sqrt/-25')
        self.assertEqual(response.status_code, 400)
        self.assertIn("La raíz cuadrada no está definida para números negativos", response.data.decode('utf-8'))

        response = self.app.get('/calc/sqrt/abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Operator cannot be converted to number", response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
