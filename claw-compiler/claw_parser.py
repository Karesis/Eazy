# claw_parser.py (Refactored - Phase 2: INDENT/DEDENT and Basic Expressions)

from typing import List, Optional

# --- NEW: Import Updated AST Nodes ---
from claw_ast import (
    ASTNode, ExpressionNode, StatementNode,
    ConstantNode, IdentifierNode, BinaryOperationNode, CallExpressionNode,
    VarDeclNode, AssignmentNode, ReturnNode, CallStatementNode,
    ExpressionStatementNode, IfNode, GotoNode, LabelNode, UnaryOperationNode,
    ParameterNode, BlockDefinition, Program
)
from claw_lexer import Token, TokenType

class ParserError(Exception): # Custom exception for parser errors
    def __init__(self, message, line, column):
        super().__init__(f"Parser Error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column

class Parser:

    PREC_LOWEST = 0
    PREC_COMPARISON = 1 # == != < <= > >=
    PREC_SUM = 2        # + -
    PREC_PRODUCT = 3    # * /
    PREC_UNARY = 4      # - (unary), ! (unary, if added later)
    # PREC_CALL = 5     # Example for future extension

    def __init__(self, tokens: List[Token]):
        # Filter out NEWLINE tokens as they are mainly structural markers now,
        # except when needed specifically (e.g., after COLON).
        # INDENT/DEDENT carry the block structure info.
        # self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE] # Option 1: Filter early
        self.tokens = tokens # Option 2: Keep NEWLINEs for now, skip them where appropriate
        self.current_token_index = 0

    # --- Helper methods ---
    @property
    def current_token(self) -> Token:
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else self.tokens[-1]

    def peek(self, offset: int = 1) -> Token:
        index = self.current_token_index + offset
        return self.tokens[index] if index < len(self.tokens) else self.tokens[-1]

    def consume(self, *expected_types: TokenType) -> Token:
        """Consumes and returns the current token, checking its type."""
        current = self.current_token
        # Allow consuming EOF multiple times without error/advance
        if current.type == TokenType.EOF:
            if not expected_types or TokenType.EOF in expected_types:
                return current
            else:
                expected_str = ", ".join(str(t) for t in expected_types)
                self.error(f"Expected one of [{expected_str}], but reached End of File")

        # Check type match
        if not expected_types or current.type in expected_types:
            self.current_token_index += 1
            return current
        else:
            expected_str = ", ".join(str(t) for t in expected_types)
            self.error(f"Expected one of [{expected_str}], but got {current.type} ('{current.lexeme}')")

    def error(self, message: str):
        token = self.current_token
        # Use custom ParserError
        raise ParserError(message, token.line, token.column)

    def skip_newlines(self):
        """Consumes one or more consecutive NEWLINE tokens."""
        consumed_newline = False
        while self.current_token.type == TokenType.NEWLINE:
            self.consume(TokenType.NEWLINE)
            consumed_newline = True
        return consumed_newline # Indicate if at least one newline was skipped

    # --- Parsing Entry Point ---
    def parse(self) -> Program:
        program_node = self.parse_program()
        if self.current_token.type != TokenType.EOF:
            self.error(f"Expected EOF, but found {self.current_token.type}")
        return program_node

    # --- Top-level rule: Program ---
    def parse_program(self) -> Program:
        program = Program(definitions=[])
        self.skip_newlines()
        while self.current_token.type == TokenType.AT:
            program.definitions.append(self.parse_block_definition())
            self.skip_newlines() # Allow blank lines between definitions
        if self.current_token.type != TokenType.EOF:
            self.error("Expected Block Definition starting with '@' or End of File.")
        return program

    # --- Parse a Block Definition ---
    def parse_block_definition(self) -> BlockDefinition:
        self.consume(TokenType.AT)
        name_token = self.consume(TokenType.IDENTIFIER)
        name_node = IdentifierNode(name=name_token.lexeme) # Use IdentifierNode

        parameters: List[ParameterNode] = []
        if self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            while self.current_token.type != TokenType.RPAREN:
                param_name_token = self.consume(TokenType.IDENTIFIER)
                # TODO: Add type parsing (e.g., ': int')
                parameters.append(ParameterNode(name=param_name_token.lexeme, param_type="int"))
                if self.current_token.type == TokenType.COMMA:
                    self.consume(TokenType.COMMA)
                elif self.current_token.type != TokenType.RPAREN:
                    self.error("Expected ',' or ')' in parameter list")
            self.consume(TokenType.RPAREN)

        self.consume(TokenType.COLON)
        if self.current_token.type != TokenType.NEWLINE:
            self.error("Expected NEWLINE after block definition colon ':'")
        self.consume(TokenType.NEWLINE)

        body: List[StatementNode] = []
        # Handle indented block
        if self.current_token.type == TokenType.INDENT: # <--- 首先检查是否有缩进
            self.consume(TokenType.INDENT)

            if self.current_token.type == TokenType.DEDENT:
                    self.error("Block body cannot be empty. Add statements after indentation.")

            # 循环解析语句，直到 DEDENT 或 EOF
            while self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
                    statement = self.parse_statement()
                    if statement: # 确保 parse_statement 返回有效节点
                            body.append(statement)
                    # else: 错误情况应该由 parse_statement 内部处理或在循环外检测

            # 循环结束后，检查是如何结束的
            if self.current_token.type == TokenType.DEDENT:
                self.consume(TokenType.DEDENT) # 正常结束，消耗 DEDENT
                # --- 新增：检查 body 是否为空（虽然上面的检查可能已经覆盖）---
                if not body:
                        # 如果能到这里，意味着 INDENT 后面可能有非语句内容或解析器逻辑问题
                        self.error("Internal Error: Block body parsed as empty despite initial check.")
                # --- 结束新增检查 ---
            elif self.current_token.type == TokenType.EOF:
                    # 在块内到达文件末尾，通常意味着缺少 DEDENT
                    self.error("Unexpected EOF inside indented block. Missing DEDENT?")
            else:
                    # 如果不是 DEDENT 也不是 EOF，可能是内部解析错误或未预料的 Token
                    self.error(f"Internal Error: Expected DEDENT or EOF after block body, got {self.current_token.type}")

        # --- 如果根本就没有 INDENT ---
        else: # self.current_token.type != TokenType.INDENT
                # 在 ':' 和 NEWLINE 之后，必须有 INDENT
                self.error("Expected indented block body after '@name:' definition.")

        # 最终创建 BlockDefinition
        # 此时 body 应该是非空的，因为空块情况已在上面报错
        return BlockDefinition(name=name_node.name, parameters=parameters, body=body)

    # --- Statement Parser (Dispatcher) ---
    def parse_statement(self) -> StatementNode:
        """Parses a single statement based on the current token."""
        token_type = self.current_token.type

        # Skip leading newlines before a statement (allows blank lines in body)
        self.skip_newlines()
        token_type = self.current_token.type # Re-read type after skipping

        statement: StatementNode

        if token_type == TokenType.KEYWORD_RETURN:
            statement = self.parse_return_statement()
        elif token_type == TokenType.KEYWORD_INT:
            statement = self.parse_variable_declaration()
        elif token_type == TokenType.KEYWORD_IF:
            statement = self.parse_if_statement()
        elif token_type == TokenType.KEYWORD_GOTO:
                statement = self.parse_goto_statement()
        elif token_type == TokenType.IDENTIFIER:
            statement = self.parse_assignment_or_call_or_label_statement()
        elif token_type == TokenType.KEYWORD_PRINT: # Example: Handle print directly
                statement = self.parse_print_statement() # Need to implement this
        elif token_type == TokenType.EOF:
            self.error("Unexpected EOF while parsing statement.")
        else:
            self.error(f"Unexpected token type at start of statement: {token_type}")

        return statement


    # --- Specific Statement Parsers ---
    def parse_return_statement(self) -> ReturnNode:
        self.consume(TokenType.KEYWORD_RETURN)
        value_expr = None
        # Check if a value follows 'return' before the newline
        if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.EOF and self.current_token.type != TokenType.DEDENT:
            value_expr = self.parse_expression()
        # Return statement should be followed by newline or end of block/file
        if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
            self.error("Expected NEWLINE or end of block after return statement")
        if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE) # Consume if present
        return ReturnNode(value=value_expr)

    def parse_variable_declaration(self) -> VarDeclNode:
        self.consume(TokenType.KEYWORD_INT)
        var_name_token = self.consume(TokenType.IDENTIFIER)
        var_name_node = IdentifierNode(name=var_name_token.lexeme)
        initializer_expr = None
        if self.current_token.type == TokenType.OPERATOR_ASSIGN:
            self.consume(TokenType.OPERATOR_ASSIGN)
            initializer_expr = self.parse_expression()
        if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
            self.error("Expected NEWLINE or end of block after variable declaration")
        if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE)
        return VarDeclNode(var_name=var_name_node, var_type="int", initializer=initializer_expr)

    def parse_if_statement(self) -> IfNode:
        self.consume(TokenType.KEYWORD_IF)
        condition = self.parse_expression()
        self.consume(TokenType.COLON)
        if self.current_token.type != TokenType.NEWLINE: self.error("Expected NEWLINE after 'if condition:'")
        self.consume(TokenType.NEWLINE)

        # Parse 'then' block (indented)
        if self.current_token.type != TokenType.INDENT: self.error("Expected indented block after 'if'")
        self.consume(TokenType.INDENT)
        then_body: List[StatementNode] = []
        while self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
            then_body.append(self.parse_statement())
        if self.current_token.type != TokenType.DEDENT: self.error("Expected DEDENT to close 'if' block body")
        self.consume(TokenType.DEDENT)

        # Parse optional 'else' block
        else_body: Optional[List[StatementNode]] = None
        # Need to check token AFTER potential newline following DEDENT
        self.skip_newlines() # Skip any blank lines between if and else
        if self.current_token.type == TokenType.KEYWORD_ELSE:
            self.consume(TokenType.KEYWORD_ELSE)
            self.consume(TokenType.COLON)
            if self.current_token.type != TokenType.NEWLINE: self.error("Expected NEWLINE after 'else:'")
            self.consume(TokenType.NEWLINE)

            if self.current_token.type != TokenType.INDENT: self.error("Expected indented block after 'else'")
            self.consume(TokenType.INDENT)
            else_body = []
            while self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
                else_body.append(self.parse_statement())
            if self.current_token.type != TokenType.DEDENT: self.error("Expected DEDENT to close 'else' block body")
            self.consume(TokenType.DEDENT)

        return IfNode(condition=condition, then_body=then_body, else_body=else_body)

    def parse_goto_statement(self) -> GotoNode:
        self.consume(TokenType.KEYWORD_GOTO)
        label_token = self.consume(TokenType.IDENTIFIER)
        label_node = IdentifierNode(name=label_token.lexeme)
        if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
            self.error("Expected NEWLINE or end of block after goto statement")
        if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE)
        return GotoNode(target_label=label_node)

    def parse_assignment_or_call_or_label_statement(self) -> StatementNode:
        """Handles lines starting with an IDENTIFIER."""
        name_token = self.consume(TokenType.IDENTIFIER)
        name_node = IdentifierNode(name=name_token.lexeme)

        if self.current_token.type == TokenType.OPERATOR_ASSIGN:
            # Assignment: IDENTIFIER = expression
            self.consume(TokenType.OPERATOR_ASSIGN)
            value_expr = self.parse_expression()
            if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
                 self.error("Expected NEWLINE or end of block after assignment statement")
            if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE)
            return AssignmentNode(target=name_node, value=value_expr)

        elif self.current_token.type == TokenType.LPAREN:
            call_expr = self._parse_call_expression_suffix(callee_node=name_node)
            if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
                self.error("Expected NEWLINE or end of block after call statement")
            if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE)
            # Decide AST node type. CallStatementNode seems appropriate.
            return CallStatementNode(call_expression=call_expr)

        elif self.current_token.type == TokenType.COLON:
            # Label definition: IDENTIFIER :
            self.consume(TokenType.COLON)
            if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
                self.error("Expected NEWLINE or end of block after label definition")
            if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE)
            # Ensure LabelNode is defined in claw_ast.py
            return LabelNode(label_name=name_node)
        else:
            self.error(f"Expected '=', '(', or ':' after identifier '{name_token.lexeme}', but got {self.current_token.type}")

    def parse_print_statement(self) -> ExpressionStatementNode:
        # Example for a built-in like 'print expression'
        print_token = self.consume(TokenType.KEYWORD_PRINT)
        # Assume print takes one argument for now
        argument = self.parse_expression() # Parse the expression to print
        # Create a 'call' expression node for print
        print_call = CallExpressionNode(
            callee_name=IdentifierNode(name=print_token.lexeme),
            arguments=[argument]
        )
        if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT and self.current_token.type != TokenType.EOF:
            self.error("Expected NEWLINE or end of block after print statement")
        if self.current_token.type == TokenType.NEWLINE: self.consume(TokenType.NEWLINE)
        # Wrap the call in an ExpressionStatementNode
        return ExpressionStatementNode(expression=print_call)


    # --- Expression Parsing (Recursive Descent with Precedence Climbing/Pratt) ---
    # This needs significant work. Starting with basic primary expressions.

    def parse_expression(self, min_precedence=0) -> ExpressionNode:
        """Parses an expression using precedence climbing."""
        unary_op_token = self.current_token
        unary_precedence = self._get_unary_operator_precedence(unary_op_token.type)

        if unary_precedence != -1 and unary_precedence >= min_precedence:
                # Consume the unary operator
                self.consume(unary_op_token.type)
                # Parse the operand with the unary operator's precedence
                operand = self.parse_expression(unary_precedence)
                left = UnaryOperationNode(operator=unary_op_token.lexeme, operand=operand)
        else:
                # If no unary operator, parse primary expression as before
                left = self.parse_primary_expression()

        # Precedence climbing loop
        while True:
            op_token = self.current_token
            precedence = self._get_binary_operator_precedence(op_token.type)

            if precedence == -1 or precedence < min_precedence:
                break

            self.consume(op_token.type)

            # Handle associativity (assuming left-associativity for now)
            right = self.parse_expression(precedence + 1)

            left = BinaryOperationNode(left=left, operator=op_token.lexeme, right=right)

        return left

    def parse_primary_expression(self) -> ExpressionNode:
        """Parses the most basic elements of an expression."""
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return ConstantNode(value=token.value)
        elif token.type == TokenType.STRING:
            self.consume(TokenType.STRING)
            return ConstantNode(value=token.value) # String literal is also a constant
        elif token.type == TokenType.IDENTIFIER:
            # Could be a variable or a function call
            self.consume(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.LPAREN:
                    # It's a function call - parse arguments
                    # We need the identifier node we just consumed
                    callee_node = IdentifierNode(name=token.lexeme)
                    return self._parse_call_expression_suffix(callee_node=callee_node)
            else:
                    # Just a variable identifier
                    return IdentifierNode(name=token.lexeme)
        elif token.type == TokenType.LPAREN:
            # Parenthesized expression
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression() # Parse expression inside parens
            self.consume(TokenType.RPAREN) # Expect closing parenthesis
            return expr
        else:
            self.error(f"Unexpected token in primary expression: {token.type}")
    
    def _get_unary_operator_precedence(self, token_type: TokenType) -> int:
        """Returns the precedence level for UNARY prefix operators."""
        if token_type == TokenType.OPERATOR_MINUS:
            return self.PREC_UNARY # Unary minus has high precedence
        # Add other unary operators like '!' here if needed
        else:
            return -1 # Not a recognized unary prefix operator

    def _get_binary_operator_precedence(self, token_type: TokenType) -> int:
        """Returns the precedence level for BINARY operators."""
        if token_type in (TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE):
            return self.PREC_PRODUCT
        elif token_type in (TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS):
            return self.PREC_SUM
        elif token_type in (TokenType.OPERATOR_GT, TokenType.OPERATOR_GE,
                            TokenType.OPERATOR_LT, TokenType.OPERATOR_LE,
                            TokenType.OPERATOR_EQ, TokenType.OPERATOR_NE):
             return self.PREC_COMPARISON
        else:
            return -1 # Not a recognized binary operator

    def _parse_call_expression_suffix(self, callee_node: Optional[IdentifierNode]=None) -> CallExpressionNode:
        """Helper to parse '( [args...] )' part of a call, assuming callee is known."""
        if callee_node is None: # If called from parse_call_statement
            callee_token = self.consume(TokenType.IDENTIFIER)
            callee_node = IdentifierNode(name=callee_token.lexeme)

        arguments: List[ExpressionNode] = []
        self.consume(TokenType.LPAREN)
        while self.current_token.type != TokenType.RPAREN:
            arguments.append(self.parse_expression()) # Parse each argument expression
            if self.current_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            elif self.current_token.type != TokenType.RPAREN:
                self.error("Expected ',' or ')' in call arguments")
        self.consume(TokenType.RPAREN)
        return CallExpressionNode(callee_name=callee_node, arguments=arguments)

# --- Example Usage & Basic Test ---
if __name__ == "__main__":
    # Import Lexer here for testing purposes
    from claw_lexer import Lexer, LexerError


    # --- NEW Test Source with Unary Minus ---
    test_source = """
@main:
  int x = -10       # Test unary minus on constant
  int y = 5
  int z = x + y     # Test addition with negative number (-10 + 5 = -5)
  int w = -(x + z)  # Test unary minus on parenthesized expression -(-10 + -5) = -(-15) = 15
  int k = 10 * -y   # Test binary op with unary minus operand (10 * -5 = -50)

  print x           # Expected: -10
  print z           # Expected: -5
  print w           # Expected: 15
  print k           # Expected: -50

  if -y < 0:       # Test unary minus in condition
    print "y is positive, so -y is negative"
  else:
    print "This should not print"

  return 0
"""
    # --- End NEW Test Source ---

    print("--- Source Code ---")
    print(test_source)
    print("-------------------")

    lexer = Lexer(test_source)
    try:
        tokens = lexer.tokenizer()
        print("\n--- Tokens ---")
        # Optional: Print tokens (excluding newlines for brevity)
        for token in tokens:
             if token.type != TokenType.NEWLINE:
                  print(token)
        print("--------------")



        parser = Parser(tokens)
        ast_tree = parser.parse()

        print("\n--- AST ---")
        # Nicer AST printing helper (remains the same)
        def print_ast_nice(node, indent=0):
            indent_str = "  " * indent
            node_type = type(node).__name__
            fields = []
            if hasattr(node, '__dataclass_fields__'):
                for name, field_info in node.__dataclass_fields__.items():
                    value = getattr(node, name)
                    if isinstance(value, ASTNode):
                        fields.append(f"{name}=...") # Indicate nested node
                    elif isinstance(value, list) and value and isinstance(value[0], ASTNode):
                         fields.append(f"{name}=[...{len(value)} items...]") # Indicate list of nodes
                    elif value is not None:
                         fields.append(f"{name}={repr(value)}") # Show simple values
            print(f"{indent_str}- {node_type}({', '.join(fields)})")

            # Recursively print children
            if hasattr(node, '__dataclass_fields__'):
                for name, field_info in node.__dataclass_fields__.items():
                    value = getattr(node, name)
                    if isinstance(value, ASTNode):
                         print_ast_nice(value, indent + 1)
                    elif isinstance(value, list):
                         for item in value:
                             if isinstance(item, ASTNode):
                                 print_ast_nice(item, indent + 1)

        print_ast_nice(ast_tree)
        print("------------")
        print("\nParser ran successfully!")

    except (LexerError, ParserError) as e:
        print(f"\nCompilation failed:")
        print(e)
    except Exception as e:
        import traceback
        print(f"\nAn unexpected error occurred:")
        traceback.print_exc()