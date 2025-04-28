# leparser.py
# Contains the Lexer and Parser for the Eazy language.

import sys
# Import AST node definitions from the separate AST file
from eazy_ast import *

# --- Token Definitions ---
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_OPERATOR = 'OPERATOR'
TT_INT = 'INT'
TT_CHAR = 'CHAR'
TT_SYMBOL = 'SYMBOL' # @ : . ( ) { } ,
TT_EOF = 'EOF'
TT_NEWLINE = 'NEWLINE'
TT_INDENT = 'INDENT'
TT_DEDENT = 'DEDENT'
TT_UNKNOWN = 'UNKNOWN'

KEYWORDS = [
    'int', 'char', 'struct', 'set', 'image', 'call', 'ret', 'goto', 'if', 'exit', 'print'
]

COMPARISON_OPS = ['==', '!=', '<', '>', '<=', '>=']
ARITHMETIC_OPS = ['+', '-', '*', '/']
ALL_OPS = COMPARISON_OPS + ARITHMETIC_OPS

class Token:
    """Represents a token produced by the Lexer."""
    def __init__(self, type_, value=None, line=0, column=0):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.value is not None:
            return f'Token({self.type}, {repr(self.value)}, L{self.line} C{self.column})'
        return f'Token({self.type}, L{self.line} C{self.column})'

