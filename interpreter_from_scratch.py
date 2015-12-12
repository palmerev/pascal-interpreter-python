#! /usr/bin/env python3

# an interpreter to process
# arithmetic expressions with multiplication and division
# NEEDS:
#   token types 'INT', 'DIV', 'MULT'
#   lexer: breaks input into tokens
#   parser: recognizes expressions based on a stream of tokens

# token types
INT, DIV, MULT = 'INT', 'DIV', 'MULT'


class TokenEP:
    def __init__(self, kind, value):
        self.kind = kind  # token type
        self.value = value

    def __str__(self):
        return "Token({}, {})".format(self.kind, self.value)


class InterpreterEP:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.current_token = None

    def error(self):
        raise Exception("error parsing input")

    def advance(self):
        if self.current_char is not None and self.pos < len(self.text) - 1:
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def integer(self):
        """Return the next integer value found in the input stream"""
        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()
        assert len(result) > 0
        return int("".join(result))

    def eat(self, token_type):
        """If the expected token_type matches the current token, advance the
        pointer, else throw an error"""
        if self.current_token.kind == token_type:
            # self.advance()
            self.current_token = self.get_next_token()
        else:
            self.error()

    def get_next_token(self):
        """Return the next token from the input stream if there are more
        characters to process, otherwise return None"""
        if self.current_char is not None:
            if self.current_char.isdigit():
                return TokenEP(INT, self.integer())
            elif self.current_char == '/':
                token = TokenEP(DIV, self.current_char)
                self.advance()
                return token
            elif self.current_char == '*':
                token = TokenEP(MULT, self.current_char)
                self.advance()
                return token
            else:
                self.error()
        else:
            return None

    def expr(self):
        # we expect the first token to be an integer
        self.current_token = self.get_next_token()
        result = int(self.current_token.value)
        op = None
        while self.current_token is not None:
            if self.current_token.kind == MULT:
                op = MULT
                self.eat(MULT)
            elif self.current_token.kind == DIV:
                op = DIV
                self.eat(DIV)

            if op == DIV:
                result = int(result / self.current_token.value)
            elif op == MULT:
                result = result * int(self.current_token.value)
            self.eat(INT)

        return result


def main():
    while True:
        try:
            text = input("mult/div> ")
        except EOFError:
            print()
            break
        if not text:
            continue
        interpreter = InterpreterEP(text.strip())
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
