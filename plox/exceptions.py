from enum import Enum


class ScannerErrorType(Enum):

    UNTERMINATED_STRING = "Unterminated String"
    UNEXPECTED_CHARACTER = "Unexpected Character"


class ScannerError(Exception):

    def __init__(self, line: int, location: str, type: ScannerErrorType) -> None:
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
