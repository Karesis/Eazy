# Eazy Language and Claw Compiler

## Project Overview

**Eazy** is an experimental and developing programming language built around the core concept of "Everything is a Block". It aims to provide a novel and low-level controllable programming paradigm, exploring different approaches to code organization and control flow compared to traditional structured and object-oriented programming.

**Claw** is the first compiler for the Eazy language, currently in its early development stages. Its short-term goal is to compile (or transpile) Eazy source code into Python code for rapid iteration and language design validation. The long-term goal is to achieve self-compilation and be able to compile low-level code suitable for developing system kernels.

This project is partly inspired by C, Python, and Assembly languages, and aspires to follow the spirit of the GNU Project by building a complete ecosystem (language, compiler, kernel, shell, etc.) from the ground up, although it is currently in a very initial exploratory phase.

## Current Status

This project is currently in a **very early** stage of development.

Completed work includes:

*   **Lexer:** Capable of breaking down Eazy source code into a sequence of Tokens.
*   **Parser (V1):** Capable of identifying top-level block definitions (`@name:`) and basic inner blocks (`goto`, `back`, and generic line blocks), and building a preliminary Abstract Syntax Tree (AST). The current version of the Parser does not perform deep parsing of line blocks (like assignments, print statements) and treats them as generic lines. Variable declarations (`int`) are skipped in this version.

## Core Concepts (Current Understanding)

*   **Everything is a Block:** The fundamental unit of code organization is a block.
*   **Inter-Block Control Flow:** Primarily achieved through `goto` and `back` instructions for jumps and returns between blocks.
*   **Named Blocks (`@name:`):** Top-level block definitions with a name.
*   **Line Blocks:** Single-line operations within a block, such as assignments, print statements, control flow instructions, etc.

*(Note: These concepts are subject to evolution as the language design progresses)*

## How to Build and Run (Current)

This project requires Python 3.6 or higher to run the current compiler components.

1.  Clone the repository:
    ```bash
    git clone https://github.com/Karesis/Eazy.git
    cd Eazy
    ```
2.  Ensure you are in the project's root directory.
3.  The Lexer and Parser modules are located in the `claw-compiler/` directory.
4.  Run the Parser to test its ability to process the example code:
    ```bash
    python claw-compiler/claw_parser.py
    ```
    (This will execute the example code at the end of `claw_parser.py`, outputting the Token list and the parsed AST structure).

## Future Plans (Preliminary)

*   Implement a code generator to translate the AST into executable Python code.
*   Gradually enhance the Parser to handle more complex line block structures (expressions, function calls, etc.).
*   Design and finalize the complete specification for the Eazy language.
*   Develop a semantic analyzer and optimizer.
*   Achieve self-compilation capability.
*   Begin development of the Neko kernel and Nya shell.

## Contribution

This project is currently in a very early personal exploration phase and is not accepting external contributions at this time. However, suggestions and discussions are welcome.

## License

This project is licensed under the [MIT License](https://github.com/Karesis/Eazy/blob/calculator/LICENSE). See the `LICENSE` file for details.
