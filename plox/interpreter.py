from typing import Any, List
from plox.ast.expr_interface import Expr
from plox.ast.expr_types import Assign, Binary, Grouping, Literal, Logical, Unary, Variable
from plox.ast.expr_visitor import ExprVisitor
from plox.ast.stmt_interface import Stmt
from plox.ast.stmt_types import Block, Expression, If, Print, VariableDeclaration, While
from plox.ast.stmt_visitor import StmtVisitor
from plox.environment import Environment
from plox.exceptions import InterpreterError, InterpreterErrorType, PLoxRuntimeError
from plox.token import Token, TokenType


class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self):
        self.had_runtime_error = False
        self.environment = Environment()

    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except PLoxRuntimeError as e:
            return self.handle_runtime_error(e)

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def visit_block_stmt(self, stmt: Block) -> Any:
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_if_stmt(self, stmt: If) -> Any:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)

    def visit_print_stmt(self, stmt: Print):
        value = self.stringify(self.evaluate(stmt.expression))
        print(value)

    def visit_variabledeclaration_stmt(self, stmt: VariableDeclaration) -> Any:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_while_stmt(self, stmt: While) -> Any:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value
    
    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.evaluate(expr.left)

        if expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left): return left
        else:
            if not self.is_truthy(left): return left

        return self.evaluate(expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
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
                self.check_number_operand(expr.operator, left, right)
                return float(left) > float(right)

            case TokenType.GREATER_EQUAL:
                self.check_number_operand(expr.operator, left, right)
                return float(left) >= float(right)

            case TokenType.LESS:
                self.check_number_operand(expr.operator, left, right)
                return float(left) < float(right)

            case TokenType.LESS_EQUAL:
                self.check_number_operand(expr.operator, left, right)
                return float(left) <= float(right)

            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)

            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

            case TokenType.MINUS:
                self.check_number_operand(expr.operator, left, right)
                return float(left) - float(right)

            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)

                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

                raise RuntimeError(
                    expr.operator, "Operands must be two numbers or two strings")

            case TokenType.SLASH:
                self.check_number_operand(expr.operator, left, right)
                return float(left) / float(right)

            case TokenType.STAR:
                self.check_number_operand(expr.operator, left, right)
                return float(left) * float(right)

            case _:
                raise InterpreterError(
                    InterpreterErrorType.INVALID_BINARY_OPERATOR)
            
    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.environment.get(expr.name)

    def evaluate(self, expr: Expr):
        return expr.accept(self)
    
    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous_env = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)

        finally:
            self.environment = previous_env

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

    def check_number_operand(self, operator: Token, *operands: object):
        for operand in operands:
            if not isinstance(operand, float):
                raise PLoxRuntimeError(operator, "Operand must be a number")

    def stringify(self, object: Any) -> str:
        if object == None:
            return "nil"

        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(object)

    def handle_runtime_error(self, error: PLoxRuntimeError) -> str:
        self.had_runtime_error = True
        return f"[line {error.token.line}] {error.message}"
