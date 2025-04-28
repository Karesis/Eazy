# main.py
# Main entry point for the Eazy language translator.
# Reads an Eazy source file, parses it, and generates C code.

import sys
import argparse # For handling command-line arguments

# Import the necessary components from other files
# Assuming leparser.py contains both Lexer and Parser
from leparser import Lexer, Parser
# Assuming generator.py contains the CodeGenerator
from generator import CodeGenerator

def main():
    """Main function to run the Eazy translator."""

    # Set up command-line argument parsing
    arg_parser = argparse.ArgumentParser(description="Translate Eazy code to C.")
    arg_parser.add_argument("input_file", help="Path to the Eazy source file (.ezy)")
    arg_parser.add_argument("-o", "--output", help="Path to the output C file (default: print to stdout)")
    # Add more arguments if needed (e.g., verbosity, optimization level)

    args = arg_parser.parse_args()

    input_filepath = args.input_file
    output_filepath = args.output

    # --- 1. Read Eazy Source Code ---
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            eazy_code = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # --- 2. Lexing ---
    print("--- Running Lexer ---", file=sys.stderr) # Progress message
    lexer = Lexer(eazy_code)
    try:
        tokens = lexer.tokenize()
        # Optional: Print tokens for debugging
        # print("--- Tokens ---")
        # for t in tokens: print(t)
        if not tokens or tokens[-1].type != 'EOF':
             print("Lexing error: Did not end with EOF or produced no tokens.", file=sys.stderr)
             # Check if any UNKNOWN tokens were generated
             unknown_tokens = [t for t in tokens if t.type == 'UNKNOWN']
             if unknown_tokens:
                 print(f"Unknown tokens found: {unknown_tokens}", file=sys.stderr)
             sys.exit(1)

    except Exception as e:
        print(f"An error occurred during lexing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # --- 3. Parsing ---
    print("--- Running Parser ---", file=sys.stderr) # Progress message
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        # Optional: Print AST for debugging
        # from leparser import print_ast # Assuming print_ast is in leparser
        # print("\n--- AST ---")
        # print_ast(ast)
    except SystemExit: # Catch sys.exit calls from parser errors
        print("Parsing failed due to syntax errors.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # --- 4. Code Generation ---
    print("--- Running Code Generator ---", file=sys.stderr) # Progress message
    generator = CodeGenerator()
    try:
        c_code = generator.generate(ast)
    except Exception as e:
        print(f"An error occurred during code generation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # --- 5. Output C Code ---
    if output_filepath:
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(c_code)
            print(f"--- C code successfully written to {output_filepath} ---", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output file '{output_filepath}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print separator before printing C code to stdout
        print("\n--- Generated C Code ---")
        print(c_code)

if __name__ == "__main__":
    main()

