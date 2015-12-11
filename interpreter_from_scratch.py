#! /usr/bin/env python3

# an interpreter to process
# arithmetic expressions with multiplication and division
# NEEDS:
#   token types 'INTEGER', 'DIV', 'MULT'
#   lexer: breaks input into tokens
#   parser: recognizes expressions based on a stream of tokens


class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return "Token({}, {})".format(self.kind, self.value)


class Interpreter:
    def __init__(self, text):
        self.text = text


def main():
    while True:
        text = input("mult/div >")
        if not text:
            continue

if __name__ == '__main__':
    main()
