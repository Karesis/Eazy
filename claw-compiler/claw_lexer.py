from enum import Enum
from dataclasses import dataclass
from typing import Any 

class TokenType(Enum):
    # Operators
    OPERATOR_PLUS = "+"
    OPERATOR_MINUS = "-"
    OPERATOR_MULTIPLY = "*"
    OPERATOR_DIVIDE = "/"
    OPERATOR_ASSIGN = "="

    # Operand Type
    NUMBER = "NUMBER"

    # Keywords
    KEYWORD_INT = "int"
    KEYWORD_PRINT = "print"
    KEYWORD_GOTO = "goto"
    KEYWORD_BACK = "back"
    KEYWORD_EXIT = "exit"

    # Identifier Category
    IDENTIFIER = "IDENTIFIER" # e.g., my_name

    # Special Symbols
    AT = "@"
    COLON = ":"
    LPAREN = "("
    RPAREN = ")"
    COMMA = ","

    # Whitespace/Control 
    SPACE = "SPACE"     # Used for some reason
    NEWLINE = "NEWLINE"

    # Markers
    EOF = "EOF"         # End-of-File marker, generated when input ends
    ERROR = "ERROR"     # Represents a lexing error

@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str      # The original text segment matched
    value: Any       # The processed value (e.g., int/float for NUMBER, str for IDENTIFIER)
    line: int        # Line number where token starts
    column: int      # Column number where token starts

SINGLE_CHAR_TOKENS = {
    '+': TokenType.OPERATOR_PLUS,
    '-': TokenType.OPERATOR_MINUS,
    '*': TokenType.OPERATOR_MULTIPLY,
    '/': TokenType.OPERATOR_DIVIDE,
    '=': TokenType.OPERATOR_ASSIGN,
    '@': TokenType.AT,
    ':': TokenType.COLON,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    ',': TokenType.COMMA,
    ' ': TokenType.SPACE,      
    '\n': TokenType.NEWLINE,   
}

KEYWORDS_MAP = {
    'int': TokenType.KEYWORD_INT,
    'print': TokenType.KEYWORD_PRINT,
    'goto': TokenType.KEYWORD_GOTO,
    'back': TokenType.KEYWORD_BACK,
    'exit': TokenType.KEYWORD_EXIT,
}

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0 # current index in source_code
        self.line = 1     # current line number
        self.column = 1   # current column number
    
    @property 
    def current_char(self) -> str | None:
        if self.position < len(self.source_code):
            return self.source_code[self.position]
        else:
            return None     # None is for eof
        
    def advance(self):
        char = self.current_char # Get char before incrementing position
        if char == '\n':
            self.line += 1
            self.column = 1
        elif char is not None: 
            self.column += 1
        if self.position < len(self.source_code):
             self.position += 1
        # return char

    def _add_token(self, token_type: TokenType, lexeme: str, value: Any, start_line: int, start_column: int):
        self.tokens.append(Token(token_type, lexeme, value, start_line, start_column))

    def _scan_number(self) -> None:
        start_pos = self.position
        start_line = self.line
        start_column = self.column
        while self.current_char is not None and self.current_char.isdigit():
            self.advance()
        lexeme = self.source_code[start_pos:self.position]
        # Now we just support int
        try:
            value = int(lexeme) 
            self._add_token(TokenType.NUMBER, lexeme, value, start_line, start_column)
        except ValueError:
             self._add_token(TokenType.ERROR, lexeme, f"Invalid number format", start_line, start_column)

    def _scan_name_or_keyword(self) -> None:
        start_pos = self.position
        start_line = self.line
        start_column = self.column
        # Scan potential identifier/keyword characters
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()

        lexeme = self.source_code[start_pos:self.position]

        # Check if it's a keyword
        token_type = KEYWORDS_MAP.get(lexeme, TokenType.IDENTIFIER) # Default to IDENTIFIER
        value = lexeme # Value is the name itself for identifiers/keywords here
        self._add_token(token_type, lexeme, value, start_line, start_column)

    def tokenizer(self) -> list[Token]:
        # Can be used for many times (initialize)
        self.tokens = []
        while self.current_char is not None:

            char = self.current_char
            start_line = self.line
            start_column = self.column

            # Skip Whitespace (Wild whitespaces)
            if char == ' ': 
                self.advance()
                continue

            # Skip comments
            elif char == '#':
                self.advance() # Consume '#'
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                # the '\n' or EOF will be handled in the mainloop
                continue
            
            # Handle Names (Identifiers or Keywords) - Must come before single char '@' check
            elif char.isalpha() or char == '_':
                self._scan_name_or_keyword()
                # Scan method has handled advancing

            # Check for Numbers
            elif char.isdigit():
                self._scan_number()
                # _scan_number handles advancing past the number

            # Check for Single-Character Tokens
            elif char in SINGLE_CHAR_TOKENS:
                token_type = SINGLE_CHAR_TOKENS[char]
                self._add_token(token_type, char, char, start_line, start_column)
                self.advance() # Consume the single character

            # Handle Unrecognized Characters
            else:
                lexeme = char
                self._add_token(TokenType.ERROR, lexeme, f"Unexpected character '{lexeme}'", start_line, start_column)
                self.advance() # Consume the error character

        # End of loop: Add the EOF token
        self._add_token(TokenType.EOF, "", None, self.line, self.column) # EOF token at the final position

        return self.tokens
    
if __name__ == "__main__":
    source = """@calculate():
    int a
    int b
    a = 10
    b = a * 5 + 2
    print b
    back ()

@main:
    goto calculate()"""
    lexer = Lexer(source)
    tokens = lexer.tokenizer()
    for token in tokens:
        print(token)
                
                
            