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

    def get_at(self, distance: int, name: str) -> object:
        environment = self.ancestor(distance)
        return environment.values[name]

    def ancestor(self, distance: int) -> "Environment":
        environment: Environment = self
        for _ in range(distance):
            assert environment.enclosing is not None
            environment = environment.enclosing
        return environment

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise PLoxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign_at(self, distance: int, name: Token, value: object):
        self.ancestor(distance).values[name.lexeme] = value