# --- Lexer Implementation ---
class Lexer:
    """Processes Eazy source text and converts it into a stream of tokens."""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.tokens = []

    def advance(self):
        """Move the position forward in the text."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        """Look at the next character without consuming it."""
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        """Skip non-newline whitespace."""
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def handle_newline(self):
        """Handle indentation/dedentation logic after a newline."""
        # Calculate indentation of the next line
        current_indent = 0
        while self.current_char == ' ':
            current_indent += 1
            self.advance()

        # Check for comments or blank lines *after* calculating indent
        is_comment_or_blank = False
        if self.current_char == '#':
            is_comment_or_blank = True
            while self.current_char is not None and self.current_char != '\n': self.advance()
        elif self.current_char == '\n':
             is_comment_or_blank = True

        # Don't adjust indent stack or emit tokens for comment/blank lines
        if is_comment_or_blank: return

        # Compare indentation only for lines with actual code
        last_indent = self.indent_stack[-1]
        if current_indent > last_indent:
            self.indent_stack.append(current_indent)
            self.tokens.append(Token(TT_INDENT, line=self.line, column=1))
        elif current_indent < last_indent:
            while current_indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token(TT_DEDENT, line=self.line, column=1))
            if current_indent != self.indent_stack[-1]:
                 print(f"IndentationError (L{self.line}): unindent does not match any outer indentation level.", file=sys.stderr)
                 self.tokens.append(Token(TT_UNKNOWN, f"Bad dedent to {current_indent}", line=self.line, column=1))

    def get_identifier(self):
        """Parse an identifier or keyword."""
        result = ''
        start_line, start_column = self.line, self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char; self.advance()
        token_type = TT_KEYWORD if result in KEYWORDS else TT_IDENTIFIER
        return Token(token_type, result, line=start_line, column=start_column)

    def get_number(self):
        """Parse an integer literal."""
        result = ''
        start_line, start_column = self.line, self.column
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char; self.advance()
        return Token(TT_INT, int(result), line=start_line, column=start_column)

    def get_char_literal(self):
        """Parse a character literal (e.g., 'a')."""
        start_line, start_column = self.line, self.column
        self.advance() # Consume '
        char_val = self.current_char
        if char_val == '\\': self.advance(); char_val += self.current_char # Handle simple escapes
        self.advance()
        if self.current_char == "'":
            self.advance(); return Token(TT_CHAR, char_val, line=start_line, column=start_column)
        else:
            print(f"SyntaxError (L{start_line} C{start_column}): Unterminated char literal", file=sys.stderr)
            return Token(TT_UNKNOWN, f"Unterminated char '{char_val}", line=start_line, column=start_column)

    def get_operator(self):
        """Parse an operator (single or multi-character)."""
        start_line, start_column = self.line, self.column
        op1 = self.current_char
        peek_char = self.peek()
        two_char_op = op1 + peek_char if peek_char else None

        if two_char_op in ALL_OPS:
            self.advance(); self.advance(); return Token(TT_OPERATOR, two_char_op, line=start_line, column=start_column)
        elif op1 in ALL_OPS:
            self.advance(); return Token(TT_OPERATOR, op1, line=start_line, column=start_column)
        else:
            return None # Not an operator

    def tokenize(self):
        """Generate all tokens from the source text."""
        self.tokens = []
        while self.current_char is not None:
            start_line, start_column = self.line, self.column

            if self.current_char.isspace() and self.current_char != '\n': self.skip_whitespace(); continue
            if self.current_char == '#':
                while self.current_char is not None and self.current_char != '\n': self.advance()
                continue

            if self.current_char == '\n':
                self.advance() # Consume '\n' first
                self.handle_newline() # Process potential indent/dedent for next line
                self.tokens.append(Token(TT_NEWLINE, line=start_line, column=start_column)) # Add NEWLINE token
                continue

            token = None
            if self.current_char.isalpha() or self.current_char == '_': token = self.get_identifier()
            elif self.current_char.isdigit(): token = self.get_number()
            elif self.current_char == "'": token = self.get_char_literal()
            else:
                op_token = self.get_operator()
                if op_token: token = op_token
                else:
                    symbol_map = {'@': TT_SYMBOL, ':': TT_SYMBOL, '.': TT_SYMBOL, '(': TT_SYMBOL,
                                  ')': TT_SYMBOL, '{': TT_SYMBOL, '}': TT_SYMBOL, ',': TT_SYMBOL}
                    if self.current_char in symbol_map:
                        token = Token(symbol_map[self.current_char], self.current_char, line=start_line, column=start_column)
                        self.advance()
                    else:
                        unknown_char = self.current_char; self.advance()
                        token = Token(TT_UNKNOWN, unknown_char, line=start_line, column=start_column)

            if token: self.tokens.append(token)

        # End of file handling
        start_line, start_column = self.line, self.column
        while self.indent_stack[-1] > 0:
             self.indent_stack.pop(); self.tokens.append(Token(TT_DEDENT, line=start_line, column=start_column))
        self.tokens.append(Token(TT_EOF, line=start_line, column=start_column))
        return self.tokens


# --- Parser Implementation ---
class Parser:
    """Parses a stream of tokens into an Abstract Syntax Tree (AST)."""
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type != TT_UNKNOWN]
        self.token_index = 0
        self.current_token = self.tokens[self.token_index] if self.tokens else Token(TT_EOF, line=1, column=1)

    def advance(self):
        """Consume the current token and move to the next one."""
        self.token_index += 1
        self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else self.tokens[-1]

    def peek(self, offset=1):
        """Look ahead at upcoming tokens without consuming."""
        peek_index = self.token_index + offset
        return self.tokens[peek_index] if peek_index < len(self.tokens) else self.tokens[-1]

    def eat(self, token_type, value=None):
        """Consume the current token if it matches the expected type/value."""
        token = self.current_token
        if token.type == token_type and (value is None or token.value == value):
            self.advance()
            return token
        else:
            expected_value_str = f" with value '{value}'" if value is not None else ""
            print(f"SyntaxError (L{token.line} C{token.column}): Expected {token_type}{expected_value_str}, got {token.type} ('{token.value}')", file=sys.stderr)
            sys.exit(1) # Or raise an exception

    def skip_newlines(self):
        """Consume any consecutive NEWLINE tokens."""
        while self.current_token.type == TT_NEWLINE:
            self.advance()

    def parse(self):
        """Start the parsing process."""
        return self.parse_program()

    def parse_program(self):
        """Parse the entire program (a sequence of blocks)."""
        blocks = []
        self.skip_newlines()
        while self.current_token.type != TT_EOF:
            if self.current_token.type == TT_SYMBOL and self.current_token.value == '@':
                blocks.append(self.parse_block_def())
            else:
                 print(f"SyntaxError (L{self.current_token.line} C{self.current_token.column}): Expected '@' to start block definition, got {self.current_token.type}", file=sys.stderr)
                 sys.exit(1)
            # Block parsing handles its own trailing newlines/dedents
        return ProgramNode(blocks)

    def parse_block_def(self):
        """Parse a block definition: @name(params): NEWLINE INDENT body DEDENT"""
        start_line, start_col = self.current_token.line, self.current_token.column
        self.eat(TT_SYMBOL, '@')
        name_token = self.eat(TT_IDENTIFIER)
        params = None
        if self.current_token.type == TT_SYMBOL and self.current_token.value == '(':
            params = self.parse_parameters()
        self.eat(TT_SYMBOL, ':')
        self.eat(TT_NEWLINE)

        body = []
        # Handle optional indentation for the block body
        if self.current_token.type == TT_INDENT:
            self.advance() # Consume INDENT
            body = self.parse_block_body()
            self.eat(TT_DEDENT) # Expect DEDENT at the end
        # Allow empty blocks (no INDENT/DEDENT needed if immediately followed by EOF or another block def)
        elif self.current_token.type not in (TT_EOF, TT_SYMBOL): # Check if something unexpected follows newline
             # If it's not EOF or another '@', it should have been INDENT or DEDENT (for empty block followed by parent dedent)
             # This logic might need refinement based on exact empty block rules.
             # Let's assume empty blocks are allowed if the next token implies the block ends.
             # If the next token is DEDENT, it means an empty block followed by parent dedent.
             if self.current_token.type == TT_DEDENT:
                 pass # Okay, empty block, parent will handle dedent.
             # If it's EOF or '@', it's also okay.
             elif self.current_token.type in (TT_EOF, TT_SYMBOL):
                 pass
             else:
                 print(f"SyntaxError (L{self.current_token.line} C{self.current_token.column}): Expected INDENT after block definition ':', got {self.current_token.type}", file=sys.stderr)
                 sys.exit(1)


        return BlockDefNode(name_token, params, body, start_line, start_col)

    def parse_parameters(self):
        """Parse block parameters: (type name, type name, ...)"""
        params = []
        self.eat(TT_SYMBOL, '(')
        if not (self.current_token.type == TT_SYMBOL and self.current_token.value == ')'):
            while True:
                type_token = self.eat(TT_KEYWORD) # Assuming types are keywords
                name_token = self.eat(TT_IDENTIFIER)
                params.append(ParamNode(type_token, name_token))
                if self.current_token.type == TT_SYMBOL and self.current_token.value == ',':
                    self.advance(); self.skip_newlines()
                else: break
        self.eat(TT_SYMBOL, ')')
        return params

    def parse_block_body(self):
        """Parse statements within an indented block."""
        statements = []
        while self.current_token.type not in (TT_DEDENT, TT_EOF):
            statements.append(self.parse_statement())
            if self.current_token.type not in (TT_DEDENT, TT_EOF):
                 self.eat(TT_NEWLINE)
                 self.skip_newlines() # Allow blank lines
        return statements

    def parse_statement(self):
        """Parse a single statement."""
        token = self.current_token
        # Check based on the starting token
        if token.type == TT_SYMBOL:
            if token.value == '@': return self.parse_block_def() # Nested block
            if token.value == '.': return self.parse_binding()
        elif token.type == TT_KEYWORD:
            if token.value in ('int', 'char'): return self.parse_var_decl()
            if token.value == 'struct': return self.parse_struct_instance()
            if token.value == 'set': return self.parse_set_statement()
            if token.value == 'image': return self.parse_image_statement()
            if token.value == 'call': return self.parse_call_statement()
            if token.value == 'ret': return self.parse_ret_statement()
            if token.value == 'goto': return self.parse_goto_statement()
            if token.value == 'if': return self.parse_if_statement()
            if token.value == 'print': return self.parse_print_statement()
            if token.value == 'exit': return self.parse_exit_statement()
        elif token.type == TT_IDENTIFIER and self.peek().type == TT_SYMBOL and self.peek().value == ':':
            return self.parse_label() # Label definition

        # If none of the above match, it's an error
        print(f"SyntaxError (L{token.line} C{token.column}): Unexpected token at start of statement: {token.type} ('{token.value}')", file=sys.stderr)
        sys.exit(1)

    # --- Statement Parsing Methods ---
    # (Keep the implementations for parse_var_decl, parse_struct_instance,
    # parse_set_statement, parse_image_statement, parse_call_statement,
    # parse_ret_statement, parse_goto_statement, parse_label, parse_if_statement,
    # parse_print_statement, parse_exit_statement, parse_binding,
    # parse_argument_list from the previous version, as they don't need
    # changes related to this refactoring)

    def parse_var_decl(self):
        type_token = self.eat(TT_KEYWORD)
        name_token = self.eat(TT_IDENTIFIER)
        return VarDeclNode(type_token, name_token)

    def parse_struct_instance(self):
        self.eat(TT_KEYWORD, 'struct')
        name_token = self.eat(TT_IDENTIFIER)
        self.eat(TT_SYMBOL, '{')
        self.skip_newlines()
        members = []
        if not (self.current_token.type == TT_SYMBOL and self.current_token.value == '}'):
             while True:
                 type_token = self.eat(TT_KEYWORD)
                 member_name = self.eat(TT_IDENTIFIER)
                 members.append(StructMemberNode(type_token, member_name))
                 self.skip_newlines()
                 if self.current_token.type == TT_SYMBOL and self.current_token.value == ',':
                     self.advance(); self.skip_newlines()
                 else: break
        self.eat(TT_SYMBOL, '}')
        return StructInstanceNode(name_token, members)

    def parse_set_statement(self):
        self.eat(TT_KEYWORD, 'set')
        target = self.parse_target_expression()
        expression = self.parse_expression()
        return SetNode(target, expression)

    def parse_image_statement(self):
        self.eat(TT_KEYWORD, 'image')
        image_name = self.eat(TT_IDENTIFIER)
        template_name = self.eat(TT_IDENTIFIER)
        args = None
        if self.current_token.type == TT_SYMBOL and self.current_token.value == '(':
            args = self.parse_argument_list()
        return ImageNode(image_name, template_name, args)

    def parse_call_statement(self):
        self.eat(TT_KEYWORD, 'call')
        result_container = self.eat(TT_IDENTIFIER)
        target_block = self.parse_target_expression()
        args = None
        if self.current_token.type == TT_SYMBOL and self.current_token.value == '(':
             args = self.parse_argument_list()
        return CallNode(result_container, target_block, args)

    def parse_ret_statement(self):
        self.eat(TT_KEYWORD, 'ret')
        value = self.parse_expression()
        return RetNode(value)

    def parse_goto_statement(self):
        self.eat(TT_KEYWORD, 'goto')
        label = self.eat(TT_IDENTIFIER)
        return GotoNode(label)

    def parse_label(self):
        name = self.eat(TT_IDENTIFIER)
        self.eat(TT_SYMBOL, ':')
        return LabelNode(name)

    def parse_if_statement(self):
        # Correct implementation: expects statement at same indent level after newline
        self.eat(TT_KEYWORD, 'if')
        condition = self.parse_comparison()
        self.eat(TT_NEWLINE)
        # The statement follows directly, without extra indent
        if self.current_token.type in (TT_DEDENT, TT_EOF): # Cannot end after if condition+newline
             print(f"SyntaxError (L{self.current_token.line} C{self.current_token.column}): Expected statement after 'if', found {self.current_token.type}", file=sys.stderr)
             sys.exit(1)
        statement = self.parse_statement()
        return IfNode(condition, statement)

    def parse_print_statement(self):
        self.eat(TT_KEYWORD, 'print')
        value = self.parse_expression()
        return PrintNode(value)

    def parse_exit_statement(self):
        self.eat(TT_KEYWORD, 'exit')
        return ExitNode()

    def parse_binding(self):
         self.eat(TT_SYMBOL, '.')
         name = self.eat(TT_IDENTIFIER)
         return BindingNode(name)

    def parse_argument_list(self):
        args = []
        self.eat(TT_SYMBOL, '(')
        if not (self.current_token.type == TT_SYMBOL and self.current_token.value == ')'):
            while True:
                args.append(self.parse_expression())
                if self.current_token.type == TT_SYMBOL and self.current_token.value == ',':
                    self.advance(); self.skip_newlines()
                else: break
        self.eat(TT_SYMBOL, ')')
        return args


    # --- Expression Parsing Methods ---
    # (Keep the implementations for parse_expression, parse_comparison,
    # parse_arithmetic, parse_term, parse_factor, parse_identifier_or_access,
    # parse_target_expression from the previous version)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        node = self.parse_arithmetic()
        while self.current_token.type == TT_OPERATOR and self.current_token.value in COMPARISON_OPS:
            op_token = self.current_token; self.advance()
            right = self.parse_arithmetic()
            node = BinaryOpNode(left=node, op_token=op_token, right=right)
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.current_token.type == TT_OPERATOR and self.current_token.value in ['+', '-']:
            op_token = self.current_token; self.advance()
            right = self.parse_term()
            node = BinaryOpNode(left=node, op_token=op_token, right=right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token.type == TT_OPERATOR and self.current_token.value in ['*', '/']:
            op_token = self.current_token; self.advance()
            right = self.parse_factor()
            node = BinaryOpNode(left=node, op_token=op_token, right=right)
        return node

    def parse_factor(self):
        token = self.current_token
        if token.type == TT_INT: self.advance(); return IntLiteralNode(token)
        if token.type == TT_CHAR: self.advance(); return CharLiteralNode(token)
        if token.type == TT_IDENTIFIER: return self.parse_identifier_or_access()
        if token.type == TT_SYMBOL and token.value == '(':
            self.advance(); expr = self.parse_expression(); self.eat(TT_SYMBOL, ')'); return expr
        print(f"SyntaxError (L{token.line} C{token.column}): Unexpected token in expression factor: {token.type} ('{token.value}')", file=sys.stderr)
        sys.exit(1)

    def parse_identifier_or_access(self):
        base_token = self.eat(TT_IDENTIFIER)
        node = IdentifierNode(base_token)
        while self.current_token.type == TT_SYMBOL and self.current_token.value == '.':
            self.advance(); member_token = self.eat(TT_IDENTIFIER)
            node = MemberAccessNode(base=node, member_token=member_token)
        return node

    def parse_target_expression(self):
         node = self.parse_identifier_or_access()
         if not isinstance(node, (IdentifierNode, MemberAccessNode)):
              first_token = node.token if hasattr(node, 'token') else node.base.token if hasattr(node, 'base') else self.current_token
              print(f"SyntaxError (L{first_token.line} C{first_token.column}): Invalid target for set/call.", file=sys.stderr)
              sys.exit(1)
         return node


# --- Example Usage (Optional: Keep for testing this file) ---
# def print_ast(node, indent=0):
#     # (Include the print_ast function here if needed for standalone testing)
#     # ... implementation ...
#     pass

# if __name__ == "__main__":
#     eazy_code_example = """
#     @main:
#         int x
#         set x 10
#         if x == 10
#             print x
#         exit
#     """
#     lexer = Lexer(eazy_code_example)
#     tokens = lexer.tokenize()
#     print("--- Tokens ---")
#     for t in tokens: print(t)

#     if tokens and tokens[-1].type == TT_EOF:
#         parser = Parser(tokens)
#         try:
#             ast = parser.parse()
#             print("\n--- AST ---")
#             # print_ast(ast) # Requires print_ast definition
#         except SystemExit:
#             print("\nParsing failed.")
#         except Exception as e:
#             print(f"\nAn unexpected error occurred during parsing: {e}")
#             import traceback
#             traceback.print_exc()
#     else:
#         print("\nLexing failed or produced no tokens.")


