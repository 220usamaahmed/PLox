from plox.token_types import TokenType


class Token:

    def __init__(self, token_type: TokenType, lexeme: str, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line

    def __repr__(self) -> str:
        return f"{self.line}: {self.token_type} - {self.lexeme}"

    def __eq__(self, __value: object) -> bool:
        return (self.token_type == __value.token_type and
                self.lexeme == __value.lexeme and
                self.line == __value.line)
