import sys
from plox.exceptions import ParserError, ScannerError
from plox.interpreter import Interpreter
from plox.parser import Parser

from plox.scanner import Scanner
from plox.utils import display_error


def run_repl():
    while True:
        contents = input("> ").strip()
        if contents == 'quit':
            break
        run(contents)


def run_file(file_path: str):
    print(f"Running script: {file_path}")
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            run(contents)
    except FileNotFoundError:
        print("The file does not exist.")
    except PermissionError:
        print("You don't have permission to read the file.")
    except IOError as e:
        print("An I/O error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def run(source: str):
    scanner = Scanner(source)

    try:
        tokens = scanner.scan_tokens()
        # for token in scanner.tokens:
        #     print(f"token: {token.line}\t{token.token_type} - {token.lexeme}")

        parser = Parser(tokens)
        expression = parser.parse()
        # print(ASTPrettyPrinter().print(expression))

        interpretor = Interpreter()
        result = interpretor.interpret(expression)

        if (scanner.had_error):
            exit(65)
        if interpretor.had_runtime_error:
            exit(70)

        print(result)

    except ScannerError as e:
        display_error(e.line, e.location, e.type.value)

    except ParserError as e:
        display_error(e.line, e.location, e.type.value)


def main():
    if len(sys.argv) == 1:
        run_repl()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print("Usage: plox [path to script]")


if __name__ == "__main__":
    main()
