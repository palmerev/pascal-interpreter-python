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


class LexerEP:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

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


class InterpreterEP:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        """If the expected token_type matches the current token, advance the
        pointer, else throw an error"""
        if self.current_token.kind == token_type:
            # self.advance()
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INT)
        return int(token.value)

    def expr(self):
        # we expect the first token to be an integer
        result = self.term()
        op = None
        while self.current_token is not None:
            if self.current_token.kind == MULT:
                op = MULT
                self.eat(MULT)
            elif self.current_token.kind == DIV:
                op = DIV
                self.eat(DIV)

            if op == DIV:
                result = int(result / self.term())
            elif op == MULT:
                result = result * int(self.term())

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
        lexer = LexerEP(text.strip())
        interpreter = InterpreterEP(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
