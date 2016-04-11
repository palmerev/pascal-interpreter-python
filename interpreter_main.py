#! /usr/bin/env python3

# Token types
#
# EOF (end of file) indicates there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULT, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', '(', ')', 'EOF'
)


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


class AST:
    """Base class representing a node in an Abstract Syntax Tree"""
    pass


class BinaryOperator(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Lexer:
    def __init__(self, text):
        # client string input e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
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

            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            else:
                self.error()

        return Token(EOF, None)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token type
        # and if they match then "eat" the current token and assign
        # the next token to self.current_token,
        # otherwise raise an Exception
        if self.current_token.type_ == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token
        if token.type_ == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type_ == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type_ in (MULT, DIV):
            token = self.current_token
            if token.type_ == MULT:
                self.eat(MULT)
            elif token.type_ == DIV:
                self.eat(DIV)

            node = BinaryOperator(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        Arithmetic expression parser / interpreter

        expr   : term ((PLUS|MINUS) term)*
        term   : factor ((MULT|DIV) factor)*
        factor : INTEGER
        """
        node = self.term()
        while self.current_token is not None and (
                self.current_token.type_ in (PLUS, MINUS)):

            token = self.current_token
            if token.type_ == PLUS:
                self.eat(PLUS)
            elif token.type_ == MINUS:
                self.eat(MINUS)

        node = BinaryOperator(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text.strip())
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
