# clawc.py (Compiler Driver Script)
import argparse
import os
import sys

# Import necessary components from your claw-compiler package

from claw_lexer import Lexer
from claw_parser import Parser
# Import the new Assembly Generator
from claw_asm_generator import AssemblyGenerator

def main():
    # --- Command Line Argument Parsing ---
    parser = argparse.ArgumentParser(description="Claw Compiler for Eazy Language (ASM Backend)")
    parser.add_argument("input_file", help="Path to the input Eazy file (.ez)")
    parser.add_argument("-o", "--output", help="Path to the output assembly file (.s)", default=None)
    # Add other options later, e.g., --backend python/asm if you keep both

    args = parser.parse_args()

    input_filepath = args.input_file
    output_filepath = args.output

    # Determine output filepath if not specified
    if output_filepath is None:
        base_name = os.path.splitext(os.path.basename(input_filepath))[0]
        output_filepath = f"{base_name}.s" # Default output to .s in current dir

    # Ensure output directory exists (simple version: assumes output is in current dir or existing dir)
    output_dir = os.path.dirname(output_filepath)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error creating output directory '{output_dir}': {e}", file=sys.stderr)
            sys.exit(1)

    # --- Compilation Pipeline ---
    try:
        # 1. Read Source Code
        with open(input_filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # 2. Lexer
        lexer = Lexer(source_code)
        tokens = lexer.tokenizer()
        # Optional: Print tokens for debugging
        # print("--- Tokens ---")
        # for token in tokens: print(token)
        # print("--------------")

        # 3. Parser
        parser = Parser(tokens)
        ast_tree = parser.parse()
        # Optional: Print AST for debugging (you might need a pretty printer)
        # print("--- AST ---")
        # print(ast_tree) # Basic print, might not be very readable
        # print("-----------")

        # 4. Code Generation (Using Assembly Generator)
        asm_generator = AssemblyGenerator()
        assembly_code = asm_generator.generate_program(ast_tree)

        # 5. Write Output Assembly File
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(assembly_code)

        print(f"Compilation successful: {input_filepath} -> {output_filepath}")

    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filepath}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error during parsing: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during compilation: {e}", file=sys.stderr)
        # Optional: Print full traceback for debugging
        # import traceback
        # traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()