## Nyan 语言设计规范 (v0.2.1)

#### 1. 介绍与设计哲学

* **语言名称:** Nyan
* **编译器名称:** Claw
* **核心哲学:**
    * **简洁与强大:** 追求最小化的语法和最少的概念，同时提供现代系统级编程的全部力量。Nyan 拒绝一切不必要的语法符号（如语句末尾的`;`，`if/for`后的`:`，以及`{}`代码块）。
    * **安全与掌控:** 通过所有权系统、借用和`unsafe`边界，在保证内存安全的同时，给与程序员最终的控制权。
    * **元信息即类型:** 将`type`, `name`, `err`等元信息提升为语言的内置基础类型，形成独特且强大的元编程与内省能力。
    * **一致性:** 简单的规则贯穿整个语言。例如，下划线`_`前缀在任何地方都代表“私有”。

#### 2. 词法与核心语法

* **注释:** 使用 `//` 进行单行注释。

    ```nyan
    // 这是一个注释
    ```
* **缩进:** 严格使用**4个空格**作为一级缩进。缩进是定义代码块的唯一方式。
* **关键字:**
    * 定义: `@`, `trait`, `struct`, `extern`, `use`, `as`, `super`
    * 控制流: `if`, `elif`, `else`, `for`, `in`, `match`, `case`, `default`, `ret`
    * 并发: `spawn`, `chan`
    * 元信息与内存: `type`, `name`, `size`, `count`, `err`, `~`, `rel`, `unsafe`
* **操作符:**
    * 并发: `<-`
    * 错误处理: `?`
    * 访问: `.`, `::`
    * 指针: `&`, `*`
    * 其他标准算术与逻辑操作符。

#### 3. 类型与数据模型

Nyan 的类型系统分为两大类，这是其核心特性。

* **3.1. 数据类型 (Data Types)**
    * **原始类型:** `int`, `float`, `char`, `bool`等。
    * **声明语法:** `TypeName VariableName`

        ```nyan
        int my_number = 10
        bool is_cat = true
        ```
    * **指针类型:** 使用 `*` 后缀，如 `int*`。

* **3.2. 元信息类型 (Meta-Info Types)**
    这些是语言内置的、用于描述数据和状态的基础类型。

    * `type`: 代表一个类型本身。
        * **字面量:** `<TypeName>`
    * `name`: 代表一个标识符的名称。
        * **字面量:** `/identifier/`
    * `err`: 代表一个错误状态。
        * **构造器:** `Err(payload)`
        * **示例:** `e = Err("File not found")`
        * 所有err都有统一的type: <err>
    * `size`: 代表物理内存大小，其具体位数与目标机器架构相关。
    * `count`: 代表逻辑元素的数量。

* **3.3. 内置元信息操作符**
    用于从数据中提取元信息。

    * `type(expr)`: 获取表达式的类型。
    * `size(expr)`: 获取表达式类型占用的内存大小。
    * `count(expr)`: 获取复合类型（如 `@block` 实例）的成员数量。
    * `name(expr)`: 获取变量或定义的名称。
    ```nyan
    @Point(int x, int y)
        .x
        .y

    @main
        p = Point(10, 20)
        p_type = type(p)   // p_type 的值是 <Point>
        p_size = size(p)   // 结果是 2 * size(int)
        p_count = count(p) // 结果是 2
    ```

#### 4. `@block` 统一对象系统

`@block` 是 Nyan 中定义函数、类、方法等的唯一构造。

* **定义与实例化:**

    ```nyan
    // 定义一个 Point 类及其构造器
    @Point(int x, int y)
        .x // .x 将参数 x 绑定为公开数据成员
        .y

    @main
        // 实例化 Point，语法和函数调用一致
        p = Point(10, 20)
        print(p.x) // -> 10
    ```
* **方法与状态访问:**

    ```nyan
    @Counter(int initial_value)
        .count = initial_value // 也可以绑定一个可变的内部状态

        // 定义一个方法
        @increment()
            .count = .count + 1 // 使用 .count 访问和修改成员状态

    @main
        c = Counter(5)
        c.increment()
        print(c.count) // -> 6
    ```
