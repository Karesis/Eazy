# Eazy 语言与 Claw 编译器

## 项目概述 (Project Overview)

**Eazy** 是一种实验性、仍在开发中的编程语言，围绕“万物皆块”（Everything is a Block）的核心概念构建。它旨在提供一种新颖且可进行底层控制的编程范式，探索与传统结构化和面向对象编程不同的代码组织与控制流方法。

**Claw** 是 Eazy 语言的第一个编译器，目前处于早期开发阶段。其短期目标是将 Eazy 源代码编译（或转译）为 Python 代码，以便快速迭代和验证语言设计。长期目标是实现自编译，并能够编译适用于开发系统内核的底层代码。

本项目部分灵感来源于 C、Python 和汇编语言，并期望遵循 GNU 项目的精神，从零开始构建一个完整的生态系统（语言、编译器、内核、Shell 等），尽管目前尚处于非常初期的探索阶段。

## 当前状态 (Current Status)

本项目目前处于**早期开发阶段**。一个**基础的编译流程**，能够将**当前支持的 Eazy 语言特性**翻译成可运行的 Python 代码，已经**建立并通过了测试验证**。

已完成的工作包括：

* **词法分析器 (Lexer):** 能够将 Eazy 源代码分解为 Token 序列。
* **语法分析器 (Parser V1):** 能够识别顶层块定义 (`@name:`) 和基本的内部块（`goto`、`back` 以及通用的行块），并构建初步的抽象语法树 (AST)。此版本的解析器将大多数行视为通用行块，未进行深度解析（例如，赋值、打印参数未被完全分析为表达式）。变量声明 (`int`) 目前会被跳过。
* **代码生成器 (Code Generator V1):** 已实现将 V1 AST 翻译为可执行的 Python 3 代码。每个 Eazy 块被翻译成一个 Python 函数，`goto` 调用目标函数，`back` 变为 `return` 语句。编译器现在以 Eazy 源文件 (`.ez`) 作为输入，并输出一个 Python 文件 (`.py`)。

**重要限制 (Important Limitation):**

请注意，当前的 V1 代码生成器将 Eazy 中的 `goto block_name` 直接翻译为 Python 中的函数调用 (`block_name()`)。这意味着简单的 Eazy 结构，例如 `@a: goto b` 紧随 `@b: goto a`，在生成的 Python 代码执行时会导致无限递归，并最终引发栈溢出错误 (stack overflow error)。

这是当前转译 (transpilation) 方法的一个已知限制。规划中的 Eazy 语言执行模型将包含更复杂的控制流管理机制（例如基于权限的跳转控制和状态跟踪），以防止或正确处理此类不受控制的跳转，但这些机制尚未在当前的 Claw 编译器 V1 中实现。因此，在当前的 V1 实现下，需要避免编写会产生直接循环 `goto` 跳转的 Eazy 代码。

## 核心概念（当前理解）(Core Concepts - Current Understanding)

* **万物皆块 (Everything is a Block):** 代码组织的基本单元是块。
* **块间控制流 (Inter-Block Control Flow):** 主要通过 `goto` 和 `back` 指令实现块之间的跳转和返回。
* **命名块 (`@name:`):** 带有名称的顶层块定义。
* **行块 (Line Blocks):** 块内的单行操作，如赋值、打印语句、控制流指令等。

*(注意：随着语言设计的进展，这些概念可能会演变)*

## 如何构建和运行（当前）(How to Build and Run - Current)

本项目需要 Python 3.6 或更高版本来运行当前的编译器可执行文件。

1.  克隆仓库：
    ```bash
    # Clone the repository from GitHub
    git clone [https://github.com/Karesis/Eazy.git](https://github.com/Karesis/Eazy.git)
    # Change directory into the cloned project
    cd Eazy
    ```
