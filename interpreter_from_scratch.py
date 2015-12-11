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
        if self.current_char is not None and self.pos > len(self.text) - 1:
            self.pos += 1
            self.current_char = self.text[self.pos]

    def eat(self, token_type):
        if self.current_token.kind == token_type:
            pass
        else:
            self.error()

    def get_next_token(self):
        pass

    def expr(self):
        try:
            result = int(self.text)
            return result
        except ValueError:
            pass





def main():
    while True:
        text = input("mult/div >")
        if not text:
            continue

if __name__ == '__main__':
    main()
