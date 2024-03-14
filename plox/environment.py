from typing import Optional, Dict
from plox.exceptions import PLoxRuntimeError
from plox.token import Token


class Environment:

    def __init__(self, enclosing: Optional["Environment"] = None):
        self.enclosing = enclosing
        self.values: Dict[str, object] = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        raise PLoxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise PLoxRuntimeError(name, f"Undefined variable {name.lexeme}.")
