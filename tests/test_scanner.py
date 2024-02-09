from typing import List
import pytest
from plox.scanner import Scanner
from plox.token import Token
from plox.token_types import TokenType


def match_tokens(expected: List[Token], scanned: List[Token]) -> bool:
    for e, s in zip(expected, scanned):
        if e != s:
            print("MISMATCH", e, s)
            return False
    return True


def test_parens():
    expected = [
        Token(TokenType.LEFT_PAREN, "(", 1),
        Token(TokenType.RIGHT_PAREN, ")", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner("()")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_brackets():
    expected = [
        Token(TokenType.LEFT_PAREN, "(", 1),
        Token(TokenType.LEFT_BRACE, "{", 1),
        Token(TokenType.LEFT_PAREN, "(", 1),
        Token(TokenType.RIGHT_PAREN, ")", 1),
        Token(TokenType.RIGHT_BRACE, "}", 1),
        Token(TokenType.RIGHT_PAREN, ")", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner("({()})")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_assignment():
    expected = [
        Token(TokenType.VAR, "var", 1),
        Token(TokenType.IDENTIFIER, "count", 1),
        Token(TokenType.EQUAL, "=", 1),
        Token(TokenType.NUMBER, "42", 1),
        Token(TokenType.SEMI_COLON, ";", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner("var count = 42;")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_single_character_tokens():
    expected = [
        Token(TokenType.LEFT_PAREN, "(", 1),
        Token(TokenType.RIGHT_PAREN, ")", 1),
        Token(TokenType.LEFT_BRACE, "{", 1),
        Token(TokenType.RIGHT_BRACE, "}", 1),
        Token(TokenType.COMMA, ",", 1),
        Token(TokenType.DOT, ".", 1),
        Token(TokenType.MINUS, "-", 1),
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.SEMI_COLON, ";", 1),
        Token(TokenType.SLASH, "/", 1),
        Token(TokenType.STAR, "*", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner("(){},.-+;/*")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_two_character_tokens():
    expected = [
        Token(TokenType.BANG, "!", 1),
        Token(TokenType.BANG_EQUAL, "!=", 1),
        Token(TokenType.EQUAL, "=", 1),
        Token(TokenType.EQUAL_EQUAL, "==", 1),
        Token(TokenType.GREATER, ">", 1),
        Token(TokenType.GREATER_EQUAL, ">=", 1),
        Token(TokenType.LESS, "<", 1),
        Token(TokenType.LESS_EQUAL, "<=", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner("! != = == > >= < <=")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_literals_and_keywords():
    expected = [
        Token(TokenType.IDENTIFIER, "identifier", 1),
        Token(TokenType.STRING, "\"string\"", 1),
        Token(TokenType.NUMBER, "123", 1),
        Token(TokenType.TRUE, "true", 1),
        Token(TokenType.FALSE, "false", 1),
        Token(TokenType.NIL, "nil", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner("identifier \"string\" 123 true false nil")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_keywords():
    expected = [
        Token(TokenType.AND, "and", 1),
        Token(TokenType.CLASS, "class", 1),
        Token(TokenType.ELSE, "else", 1),
        Token(TokenType.FUN, "fun", 1),
        Token(TokenType.FOR, "for", 1),
        Token(TokenType.IF, "if", 1),
        Token(TokenType.OR, "or", 1),
        Token(TokenType.PRINT, "print", 1),
        Token(TokenType.RETURN, "return", 1),
        Token(TokenType.SUPER, "super", 1),
        Token(TokenType.THIS, "this", 1),
        Token(TokenType.VAR, "var", 1),
        Token(TokenType.WHILE, "while", 1),
        Token(TokenType.EOF, "", 1)
    ]

    scanner = Scanner(
        "and class else fun for if or print return super this var while")
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_multiple_lines():
    code = """
    var name = "John";
    var age = 30;
    print("Name:", name);
    print("Age:", age);
    """
    expected = [
        Token(TokenType.VAR, "var", 2),
        Token(TokenType.IDENTIFIER, "name", 2),
        Token(TokenType.EQUAL, "=", 2),
        Token(TokenType.STRING, "\"John\"", 2),
        Token(TokenType.SEMI_COLON, ";", 2),
        Token(TokenType.VAR, "var", 3),
        Token(TokenType.IDENTIFIER, "age", 3),
        Token(TokenType.EQUAL, "=", 3),
        Token(TokenType.NUMBER, "30", 3),
        Token(TokenType.SEMI_COLON, ";", 3),
        Token(TokenType.PRINT, "print", 4),
        Token(TokenType.LEFT_PAREN, "(", 4),
        Token(TokenType.STRING, "\"Name:\"", 4),
        Token(TokenType.COMMA, ",", 4),
        Token(TokenType.IDENTIFIER, "name", 4),
        Token(TokenType.RIGHT_PAREN, ")", 4),
        Token(TokenType.SEMI_COLON, ";", 4),
        Token(TokenType.PRINT, "print", 5),
        Token(TokenType.LEFT_PAREN, "(", 5),
        Token(TokenType.STRING, "\"Age:\"", 5),
        Token(TokenType.COMMA, ",", 5),
        Token(TokenType.IDENTIFIER, "age", 5),
        Token(TokenType.RIGHT_PAREN, ")", 5),
        Token(TokenType.SEMI_COLON, ";", 5),
        Token(TokenType.EOF, "", 6)
    ]

    scanner = Scanner(code)
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)


def test_multiple_lines_with_comments():
    code = """
    // Define variables
    var name = "Alice"; // Name variable
    var age = 25; // Age variable

    // Print details
    print("Name:", name); // Print Name
    print("Age:", age); // Print Age
    """
    expected = [
        Token(TokenType.VAR, "var", 3),
        Token(TokenType.IDENTIFIER, "name", 3),
        Token(TokenType.EQUAL, "=", 3),
        Token(TokenType.STRING, "\"Alice\"", 3),
        Token(TokenType.SEMI_COLON, ";", 3),
        Token(TokenType.VAR, "var", 4),
        Token(TokenType.IDENTIFIER, "age", 4),
        Token(TokenType.EQUAL, "=", 4),
        Token(TokenType.NUMBER, "25", 4),
        Token(TokenType.SEMI_COLON, ";", 4),
        Token(TokenType.PRINT, "print", 7),
        Token(TokenType.LEFT_PAREN, "(", 7),
        Token(TokenType.STRING, "\"Name:\"", 7),
        Token(TokenType.COMMA, ",", 7),
        Token(TokenType.IDENTIFIER, "name", 7),
        Token(TokenType.RIGHT_PAREN, ")", 7),
        Token(TokenType.SEMI_COLON, ";", 7),
        Token(TokenType.PRINT, "print", 8),
        Token(TokenType.LEFT_PAREN, "(", 8),
        Token(TokenType.STRING, "\"Age:\"", 8),
        Token(TokenType.COMMA, ",", 8),
        Token(TokenType.IDENTIFIER, "age", 8),
        Token(TokenType.RIGHT_PAREN, ")", 8),
        Token(TokenType.SEMI_COLON, ";", 8),
        Token(TokenType.EOF, "", 9)
    ]

    scanner = Scanner(code)
    scanner.scan_tokens()

    assert match_tokens(expected, scanner.tokens)
