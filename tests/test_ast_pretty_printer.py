from plox.ast.expr_types import Binary, Grouping, Literal, Unary
from plox.token import Token, TokenType
from tools.pretty_printer import ASTPrettyPrinter


def test_expression():
    l = Unary(Token(TokenType.MINUS, "-", 1), Literal(123))
    o = Token(TokenType.STAR, "*", 1)
    r = Grouping(Literal(45.67))

    b = Binary(l, o, r)

    assert ASTPrettyPrinter().print(b) == "(* (- 123) (group 45.67))"
