#! /usr/bin/env python3

import unittest
from interpreter_main import Token, Interpreter, Lexer, INTEGER, PLUS, EOF
from interpreter_from_scratch import InterpreterEP, TokenEP, LexerEP, INT


class InterpreterAdditionTestCase(unittest.TestCase):

    def test_single_digit_addition_no_whitespace(self):
        self.text = "1+1"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, eval(self.text))

    def test_integer_single_digit(self):
        self.text = "1"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        one = self.interpreter.expr()
        self.assertEqual(one, eval(self.text))

    def test_integer_double_digit(self):
        self.text = "12"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        twelve = self.interpreter.expr()
        self.assertEqual(twelve, eval(self.text))

    def test_integer_multidigit_plus_digit(self):
        self.text = "123+4"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        one_twenty_seven = self.interpreter.expr()
        self.assertEqual(one_twenty_seven, eval(self.text))


class InterpreterSubtractionTestCase(unittest.TestCase):
    def test_subtraction(self):
        self.text = "13 - 12"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, eval(self.text))


class InterpreterMultiplicationTestCase(unittest.TestCase):
    def test_multiplication(self):
        self.text = "2 * 3"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, eval(self.text))


class InterpreterFloorDivisionTestCase(unittest.TestCase):
    def test_floor_division_no_truncation(self):
        self.text = "4 / 2"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, int(eval(self.text)))

    def test_floor_division_with_truncated_result(self):
        self.text = " 3 / 2"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, int(eval(self.text)))


class InterpreterLongExpressionTestCase(unittest.TestCase):
    def test_three_term_expression(self):
        self.text = "1 + 5 / 2"
        self.lexer = Lexer(self.text)
        self.interpreter = Interpreter(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, int(eval(self.text)))


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


class InterpreterFromScratchTestCase(unittest.TestCase):
    def test_can_create_interpreter(self):
        self.txt = "2*3"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        self.assertEqual(self.interpreter.lexer.text, self.txt)

    @unittest.skip
    def test_expr_returns_same_input_if_integer(self):
        self.txt = "3"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        self.assertEqual(self.interpreter.expr(), int(self.txt))

    @unittest.skip
    def test_expr_multiplication(self):
        self.txt = "2 * 3"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        self.assertEqual(self.interpreter.expr(), eval(self.txt))

    def test_get_next_token_returns_token_of_current_char(self):
        self.txt = "12"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        token = self.interpreter.current_token
        self.assertIsInstance(token, TokenEP)
        self.assertEqual(token.kind, INT)
        self.assertEqual(token.value, int(self.txt))

    def test_get_next_token_tokenizes_expression(self):
        self.txt = "6/2"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        tkn1 = self.interpreter.current_token
        self.assertEqual(tkn1.value, 6)
        tkn2 = self.interpreter.lexer.get_next_token()
        self.assertEqual(tkn2.value, "/")
        tkn3 = self.interpreter.lexer.get_next_token()
        self.assertEqual(tkn3.value, 2)

    def test_expr_returns_single_int(self):
        self.txt = "12"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, int(self.txt))

    def test_expr_evaluates_simple_expression(self):
        self.txt = "6/2"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, eval(self.txt))

    def test_expr_evaluates_long_expression(self):
        self.txt = "160/2*30"
        self.lexer = LexerEP(self.txt)
        self.interpreter = InterpreterEP(self.lexer)
        result = self.interpreter.expr()
        self.assertEqual(result, eval(self.txt))
