# Eazy Language and Claw Compiler

## Project Overview

**Eazy** is an experimental and developing programming language built around the core concept of "Everything is a Block". It aims to provide a novel and low-level controllable programming paradigm, exploring different approaches to code organization and control flow compared to traditional structured and object-oriented programming.

**Claw** is the first compiler for the Eazy language, currently in its early development stages. Its short-term goal is to compile (or transpile) Eazy source code into Python code for rapid iteration and language design validation. The long-term goal is to achieve self-compilation and be able to compile low-level code suitable for developing system kernels.

This project is partly inspired by C, Python, and Assembly languages, and aspires to follow the spirit of the GNU Project by building a complete ecosystem (language, compiler, kernel, shell, etc.) from the ground up, although it is currently in a very initial exploratory phase.

## Current Status

This project is currently in its **early development stage**. A basic compilation pipeline enabling the translation of currently supported Eazy language features into runnable Python code has been established and verified through testing.

Completed work includes:

* **Lexer:** Capable of breaking down Eazy source code into a sequence of Tokens (including `@`, `:`, `goto`, `back`, `int`, identifiers, numbers, basic operators, and parentheses `( ) ,`).
* **Parser (V1 - Enhanced):** Capable of identifying top-level block definitions with optional parameters (`@name(p1, p2):`), `goto` statements with optional arguments (`goto name(a1, 5)`), `back` statements with optional multiple return values (`back r1, r2`), and generic line blocks. It builds an Abstract Syntax Tree (AST) reflecting these structures. Variable declarations (`int`) are currently skipped (treated as comments in generated code).
* **Code Generator (V1 - Enhanced):** Implemented to translate the enhanced AST into executable Python 3 code. Each Eazy block becomes a Python function with corresponding parameters. `goto` becomes a Python function call assigned to a temporary variable `_tmp_return`. `back` becomes a Python `return` statement (returning single values or tuples for multiple values). The compiler takes an Eazy source file (`.ez`) as input and outputs a Python file (`.py`).
* **V1 Return Value Simulation:** Please note that the V1 Code Generator uses a temporary variable (`_tmp_return`) to capture the result of a `goto` call (which translates to a Python function call). To use the returned value(s) in the **current V1 transpiled Python output**, subsequent Eazy code needs to be written to reference this `_tmp_return` variable (and potentially unpack it if multiple values are returned) instead of directly using the variable names specified in the `back` statement. This is a V1 workaround necessary due to the difference between Eazy's intended "value injection" semantics and Python's standard function return mechanism.

## Important Limitation

Please note that the current V1 code generator translates Eazy's `goto block_name(...)` directly into a Python function call (`_tmp_return = block_name(...)`). This means simple Eazy structures creating direct mutual recursion (e.g., `@a: goto b` followed by `@b: goto a`) will result in infinite recursion and eventually cause a stack overflow error when the generated Python code is executed.

Additionally, the V1 code generator's handling of return values is a **simulation**, as described in the "Current Status" section. The Eazy code calling a `goto` must explicitly use the `_tmp_return` variable (potentially unpacking it) to access the results. This differs from the target Eazy semantic where returned variables are intended to become directly available by name in the caller's scope. This unique semantic, along with sophisticated control flow, will require a more advanced backend beyond the current V1 Python transpiler.

The planned Eazy language execution model will include more sophisticated control flow management mechanisms (e.g., the planned "Flow" and "Privilege" systems) to prevent or properly handle such uncontrolled jumps and implement the intended return value semantics, but these are not yet implemented in the current Claw compiler V1.

## Core Concepts (Current Design)

