from typing import Any
from plox.ast.expr_interface import Expr
from plox.ast.expr_types import Binary, Grouping, Literal, Unary
from plox.ast.expr_visitor import ExprVisitor
from plox.exceptions import InterpreterError, InterpreterErrorType
from plox.token import TokenType


class Interpreter(ExprVisitor):

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.MINUS:
                return -float(right)

            case TokenType.BANG:
                return not self.is_truthy(right)

            case _:
                raise InterpreterError(
                    InterpreterErrorType.INVALID_UNARY_OPERATOR)

    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.GREATER:
                return float(left) > float(right)

            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)

            case TokenType.LESS:
                return float(left) < float(right)

            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)

            case TokenType.MINUS:
                return float(left) - float(right)

            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)

            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)

                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

            case TokenType.SLASH:
                return float(left) / float(right)

            case TokenType.STAR:
                return float(left) * float(right)

            case _:
                raise InterpreterError(
                    InterpreterErrorType.INVALID_BINARY_OPERATOR)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def is_truthy(self, object: Any) -> bool:
        if (object == None):
            return False
        if (isinstance(object, bool)):
            return object
        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        if a == None and b == None:
            return True
        if a == None:
            return False

        return a == b
