import sys
import os
import argparse # For command-line argument parsing
import textwrap # Helpful for managing indentation
from typing import Any
from claw_ast import Program, BlockDefinition, GenericLineBlock, GotoBlock, BackBlock, ASTNode, BlockContent
from claw_lexer import Lexer, TokenType
from claw_parser import Parser 


class CodeGenerator:
    """
    Generates target code (Python functions) from the Eazy AST (V1 Strategy).
    Finds the 'main' block for the entry point.
    Handles simple type declarations by commenting them out.
    """
    def __init__(self):
        # Stores the generated Python code for each block function
        self.generated_block_functions_code = []
        self.main_block_found = False # Flag to track if 'main' block exists

    def generate(self, ast_root: Program) -> str:
        """Starts the code generation process and assembles the final script."""
        # Reset state for potentially multiple generations with the same instance
        self.generated_block_functions_code = []
        self.main_block_found = False

        # Visit the root Program node to generate code for all blocks
        self.visit(ast_root)

        # Assemble the final Python script
        python_code_parts = [
            "# Generated Python code from Eazy language (Claw compiler V1)\n",
            f"# Source file: {getattr(ast_root, 'source_filename', 'unknown')}\n\n", # Add source filename if available
            "# Generated block functions:\n"
        ]

        # Add all generated function definitions
        for func_code in self.generated_block_functions_code:
            python_code_parts.append(func_code)
            python_code_parts.append("\n") # Add a blank line between functions

        # --- Add the entry point call ---
        # Logic now specifically looks for 'main' block
        if self.main_block_found:
            python_code_parts.append(f"# Entry point:\n")
            # Call the main function
            python_code_parts.append(f"main()\n")
        elif ast_root.block_definitions:
             # If no 'main' block was found, report error (or choose other fallback)
             print("Error: Entry point 'main' block not found in the source code.", file=sys.stderr)
             # Indicate failure - returning None or empty string could signal this
             # Or raise an exception if preferred
             return None # Signal generation failure
        else:
             # No blocks defined at all
             python_code_parts.append("# No blocks defined in the source code.\n")

        return "".join(python_code_parts)

    def visit(self, node: ASTNode) -> Any:
        """Dispatches the visitor based on the node type using getattr."""
        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name, self.visit_ASTNode)
        return visitor_method(node)

    def visit_ASTNode(self, node: ASTNode):
         """Fallback for unhandled AST node types."""
         raise NotImplementedError(f"Visitor method not implemented for node type: {type(node).__name__}")

    # --- Visitor methods for specific AST nodes ---

    def visit_Program(self, node: Program):
        """Visits all block definitions within the program."""
        # Store source filename in AST root if parser adds it, useful for header
        # setattr(node, 'source_filename', node.filename_if_parser_adds_it)
        for block_def in node.block_definitions:
            self.visit(block_def)

    def visit_BlockDefinition(self, node: BlockDefinition):
        """Generates a Python function for an Eazy block."""
        function_name = node.name
        # Check if this is the main block
        if function_name == "main":
            self.main_block_found = True

        # Start the function definition string
        function_code_lines = [f"def {function_name}():\n"]

        inner_lines = []
        # Visit each statement/instruction within the block
        for content_node in node.inner_content:
            line = self.visit(content_node)
            if line:
                inner_lines.append(line)

        # Handle empty blocks: add 'pass' if no content generated
        if not inner_lines:
             inner_lines.append("pass\n")

        # Indent the collected inner lines
        indented_inner_code = textwrap.indent("".join(inner_lines), "    ")
        function_code_lines.append(indented_inner_code)

        # Store the complete function code
        self.generated_block_functions_code.append("".join(function_code_lines))

    def visit_GenericLineBlock(self, node: GenericLineBlock) -> str:
        """Translates a generic line into a Python statement."""
        if not node.line_tokens:
            return ""

        first_token = node.line_tokens[0]

        # --- Handle Type Declarations (Example: "int a") ---
        # Add other Eazy type keywords as needed (e.g., KEYWORD_STRING)
        if first_token.type == TokenType.KEYWORD_INT and len(node.line_tokens) >= 2:
             identifier_name = node.line_tokens[1].lexeme
             # Convert to Python comment (Python 3 type hints are different)
             return f"# Eazy type hint: int {identifier_name}\n"

        # --- Handle Print Statements ---
        elif first_token.type == TokenType.KEYWORD_PRINT:
            if len(node.line_tokens) > 1:
                # Join arguments with spaces - V1 approximation
                args_str = " ".join(t.lexeme for t in node.line_tokens[1:])
                # Generate Python 3 print()
                return f"print({args_str})\n"
            else:
                return "print()\n" # print with no args

        # --- Handle Other Lines ---
        else:
            # Default: Join tokens with spaces. Assumes valid Python when spaced.
            python_line = " ".join(t.lexeme for t in node.line_tokens)
            return python_line + "\n"

    def visit_GotoBlock(self, node: GotoBlock) -> str:
        """Translates 'goto block' to a Python function call."""
        function_name = node.target_block_name
        return f"{function_name}()\n"

    def visit_BackBlock(self, node: BackBlock) -> str:
        """Translates 'back' to a Python 'return' statement."""
        return "return\n"

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