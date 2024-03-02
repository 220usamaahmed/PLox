from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.scanner import Scanner


def interpret(source: str) -> str:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    return interpreter.interpret(ast)


def test_addition():
    source = "1 + 1"
    assert interpret(source) == "2"


def test_complex_expression():
    source = "1 + 2 - 3 * 4 / 5"
    assert interpret(source) == str(1 + 2 - 3 * 4 / 5)


def test_grouping():
    source = "((1 + 3) / 2) + 1 - (100.5 / 0.5)"
    assert interpret(source) == str(-198)


def test_comparison():
    source = "1 < 2"
    assert interpret(source) == "True"

    source = "1 > 2"
    assert interpret(source) == "False"

    source = "1 <= 1"
    assert interpret(source) == "True"

    source = "1 >= 2"
    assert interpret(source) == "False"


def test_inequality():
    source = "1 == 1"
    assert interpret(source) == "True"

    source = "4 == 5"
    assert interpret(source) == "False"


def test_complex_expression_and_equality():
    source = "((1 + 3) / 2) + 1 - (100.5 / 0.5) == -198"
    assert interpret(source) == "True"
