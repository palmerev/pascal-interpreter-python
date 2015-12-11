#! /usr/bin/env python3

# an interpreter to process
# arithmetic expressions with multiplication and division
# NEEDS:
#   token types 'INTEGER', 'DIV', 'MULT'
#   lexer: breaks input into tokens
#   parser: recognizes expressions based on a stream of tokens


class Interpreter:
    pass


class Token:
    pass


def main():
    while True:
        text = input("mult/div >")
        if not text:
            continue

if __name__ == '__main__':
    main()
