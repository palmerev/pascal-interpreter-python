#! /usr/bin/env python3

import unittest
from interpreter_main import Token, Interpreter, INTEGER, PLUS, EOF


class InterpreterAdditionTestCase(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter(" ")

    def tearDown(self):
        del self.interpreter

    def test_single_digit_addition_no_whitespace(self):
        self.interpreter.text = "1+1"
        result = self.interpreter.expr()
        self.assertEqual(result, 2)

    def test_parse_int_single_digit(self):
        self.interpreter.text = "1"
        one = self.interpreter.parse_int()
        self.assertEqual(one.value, Token(INTEGER, 1).value)

    def test_parse_int_double_digit(self):
        self.interpreter.text = "12"
        twelve = self.interpreter.parse_int()
        self.assertEqual(twelve.value, Token(INTEGER, 12).value)

    def test_parse_int_multidigit_plus_digit(self):
        self.interpreter.text = "123+4"
        one = self.interpreter.parse_int()
        self.assertEqual(one.value, Token(INTEGER, 123).value)
        self.assertEqual(self.interpreter.pos, 2)  # pos on last char of integer


class InterpreterSubtractionTestCase(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter(" ")

    def tearDown(self):
        del self.interpreter

    def test_subtraction(self):
        self.interpreter.text = "13 - 12"
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
