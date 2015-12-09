#! /usr/bin/env python3

# Token types
#
# EOF (end of file) indicates there is no more input left for lexical analysis
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


class Token:
    def __init__(self, type_, value):
        # token type: INTEGER, PLUS, or EOF
        self.type_ = type_
        # token value: 0 through 9, +, or None
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

    def parse_int(self):
        token_chars = []
        current_char = self.text[self.pos]
        while current_char.isdigit():
            token_chars.append(current_char)
            # if the next character is an INTEGER reassign the current_char
            if self.peek() == INTEGER:
                self.pos += 1
                current_char = self.text[self.pos]
            # otherwise, stop parsing
            else:
                break
        token = Token(INTEGER, int("".join(token_chars)))
        return token

    def get_next_token(self):
        """
        Lexical analyzer (also known as a scanner or tokenizer)

        Responsible for breaking input apart into tokens, one token at a time.
        """
        text = self.text

        # return EOF if self.pos is past the end of self.text
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]
        while current_char.isspace():
            self.pos += 1
            current_char = text[self.pos]

        # while each character is a digit, convert it to an INTEGER
        # create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = self.parse_int()
            self.pos += 1
            return token

        elif current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

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
        """expr -> INTEGER PLUS INTEGER"""
        # import pdb
        # pdb.set_trace()

        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)
        # we expect the current token to be a '+' token
        # op = self.current_token
        self.eat(PLUS)
        # we expect the the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call self.current_token is set to EOF token
        # at this point INTEGER PLUS INTEGER sequence of tokens has been
        # successfully found and the method can just return the result of
        # adding two integers
        result = left.value + right.value
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
