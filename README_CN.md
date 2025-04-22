# Eazy 语言与 Claw 编译器

## 项目概述 (Project Overview)

**Eazy** 是一种实验性、仍在开发中的编程语言，围绕“万物皆块”（Everything is a Block）的核心概念构建。它旨在提供一种新颖且可进行底层控制的编程范式，探索与传统结构化和面向对象编程不同的代码组织与控制流方法。

**Claw** 是 Eazy 语言的第一个编译器，目前处于早期开发阶段。其短期目标是将 Eazy 源代码编译（或转译）为 Python 代码，以便快速迭代和验证语言设计。长期目标是实现自编译，并能够编译适用于开发系统内核的底层代码。

本项目部分灵感来源于 C、Python 和汇编语言，并期望遵循 GNU 项目的精神，从零开始构建一个完整的生态系统（语言、编译器、内核、Shell 等），尽管目前尚处于非常初期的探索阶段。

## 当前状态 (Current Status)

本项目目前处于**早期开发阶段**。一个**基础的编译流程**，能够将**当前支持的 Eazy 语言特性**翻译成可运行的 Python 代码，已经**建立并通过了测试验证**。

已完成的工作包括：

* **词法分析器 (Lexer):** 能够将 Eazy 源代码分解为 Token 序列（包括 `@`, `:`, `goto`, `back`, `int`, 标识符, 数字, 基本运算符, 以及括号 `( ) ,`）。
* **语法分析器 (Parser V1 - 已增强):** 能够识别带可选参数的顶层块定义 (`@name(p1, p2):`)、带可选参数的 `goto` 语句 (`goto name(a1, 5)`)、带可选多个返回值的 `back` 语句 (`back r1, r2`) 以及通用的行块。它能构建反映这些结构的抽象语法树 (AST)。变量声明 (`int`) 目前会被跳过（在生成的代码中转为注释）。
* **代码生成器 (Code Generator V1 - 已增强):** 已实现将增强后的 AST 翻译为可执行的 Python 3 代码。每个 Eazy 块被翻译成带相应参数的 Python 函数。`goto` 变为赋值给临时变量 `_tmp_return` 的 Python 函数调用。`back` 变为 Python 的 `return` 语句（返回单个值或包含多个值的元组）。编译器现在以 Eazy 源文件 (`.ez`) 作为输入，并输出一个 Python 文件 (`.py`)。
* **V1 返回值模拟:** 请注意，V1 代码生成器使用一个临时变量 (`_tmp_return`) 来捕获 `goto` 调用（即 Python 函数调用）的结果。为了在**当前 V1 转译出的 Python 输出**中使用返回值，后续的 Eazy 代码需要引用这个 `_tmp_return` 变量（如果返回多个值，可能还需要解包）来访问结果，而不是直接使用 `back` 语句中的变量名。这是 V1 的一个变通方法，因为 Eazy 目标中的“值注入”语义与 Python 的标准函数返回机制不同。

## 重要限制 (Important Limitation)

请注意，当前的 V1 代码生成器将 Eazy 中的 `goto block_name(...)` 直接翻译为 Python 中的函数调用 (`_tmp_return = block_name(...)`)。这意味着简单的 Eazy 结构，例如 `@a: goto b` 紧随 `@b: goto a`，在生成的 Python 代码执行时仍然会导致无限递归，并最终引发栈溢出错误 (stack overflow error)。

此外，如“当前状态”部分所述，V1 代码生成器对返回值的处理是一种**模拟**。它将 `goto block(...)` 翻译为 `_tmp_return = block(...)`，将 `back val1, val2` 翻译为 `return val1, val2`。调用 `goto` 的 Eazy 代码必须显式使用 `_tmp_return` 变量（并可能解包）来访问结果。这与目标的 Eazy 语义（即返回的变量按名称在调用者作用域中直接可用）不同。这种独特的语义以及复杂的控制流，将需要一个超越当前 V1 Python 转译器的更高级的后端。

规划中的 Eazy 语言执行模型将包含更复杂的控制流管理机制（例如规划中的“流”和“权级”系统）来防止或正确处理此类不受控制的跳转，并实现预期的返回值语义，但这些机制尚未在当前的 Claw 编译器 V1 中实现。

## 核心概念（当前设计）(Core Concepts - Current Design)

* **万物皆块 (Everything is a Block):** 代码组织的基本单元是块。
* **命名块 (`@name:` 或 `@name(...)`):** 带名称的顶层块定义。可以（可选地）定义参数。
* **参数 (Parameters):** 块可以通过 `@name(param1, param2):` 定义命名参数，以接收通过 `goto` 调用传入的值。
* **参数 (Arguments):** `goto` 语句可以通过 `goto name(arg1, 5)` 将参数传递给目标块的参数。
* **返回值 (Return Values):** `back` 语句可以返回零个 (`back`)、一个 (`back result`) 或多个值 (`back val1, val2`) 给调用者上下文。（V1 通过 Python 的 `return` 模拟，并需要调用者使用 `_tmp_return` 来适配）。
* **块间控制流 (Inter-Block Control Flow):** 主要通过 `goto` (带参数) 和 `back` (带返回值) 指令实现块之间的跳转和返回。
* **行块 (Line Blocks):** 块内的单行操作，如赋值、打印语句、控制流指令等。（目前解析为 `GenericLineBlock`）。

