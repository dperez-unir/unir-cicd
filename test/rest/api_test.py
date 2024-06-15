import unittest
from unittest.mock import patch
import http.client
import os
import unittest
from flask import Flask
from app import util
from app.calc import Calculator
from app.api import api_application
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urljoin

import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
DEFAULT_TIMEOUT = 2  # in secs


def call_end_point(path):
    url = urljoin(BASE_URL, path)
    response = urlopen(url, timeout=DEFAULT_TIMEOUT)
    response_data = response.read().decode('utf-8')
    return response, response_data


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")


    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )

    def test_add_correct_params(self):
        response, response_data = call_end_point("/calc/add/4/5")
        self.assertEqual(response.status, 200)
        self.assertEqual(response_data, '9')

        response, response_data = call_end_point("/calc/add/4.5/5.5")
        self.assertEqual(response.status, 200)
        self.assertEqual(response_data, '10.0')

    def test_add_invalid_params(self):
        try:
            response, response_data = call_end_point("/calc/add/4/abc")
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)

    def test_substract_correct_params(self):
        response, response_data = call_end_point("/calc/substract/10/5")
        self.assertEqual(response.status, 200)
        self.assertEqual(response_data, '5')

    def test_substract_invalid_params(self):
        try:
            response, response_data = call_end_point("/calc/substract/10/abc")
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)

    def test_power_correct_params(self):
        response, response_data = call_end_point("/calc/power/2/3")
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 8.0)

        response, response_data = call_end_point("/calc/power/4/0.5")
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 2.0)

    def test_power_invalid_params(self):
        try:
            response, response_data = call_end_point("/calc/power/2/abc")
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)

    def test_multiply_correct_params(self):
        response, response_data = call_end_point("/calc/multiply/2/3")
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 6.0)

        response, response_data = call_end_point("/calc/multiply/4.5/2")
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 9.0)

    def test_multiply_invalid_params(self):
        try:
            response, response_data= call_end_point('/calc/multiply/2/abc')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)

    def test_divide_correct_params(self):
        response, response_data = call_end_point('/calc/divide/6/3')
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 2.0)

        response, response_data = call_end_point('/calc/divide/7.5/2.5')
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 3.0)

    def test_divide_invalid_params(self):
        try:
            response, response_data = call_end_point('/calc/divide/6/0')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Division by zero is not possible", response_data)

        try:
            response, response_data = call_end_point('/calc/divide/6/abc')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)

        try:
            response, response_data = call_end_point('/calc/divide/6/0')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Division by zero is not possible", response_data)

    def test_log10_correct_params(self):
        response, response_data = call_end_point('/calc/log10/100')
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 2.0)

        response, response_data = call_end_point('/calc/log10/1000')
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 3.0)

    def test_log10_invalid_params(self):
        try:
            response, response_data = call_end_point('/calc/log10/-10')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("El logaritmo en base 10 solo está definido para números positivos", response_data)

        try:
            response, response_data = call_end_point('/calc/log10/abc')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)

    def test_sqrt_correct_params(self):
        response, response_data = call_end_point('/calc/sqrt/25')
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 5.0)

        response, response_data = call_end_point('/calc/sqrt/0.25')
        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(float(response_data), 0.5)

    def test_sqrt_invalid_params(self):
        try:
            response, response_data = call_end_point('/calc/sqrt/-25')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("La raíz cuadrada no está definida para números negativos", response_data)

        try:
            response, response_data = call_end_point('/calc/sqrt/abc')
        except HTTPError as e:
            response_data = e.read().decode('utf-8')
            self.assertEqual(e.code, 400)
            self.assertIn("Operator cannot be converted to number", response_data)


if __name__ == '__main__':
    unittest.main()
