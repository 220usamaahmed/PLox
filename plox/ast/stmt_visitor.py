from plox.ast.stmt_types import Block, Function, Class, Expression, If, Print, Return, VariableDeclaration, While
from typing import Any


class StmtVisitor: 

    def visit_block_stmt(self, stmt: Block) -> Any:
        raise Exception('visit_block_stmt(statements: List[Stmt]) not implemented')


    def visit_function_stmt(self, stmt: Function) -> Any:
        raise Exception('visit_function_stmt(name: Token, params: List[Token], body: List[Stmt]) not implemented')


    def visit_class_stmt(self, stmt: Class) -> Any:
        raise Exception('visit_class_stmt(name: Token, superclass: Variable, method: List[Function]) not implemented')


    def visit_expression_stmt(self, stmt: Expression) -> Any:
        raise Exception('visit_expression_stmt(expression: Expr) not implemented')


    def visit_if_stmt(self, stmt: If) -> Any:
        raise Exception('visit_if_stmt(condition: Expr, thenBranch: Stmt, elseBranch: Stmt) not implemented')


    def visit_print_stmt(self, stmt: Print) -> Any:
        raise Exception('visit_print_stmt(expression: Expr) not implemented')


    def visit_return_stmt(self, stmt: Return) -> Any:
        raise Exception('visit_return_stmt(keyword: Token, expr: Expr) not implemented')


    def visit_variabledeclaration_stmt(self, stmt: VariableDeclaration) -> Any:
        raise Exception('visit_variabledeclaration_stmt(name: Token, initializer: Expr) not implemented')


    def visit_while_stmt(self, stmt: While) -> Any:
        raise Exception('visit_while_stmt(condition: Expr, body: Stmt) not implemented')