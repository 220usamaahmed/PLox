"""
EXPRESSION GRAMMAR
------------------
expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
               | equality
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → "true" | "false" | "nil"
               | NUMBER | STRING
               | "(" expression ")"
               | IDENTIFIER ;


STATEMENT GRAMMAR
-----------------
program        → declaration* EOF ;
declaration    → varDecl
               | statement
statement      → exprStmt
               | printStmt
               | block ;
exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
block          → "{" declaration* "}"
varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
"""

from typing import List
from plox.ast.expr_interface import Expr
from plox.ast.expr_types import Assign, Binary, Grouping, Unary, Literal, Variable
from plox.ast.stmt_interface import Stmt
from plox.ast.stmt_types import Block, Expression, Print, VariableDeclaration
from plox.exceptions import ParserError, ParserErrorType
from plox.token import Token, TokenType


class Parser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements: List[Stmt] = []

        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration();
            
            return self.statement()
        except ParserError:
            self.synchronize()

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expression_statement()

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMI_COLON, ParserErrorType.MISSING_SEMI_COLON)
        return Expression(expr)
    
    def block(self) -> List[Stmt]:
        statements: List[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, ParserErrorType.MISSING_CLOSING_BRACE)
        return statements

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMI_COLON, ParserErrorType.MISSING_SEMI_COLON)
        return Print(value)

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, ParserErrorType.MISSING_IDENTIFIER)

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        
        self.consume(TokenType.SEMI_COLON, ParserErrorType.MISSING_SEMI_COLON)
        return VariableDeclaration(name, initializer)

    def expression(self) -> Expr:
        return self.assignment()
    
    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            
            # TODO: Handle error reporting
            print(f"Invalid assignment target. {equals}") 
        
        return expr


    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        
        if self.match(TokenType.TRUE):
            return Literal(True)
        
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().value)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN,
                         ParserErrorType.MISSING_RIGHT_PARAN)
            return Grouping(expr)

        token = self.peek()
        if token.token_type == TokenType.EOF:
            location = "End of line"
        else:
            location = f"Near '{token.lexeme}'"
        raise ParserError(token.line, location,
                          ParserErrorType.EXPRESSION_EXPECTED)

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, token_type: TokenType, type: ParserErrorType) -> Token:
        if self.check(token_type):
            return self.advance()

        token = self.peek()
        if token.token_type == TokenType.EOF:
            location = "End of line"
        else:
            location = f"Near '{token.lexeme}'"
        raise ParserError(token.line, location, type)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMI_COLON:
                return

            if self.peek().token_type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()
