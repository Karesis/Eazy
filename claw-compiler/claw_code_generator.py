import sys
import os
import argparse
import textwrap
from typing import Any, List, Optional # Ensure Optional is imported if needed elsewhere

# Assuming claw_ast defines these correctly now
from claw_ast import Program, BlockDefinition, GenericLineBlock, GotoBlock, BackBlock, ASTNode, BlockContent
# Assuming claw_lexer defines Token and TokenType
from claw_lexer import Lexer, TokenType, Token # Added Token import
# Assuming claw_parser defines Parser
from claw_parser import Parser


class CodeGenerator:
    """
    Generates target code (Python functions) from the Eazy AST (V1 Strategy).
    Handles parameters, arguments, and basic return values.
    Finds the 'main' block for the entry point.
    """
    def __init__(self):
        self.generated_block_functions_code = []
        self.main_block_found = False

    def generate(self, ast_root: Program) -> Optional[str]: # Return Optional[str] to signal failure
        """Starts the code generation process and assembles the final script."""
        self.generated_block_functions_code = []
        self.main_block_found = False
        source_filename = getattr(ast_root, 'source_filename', 'unknown') # Get filename if attached by parser

        self.visit(ast_root)

        if not self.main_block_found and any(ast_root.block_definitions):
             print(f"Error: Entry point '@main:' block not found in '{source_filename}'.", file=sys.stderr)
             return None # Signal generation failure

        python_code_parts = [
            f"# Generated Python code from Eazy language (Claw compiler V1)\n",
            f"# Source file: {source_filename}\n\n",
            "# === Generated block functions ===\n"
        ]

        for func_code in self.generated_block_functions_code:
            python_code_parts.append(func_code)
            python_code_parts.append("\n")

        # --- Add the entry point call ---
        if self.main_block_found:
            python_code_parts.append(f"# === Entry point ===\n")
            python_code_parts.append(f"if __name__ == \"__main__\":\n") # Good practice for Python scripts
            python_code_parts.append(f"    main()\n")
        elif not ast_root.block_definitions:
            python_code_parts.append("# No blocks defined in the source code.\n")
        # else: Error already printed if main not found but blocks exist

        return "".join(python_code_parts)

    def visit(self, node: ASTNode) -> Any:
        """Dispatches the visitor based on the node type using getattr."""
        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name, self.visit_ASTNode)
        return visitor_method(node)

    def visit_ASTNode(self, node: ASTNode):
         """Fallback for unhandled AST node types."""
         # Provide more context in the error message
         raise NotImplementedError(f"Code Generation not implemented for AST node type: {type(node).__name__}")

    # --- Visitor methods for specific AST nodes ---

    def visit_Program(self, node: Program):
        """Visits all block definitions within the program."""
        for block_def in node.block_definitions:
            self.visit(block_def)

    def visit_BlockDefinition(self, node: BlockDefinition):
        """Generates a Python function for an Eazy block, including parameters."""
        function_name = node.name
        if function_name == "main":
            self.main_block_found = True

        # --- NEW: Handle parameters ---
        # Join parameter names (strings) with commas for the function signature
        params_str = ', '.join(node.parameters)
        function_signature = f"def {function_name}({params_str}):\n"
        # --- End NEW ---

        function_code_lines = [function_signature]
        inner_lines = []
        for content_node in node.inner_content:
            # Visit inner content nodes; result could be None, str, or list of strs
            result = self.visit(content_node)
            if isinstance(result, str):
                inner_lines.append(result)
            elif isinstance(result, list): # Handle cases returning multiple lines if needed
                 inner_lines.extend(result)
            # Ignore None results (e.g., from skipped nodes)

        if not inner_lines:
            inner_lines.append("pass\n")

        indented_inner_code = textwrap.indent("".join(inner_lines), "    ")
        function_code_lines.append(indented_inner_code)

        self.generated_block_functions_code.append("".join(function_code_lines))

    def visit_GenericLineBlock(self, node: GenericLineBlock) -> Optional[str]:
        """Translates a generic line into a Python statement."""
        if not node.line_tokens:
            return None # Skip empty lines effectively

        first_token = node.line_tokens[0]

        # --- Handle Type Declarations (Still comment out) ---
        if first_token.type == TokenType.KEYWORD_INT and len(node.line_tokens) >= 2:
            # Assuming second token is the identifier
            identifier_name = node.line_tokens[1].lexeme
            # Simple comment for V1
            return f"# Eazy type hint: int {identifier_name}\n"

        # --- Handle Print Statements (Keep as is) ---
        elif first_token.type == TokenType.KEYWORD_PRINT:
            # Rebuild the argument string from tokens after 'print'
            if len(node.line_tokens) > 1:
                # TODO: This simple join might not handle complex print arguments correctly later
                # For V1, join lexemes. Assumes arguments are simple identifiers/literals.
                args_str = " ".join(t.lexeme for t in node.line_tokens[1:])
                # Generate Python 3 print(). Needs careful handling of quotes if strings are added.
                # For now, assume no strings need explicit quoting.
                return f"print({args_str})\n"
            else:
                return "print()\n" # print with no args

        # --- Handle Other Lines (Assignments, etc.) ---
        else:
            # Default: Join tokens with spaces. Assumes valid Python when spaced.
            # TODO: This is a major simplification. Needs real expression parsing/generation later.
            python_line = " ".join(t.lexeme for t in node.line_tokens)
            return python_line + "\n"

    def visit_GotoBlock(self, node: GotoBlock) -> str:
        """Translates 'goto block(arg1, ...)' to a Python function call."""
        function_name = node.target_block_name
        # --- NEW: Handle arguments ---
        # Join argument token lexemes with commas for the function call
        # Assumes lexemes of IDENTIFIERs/NUMBERs are valid Python arguments
        args_str = ', '.join(arg.lexeme for arg in node.arguments)
        return f"_tmp_return = {function_name}({args_str})\n"
        # --- End NEW ---

    def visit_BackBlock(self, node: BackBlock) -> str:
        """
        Translates 'back [val1, val2, ...]' to a Python 'return' statement.
        V1 Limitation: This generates standard Python return, which does NOT
        match the Eazy semantic of injecting variables into the caller's scope.
        """
        # --- NEW: Handle return values ---
        if not node.return_values:
            # No return values -> return (implicitly None in Python)
            return "return\n"
        elif len(node.return_values) == 1:
            # Single return value -> return value_lexeme
            return f"return {node.return_values[0].lexeme}\n"
        else:
            # Multiple return values -> return val1_lexeme, val2_lexeme, ...
            # Python automatically packs these into a tuple.
            returns_str = ', '.join(val.lexeme for val in node.return_values)
            return f"return {returns_str}\n"