* **Everything is a Block:** The fundamental unit of code organization is a block.
* **Named Blocks (`@name:` or `@name(...)`):** Top-level block definitions with a name. Can optionally define parameters.
* **Parameters:** Blocks can define named parameters (`@name(param1, param2):`) to receive input values when called via `goto`.
* **Arguments:** `goto` statements can pass arguments (`goto name(arg1, 5)`) to the target block's parameters.
* **Return Values:** `back` statements can return zero (`back`), one (`back result`), or multiple values (`back val1, val2`) to the caller context. (V1 simulates this via Python's `return` and requires caller adaptation using `_tmp_return`).
* **Inter-Block Control Flow:** Primarily achieved through `goto` (with arguments) and `back` (with return values).
* **Line Blocks:** Single-line operations within a block, such as assignments, print statements, control flow instructions, etc. (Currently parsed as `GenericLineBlock`).

*(Note: These concepts, especially regarding execution semantics like return values and control flow, are subject to evolution as the language design and compiler backend progresses beyond V1.)*

## How to Build and Run (Current)

This project requires Python 3.6 or higher to run the current compiler executable.

1.  Clone the repository:
    ```bash
    # Clone the repository from GitHub
    git clone https://github.com/Karesis/Eazy.git
    # Change directory into the cloned project
    cd Eazy
    ```
2.  Ensure you are in the project's root directory.
3.  The compiler executable (`claw_code_generator.py`), Lexer, and Parser modules are located in the `claw-compiler/` directory. Example Eazy source files are in `claw-compiler/samples/`.
4.  **Compile an Eazy source file to Python:**
    Use `claw_code_generator.py` as a command-line tool.
    ```bash
    # Run the code generator script with the input Eazy file
    # Specify the output Python file using -o
    python claw-compiler/claw_code_generator.py claw-compiler/samples/your_test.ez -o claw-compiler/samples/your_test.py

    # Or use the default output name (input filename with .py extension)
    python claw-compiler/claw_code_generator.py claw-compiler/samples/your_test.ez
    # This will generate your_test.py in the same directory as the input.
    ```
    Replace `your_test.ez` with the path to your Eazy source file. The `-o` flag is optional to specify the output file path.
5.  **Run the generated Python code:**
    Execute the generated `.py` file directly using the Python interpreter.
    ```bash
    # Execute the generated Python script
    python claw-compiler/samples/your_test.py
    ```
    You should see the output from the Eazy program's execution (keeping in mind the V1 limitations).

## Example: Parameters and Return Values

Here is an example demonstrating parameters, arguments, and return values (including the necessary V1 adaptation for using return values).

```eazy
# file: parameter_test.ez
# Demonstrates parameters, arguments, and return values

@add(x, y):       # Block with parameters
    int sum
    sum = x + y    # Basic operation
    print sum
    back sum        # Back with single return value

@process(data, factor): # Another block with params
    int processed
    int desc
    processed = data * factor
    # Note: String literals not yet supported by Lexer/Parser V1
    # Using an int assignment here for demonstration
    desc = 101 # Placeholder for "processed_data" concept
    back processed, desc # Back with multiple return values

@helper():         # Block with explicit empty parameters
    print "Helper called"
    back            # Back with no return value

@main:             # Entry point
    int a = 10      # Declare and initialize
    int result = 0
    int desc_val = 0 # Variable to hold description value
    # V1 Workaround: Declare temporary variables needed for multi-return unpacking
    int temp_p
    int temp_d

    goto add(a, 5)      # Call add
    # V1: Must use _tmp_return to get 'sum'
    result = _tmp_return
    print result        # Expected output: 15

    goto process(result, a) # Call process
    # V1: Must use _tmp_return (a tuple) to get 'processed', 'desc'
    # Need Eazy syntax or multi-step assignment to unpack.
    # Assuming a hypothetical multi-assignment syntax for Eazy V1 demo:
    temp_p, temp_d = _tmp_return # Assign tuple to temps
    result = temp_p              # Assign from temp
    desc_val = temp_d            # Assign from temp
    print result        # Expected output: 150 (15 * 10)
    print desc_val      # Expected output: 101

    goto helper()       # Call helper
    # _tmp_return might be None or unchanged after helper returns.
    # Eazy needs rules for handling calls that don't return values.

    print "Main finished"
    back
```

This example shows how blocks can define and receive parameters, and how `goto` passes arguments. It also demonstrates `back` returning single or multiple values. **Note:** The comments highlight where the Eazy code needs adaptation (using `_tmp_return` and potential unpacking) to work correctly with the **current V1 Python code generator's simulation** of return values. The final Eazy language aims for more direct access to returned values.

## Future Plans (Preliminary)

* Gradually enhance the Parser to handle more complex line block structures (expressions, proper variable scopes, etc.).
* Design and implement the "Flow" and "Privilege" concepts for advanced control flow and state management.
* Design and finalize the complete specification for the Eazy language, including precise rules for scope, execution model, and the intended return value mechanism.
* Develop a semantic analyzer and potentially an optimizer.
* Improve the Code Generator or develop new backends (e.g., targeting C, LLVM, or a custom bytecode VM) to better support Eazy's unique semantics.
* Achieve self-compilation capability.
* Begin development of the Neko kernel and Nya shell based on the Eazy language.

## Contribution

This project is currently in a very early personal exploration phase and is not accepting external contributions at this time. However, suggestions and discussions are welcome via GitHub Issues or other channels if established.

## License

This project is licensed under the [MIT License](https://github.com/Karesis/Eazy/blob/calculator/LICENSE). See the `LICENSE` file for details.
