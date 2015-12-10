#! /usr/bin/env python3

# Token types
#
# EOF (end of file) indicates there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EOF'


class Token:
    def __init__(self, type_, value):
        # token type: INTEGER, PLUS, MINUS, MULT, DIV or EOF
        self.type_ = type_
        # token value: 0 through 9, +, -, *, /, or None
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type_, repr(self.value))

    def __repr__(self):
        return self.__str__()

    # adding two INTEGER tokens concatenates their digits
    def __add__(self, other):
        if self.type_ == other.type_ == INTEGER:
            return Token(self.type_, int(str(self.value) + str(other.value)))
        else:
            raise Exception('error adding tokens: incorrect token type')

    def __radd__(self, other):
        if self.type_ == other.type_ == INTEGER:
            return Token(self.type_, int(str(self.value) + str(other.value)))
        else:
            raise Exception('error adding tokens: incorrect token type')


class Interpreter:
    def __init__(self, text):
        # client string input e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]
    ########################################################
    # Lexer - breaks the input into tokens
    ########################################################

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """Increment self.pos and set self.current_char."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a multidigit integer read from input"""
        token_string = ''
        while self.current_char is not None and self.current_char.isdigit():
            token_string += self.current_char
            self.advance()
        return int(token_string)

    def get_next_token(self):
        """
        Lexical analyzer (also known as a scanner or tokenizer)

        Responsible for breaking input apart into tokens, one token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            elif self.current_char == '*':
                self.advance()
                return Token(MULT, '*')

            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            else:
                self.error()

    #####################################################
    # Parser / Interpreter code
    #####################################################
    def eat(self, token_type):
        # compare the current token type with the passed token type
        # and if they match then "eat" the current token and assign
        # the next token to self.current_token,
        # otherwise raise an Exception
        if self.current_token.type_ == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return an INTEGER token value"""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """
        Arithmetic expression parser / interpreter
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        expr -> INTEGER MULT INTEGER
        expr -> INTEGER DIV INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token is not None and self.current_token.type_ in (PLUS, MINUS, MULT, DIV):

            token = self.current_token
            if token.type_ == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type_ == MULT:
                self.eat(MULT)
                result = result * self.term()
            elif token.type_ == DIV:
                self.eat(DIV)
                result = int(result / self.term())
            elif token.type_ == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text.strip())
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
