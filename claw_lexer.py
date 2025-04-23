# --- Import ---
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional

# --- Structure ---
class TokenType(Enum):
    # Operators
    OPERATOR_PLUS = "+"
    OPERATOR_MINUS = "-"
    OPERATOR_MULTIPLY = "*"
    OPERATOR_DIVIDE = "/"
    OPERATOR_ASSIGN = "="
    OPERATOR_EQ = "=="      # Equal
    OPERATOR_NE = "!="      # Not Equal
    OPERATOR_LT = "<"       # Less Than
    OPERATOR_LE = "<="      # Less Than or Equal
    OPERATOR_GT = ">"       # Greater Than
    OPERATOR_GE = ">="      # Greater Than or Equal

    # Operand Type
    NUMBER = "NUMBER"       # Currently only integer
    STRING = "STRING"

    # Keywords
    KEYWORD_INT = "int"
    KEYWORD_PRINT = "print" # Example built-in
    KEYWORD_GOTO = "goto"   # For intra-block jumps
    KEYWORD_EXIT = "exit"   # Example built-in
    KEYWORD_RETURN = "return" # For returning from blocks
    KEYWORD_IF = "if"
    KEYWORD_ELSE = "else"

    # Identifier Category
    IDENTIFIER = "IDENTIFIER" # Variable names, block names, labels

    # Special Symbols
    AT = "@"
    COLON = ":"
    LPAREN = "("
    RPAREN = ")"
    COMMA = ","

    # Whitespace/Control
    NEWLINE = "NEWLINE"     # Significant for ending statements and structure
    INDENT = "INDENT"       # Pseudo-token for increased indentation
    DEDENT = "DEDENT"       # Pseudo-token for decreased indentation

    # Markers
    EOF = "EOF"             # End-of-File marker
    ERROR = "ERROR"         # Represents a lexing error

# Token Dictionary
SINGLE_CHAR_TOKENS = {
    '+': TokenType.OPERATOR_PLUS, 
    '-': TokenType.OPERATOR_MINUS,
    '*': TokenType.OPERATOR_MULTIPLY, 
    '/': TokenType.OPERATOR_DIVIDE,
    '@': TokenType.AT, 
    ':': TokenType.COLON,
    '(': TokenType.LPAREN, 
    ')': TokenType.RPAREN, 
    ',': TokenType.COMMA,
    '\n': TokenType.NEWLINE,
}
KEYWORDS_MAP = {
    'int': TokenType.KEYWORD_INT, 
    'print': TokenType.KEYWORD_PRINT,
    'goto': TokenType.KEYWORD_GOTO, 
    'exit': TokenType.KEYWORD_EXIT,
    'if': TokenType.KEYWORD_IF, 
    'else': TokenType.KEYWORD_ELSE,
    'return': TokenType.KEYWORD_RETURN
}

@dataclass(froze=True)
class Token:
    type: TokenType
    lexeme: str
    value: Any
    # Location
    line: int
    column: int

# --- Lexer Class ---
class Lexer:
    # Init Class
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        # Code String Pointer
        self.position = 0
        # Location Infomation
        self.line = 1
        self.column = 1
        # Stack For Indentations
        self.indent_stack: List[int] = [0]
        self.at_line_start = True   # If its after a '\n', else ignore
    @property
    def current_char(self) -> Optional[str]:
        return self.source_code[self.position] if self.position < len(self.source_code) else None
