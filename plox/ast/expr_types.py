from typing import List
from plox.token import Token
from plox.ast.expr_visitor import ExprVisitor
from plox.ast.expr_interface import Expr


class Assign(Expr):

    def __init__(self, name: Token, expr: Expr):      
        self.name = name
        self.expr = expr

    def accept(self, visitor: ExprVisitor):
        visitor.visit_assign_expr(self)


class Binary(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr):      
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        visitor.visit_binary_expr(self)


class Call(Expr):

    def __init__(self, callee: Expr, paren: Token, params: List[Expr]):      
        self.callee = callee
        self.paren = paren
        self.params = params

    def accept(self, visitor: ExprVisitor):
        visitor.visit_call_expr(self)


class Get(Expr):

    def __init__(self, object: Expr, name: Token):      
        self.object = object
        self.name = name

    def accept(self, visitor: ExprVisitor):
        visitor.visit_get_expr(self)


class Grouping(Expr):

    def __init__(self, expression: Expr):      
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        visitor.visit_grouping_expr(self)


class Literal(Expr):

    def __init__(self, expr: object):      
        self.expr = expr

    def accept(self, visitor: ExprVisitor):
        visitor.visit_literal_expr(self)


class Logical(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr):      
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        visitor.visit_logical_expr(self)


class Set(Expr):

    def __init__(self, object: Expr, name: Token, expr: Expr):      
        self.object = object
        self.name = name
        self.expr = expr

    def accept(self, visitor: ExprVisitor):
        visitor.visit_set_expr(self)


class Super(Expr):

    def __init__(self, keyword: Token, method: Token):      
        self.keyword = keyword
        self.method = method

    def accept(self, visitor: ExprVisitor):
        visitor.visit_super_expr(self)


class This(Expr):

    def __init__(self, keyword: Token):      
        self.keyword = keyword

    def accept(self, visitor: ExprVisitor):
        visitor.visit_this_expr(self)


class Unary(Expr):

    def __init__(self, operator: Token, right: Expr):      
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        visitor.visit_unary_expr(self)


class Variable(Expr):

    def __init__(self, name: Token):      
        self.name = name

    def accept(self, visitor: ExprVisitor):
        visitor.visit_variable_expr(self)

