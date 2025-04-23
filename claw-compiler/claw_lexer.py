# claw_lexer.py (Refactored with Indentation Handling)

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional

# --- Token Type Enum ---
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

# --- Token Dataclass ---
@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    value: Any
    line: int
    column: int # Start column of the lexeme

# --- Lexer Configuration ---
SINGLE_CHAR_TOKENS = {
    '+': TokenType.OPERATOR_PLUS, '-': TokenType.OPERATOR_MINUS,
    '*': TokenType.OPERATOR_MULTIPLY, '/': TokenType.OPERATOR_DIVIDE,
    '@': TokenType.AT, ':': TokenType.COLON,
    '(': TokenType.LPAREN, ')': TokenType.RPAREN, ',': TokenType.COMMA,
    '\n': TokenType.NEWLINE,
}

KEYWORDS_MAP = {
    'int': TokenType.KEYWORD_INT, 'print': TokenType.KEYWORD_PRINT,
    'goto': TokenType.KEYWORD_GOTO, 'exit': TokenType.KEYWORD_EXIT,
    'if': TokenType.KEYWORD_IF, 'else': TokenType.KEYWORD_ELSE,
    'return': TokenType.KEYWORD_RETURN
}

# --- Lexer Error Class ---
class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column

# --- Lexer Class ---
class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack: List[int] = [0] # Stores indentation levels (space counts)
        self.at_line_start = True         # True if the next char is the logical start of a line

    # --- Helper Methods ---
    @property
    def current_char(self) -> Optional[str]:
        return self.source_code[self.position] if self.position < len(self.source_code) else None

    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.position + offset
        return self.source_code[peek_pos] if peek_pos < len(self.source_code) else None

    def advance(self) -> Optional[str]:
        char = self.current_char
        if char is not None:
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
                self.at_line_start = True # New line means potential indent change
            else:
                self.column += 1
        return char

    def error(self, message: str):
        raise LexerError(message, self.line, self.column)

    def _add_token(self, token_type: TokenType, lexeme: str = "", value: Any = None, start_line: Optional[int] = None, start_column: Optional[int] = None):
        if start_line is None: start_line = self.line
        # Column for INDENT/DEDENT is always 1, others use current column
        if start_column is None: start_column = 1 if token_type in (TokenType.INDENT, TokenType.DEDENT) else self.column
        if value is None and token_type not in (TokenType.INDENT, TokenType.DEDENT, TokenType.EOF, TokenType.NEWLINE):
                value = lexeme # Default value is the lexeme itself
        self.tokens.append(Token(token_type, lexeme, value, start_line, start_column))
        # If we added a token other than structure tokens, we are no longer at line start
        if token_type not in (TokenType.INDENT, TokenType.DEDENT, TokenType.NEWLINE):
                self.at_line_start = False

    # --- Indentation Handling ---
    def _handle_indentation(self):
        # Calculate leading spaces on the current line
        line_start_pos = self.source_code.rfind('\n', 0, self.position) + 1
        current_indent = 0
        temp_pos = line_start_pos
        while temp_pos < len(self.source_code):
            char = self.source_code[temp_pos]
            if char == ' ':
                current_indent += 1
                temp_pos += 1
            elif char == '\t':
                self.error("Tabs are not allowed for indentation. Use spaces.") # Or handle tab width
            else:
                break # Stop at first non-space character

        # Skip calculating indent for blank lines or comment lines
        # Check character at the calculated indent position
        first_char_pos = line_start_pos + current_indent
        first_char = self.source_code[first_char_pos] if first_char_pos < len(self.source_code) else None

        if first_char is None or first_char == '\n' or first_char == '#':
            # Blank line or comment line, ignore indentation level
            self.at_line_start = True # Remain at line start conceptually to skip it
            return False # Indicate that no real content was found on this line

        # Consume the leading whitespace we just measured
        spaces_to_advance = current_indent
        start_line = self.line  # Save position before advancing
        for _ in range(spaces_to_advance):
            self.advance() # Updates self.position, self.line, self.column

        # Compare with previous indent level
        last_indent = self.indent_stack[-1]

        if current_indent > last_indent:
            self.indent_stack.append(current_indent)
            self._add_token(TokenType.INDENT, start_line=start_line, start_column=1)
        elif current_indent < last_indent:
            while current_indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self._add_token(TokenType.DEDENT, start_line=start_line, start_column=1)
            if current_indent != self.indent_stack[-1]:
                self.error(f"Inconsistent dedentation. Dedented to unknown level {current_indent}.")

        self.at_line_start = False # Processed indent, now expect content
        return True # Indicate that content follows

    # --- Scanning Methods ---
    def _scan_number(self) -> None:
        start_pos = self.position
        start_line, start_column = self.line, self.column
        while self.current_char is not None and self.current_char.isdigit():
            self.advance()
        lexeme = self.source_code[start_pos:self.position]
        try:
            value = int(lexeme)
            self._add_token(TokenType.NUMBER, lexeme, value, start_line, start_column)
        except ValueError:
            self._add_token(TokenType.ERROR, lexeme, f"Invalid number format", start_line, start_column)
    
    # Add this method to the Lexer class
    def _scan_string(self) -> None:
        start_pos = self.position
        start_line, start_column = self.line, self.column

        self.advance() # Consume the opening double quote "

        string_content = ""
        while self.current_char is not None and self.current_char != '"':
            # Handle escape sequences later if needed (e.g., \n, \t, \")
            # For now, just append the character
            char = self.current_char
            string_content += char
            self.advance()

        if self.current_char is None:
            # Reached EOF without finding the closing quote
            # Use the original starting position for the error token
            self.position = start_pos
            self.line = start_line
            self.column = start_column
            self.error("Unterminated string literal")
        else:
            # Found the closing quote
            self.advance() # Consume the closing double quote "
            lexeme = self.source_code[start_pos:self.position] # The full lexeme including quotes
            # The value is the content inside the quotes
            self._add_token(TokenType.STRING, lexeme, string_content, start_line, start_column)    

    def _scan_name_or_keyword(self) -> None:
        start_pos = self.position
        start_line, start_column = self.line, self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        lexeme = self.source_code[start_pos:self.position]
        token_type = KEYWORDS_MAP.get(lexeme, TokenType.IDENTIFIER)
        self._add_token(token_type, lexeme, lexeme, start_line, start_column)

    # --- Main Tokenizer Method ---
    def tokenizer(self) -> list[Token]:
        self.tokens = []
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.at_line_start = True

        while self.current_char is not None:
            start_line, start_column = self.line, self.column

            if self.at_line_start:
                # Handle indentation ONLY if the line isn't blank/comment
                if not self._handle_indentation():
                        # Skip the rest of the blank/comment line
                        while self.current_char is not None and self.current_char != '\n':
                            self.advance()
                        if self.current_char == '\n':
                            self.advance() # Consume the newline, sets at_line_start=True
                        continue # Start next line processing


            # --- Process non-whitespace / non-comment characters ---
            char = self.current_char

            if char == '\n':
                self._add_token(TokenType.NEWLINE, '\n', '\n', start_line, start_column)
                self.advance()
            elif char == '#': # Comment mid-line (or start if indent handling skipped it)
                while self.current_char is not None and self.current_char != '\n':
                        self.advance()
            elif char.isspace(): # Skip other whitespace (should ideally only be spaces within line now)
                    self.advance()
            elif char.isalpha() or char == '_':
                self._scan_name_or_keyword()
            elif char.isdigit():
                self._scan_number()
            elif char == '"':
                self._scan_string() # Call a new method to handle strings
            elif char == '=':
                    lexeme = "="
                    next_char = self.peek()
                    if next_char == '=':
                        lexeme = "=="; self.advance(); self.advance()
                        self._add_token(TokenType.OPERATOR_EQ, lexeme, lexeme, start_line, start_column)
                    else:
                        self.advance()
                        self._add_token(TokenType.OPERATOR_ASSIGN, lexeme, lexeme, start_line, start_column)
            elif char == '!':
                    if self.peek() == '=':
                        lexeme = "!="; self.advance(); self.advance()
                        self._add_token(TokenType.OPERATOR_NE, lexeme, lexeme, start_line, start_column)
                    else:
                        self.advance(); self.error("Unexpected character '!'")
            elif char == '<':
                    lexeme = "<"
                    next_char = self.peek()
                    if next_char == '=':
                        lexeme = "<="; self.advance(); self.advance()
                        self._add_token(TokenType.OPERATOR_LE, lexeme, lexeme, start_line, start_column)
                    else:
                        self.advance()
                        self._add_token(TokenType.OPERATOR_LT, lexeme, lexeme, start_line, start_column)
            elif char == '>':
                    lexeme = ">"
                    next_char = self.peek()
                    if next_char == '=':
                        lexeme = ">="; self.advance(); self.advance()
                        self._add_token(TokenType.OPERATOR_GE, lexeme, lexeme, start_line, start_column)
                    else:
                        self.advance()
                        self._add_token(TokenType.OPERATOR_GT, lexeme, lexeme, start_line, start_column)
            elif char in SINGLE_CHAR_TOKENS:
                    token_type = SINGLE_CHAR_TOKENS[char]
                    self._add_token(token_type, char, char, start_line, start_column)
                    self.advance()
            else:
                    lexeme = char
                    self.advance()
                    self.error(f"Unexpected character '{lexeme}'")

        # --- End of File ---
        # Ensure consistent newline at end if last line wasn't blank
        if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
             self._add_token(TokenType.NEWLINE, start_line=self.line, start_column=self.column)

        # Emit remaining DEDENTs
        while self.indent_stack[-1] > 0:
            self.indent_stack.pop()
            self._add_token(TokenType.DEDENT, start_line=self.line, start_column=1)

        self._add_token(TokenType.EOF, start_line=self.line, start_column=self.column)
        return self.tokens

# --- Example Usage ---
if __name__ == "__main__":
    source = """
# Example Eazy Code with Indentation

@main:
    int x = 10
    int y = 0
    print x # Unindented statement in @main

    if x > 5:
      print "x is greater than 5" # Indented block for if (2 spaces)
      y = x * 2
      if y > 15:
          print "y is also greater than 15" # Nested indent (4 spaces total)
      print "finished inner if"       # Matches inner indent level (4 spaces)
    # Dedent to 2 spaces automatically detected before else
    else:
      print "x is not greater than 5" # Indented block for else (2 spaces)
      y = 5
    # Dedent to 0 spaces automatically detected here

    print y # Back to @main's base indentation level (0 spaces)
    call calculate(x, y)
    return 0 # Final return

@calculate(a, b):
    int result = a + b # Indentation doesn't matter logically here
    print result
    return result
"""
    lexer = Lexer(source)
    try:
        tokens = lexer.tokenizer()
        for token in tokens:
             # Optional: Filter out NEWLINE for cleaner test output
             # if token.type != TokenType.NEWLINE:
             print(token)
    except LexerError as e:
        print(e)