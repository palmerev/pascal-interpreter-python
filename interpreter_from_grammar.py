#! /usr/bin/env python3

###############################################################################
# GRAMMAR
#    expr   : factor ((MUL|DIV|PLUS|MINUS) factor)*
#    factor : INTEGER

# Each rule becomes a method name, references to that rule become method calls.
# Alternatives (a1 | a2| aN) become an if-elif-else statement
# Optional grouping (...)* become a while loop (zero or more iterations)
# Each token reference T becomes a call to the method 'eat', eat(T)
###############################################################################
from interpreter_main import Token, INTEGER, PLUS, MINUS, MULT, DIV, EOF


class GrammarLexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid Syntax while lexing')

    def advance(self):
        """increment the self.pos and update self.current_char (set to None
        if self.pos is past the end of the input)"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result_string = ''
        while self.current_char is not None and self.current_char.isdigit():
            result_string += self.current_char
            self.advance()
        if len(result_string) > 0:
            return int(result_string)
        else:
            raise Exception('Couldn\'t get integer value from input')

    def get_next_token(self):
        self.skip_whitespace()
        token = None
        if self.current_char is None:
            return Token(EOF, None)
        if self.current_char.isdigit():
            token = Token(INTEGER, self.integer())
            return token
        elif self.current_char == '+':
            token = Token(PLUS, '+')
            self.advance()
            return token
        elif self.current_char == '-':
            token = Token(MINUS, '-')
            self.advance()
            return token
        elif self.current_char == '*':
            token = Token(MULT, '*')
            self.advance()
            return token
        elif self.current_char == '/':
            token = Token(DIV, '/')
            self.advance()
            return token
        else:
            self.error()

    def __str__(self):
        return '<GrammarLexer text:{}, pos:{}, current_char:{}>'.format(
            self.text, self.pos, self.current_char)

    def __repr__(self):
        return self.__str__()


class GrammarInterpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax while parsing')

    def eat(self, expected_type):
        if self.current_token.type_ == expected_type:
            # print("ate an {} {}".format(
            #     expected_type, self.current_token.value))
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """Consume an integer token and returns its value"""
        token = self.current_token
        self.eat(INTEGER)
        return int(token.value)

    def expr(self):
        result = self.factor()
        while self.current_token.type_ in (PLUS, MINUS, MULT, DIV):
            token = self.current_token
            if token.type_ == PLUS:
                self.eat(PLUS)
                result = result + self.factor()
            elif token.type_ == MINUS:
                self.eat(MINUS)
                result = result - self.factor()
            elif token.type_ == MULT:
                self.eat(MULT)
                result = result * self.factor()
            elif token.type_ == DIV:
                self.eat(DIV)
                result = int(result / self.factor())  # floor division

        if self.current_token.type_ == EOF:
            return result
        elif self.current_token.type_ not in (
                PLUS, MINUS, MULT, DIV, INTEGER, EOF):
            raise Exception('Invalid syntax: unknown token type "%s"' %
                self.current_token.type_)


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = GrammarLexer(text.strip())
        interpreter = GrammarInterpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