2.  确保您位于项目的根目录。
3.  编译器可执行文件 (`claw_code_generator.py`)、词法分析器和语法分析器模块位于 `claw-compiler/` 目录下。示例 Eazy 源文件位于 `claw-compiler/samples/`。
4.  **将 Eazy 源文件编译为 Python 文件：**
    将 `claw_code_generator.py` 作为命令行工具使用。
    ```bash
    # Run the code generator script with the input Eazy file
    # Specify the output Python file using -o
    python claw-compiler/claw_code_generator.py claw-compiler/samples/my_program.ez -o claw-compiler/samples/my_program.py

    # Or use the default output name (input filename with .py extension)
    python claw-compiler/claw_code_generator.py claw-compiler/samples/my_program.ez
    # 这将在与输入文件相同的目录下生成 my_program.py。
    ```
    将 `my_program.ez` 替换为您的 Eazy 源文件的路径。`-o` 标志是可选的，用于指定输出文件路径。
5.  **运行生成的 Python 代码：**
    使用 Python 解释器直接执行生成的 `.py` 文件。
    ```bash
    # Execute the generated Python script
    python claw-compiler/samples/my_program.py
    ```
    您应该能看到 Eazy 程序执行的输出。

## 示例 (Examples)

这里有几个简单的示例，展示了 Eazy 语言和 Claw 编译器 V1 当前的功能。

### 示例 1: 简单的块调用 (`my_program.ez`)

```eazy
@helper:
    print "This is the helper block"
    back

@main:               # <--- entry point for execution (执行入口点)
    print "Starting main"
    goto helper      # Jump to the helper block (跳转到 helper 块)
    print "Returned from helper"
    int result       # Declare variable (currently skipped by parser V1) (声明变量，当前被 V1 解析器跳过)
    result = 10 * 2  # Assignment (treated as generic line block) (赋值，被视为通用行块)
    print result     # Print the result (打印结果)
    back             # Return from main, exiting the program (从 main 返回，退出程序)

@another_block:
    print "This won't run unless called via goto"
    back
```

此示例展示了基本的块定义、`goto`、`back` 和 `print`。

### 示例 2: 更复杂的流程 (`a_little_complex.ez`)

