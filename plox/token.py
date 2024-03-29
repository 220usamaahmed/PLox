from enum import Enum
from typing import Optional


class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = "LEFTPAREN"
    RIGHT_PAREN = "RIGHTPAREN"
    LEFT_BRACE = "LEFTBRACE"
    RIGHT_BRACE = "RIGHTBRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMI_COLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"

    # One or two character tokens
    BANG = "BANG"
    BANG_EQUAL = "BANGEQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUALEQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATEREQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESSEQUAL"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    # Keywords
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FUN = "FUN"
    FOR = "FOR"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"

    # End of file
    EOF = "EOF"


class Token:

    def __init__(
        self,
        token_type: TokenType,
        lexeme: str,
        line: int,
        value: Optional[object] = None,
    ):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.value = value

    def __repr__(self) -> str:
        return f"{self.line}: {self.token_type} - {self.lexeme}"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Token):
            return False

        return (
            self.token_type == __value.token_type
            and self.lexeme == __value.lexeme
            and self.line == __value.line
        )
