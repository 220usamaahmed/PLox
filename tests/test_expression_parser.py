from plox.parser import Parser
from plox.scanner import Scanner
from tools.pretty_printer import ASTPrettyPrinter


def parse(source: str) -> str:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    ast = parser.parse()

    return ASTPrettyPrinter().print(ast)


def test_addition():
    source = "1 + 1"
    assert parse(source) == "(+ 1.0 1.0)"


def test_addition_and_subtraction():
    source = "1 + 1 - 1"
    assert parse(source) == "(- (+ 1.0 1.0) 1.0)"


def test_multiplication_and_division():
    source = "2 * 3 / 4"
    assert parse(source) == "(/ (* 2.0 3.0) 4.0)"


def test_basic_primaries():
    source = "123"
    assert parse(source) == "123.0"

    source = "true"
    assert parse(source) == "True"

    source = "false"
    assert parse(source) == "False"

    source = "nil"
    assert parse(source) == "None"


def test_expression_primary():
    source = "(123 - (456 / 789))"
    assert parse(source) == "(group (- 123.0 (group (/ 456.0 789.0))))"


def test_unary():
    source = "!false"
    assert parse(source) == "(! False)"


def test_factor():
    source = "-123 + 1"
    assert parse(source) == "(+ (- 123.0) 1.0)"


def test_equality():
    source = "2 == 2"
    assert parse(source) == "(== 2.0 2.0)"

    source = "2 != 2"
    assert parse(source) == "(!= 2.0 2.0)"


def test_comparison():
    source = "2 > 2"
    assert parse(source) == "(> 2.0 2.0)"

    source = "2 >= 2"
    assert parse(source) == "(>= 2.0 2.0)"

    source = "2 < 2"
    assert parse(source) == "(< 2.0 2.0)"

    source = "2 <= 2"
    assert parse(source) == "(<= 2.0 2.0)"


def test_complex_expression():
    source = "(1 + 2 / 2) * -1 >= 0 == false"
    assert parse(
        source) == "(== (>= (* (group (+ 1.0 (/ 2.0 2.0))) (- 1.0)) 0.0) False)"
