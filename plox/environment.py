from plox.exceptions import PLoxRuntimeError
from plox.token import Token


class Environment:

    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        print(f"Defining {name} = {value}")
        self.values[name] = value
        print(self.values)

    def get(self, name: Token) -> object:
        print(f"Getting {name.lexeme}, {self.values}")

        if name.lexeme in self.values:
            print(f"{name} found: {self.values[name.lexeme]}")
            return self.values[name.lexeme]
        
        raise PLoxRuntimeError(name, f"Undefined variable {name.lexeme}.")