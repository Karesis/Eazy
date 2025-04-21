# Eazy Language and Claw Compiler

## Project Overview

**Eazy** is an experimental and developing programming language built around the core concept of "Everything is a Block". It aims to provide a novel and low-level controllable programming paradigm, exploring different approaches to code organization and control flow compared to traditional structured and object-oriented programming.

**Claw** is the first compiler for the Eazy language, currently in its early development stages. Its short-term goal is to compile (or transpile) Eazy source code into Python code for rapid iteration and language design validation. The long-term goal is to achieve self-compilation and be able to compile low-level code suitable for developing system kernels.

This project is partly inspired by C, Python, and Assembly languages, and aspires to follow the spirit of the GNU Project by building a complete ecosystem (language, compiler, kernel, shell, etc.) from the ground up, although it is currently in a very initial exploratory phase.

## Current Status

This project is currently in its **early development stage**. A **basic compilation pipeline** enabling the translation of **currently supported Eazy language features** into runnable Python code has been **established and verified through testing**.

Completed work includes:

* **Lexer:** Capable of breaking down Eazy source code into a sequence of Tokens.
* **Parser (V1):** Capable of identifying top-level block definitions (`@name:`) and basic inner blocks (`goto`, `back`, and generic line blocks), and building a preliminary Abstract Syntax Tree (AST). This version of the Parser treats most lines as generic line blocks without deep parsing (e.g., assignments, print arguments are not fully analyzed as expressions). Variable declarations (`int`) are currently skipped.
* **Code Generator (V1):** Implemented to translate the V1 AST into executable Python 3 code. Each Eazy block is translated into a Python function, `goto` calls the target function, and `back` becomes a `return` statement. The compiler now takes an Eazy source file (`.ez`) as input and outputs a Python file (`.py`).

**Important Limitation:**

Please note that the current V1 code generator translates Eazy's `goto block_name` directly into a Python function call (`block_name()`). This means simple Eazy structures, such as `@a: goto b` followed by `@b: goto a`, will result in infinite recursion and eventually cause a stack overflow error when the generated Python code is executed.

This is a known limitation of the current transpilation approach. The planned Eazy language execution model will include more sophisticated control flow management mechanisms (e.g., privilege-based jump control and state tracking) to prevent or properly handle such uncontrolled jumps, but these are not yet implemented in the current Claw compiler V1. Therefore, writing Eazy code that creates direct circular `goto` jumps should be avoided with the current V1 implementation.

## Core Concepts (Current Understanding)

* **Everything is a Block:** The fundamental unit of code organization is a block.
* **Inter-Block Control Flow:** Primarily achieved through `goto` and `back` instructions for jumps and returns between blocks.
* **Named Blocks (`@name:`):** Top-level block definitions with a name.
* **Line Blocks:** Single-line operations within a block, such as assignments, print statements, control flow instructions, etc.

*(Note: These concepts are subject to evolution as the language design progresses)*

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
    python claw-compiler/claw_code_generator.py claw-compiler/samples/my_program.ez -o claw-compiler/samples/my_program.py

    # Or use the default output name (input filename with .py extension)
    python claw-compiler/claw_code_generator.py claw-compiler/samples/my_program.ez
    # This will generate my_program.py in the same directory as the input.
    ```
    Replace `my_program.ez` with the path to your Eazy source file. The `-o` flag is optional to specify the output file path.
5.  **Run the generated Python code:**
    Execute the generated `.py` file directly using the Python interpreter.
    ```bash
    # Execute the generated Python script
    python claw-compiler/samples/my_program.py
    ```
    You should see the output from the Eazy program's execution.

## Examples

Here are a few simple examples demonstrating the current capabilities of the Eazy language and Claw compiler V1.

### Example 1: Simple Block Call (`my_program.ez`)

```eazy
@helper:
    print "This is the helper block"
    back

@main:               # <--- entry point for execution
    print "Starting main"
    goto helper      # Jump to the helper block
    print "Returned from helper"
    int result       # Declare variable (currently skipped by parser V1)
    result = 10 * 2  # Assignment (treated as generic line block)
    print result     # Print the result
    back             # Return from main, exiting the program

@another_block:
    print "This won't run unless called via goto"
    back
