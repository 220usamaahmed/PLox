from enum import Enum
from typing import Any, Dict, List
from plox.ast.expr_interface import Expr
from plox.ast.expr_types import (
    Assign,
    Binary,
    Call,
    Get,
    Grouping,
    Literal,
    Logical,
    Set,
    This,
    Unary,
    Variable,
)
from plox.ast.expr_visitor import ExprVisitor
from plox.ast.stmt_interface import Stmt
from plox.ast.stmt_types import (
    Block,
    Class,
    Expression,
    Function,
    If,
    Print,
    Return,
    VariableDeclaration,
    While,
)
from plox.ast.stmt_visitor import StmtVisitor
from plox.interpreter import Interpreter
from plox.token import Token


class FunctionType(Enum):

    NONE = "None"
    FUNCTION = "Function"
    INITIALIZER = "Initializer"
    METHOD = "Method"


class ClassType(Enum):

    NONE = "None"
    CLASS = "Class"


class Resolver(ExprVisitor, StmtVisitor):

    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: List[Dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def visit_block_stmt(self, stmt: Block) -> Any:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def resolve(self, statements: List[Stmt]):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolve_expr(self, expr: Expr):
        expr.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if len(self.scopes) == 0:
            return

        if name.lexeme in self.scopes[-1]:
            raise Exception("Already a variable with this name in this scope")

        self.scopes[-1][name.lexeme] = False

    def define(self, name: Token):
        if len(self.scopes) == 0:
            return

        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        for i in reversed(range(len(self.scopes))):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, function: Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def visit_variabledeclaration_stmt(self, stmt: VariableDeclaration) -> Any:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def visit_variable_expr(self, expr: Variable) -> Any:
        if (
            not (len(self.scopes) == 0)
            and self.scopes[-1].get(expr.name.lexeme) == False
        ):
            raise Exception("Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)

    def visit_assign_expr(self, expr: Assign) -> Any:
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_function_stmt(self, stmt: Function) -> Any:
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_expression_stmt(self, stmt: Expression) -> Any:
        self.resolve_expr(stmt.expression)

    def visit_if_stmt(self, stmt: If) -> Any:
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolve_stmt(stmt.elseBranch)

    def visit_print_stmt(self, stmt: Print) -> Any:
        self.resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt: Return) -> Any:
        if self.current_function == FunctionType.NONE:
            raise Exception("Can't return from top-level code")

        if self.current_function == FunctionType.INITIALIZER:
            raise Exception("Can't return a value from an initializer")

        if stmt.expr is not None:
            self.resolve_expr(stmt.expr)

    def visit_while_stmt(self, stmt: While) -> Any:
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_binary_expr(self, expr: Binary) -> Any:
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call_expr(self, expr: Call) -> Any:
        self.resolve_expr(expr.callee)

        for argument in expr.params:
            self.resolve_expr(argument)

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        self.resolve_expr(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> Any:
        return

    def visit_logical_expr(self, expr: Logical) -> Any:
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_unary_expr(self, expr: Unary) -> Any:
        self.resolve_expr(expr.right)

    def visit_class_stmt(self, stmt: Class) -> Any:
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass is not None and stmt.name.lexeme == stmt.superclass.name.lexeme:
            raise Exception("A class can't inherit from itself.")

        if stmt.superclass is not None:
            self.resolve_expr(stmt.superclass) 

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.INITIALIZER if method.name == "init" else FunctionType.METHOD
            self.resolve_function(method, declaration)

        self.end_scope()
        self.current_class = enclosing_class

    def visit_get_expr(self, expr: Get) -> Any:
        self.resolve_expr(expr.object)

    def visit_set_expr(self, expr: Set) -> Any:
        self.resolve_expr(expr.value)
        self.resolve_expr(expr.object)

    def visit_this_expr(self, expr: This) -> Any:
        if self.current_class == ClassType.NONE:
            # TODO: Handle errors...
            raise Exception("Can't use 'this' outside of a class")

        self.resolve_local(expr, expr.keyword)
