from typing import TYPE_CHECKING, List
import time

from plox.ast.stmt_types import Function
from plox.environment import Environment

if TYPE_CHECKING:
    from plox.interpreter import Interpreter

class Callable:

    def call(self, interpreter: 'Interpreter', arguments: List[object]):
        raise Exception('call(interpreter: Interpreter, arguments: List[object]) is not implemented')
    
    def arity(self) -> int:
        raise Exception('arity() -> int is not implemented')
    

class Clock(Callable):

    def call(self, interpreter: 'Interpreter', arguments: List[object]):
        return time.time()

    def arity(self) -> int:
        return 0
    
    def __repr__(self) -> str:
        return "<native clock fn>"

class PLoxFunction(Callable):

    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter: 'Interpreter', arguments: List[object]):
        environment = Environment(interpreter.globals)
        for i, params in enumerate(self.declaration.params):
            environment.define(params.lexeme, arguments[i])
        interpreter.execute_block(self.declaration.body, environment)
        return None

    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __repr__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"