```eazy
# --- Complex Eazy Example ---
# A simple program to simulate getting two numbers, calculating their sum,
# and printing the result. Demonstrates V1 limitations regarding scope.
# (一个模拟获取两个数字、计算它们的和并打印结果的简单程序。演示 V1 在作用域方面的限制。)

@main:
    print "Program starting in main block."
    int num1     # Declare variable num1 (becomes comment in Python via V1) (声明变量 num1，在 V1 中转译为 Python 注释)
    int num2     # Declare variable num2
    int sum_res  # Declare variable for the sum result

    # Initialize variables (In V1, these are local to the 'main' Python function)
    # (初始化变量，在 V1 中，它们是 'main' Python 函数的局部变量)
    num1 = 0
    num2 = 0
    sum_res = 0

    print "Variables initialized."
    goto get_input  # Jump to the block for getting input (跳转到获取输入的块)

    # --- This part executes *after* get_input flow potentially returns ---
    # Note: In V1, 'num1' and 'num2' set in get_input won't be seen here
    # because Python functions have local scope. 'sum_res' from
    # calculate_sum also won't be accessible here for the same reason.
    # This highlights V1's scope limitations due to Python function mapping.
    # (--- 这部分在 get_input 流程可能返回后执行 ---)
    # (注意：在 V1 中，由于 Python 函数具有局部作用域，这里看不到在 get_input 中设置的 'num1' 和 'num2'。)
    # (出于同样原因，来自 calculate_sum 的 'sum_res' 在这里也无法访问。)
    # (这突显了由于 Python 函数映射导致的 V1 作用域限制。)
    print "Main: Returned from get_input flow (or subsequent returns)."
    print "Main: Values in main's scope are:"
    print num1 # Will print the initial value 0 (将打印初始值 0)
    print num2 # Will print the initial value 0 (将打印初始值 0)

    print "Program finished in main."
    back       # Return from main (ends the program execution) (从 main 返回，结束程序执行)


@get_input:
    print "Entering get_input block."
    # Simulate getting input by assigning fixed values here.
    # These variables are local to the 'get_input' Python function in V1.
    # (通过在此处赋固定值来模拟获取输入。)
    # (在 V1 中，这些变量是 'get_input' Python 函数的局部变量。)
    int local_num1
    int local_num2
    local_num1 = 15
    local_num2 = 27
    print "Input received (simulated):"
    print local_num1
    print local_num2

    # Jump to calculate the sum. Cannot easily pass V1 local variables.
    # calculate_sum will have to define its own numbers for this demo.
    # (跳转去计算总和。无法轻易传递 V1 的局部变量。)
    # (calculate_sum 将不得不为此演示定义自己的数字。)
    goto calculate_sum

    # This print statement might be unreachable if calculate_sum doesn't return
    # directly or indirectly back here. Python's call stack manages returns.
    # (如果 calculate_sum 不直接或间接返回到这里，这条打印语句可能无法到达。Python 的调用栈管理返回。)
    print "get_input: Returned from calculate_sum."
    back           # Return from get_input (goes back to the caller, main in this path) (从 get_input 返回，回到此路径中的调用者 main)


@calculate_sum:
    print "Entering calculate_sum block."
    # Since we can't easily access num1/num2 from get_input in V1's scope model,
    # define local values here for the calculation demonstration.
    # (由于在 V1 的作用域模型中无法轻易访问来自 get_input 的 num1/num2，)
    # (在此处定义局部值用于计算演示。)
    int calc_a
    int calc_b
    int local_sum

    calc_a = 50 # Use different values for clarity (使用不同的值以便区分)
    calc_b = 30
    print "Calculating sum for:"
    print calc_a
    print calc_b

    local_sum = calc_a + calc_b # Perform the addition (执行加法)

    # Jump to print the result. Again, passing 'local_sum' is not directly
    # supported by the current V1 translation mechanism's scope handling.
    # print_result will print a value based on its own local context.
    # (跳转去打印结果。同样，当前 V1 翻译机制的作用域处理不直接支持传递 'local_sum'。)
    # (print_result 将根据其自身的局部上下文打印一个值。)
    goto print_result

    # This print statement is likely unreachable. (这条打印语句很可能无法到达。)
    print "calculate_sum: Returned from print_result."
    back             # Return from calculate_sum (goes back to the caller, get_input) (从 calculate_sum 返回，回到调用者 get_input)


@print_result:
    print "Entering print_result block."
    # Cannot easily access 'local_sum' from calculate_sum in V1.
    # Print a fixed value or a value defined locally here.
    # (在 V1 中无法轻易访问来自 calculate_sum 的 'local_sum'。)
    # (打印一个固定值或在此处局部定义的值。)
    int final_result
    final_result = 80 # The expected sum from calculate_sum's local values (50+30) (来自 calculate_sum 局部变量的预期和)

    print "--- Calculation Result ---"
    print final_result
    print "--------------------------"

    # This is the end of this execution path initiated by the goto from calculate_sum.
    # 'back' returns control to the caller function in the Python call stack.
    # If calculate_sum called us, we return to calculate_sum's context.
    # (这是由来自 calculate_sum 的 goto 启动的执行路径的终点。)
    # ('back' 将控制权返回给 Python 调用栈中的调用函数。)
    # (如果 calculate_sum 调用了我们，我们将返回到 calculate_sum 的上下文。)
    back             # Return from print_result (goes back to the caller, calculate_sum) (从 print_result 返回，回到调用者 calculate_sum)
```

此示例演示了涉及多个块和嵌套跳转/返回的更复杂流程，并突出了由于基于 Python 函数的翻译而产生的当前作用域限制。

## 未来计划（初步）(Future Plans - Preliminary)

* 逐步增强语法分析器，以处理更复杂的行块结构（表达式、函数调用、变量作用域等）。
* 设计并最终确定 Eazy 语言的完整规范，包括适当的作用域和控制流规则。
* 开发语义分析器和可能的优化器。
* 改进代码生成器或开发新的后端（例如，针对 C 或 LLVM）。
* 实现自编译能力。
* 开始基于 Eazy 语言开发 Neko 内核和 Nya Shell。

## 贡献 (Contribution)

本项目目前处于非常早期的个人探索阶段，暂时不接受外部贡献。但是，欢迎通过 GitHub Issues 或将来可能建立的其他渠道提出建议和讨论。

## 许可证 (License)

本项目根据 [MIT 许可证](https://github.com/Karesis/Eazy/blob/calculator/LICENSE) 授权。详情请参阅 `LICENSE` 文件。