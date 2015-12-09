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

    def parse_int(self):
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
                return Token(INTEGER, self.parse_int())

            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            elif self.current_char == '*':
                self.advance()
                return Token(MULT, '*')

            else:
                self.error()

    def peek(self):
        """examines the next character and returns its token type,
        or None if it's not a valid lexeme"""
        # if there are characters to read beyond self.pos,
        # examine the next character
        if self.pos < len(self.text) - 1:
            next_char = self.text[self.pos + 1]
            # return the token type of the next character
            if next_char.isdigit():
                return INTEGER
            elif next_char == '+':
                return PLUS
            # if character isn't a valid token
            else:
                return None
        else:
            return EOF

    def eat(self, token_type):
        # compare the current token type with the passed token type
        # and if they match then "eat" the current token and assign
        # the next token to self.current_token,
        # otherwise raise an Exception
        if self.current_token.type_ == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        expr -> INTEGER MULT INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)
        # we expect the current token to be a '+' or  '-'
        op = self.current_token
        if op.type_ == PLUS:
            self.eat(PLUS)
        elif op.type_ == MULT:
            self.eat(MULT)
        else:
            self.eat(MINUS)

        # we expect the current token to be an integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call self.current_token is set to EOF token

        # at this point INTEGER PLUS INTEGER or INTEGER MINUS INTEGER sequence
        # of tokens has been successfully found and the method can just return
        # the result of adding or substracting two integers
        if op.type_ == PLUS:
            result = left.value + right.value
        elif op.type_ == MINUS:
            result = left.value - right.value
        elif op.type_ == MULT:
            result = left.value * right.value
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
