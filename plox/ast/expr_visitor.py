from plox.ast.expr_types import Assign, Binary, Call, Get, Grouping, Literal, Logical, Set, Super, This, Unary, Variable


class ExprVisitor: 

    def visit_assign_expr(self, expr: Assign):
        raise Exception('visit_assign_expr(name: Token, expr: Expr) not implemented')


    def visit_binary_expr(self, expr: Binary):
        raise Exception('visit_binary_expr(left: Expr, operator: Token, right: Expr) not implemented')


    def visit_call_expr(self, expr: Call):
        raise Exception('visit_call_expr(callee: Expr, paren: Token, params: List[Expr]) not implemented')


    def visit_get_expr(self, expr: Get):
        raise Exception('visit_get_expr(object: Expr, name: Token) not implemented')


    def visit_grouping_expr(self, expr: Grouping):
        raise Exception('visit_grouping_expr(expression: Expr) not implemented')


    def visit_literal_expr(self, expr: Literal):
        raise Exception('visit_literal_expr(expr: object) not implemented')


    def visit_logical_expr(self, expr: Logical):
        raise Exception('visit_logical_expr(left: Expr, operator: Token, right: Expr) not implemented')


    def visit_set_expr(self, expr: Set):
        raise Exception('visit_set_expr(object: Expr, name: Token, expr: Expr) not implemented')


    def visit_super_expr(self, expr: Super):
        raise Exception('visit_super_expr(keyword: Token, method: Token) not implemented')


    def visit_this_expr(self, expr: This):
        raise Exception('visit_this_expr(keyword: Token) not implemented')


    def visit_unary_expr(self, expr: Unary):
        raise Exception('visit_unary_expr(operator: Token, right: Expr) not implemented')


    def visit_variable_expr(self, expr: Variable):
        raise Exception('visit_variable_expr(name: Token) not implemented')