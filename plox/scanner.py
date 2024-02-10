from typing import List
from plox.exceptions import ScannerError, ScannerErrorType
from plox.token import Token, TokenType


class Scanner():

    def __init__(self, source: str):
        self.source: str = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.had_error: bool = False

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line))

    def scan_token(self):
        character = self.advance()
        match character:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMI_COLON)
            case '*': self.add_token(TokenType.STAR)
            case '!':
                if self.match_character('='):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case '=':
                if self.match_character('='):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case '<':
                if self.match_character('='):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case '>':
                if self.match_character('='):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)

            case '/':
                if self.match_character('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t': pass
            case '\n': self.line += 1
            case '"': self.match_string()
            case _:
                if character.isdigit():
                    self.match_number()
                elif self.is_alpha(character):
                    self.match_identifier_or_reserved_word()
                else:
                    self.had_error = True
                    raise ScannerError(
                        self.line, "", ScannerErrorType.UNEXPECTED_CHARACTER)

    def advance(self) -> str:
        character = self.source[self.current]
        self.current += 1

        return character

    def match_character(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def match_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.had_error = True
            raise ScannerError(
                self.line, "", ScannerErrorType.UNTERMINATED_STRING)

        self.advance()

        self.add_token(TokenType.STRING)

    def match_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER)

    def match_identifier_or_reserved_word(self):
        while self.peek().isalnum():
            self.advance()

        character = self.source[self.start:self.current]

        match character:
            case 'and': self.add_token(TokenType.AND)
            case 'class': self.add_token(TokenType.CLASS)
            case 'else': self.add_token(TokenType.ELSE)
            case 'false': self.add_token(TokenType.FALSE)
            case 'for': self.add_token(TokenType.FOR)
            case 'fun': self.add_token(TokenType.FUN)
            case 'if': self.add_token(TokenType.IF)
            case 'nil': self.add_token(TokenType.NIL)
            case 'or': self.add_token(TokenType.OR)
            case 'print': self.add_token(TokenType.PRINT)
            case 'return': self.add_token(TokenType.RETURN)
            case 'super': self.add_token(TokenType.SUPER)
            case 'this': self.add_token(TokenType.THIS)
            case 'true': self.add_token(TokenType.TRUE)
            case 'var': self.add_token(TokenType.VAR)
            case 'while': self.add_token(TokenType.WHILE)
            case _: self.add_token(TokenType.IDENTIFIER)

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def is_alpha(self, character: str) -> bool:
        return character.isalnum() or character == '_'