# --- Main execution block ---
if __name__ == "__main__":
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Compile Eazy (.ez) file to Python (.py).")
    parser.add_argument("input_file", help="Path to the input Eazy (.ez) file.")
    parser.add_argument("-o", "--output", help="Path to the output Python (.py) file. Defaults to input filename with .py extension.")
    # Add more arguments if needed (e.g., verbosity, optimization level)

    args = parser.parse_args()

    input_filepath = args.input_file
    output_filepath = args.output

    # Determine default output filepath if not specified
    if not output_filepath:
        base_name = os.path.splitext(input_filepath)[0]
        output_filepath = base_name + ".py"

    # --- Read Input File ---
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
            print(f"Read source from: {input_filepath}")
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Compilation Pipeline ---
    try:
        # 1. Lexing
        print("Lexing...")
        lexer = Lexer(source_code)
        tokens = list(lexer.tokenizer()) # Consume generator for parser

        # Optional: Print tokens for debugging
        # print("--- Tokens ---")
        # for token in tokens:
        #     print(token)
        # print("--------------")

        # 2. Parsing
        print("Parsing...")
        parser_instance = Parser(tokens)
        ast_tree = parser_instance.parse()
        # Optionally add filename to AST root if parser supports it
        setattr(ast_tree, 'source_filename', os.path.basename(input_filepath))

        # Optional: Print AST for debugging
        # print("\n--- AST ---")
        # from claw_parser import print_ast # Assuming a helper function
        # print_ast(ast_tree)
        # print("-----------")

        # 3. Code Generation
        print("Generating Code...")
        generator = CodeGenerator()
        generated_python_code = generator.generate(ast_tree)

        if generated_python_code is None:
            # Error occurred during generation (e.g., no main block)
            print("Code generation failed.", file=sys.stderr)
            sys.exit(1)

        # --- Write Output File ---
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(generated_python_code)
            print(f"Successfully generated Python code to: {output_filepath}")
        except Exception as e:
            print(f"Error writing output file '{output_filepath}': {e}", file=sys.stderr)
            sys.exit(1)

    except SyntaxError as e:
        # Catch parsing errors specifically if Parser raises them
        print(f"\nSyntax Error during parsing: {e}", file=sys.stderr)
        # Potentially add line/column info if the parser provides it
        sys.exit(1)
    except NotImplementedError as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("This might indicate an AST node type that the code generator doesn't handle yet.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch other potential errors (lexing, unexpected issues)
        import traceback
        print(f"\nAn unexpected error occurred during compilation: {type(e).__name__}: {e}", file=sys.stderr)
        # traceback.print_exc(file=sys.stderr) # Uncomment for detailed traceback
        sys.exit(1)