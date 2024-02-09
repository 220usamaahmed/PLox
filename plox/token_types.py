from enum import Enum


class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = 'LEFTPAREN'
    RIGHT_PAREN = 'RIGHTPAREN'
    LEFT_BRACE = 'LEFTBRACE'
    RIGHT_BRACE = 'RIGHTBRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMI_COLON = 'SEMICOLON'
    SLASH = 'SLASH'
    STAR = 'STAR'

    # One or two character tokens
    BANG = 'BANG'
    BANG_EQUAL = 'BANGEQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUALEQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATEREQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESSEQUAL'

    # Literals
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    # Keywords
    AND = 'AND'
    CLASS = 'CLASS'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    NIL = 'NIL'
    OR = 'OR'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'

    # End of file
    EOF = 'EOF'