*(注意：这些概念，特别是关于返回值、控制流等执行语义，随着语言设计和编译器后端 V1 之后的进展，可能会演变)*

## 如何构建和运行（当前）(How to Build and Run - Current)

本项目需要 Python 3.6 或更高版本来运行当前的编译器可执行文件。

1.  克隆仓库：
    ```bash
    # Clone the repository from GitHub
    git clone https://github.com/Karesis/Eazy.git
    # Change directory into the cloned project
    cd Eazy
    ```
2.  确保您位于项目的根目录。
3.  编译器可执行文件 (`claw_code_generator.py`)、词法分析器和语法分析器模块位于 `claw-compiler/` 目录下。示例 Eazy 源文件位于 `claw-compiler/samples/`。
4.  **将 Eazy 源文件编译为 Python 文件：**
    将 `claw_code_generator.py` 作为命令行工具使用。
    ```bash
    # 使用输入 Eazy 文件运行代码生成器脚本
    # 使用 -o 指定输出 Python 文件
    python claw-compiler/claw_code_generator.py claw-compiler/samples/your_test.ez -o claw-compiler/samples/your_test.py

    # 或使用默认输出名称（输入文件名加 .py 后缀）
    python claw-compiler/claw_code_generator.py claw-compiler/samples/your_test.ez
    # 这将在与输入文件相同的目录下生成 your_test.py。
    ```
    将 `your_test.ez` 替换为您的 Eazy 源文件的路径。`-o` 标志是可选的，用于指定输出文件路径。
5.  **运行生成的 Python 代码：**
    使用 Python 解释器直接执行生成的 `.py` 文件。
    ```bash
    # 执行生成的 Python 脚本
    python claw-compiler/samples/your_test.py
    ```
    您应该能看到 Eazy 程序执行的输出（请注意 V1 的限制）。

## 示例 (Examples)

### 示例：参数与返回值 (`parameter_test.ez`)

下面是一个演示参数、参数和返回值（包括必要的 V1 返回值适配）的示例。

```eazy
# file: parameter_test.ez
# 演示参数、参数和返回值

@add(x, y):       # 带参数的块
    int sum
    sum = x + y    # 基本操作
    print sum
    back sum        # 返回单个值

@process(data, factor): # 另一个带参数的块
    int processed
    int desc
    processed = data * factor
    # 注意：字符串字面量 V1 暂不支持
    # 这里用整数赋值作为演示
    desc = 101 # 代表 "processed_data" 概念的占位符
    back processed, desc # 返回多个值

@helper():         # 带空参数列表的块
    print "Helper called"
    back            # 无返回值

@main:             # 入口块
    int a = 10      # 声明并初始化
    int result = 0
    int desc_val = 0 # 用于保存描述值的变量
    # V1 变通需要：声明用于多返回值解包的临时变量 (如果 Eazy V1 不直接支持解包)
    int temp_p
    int temp_d

    goto add(a, 5)      # 调用 add
    # V1: 必须使用 _tmp_return 获取 'sum' 的值
    result = _tmp_return
    print result        # 预期输出: 15

    goto process(result, a) # 调用 process
    # V1: 必须使用 _tmp_return (一个元组) 获取 'processed', 'desc' 的值
    # 需要 Eazy 语法或分步赋值来解包
    # 假设 Eazy V1 需要分步或有特定解包语法:
    temp_p, temp_d = _tmp_return # 假设 Eazy 能将元组解包给临时变量
    result = temp_p              # 从临时变量赋值
    desc_val = temp_d            # 从临时变量赋值
    print result        # 预期输出: 150 (15 * 10)
    print desc_val      # 预期输出: 101

    goto helper()       # 调用 helper
    # helper 不返回值, _tmp_return 的值可能变为 None 或保持不变 (需规则定义)

    print "Main finished"
    back
```

这个示例展示了块如何定义和接收参数，以及 `goto` 如何传递参数。它也演示了 `back` 返回单个或多个值。**请注意：** 注释中强调了 Eazy 代码需要进行适配（使用 `_tmp_return` 和可能的解包）才能配合**当前 V1 Python 代码生成器的返回值模拟**正常工作。最终的 Eazy 语言旨在实现更直接的返回值访问方式。

## 未来计划（初步）(Future Plans - Preliminary)

* 逐步增强语法分析器，以处理更复杂的行块结构（表达式、变量作用域等）。
* **设计并实现“流”和“权级”概念，用于高级控制流和状态管理。**
* 设计并最终确定 Eazy 语言的完整规范，包括作用域、执行模型以及**预期的返回值机制**的精确规则。
* 开发语义分析器和可能的优化器。
* **改进代码生成器或开发新的后端**（例如，针对 C、LLVM 或自定义字节码虚拟机）以更好地支持 Eazy 的独特语义。
* 实现自编译能力。
* 开始基于 Eazy 语言开发 Neko 内核和 Nya Shell。

## 贡献 (Contribution)

本项目目前处于非常早期的个人探索阶段，暂时不接受外部贡献。但是，欢迎通过 GitHub Issues 或将来可能建立的其他渠道提出建议和讨论。

## 许可证 (License)

本项目根据 [MIT 许可证](https://github.com/Karesis/Eazy/blob/calculator/LICENSE) 授权。详情请参阅 `LICENSE` 文件。
