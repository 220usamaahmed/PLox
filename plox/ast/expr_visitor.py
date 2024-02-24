from plox.ast.expr_types import Assign, Binary, Call, Get, Grouping, Literal, Logical, Set, Super, This, Unary, Variable
from typing import Any


class ExprVisitor: 

    def visit_assign_expr(self, expr: Assign) -> Any:
        raise Exception('visit_assign_expr(name: Token, value: Expr) not implemented')


    def visit_binary_expr(self, expr: Binary) -> Any:
        raise Exception('visit_binary_expr(left: Expr, operator: Token, right: Expr) not implemented')


    def visit_call_expr(self, expr: Call) -> Any:
        raise Exception('visit_call_expr(callee: Expr, paren: Token, params: List[Expr]) not implemented')


    def visit_get_expr(self, expr: Get) -> Any:
        raise Exception('visit_get_expr(object: Expr, name: Token) not implemented')


    def visit_grouping_expr(self, expr: Grouping) -> Any:
        raise Exception('visit_grouping_expr(expression: Expr) not implemented')


    def visit_literal_expr(self, expr: Literal) -> Any:
        raise Exception('visit_literal_expr(value: object) not implemented')


    def visit_logical_expr(self, expr: Logical) -> Any:
        raise Exception('visit_logical_expr(left: Expr, operator: Token, right: Expr) not implemented')


    def visit_set_expr(self, expr: Set) -> Any:
        raise Exception('visit_set_expr(object: Expr, name: Token, value: Expr) not implemented')


    def visit_super_expr(self, expr: Super) -> Any:
        raise Exception('visit_super_expr(keyword: Token, method: Token) not implemented')


    def visit_this_expr(self, expr: This) -> Any:
        raise Exception('visit_this_expr(keyword: Token) not implemented')


    def visit_unary_expr(self, expr: Unary) -> Any:
        raise Exception('visit_unary_expr(operator: Token, right: Expr) not implemented')


    def visit_variable_expr(self, expr: Variable) -> Any:
        raise Exception('visit_variable_expr(name: Token) not implemented')