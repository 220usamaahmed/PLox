from typing import Any
from plox.ast.expr_visitor import ExprVisitor
from plox.ast.stmt_types import Block
from plox.ast.stmt_visitor import StmtVisitor
from plox.interpreter import Interpreter


class Resolver(ExprVisitor, StmtVisitor):

    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter()

    def visit_block_stmt(self, stmt: Block) -> Any:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
