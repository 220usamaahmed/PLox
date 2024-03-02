from enum import Enum

from plox.token import Token


class ScannerErrorType(Enum):

    UNTERMINATED_STRING = "Unterminated String"
    UNEXPECTED_CHARACTER = "Unexpected Character"


class ScannerError(Exception):

    def __init__(self, line: int, location: str, type: ScannerErrorType):
        super().__init__(f"[{line}]: {type}")

        self.line = line
        self.location = location
        self.type = type


class ParserErrorType(Enum):

    MISSING_RIGHT_PARAN = "Missing Right Paran"
    EXPRESSION_EXPECTED = "Expression Expected"


class ParserError(Exception):

    def __init__(self, line: int, location: str, type: ParserErrorType):
        super().__init__(f"[{line}]: {type}")

        self.line = line
        self.location = location
        self.type = type


class InterpreterErrorType(Enum):

    INVALID_UNARY_OPERATOR = "Invalid Unary Operator"
    INVALID_BINARY_OPERATOR = "Invalid Binary Operator"


class InterpreterError(Exception):

    def __init__(self, type: InterpreterErrorType):
        super().__init__(type.value)

        self.type = type


class PLoxRuntimeError(Exception):

    def __init__(self, token: Token, message: str):
        super().__init__(message)

        self.token = token
        self.message = message