```

This example shows basic block definition, `goto`, `back`, and `print`.

### Example 2: A More Complex Flow (`a_little_complex.ez`)

```eazy
# --- Complex Eazy Example ---
# A simple program to simulate getting two numbers, calculating their sum,
# and printing the result. Demonstrates V1 limitations regarding scope.

@main:
    print "Program starting in main block."
    int num1     # Declare variable num1 (becomes comment in Python via V1)
    int num2     # Declare variable num2
    int sum_res  # Declare variable for the sum result

    # Initialize variables (In V1, these are local to the 'main' Python function)
    num1 = 0
    num2 = 0
    sum_res = 0

    print "Variables initialized."
    goto get_input  # Jump to the block for getting input

    # --- This part executes *after* get_input flow potentially returns ---
    # Note: In V1, 'num1' and 'num2' set in get_input won't be seen here
    # because Python functions have local scope. 'sum_res' from
    # calculate_sum also won't be accessible here for the same reason.
    # This highlights V1's scope limitations due to Python function mapping.
    print "Main: Returned from get_input flow (or subsequent returns)."
    print "Main: Values in main's scope are:"
    print num1 # Will print the initial value 0
    print num2 # Will print the initial value 0

    print "Program finished in main."
    back       # Return from main (ends the program execution)


@get_input:
    print "Entering get_input block."
    # Simulate getting input by assigning fixed values here.
    # These variables are local to the 'get_input' Python function in V1.
    int local_num1
    int local_num2
    local_num1 = 15
    local_num2 = 27
    print "Input received (simulated):"
    print local_num1
    print local_num2

    # Jump to calculate the sum. Cannot easily pass V1 local variables.
    # calculate_sum will have to define its own numbers for this demo.
    goto calculate_sum

    # This print statement might be unreachable if calculate_sum doesn't return
    # directly or indirectly back here. Python's call stack manages returns.
    print "get_input: Returned from calculate_sum."
    back           # Return from get_input (goes back to the caller, main in this path)


@calculate_sum:
    print "Entering calculate_sum block."
    # Since we can't easily access num1/num2 from get_input in V1's scope model,
    # define local values here for the calculation demonstration.
    int calc_a
    int calc_b
    int local_sum

    calc_a = 50 # Use different values for clarity
    calc_b = 30
    print "Calculating sum for:"
    print calc_a
    print calc_b

    local_sum = calc_a + calc_b # Perform the addition

    # Jump to print the result. Again, passing 'local_sum' is not directly
    # supported by the current V1 translation mechanism's scope handling.
    # print_result will print a value based on its own local context.
    goto print_result

    # This print statement is likely unreachable.
    print "calculate_sum: Returned from print_result."
    back             # Return from calculate_sum (goes back to the caller, get_input)


@print_result:
    print "Entering print_result block."
    # Cannot easily access 'local_sum' from calculate_sum in V1.
    # Print a fixed value or a value defined locally here.
    int final_result
    final_result = 80 # The expected sum from calculate_sum's local values (50+30)

    print "--- Calculation Result ---"
    print final_result
    print "--------------------------"

    # This is the end of this execution path initiated by the goto from calculate_sum.
    # 'back' returns control to the caller function in the Python call stack.
    # If calculate_sum called us, we return to calculate_sum's context.
    back             # Return from print_result (goes back to the caller, calculate_sum)
```

This example demonstrates a more complex flow involving multiple blocks and nested jumps/returns, highlighting the current scope limitations due to the Python function-based translation.

## Future Plans (Preliminary)

* Gradually enhance the Parser to handle more complex line block structures (expressions, function calls, variable scopes, etc.).
* Design and finalize the complete specification for the Eazy language, including proper scope and control flow rules.
* Develop a semantic analyzer and potentially an optimizer.
* Improve the Code Generator or develop new backends (e.g., targeting C or LLVM).
* Achieve self-compilation capability.
* Begin development of the Neko kernel and Nya shell based on the Eazy language.

## Contribution

This project is currently in a very early personal exploration phase and is not accepting external contributions at this time. However, suggestions and discussions are welcome via GitHub Issues or other channels if established.

## License

This project is licensed under the [MIT License](https://github.com/Karesis/Eazy/blob/calculator/LICENSE). See the `LICENSE` file for details.