* **私有性:** `_` 前缀的成员或方法是私有的。
* **无参调用:** 无参数的块或方法，调用时 `()` 可选。
* **继承:**

    ```nyan
    // Parent 是一个已定义的 @block
    @Child(int a, int b) : Parent
        super(a) // 调用父类的构造器
        .b = b   // 绑定自己的成员
    ```

#### 5. 内存与所有权模型

1.  **所有权:** 内存分配（如 `malloc` 的结果）归属于创建它的块。块跟踪的是**内存分配本身**。
2.  **自动释放:** 块结束时，自动释放其拥有的所有内存。
3.  **借用:** 默认情况下，向函数传递指针是**借用**，不转移所有权。
4.  **所有权转移 (`move`):**
    * `ret ptr`: 返回指针会转移所有权。
    * `~p` : 在函数调用中，显式将 `p` 的所有权移入函数。
    * 如果是结构体等，ret 和 ~都会将所有附带的所有权全部转移(所有权是深转移的)

#### 6. 错误处理与控制流

* **隐式双通道返回:** 任何 `@block` 的返回值都是一个隐式的 `T | err` 联合体。函数签名 `-> <T>` 只需声明成功类型。
* **错误传播 (`?`):**

    ```nyan
    @main
        // read_file 可能返回 str 或 err
        // 如果是 err，? 会让 @main 立即返回这个 err
        content = read_file("path")?
    ```
* **`match` 与类型模式:**

    ```nyan
    match read_file("path")
        case content
            print("成功: {content}")
        case e
            print("失败: {e.message}")
        default // 可选的默认分支
            print("发生了未知类型的错误")
    ```
    
    * 由于存在`type`类型，编译器会自行检查content( <str> )和 e ( <err> )

#### 7. 泛型与 Trait 系统

* **泛型定义:** `@Name<T, K>`
* **泛型实例化:** `Name<int, str>(arg1, arg2)`
* **Trait (契约定义):**

    ```nyan
    trait Comparable
        // 要求实现者必须支持 '>' 操作符
        @>(other) -> bool
    ```
* **Trait 实现:**

    ```nyan
    @MyNumber(int value) : Comparable
        .value
        @>(other: MyNumber) -> bool
            ret .value > other.value
    ```
* **泛型约束 (`where`):**

    ```nyan
    @sort<T>(List<T> list) where T : Comparable
    ```

#### 8. 并发模型

* **原语:** `spawn`, `chan`, `<-`
* **启动 Actor:** `spawn my_actor()`
* **通道声明与创建:** `chan my_chan: int`
* **通信:** `my_chan <- 42` (发送), `value = (<-my_chan)?` (接收)
* **生命周期:** 通道变量离开作用域时，通道被**自动关闭**。

#### 9. 模块化系统

* **规则:** 一文件一模块，`_` 前缀为私有。
* **`use` 语法:**

    ```nyan
    // 导入特定成员，并支持重命名和多行
    use my_lib::
        JSONParser as Parser,
        encode as to_json
    
    // 导入所有
    use my_other_lib::*
    ```

#### 10. 外部函数接口 (FFI)

* **`extern C` 块:** 用于声明C语言接口。
* **`struct` 定义:** 在 `extern C` 块内使用 `struct` 定义C兼容的内存布局。
* **`unsafe` 块:** 所有 FFI 调用都必须在 `unsafe` 块中。
* **`rel` 操作符:** 在 `unsafe` 块中，使用 `rel ptr` 来解除 Nyan 对指针的所有权管理，以便安全地传递给C。

    ```nyan
    extern C
        struct C_Point { int x; int y }
        draw(C_Point* p)

    @main
        p_nyan = Point(1, 2)
        p_c = C_Point(p_nyan.x, p_nyan.y)
        unsafe
            draw(&p_c)
    ```

#### 11. 标准库哲学

* **定位:** 提供一套精心策划的、跨领域通用的**核心工具集**，杜绝“重复劳动”，但不追求“大而全”。
* **核心模块 (提案):** `io`, `os`, `collections`, `math`, `string`, `error`。
* **实现方式:** 标准库将大量使用 Nyan 的高级特性（如 Trait 和泛型）来构建。例如，`io.print` 的实现将基于一个 `Display` trait。


