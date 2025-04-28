# Eazy Language to C Translator

## Project Overview

**Eazy** is an experimental programming language designed around the core philosophy of "Everything is a Block". It aims to bridge the gap between high-level structured programming and low-level control by providing mechanisms for fine-grained operations while maintaining a block-based structure. The language specification can be found in [EazyLaw.md](./EazyLaw.md).

This project provides a translator that compiles Eazy source code (`.ezy`) into C code (`.c`). It serves as a reference implementation and a tool for experimenting with the Eazy language design.

## Core Concepts (Highlights from EazyLaw.md)

Eazy introduces several unique concepts:

* **Blocks (`@name:` or `@name(...)`):** The fundamental unit of code and scope. Blocks can define parameters.
* **Containers:** Abstract concept for data storage, from simple types (`int`, `char`) to structured instances (`struct`).
* **`image`:** Executes a block in an isolated context and captures its bound state (`.binding`) into a snapshot (implemented as a C struct).
* **`call`:** Directly executes a block, transferring control flow, and expects a single return value via the `ret` statement. Ignores bindings.
* **`struct`:** Directly declares and creates a *single instance* of a structured container on the *heap* (e.g., `struct point { int x, int y }`). Access members using `instance->member` in the generated C.
* **Bindings (`.name`):** Marks an internal container's value within a block to be included in snapshots created by `image`.
* **Labels & `goto`:** Provides basic intra-block control flow. `goto` is restricted to the same block and level.
* **Nested Blocks:** Allows defining blocks within other blocks, sharing the parent's scope but maintaining relative logical independence. Interaction primarily via `image` and `call`.
* **Path Calls (`call result parent.child(...)`):** A mechanism (currently planned/partially implemented in parser) to call nested blocks while establishing the necessary parent context.

Refer to [EazyLaw.md](./EazyLaw.md) for a complete and detailed explanation of the language features and semantics.

## Current Status

* **Translator:** Compiles Eazy source code to C.
* **Lexer (`leparser.py`):** Tokenizes Eazy source, handling keywords, identifiers, operators (including comparisons), literals, symbols, newlines, and indentation.
* **Parser (`leparser.py`):** Builds an Abstract Syntax Tree (AST) from the token stream, based on the Eazy grammar defined in `EazyLaw.md`. AST node definitions are in `eazy_ast.py`.
* **Code Generator (`generator.py`):** Traverses the AST and generates corresponding C code.
    * Maps Eazy blocks (`@name`) to C functions (`name` or `main`).
    * Implements `image` using C structs for snapshots and passing pointers.
    * Implements `call` using direct C function calls.
    * Allocates `struct` instances on the heap using `malloc`.
    * Handles basic variable declarations (`int`, `char`), `set`, `if`, `goto`, `print`, `exit`, `ret`.
    * Uses a symbol table (`SymbolTable`) for basic scope management and type information (e.g., distinguishing struct pointers from image snapshots for `.` vs `->`).
* **Main Script (`main.py`):** Orchestrates the lexing, parsing, and code generation process.

## Project Structure

.├── eazy_ast.py       # AST Node definitions├── EazyLaw.md        # Eazy language specification├── generator.py      # CodeGenerator and SymbolTable classes├── leparser.py       # Lexer and Parser classes├── LICENSE           # Project License├── main.py           # Main translator script└── README.md         # This file
## How to Run

This project requires Python 3 (tested with 3.x).

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <your-repo-url>
    cd Eazy
    ```
2.  **Ensure you have an Eazy source file (e.g., `example.ezy`).**
3.  **Run the translator using `main.py`:**
    ```bash
    # Translate example.ezy and print C code to console
    python main.py example.ezy

    # Translate example.ezy and save C code to output.c
    python main.py example.ezy -o output.c
    ```
4.  **Compile the generated C code:**
    Use a C compiler like GCC or Clang.
    ```bash
    gcc output.c -o executable_name -lm # Add -lm if using math functions

    # Or using Clang
    clang output.c -o executable_name -lm
    ```
5.  **Run the compiled executable:**
    ```bash
    ./executable_name
    ```

## Future Plans / Limitations

* **Semantic Analysis:** Implement a dedicated semantic analysis phase to perform more robust checks (type compatibility, scope resolution, `goto` target validation, `ret` type consistency) before code generation.
* **Type System:** Refine type handling in the generator based on semantic analysis results (e.g., for `printf` format specifiers, accurate struct/image member types).
* **Path Calls:** Fully implement the code generation logic for path calls (`parent.child`).
* **Memory Management:** Currently, heap-allocated `struct` instances are not explicitly `free`d. Implement a memory management strategy or rely on program termination for cleanup.
* **Error Reporting:** Improve the detail and user-friendliness of error messages during all phases.
* **Nested Block Context:** Ensure the context for nested blocks (shared scope access) is correctly handled in the generated C code, especially for `call`.

## License

This project is licensed under the [MIT License](./LICENSE).

