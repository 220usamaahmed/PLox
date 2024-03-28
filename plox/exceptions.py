from enum import Enum

from plox.token import Token


class ScannerErrorType(Enum):

    UNTERMINATED_STRING = "Unterminated string"
    UNEXPECTED_CHARACTER = "Unexpected character"


class ScannerError(Exception):

    def __init__(self, line: int, location: str, type: ScannerErrorType):
        super().__init__(f"[{line}]: {type}")

        self.line = line
        self.location = location
        self.type = type


class ParserErrorType(Enum):

    MISSING_LEFT_PARAN = "Missing left paran"
    MISSING_RIGHT_PARAN = "Missing right paran"
    MISSING_OPENING_BRACE = "Missing opening brace"
    MISSING_CLOSING_BRACE = "Missing closing brace"
    MISSING_SEMI_COLON = "Missing semi colon"
    EXPRESSION_EXPECTED = "Expression expected"
    EXPECTED_FUNCTION_NAME = "Expected function name"
    EXPECTED_CLASS_NAME = "Expected class name"
    EXPECTED_SUPERCLASS_NAME = "Expected superclass name"
    EXPECTED_METHOD_NAME = "Expected method name"
    EXPECTED_PROPERTY_NAME = "Expected property name"
    MISSING_IDENTIFIER = "Missing identifier"


class ParserError(Exception):

    def __init__(self, line: int, location: str, type: ParserErrorType):
        super().__init__(f"[{line}]: {type}")

        self.line = line
        self.location = location
        self.type = type


class InterpreterErrorType(Enum):

    INVALID_UNARY_OPERATOR = "Invalid unary operator"
    INVALID_BINARY_OPERATOR = "Invalid binary operator"


class InterpreterError(Exception):

    def __init__(self, type: InterpreterErrorType):
        super().__init__(type.value)

        self.type = type


class PLoxRuntimeError(Exception):

    def __init__(self, token: Token, message: str):
        super().__init__(message)

        self.token = token
        self.message = message
