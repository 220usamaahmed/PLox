from typing import TYPE_CHECKING, List
import time

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