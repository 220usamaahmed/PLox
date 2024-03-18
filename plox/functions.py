from typing import TYPE_CHECKING, List, Any
import time

from plox.ast.stmt_types import Function
from plox.environment import Environment

if TYPE_CHECKING:
    from plox.oop import PLoxInstance
    from plox.interpreter import Interpreter


class Callable:

    def call(self, interpreter: "Interpreter", arguments: List[object]) -> Any:
        raise Exception(
            "call(interpreter: Interpreter, arguments: List[object]) is not implemented"
        )

    def arity(self) -> int:
        raise Exception("arity() -> int is not implemented")


class Clock(Callable):

    def call(self, interpreter: "Interpreter", arguments: List[object]):
        return time.time()

    def arity(self) -> int:
        return 0

    def __repr__(self) -> str:
        return "<native clock fn>"


class PLoxFunction(Callable):

    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: "Interpreter", arguments: List[object]):
        environment = Environment(self.closure)
        for i, params in enumerate(self.declaration.params):
            environment.define(params.lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as e:
            return e.value
        return None

    def bind(self, instance: "PLoxInstance"):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return PLoxFunction(self.declaration, environment)

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"


class ReturnException(RuntimeError):

    def __init__(self, value: object):
        self.value = value
