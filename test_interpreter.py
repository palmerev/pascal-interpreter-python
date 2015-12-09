#! /usr/bin/env python3

import unittest
from interpreter_main import Token, Interpreter, INTEGER, PLUS, EOF


class InterpreterAdditionTestCase(unittest.TestCase):

    def test_single_digit_addition_no_whitespace(self):
        self.interpreter = Interpreter("1+1")
        result = self.interpreter.expr()
        self.assertEqual(result, 2)

    def test_integer_single_digit(self):
        self.interpreter = Interpreter("1")
        one = self.interpreter.integer()
        self.assertEqual(one, 1)

    def test_integer_double_digit(self):
        self.interpreter = Interpreter("12")
        twelve = self.interpreter.integer()
        self.assertEqual(twelve, 12)

    def test_integer_multidigit_plus_digit(self):
        self.interpreter = Interpreter("123+4")
        one = self.interpreter.integer()
        self.assertEqual(one, 123)


class InterpreterSubtractionTestCase(unittest.TestCase):

    def test_subtraction(self):
        self.interpreter = Interpreter("13 - 12")
        result = self.interpreter.expr()
        self.assertEqual(result, 1)


class InterpreterMultiplicationTestCase(unittest.TestCase):
    def test_multiplication(self):
        self.interpreter = Interpreter("2 * 3")
        result = self.interpreter.expr()
        self.assertEqual(result, 6)


class InterpreterFloorDivisionTestCase(unittest.TestCase):
    def test_floor_division_no_truncation(self):
        self.interpreter = Interpreter("4 / 2")
        result = self.interpreter.expr()
        self.assertEqual(result, 2)

    def test_floor_division_with_truncated_result(self):
        self.interpreter = Interpreter("3 / 2")
        result = self.interpreter.expr()
        self.assertEqual(result, 1)


class TokenTestCase(unittest.TestCase):
    def setUp(self):
        self.plus_token = Token(PLUS, '+')
        self.eof_token = Token(EOF, None)

    def tearDown(self):
        del self.plus_token
        del self.eof_token

    def test_can_add_two_integer_tokens(self):
        int_token1 = Token(INTEGER, 1)
        int_token2 = Token(INTEGER, 2)
        result = int_token1 + int_token2
        self.assertEqual(result.value, 12)
