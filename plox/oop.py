from typing import TYPE_CHECKING, Any, Dict, List, Optional
from plox.exceptions import PLoxRuntimeError
from plox.functions import Callable, PLoxFunction
from plox.token import Token

if TYPE_CHECKING:
    from plox.interpreter import Interpreter


class PLoxClass(Callable):

    def __init__(self, name: str, superclass: Optional["PLoxClass"], methods: Dict[str, PLoxFunction]) -> None:
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __repr__(self) -> str:
        return self.name

    def call(self, interpreter: "Interpreter", arguments: List[object]) -> Any:
        instance = PLoxInstance(self)

        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        if initializer := self.find_method("init"): 
            return initializer.arity()

        return 0

    def find_method(self, name: str) -> PLoxFunction | None:
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.methods.get(name)


class PLoxInstance:

    def __init__(self, plox_class: PLoxClass) -> None:
        self.plox_class = plox_class
        self.fields: Dict[str, object] = {}

    def get(self, name: Token) -> object:
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        method = self.plox_class.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise PLoxRuntimeError(name, f"Undefined property {name.lexeme}")

    def set(self, name: Token, value: object):
        self.fields[name.lexeme] = value

    def __repr__(self) -> str:
        return f"{self.plox_class.name} instance"
