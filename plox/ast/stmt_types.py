from typing import TYPE_CHECKING, List
from plox.token import Token
from plox.ast.expr_interface import Expr

if TYPE_CHECKING:
    from plox.ast.stmt_visitor import StmtVisitor
from plox.ast.stmt_interface import Stmt


class Block(Stmt):

    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_block_stmt(self)


class Function(Stmt):

    def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_function_stmt(self)


class Class(Stmt):

    def __init__(self, name: Token, methods: List[Function]):
        self.name = name
        self.methods = methods

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_class_stmt(self)


class Expression(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_expression_stmt(self)


class If(Stmt):

    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt | None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_if_stmt(self)


class Print(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_print_stmt(self)


class Return(Stmt):

    def __init__(self, keyword: Token, expr: Expr | None):
        self.keyword = keyword
        self.expr = expr

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_return_stmt(self)


class VariableDeclaration(Stmt):

    def __init__(self, name: Token, initializer: Expr | None):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_variabledeclaration_stmt(self)


class While(Stmt):

    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: "StmtVisitor"):
        return visitor.visit_while_stmt(self)
