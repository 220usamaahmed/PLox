from plox.ast.expr_interface import Expr
from plox.ast.expr_types import Assign, Binary, Call, Get, Grouping, Literal, Logical, Set, Super, This, Unary, Variable
from plox.ast.expr_visitor import ExprVisitor


class ASTPrettyPrinter(ExprVisitor):

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        output = ""
        for expr in exprs:
            output += " " + str(expr.accept(self))

        return f"({name}{output})"

    def visit_literal_expr(self, expr: Literal):
        return str(expr.value)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_assign_expr(self, expr: Assign):
        raise Exception(
            'ASTPrettyPrinter.visit_assign_expr(name: Token, expr: Expr) not implemented')

    def visit_call_expr(self, expr: Call):
        raise Exception(
            'ASTPrettyPrinter.visit_call_expr(callee: Expr, paren: Token, params: List[Expr]) not implemented')

    def visit_get_expr(self, expr: Get):
        raise Exception(
            'ASTPrettyPrinter.visit_get_expr(object: Expr, name: Token) not implemented')

    def visit_logical_expr(self, expr: Logical):
        raise Exception(
            'ASTPrettyPrinter.visit_logical_expr(left: Expr, operator: Token, right: Expr) not implemented')

    def visit_set_expr(self, expr: Set):
        raise Exception(
            'ASTPrettyPrinter.visit_set_expr(object: Expr, name: Token, expr: Expr) not implemented')

    def visit_super_expr(self, expr: Super):
        raise Exception(
            'ASTPrettyPrinter.visit_super_expr(keyword: Token, method: Token) not implemented')

    def visit_this_expr(self, expr: This):
        raise Exception(
            'ASTPrettyPrinter.visit_this_expr(keyword: Token) not implemented')

    def visit_variable_expr(self, expr: Variable):
        raise Exception(
            'ASTPrettyPrinter.visit_variable_expr(name: Token) not implemented')
