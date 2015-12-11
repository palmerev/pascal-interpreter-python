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
        self.kind = kind
        self.value = value

    def __str__(self):
        return "Token({}, {})".format(self.kind, self.value)


class InterpreterEP:
    def __init__(self, text):
        self.text = text

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
