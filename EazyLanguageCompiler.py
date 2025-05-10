import sys
import os
import subprocess
import argparse

from antlr4 import FileStream, CommonTokenStream

from llvmlite import ir
import llvmlite.binding as llvm

from EazyLepaser.EazyLanguageLexer import EazyLanguageLexer
from EazyLepaser.EazyLanguageParser import EazyLanguageParser
from EazyLepaser.EazyLanguageVisitor import EazyLanguageVisitor

class MyEazyTreeWalker(EazyLanguageVisitor):
    def __init__(self):
        super().__init__()
        self.module = ir.Module(name="eazy_module") # 1. 创建 LLVM 模块

        # --- 新增/修改代码开始 ---
        # 1. 初始化 LLVM 的目标信息 (非常重要！)
        llvm.initialize()
        llvm.initialize_native_target()   # 初始化本地目标
        llvm.initialize_native_asmprinter() # 初始化本地汇编打印机

        # 2. 获取当前机器的默认 target triple，并设置到模块上
        target_triple = llvm.get_default_triple()
        self.module.triple = target_triple

        # 3. (可选但推荐) 获取并设置与该 target triple 对应的 data layout
        #    Data layout 字符串告诉 LLVM 关于目标平台类型大小、对齐方式、字节序等信息
        target = llvm.Target.from_triple(target_triple)
        target_machine = target.create_target_machine()
        self.module.data_layout = str(target_machine.target_data)


        self.builder = None # IRBuilder 会在进入函数时创建
        self.current_function = None # 当前正在构建的函数
        
        self.named_values = {} 
        self.labels = {} # 存储标签名 -> BasicBlock 对象的映射

        void_ptr_type = ir.IntType(8).as_pointer()  # char* 类型 (i8*)
        printf_return_type = ir.IntType(32)         # printf 返回 int (i32)
        # printf 的第一个参数是格式化字符串 (char*)
        # var_arg=True 表示它是一个可变参数函数 (像 ... 那样)
        printf_func_type = ir.FunctionType(printf_return_type,
                                           [void_ptr_type],
                                           var_arg=True)
        # 在我们的模块中添加这个函数的声明
        self.printf_func = ir.Function(self.module, printf_func_type, name="printf")

        # 2. 准备 printf 要用的格式化字符串 "%d\n" 作为全局常量
        #    C 字符串需要以空字符 '\0' 结尾
        fmt_int_str_val = "%d\n\0"
        # 将 Python 字符串转换为字节数组
        c_fmt_int_str_bytes = bytearray(fmt_int_str_val.encode("utf8"))
        # 创建 LLVM 数组类型：[<length> x i8]
        fmt_int_str_type = ir.ArrayType(ir.IntType(8), len(c_fmt_int_str_bytes))
        # 创建该类型的常量
        c_fmt_int_str_llvm_const = ir.Constant(fmt_int_str_type, c_fmt_int_str_bytes)

        # 在模块中创建一个全局变量来存储这个格式化字符串常量
        self.global_fmt_int_str = ir.GlobalVariable(self.module,
                                                  c_fmt_int_str_llvm_const.type,
                                                  name=".str.int_format") # 给它一个名字
        self.global_fmt_int_str.linkage = 'internal' # 内部链接，只在本模块可见
        self.global_fmt_int_str.global_constant = True # 标记为常量
        self.global_fmt_int_str.initializer = c_fmt_int_str_llvm_const # 初始化它的值
        

    def visitProgram(self, ctx:EazyLanguageParser.ProgramContext):
        # 为整个 .ez 文件创建一个 main 函数作为入口
        main_func_type = ir.FunctionType(ir.IntType(32), [], False) # main 返回 i32，无参数
        self.current_function = ir.Function(self.module, main_func_type, name="main")
        
        # 创建入口基本块，并设置 builder
        entry_block = self.current_function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        
        # print("[LLVM Visitor] >>> Visiting Program, created main function")
        
        self.visitChildren(ctx) # 访问所有语句，它们会在 main 函数中生成指令

        # main 函数的结尾，所有路径都应有 ret 指令
        # 如果 builder 当前没有终结指令 (terminator)，则添加一个
        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0)) # main 函数返回 0
        
        # print("[LLVM Visitor] <<< Leaving Program")
        return None # Program 访问不直接返回值，结果在 self.module 中

    # 对于我们这个简单的 simplist.ez (print 1+2*3)，以下语句的visit方法
    # 如果没有被显式调用（因为simpllist.ez里没有这些语句），则不会执行。
    # 我们主要关注 printStatement 和表达式部分。

    def visitLabelDefinition(self, ctx:EazyLanguageParser.LabelDefinitionContext):
     label_name = ctx.ID().getText()
     # print(f"[LLVM Visitor] --- Defining label: {label_name}")

     # 检查这个标签是否因为前向跳转已经被创建了
     if label_name in self.labels:
         target_block = self.labels[label_name]
         # 如果块已经有终结指令了 (比如之前的块没有正确跳转到它)，可能需要处理
         # 但通常我们期望跳转指令会正确指向这个块
         if target_block.is_terminated: # 这种情况不应该发生如果之前的块正确跳转了
              # Could be an error or we might need to start a new block after it.
              # For simplicity, let's assume for now this doesn't happen with simple gotos.
              pass # Or log a warning
     else:
         # 如果标签是第一次遇到（不是前向跳转的目标），则为它创建一个新的基本块
         target_block = self.current_function.append_basic_block(name=label_name)
         self.labels[label_name] = target_block # 存储起来

     # 当前基本块（执行label定义之前的那个块）如果没有终结，应该无条件跳转到这个新定义的标签块
     if not self.builder.block.is_terminated:
         self.builder.branch(target_block)
     
     # 将 IRBuilder 的插入点移动到这个新（或已存在）的标签块的末尾
     self.builder.position_at_end(target_block)
     return None

    def visitBoxStatement(self, ctx:EazyLanguageParser.BoxStatementContext):
        var_name = ctx.ID().getText()
        # print(f"[LLVM Visitor] --- Declaring variable (box): {var_name}")
        # 在当前函数的入口块创建内存分配指令 (alloca)
        # alloca 指令通常放在函数的最开始，所以我们用一个临时 builder
        with self.builder.goto_entry_block(): # builder暂时跳到函数入口块的开头
            # 假设所有变量都是 i32 类型
            var_addr = self.builder.alloca(ir.IntType(32), name=var_name)
        self.named_values[var_name] = var_addr # 存储变量的内存地址
        
        # EazyLanguage 的 box int x; 语句不带初始赋值，所以这里不 store
        # 如果需要默认值0，可以在 alloca 后紧跟一个 store 常量0的操作
        # self.builder.store(ir.Constant(ir.IntType(32), 0), var_addr)
        return None

    def visitAssignStatement(self, ctx:EazyLanguageParser.AssignStatementContext):
        var_name = ctx.ID().getText()
        value_to_store = self.visit(ctx.commonExpression()) # 获取表达式的 LLVM Value

        if var_name in self.named_values:
            var_addr = self.named_values[var_name] # 获取变量的内存地址
            self.builder.store(value_to_store, var_addr) # 创建 store 指令
            # print(f"[LLVM Visitor] --- Assigned value to '{var_name}'")
        else:
            print(f"LLVM代码生成错误: 尝试赋值给未声明的变量 '{var_name}'")
            # 应该有错误处理机制
        return None

    def visitPrintStatement(self, ctx:EazyLanguageParser.PrintStatementContext):
        value_to_print_llvm = self.visit(ctx.commonExpression())
        fmt_ptr_for_printf = self.builder.bitcast(self.global_fmt_int_str, ir.IntType(8).as_pointer())
        self.builder.call(self.printf_func, [fmt_ptr_for_printf, value_to_print_llvm], name="printf_call")
        return None
        
    def visitIfGotoStatement(self, ctx:EazyLanguageParser.IfGotoStatementContext):
     condition_llvm_value = self.visit(ctx.commonExpression()) # 得到 i32 或 i1
     target_label_name = ctx.ID().getText()

     condition_i1 = None
     if condition_llvm_value.type == ir.IntType(32):
         zero_i32 = ir.Constant(ir.IntType(32), 0)
         condition_i1 = self.builder.icmp_signed('!=', condition_llvm_value, zero_i32, name="if_cond_bool")
     elif condition_llvm_value.type == ir.IntType(1):
         condition_i1 = condition_llvm_value
     else:
         # 错误处理
         print(f"LLVM代码生成错误: IF 条件的类型不是 i32 或 i1，而是 {condition_llvm_value.type}")
         return None

     # print(f"[LLVM Visitor] --- IF condition (i1): {condition_i1}, GOTO {target_label_name}")

     # 准备跳转目标基本块 (true_dest_block)
     true_dest_block = None
     if target_label_name in self.labels:
         true_dest_block = self.labels[target_label_name]
     else:
         # 标签在后面定义 (前向跳转)
         # 先为它创建一个基本块，并存起来，等 visitLabelDefinition 时再用
         true_dest_block = self.current_function.append_basic_block(name=target_label_name)
         self.labels[target_label_name] = true_dest_block
     
     # 创建 "else" 分支的基本块 (如果条件为假，程序继续顺序执行的地方)
     # 这个块是紧跟在 if 语句之后的代码应该在的地方
     else_block = self.current_function.append_basic_block(name=f"else_after_if_{target_label_name}")

     # 生成条件分支指令
     self.builder.cbranch(condition_i1, true_dest_block, else_block)

     # !! 重要：后续指令应该生成在 else_block 中 !!
     # 所以，我们将 builder 的插入点移动到 else_block 的末尾
     self.builder.position_at_end(else_block)
     return None

    # --- 表达式求值，返回 LLVM Value ---
    def visitCommonExpression(self, ctx:EazyLanguageParser.CommonExpressionContext):
        return self.visit(ctx.relationalExpression())

    def visitRelationalExpression(self, ctx:EazyLanguageParser.RelationalExpressionContext):
        left_llvm_val = self.visit(ctx.additiveExpression(0)) # 计算左操作数 (总是 i32)

        if ctx.getChildCount() > 1: # 意味着有比较操作符和右操作数
            op_node = ctx.getChild(1) # 操作符节点
            right_llvm_val = self.visit(ctx.additiveExpression(1)) # 计算右操作数 (总是 i32)
            op_type = op_node.symbol.type
            
            # 比较指令返回 i1 类型 (布尔)
            if op_type == EazyLanguageParser.ABOVE: # '>'
                return self.builder.icmp_signed('>', left_llvm_val, right_llvm_val, name="cmp_gt")
            elif op_type == EazyLanguageParser.UNDER: # '<'
                return self.builder.icmp_signed('<', left_llvm_val, right_llvm_val, name="cmp_lt")
            elif op_type == EazyLanguageParser.EQUAL: # '=='
                return self.builder.icmp_signed('==', left_llvm_val, right_llvm_val, name="cmp_eq")
        
        # 如果没有比较操作符 (例如 'print 1+2*3' 中的 '1+2*3')，
        # 就直接返回左边 (也是唯一一边) 算术表达式的 i32 值。
        return left_llvm_val

    def visitAdditiveExpression(self, ctx:EazyLanguageParser.AdditiveExpressionContext):
        left_llvm_val = self.visit(ctx.multiplicativeExpression(0))
        current_result_val = left_llvm_val

        num_ops = ctx.getChildCount() // 2
        for i in range(num_ops):
            op_node = ctx.getChild(i * 2 + 1)
            right_llvm_val = self.visit(ctx.getChild(i * 2 + 2))
            op_type = op_node.symbol.type

            if op_type == EazyLanguageParser.ADD:
                current_result_val = self.builder.add(current_result_val, right_llvm_val, name="add_tmp")
            elif op_type == EazyLanguageParser.SUB:
                current_result_val = self.builder.sub(current_result_val, right_llvm_val, name="sub_tmp")
        return current_result_val

    def visitMultiplicativeExpression(self, ctx:EazyLanguageParser.MultiplicativeExpressionContext):
        left_llvm_val = self.visit(ctx.primaryExpression(0))
        current_result_val = left_llvm_val

        num_ops = ctx.getChildCount() // 2
        for i in range(num_ops):
            op_node = ctx.getChild(i * 2 + 1)
            right_llvm_val = self.visit(ctx.getChild(i * 2 + 2))
            op_type = op_node.symbol.type

            if op_type == EazyLanguageParser.MUL:
                current_result_val = self.builder.mul(current_result_val, right_llvm_val, name="mul_tmp")
            elif op_type == EazyLanguageParser.DIV:
                # 对于除法，LLVM 有 sdiv (有符号) 和 udiv (无符号)
                # 我们假设是有符号除法
                current_result_val = self.builder.sdiv(current_result_val, right_llvm_val, name="div_tmp")
        return current_result_val

    def visitNumberAtom(self, ctx:EazyLanguageParser.NumberAtomContext):
        num_val = int(ctx.NUMBER().getText())
        return ir.Constant(ir.IntType(32), num_val) # 返回 LLVM 整数常量

    def visitIdAtom(self, ctx:EazyLanguageParser.IdAtomContext):
        var_name = ctx.ID().getText()
        if var_name in self.named_values:
            var_addr = self.named_values[var_name] # 获取变量地址 (AllocaInst)
            return self.builder.load(var_addr, name=var_name+"_val") # 从内存加载值
        else:
            print(f"LLVM代码生成错误: 使用了未声明的变量 '{var_name}'")
            # 应该有错误处理并返回一个合适的LLVM Value或抛异常
            # 暂时返回一个0常量
            return ir.Constant(ir.IntType(32), 0)


    def visitParensExpr(self, ctx:EazyLanguageParser.ParensExprContext):
        return self.visit(ctx.commonExpression()) # 返回括号内表达式的 LLVM Value

    def visitUnaryMinusExpr(self, ctx:EazyLanguageParser.UnaryMinusExprContext):
        # print(f"[LLVM Visitor] --- Visiting UnaryMinusExpr: - (...child...)")
        # ctx.primaryExpression() 是被取反的那个表达式的上下文
        # 我们先递归调用 visit 获取它对应的 LLVM Value
        value_to_negate = self.visit(ctx.primaryExpression()) 

        # 生成 LLVM 指令来实现取反 (通常是 0 - value)
        # 确保 value_to_negate 是我们期望的类型，比如 i32
        if value_to_negate.type == ir.IntType(32):
            zero = ir.Constant(ir.IntType(32), 0)
            return self.builder.sub(zero, value_to_negate, name="neg_tmp")
        else:
            # 错误处理或类型转换
            print(f"LLVM代码生成错误: 一元负号的操作数类型不是 i32，而是 {value_to_negate.type}")
            # 可以返回一个默认值或抛出异常
            return ir.Constant(ir.IntType(32), 0) # 简单返回0

def main(argv):
    # --- 1. 设置命令行参数解析 ---
    arg_parser = argparse.ArgumentParser(description="EazyLanguage Compiler")
    arg_parser.add_argument("inputfile", help="EazyLanguage source file (.ez)")
    arg_parser.add_argument("-o", "--output", help="Specify the output file name/path for the final product.")

    # 创建一个互斥组，因为 --emit-llvm 和 -S (以及默认的生成可执行文件) 是互斥的编译目标阶段
    output_type_group = arg_parser.add_mutually_exclusive_group()
    output_type_group.add_argument("-ll", "--emit-llvm", action="store_true", 
                                   help="Stop after generating LLVM IR (.ll) file.")
    output_type_group.add_argument("-s", "--emit-asm", action="store_true", # 标准编译器通常用 -S 代表汇编
                                   help="Stop after generating Assembly (.s) file.")
    # 如果没有 --emit-llvm 或 -S，则默认尝试生成可执行文件

    args = arg_parser.parse_args(argv[1:]) # 解析参数

    input_file_path = args.inputfile
    # 从输入文件路径中获取不带后缀的基本文件名，例如 "path/to/myfile.ez" -> "myfile"
    base_input_name_for_defaults = os.path.splitext(os.path.basename(input_file_path))[0]

    # --- 2. 决定各个阶段的输出文件名 ---
    # 如果 -o 未指定，我们会根据输入文件名和编译阶段来生成默认的输出文件名
    
    # .ll 文件的路径
    path_ll = ""
    if args.emit_llvm: # 如果最终目标是 .ll 文件
        path_ll = args.output if args.output else base_input_name_for_defaults + ".ll"
    else: # 如果 .ll 只是中间文件
        path_ll = base_input_name_for_defaults + ".temp.ll" # 用一个临时名字

    # .s 文件的路径
    path_s = ""
    if args.emit_asm: # 如果最终目标是 .s 文件
        path_s = args.output if args.output else base_input_name_for_defaults + ".s"
    elif not args.emit_llvm: # 如果 .s 是中间文件 (目标是可执行文件)
        path_s = base_input_name_for_defaults + ".temp.s"

    # 可执行文件的路径
    path_exe = ""
    if not args.emit_llvm and not args.emit_asm: # 如果最终目标是可执行文件
        path_exe = args.output if args.output else base_input_name_for_defaults # Linux/macOS 通常不带后缀
        if os.name == 'nt' and not path_exe.lower().endswith('.exe'): # Windows 加上 .exe
            path_exe += '.exe'
    
    # --- 3. 执行编译流程 ---
    llvm_ir_string = ""
    try:
        print(f"--- 正在处理 EazyLanguage 文件: {input_file_path} ---")
        input_stream = FileStream(input_file_path, encoding='utf-8')
        lexer = EazyLanguageLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = EazyLanguageParser(stream)

        print("--- 开始解析 ---")
        tree = parser.program()
        print("--- 解析成功！ ---")

        print("\n--- 开始用 Visitor 生成 LLVM IR ---")
        walker = MyEazyTreeWalker() 
        walker.visit(tree)
        print("--- Visitor 遍历完成 ---")
        
        llvm_ir_string = str(walker.module)

    except Exception as e:
        print("--- 编译器前端（解析或IR生成）发生错误 ---")
        print(e)
        import traceback
        traceback.print_exc()
        return # 前端出错，无法继续

    # --- 阶段一：写入 .ll 文件 ---
    try:
        # 确保目标目录存在 (如果 path_ll 包含路径的话)
        output_dir_ll = os.path.dirname(path_ll)
        if output_dir_ll and not os.path.exists(output_dir_ll):
            os.makedirs(output_dir_ll)
            print(f"创建目录: {output_dir_ll}")

        with open(path_ll, "w", encoding='utf-8') as f:
            f.write(llvm_ir_string)
        print(f"LLVM IR 已成功保存到文件: {path_ll}")
    except IOError as e:
        print(f"错误：无法将 LLVM IR 写入文件 {path_ll}: {e}")
        return

    if args.emit_llvm:
        print("编译流程结束 (仅生成 LLVM IR)。")
        return

    # --- 阶段二：从 .ll 生成 .s (汇编) 文件 ---
    # 此时 path_s 应该已经被正确设置了 (要么是最终目标，要么是临时文件名)
    print(f"\n--- 尝试从 '{path_ll}' 生成汇编文件: {path_s} ---")
    try:
        subprocess.run(['llc', path_ll, '-o', path_s], check=True)
        print(f"汇编文件已成功生成: {path_s}")
    except FileNotFoundError:
        print("错误: 'llc' 命令未找到。请确保 LLVM 已正确安装并将其可执行文件路径加入到系统的 PATH 环境变量中。")
        return
    except subprocess.CalledProcessError as e:
        print(f"错误: 'llc' 执行失败 (返回码 {e.returncode}): {e}")
        return
    
    # 如果 .ll 是临时文件且不是用户通过-o指定的最终.ll输出，可以考虑删除
    if path_ll.endswith(".temp.ll") and path_ll != args.output : # 简单判断是否为临时ll
        try:
            # print(f"  (清理临时LLVM IR文件: {path_ll})")
            # os.remove(path_ll) # 注意：自动删除文件需谨慎
            pass # 暂时不自动删除
        except OSError as e:
            print(f"警告：无法删除临时文件 {path_ll}: {e}")


    if args.emit_asm:
        print("编译流程结束 (已生成汇编文件)。")
        return

    # --- 阶段三：从 .s 生成可执行文件 ---
    # 此时 path_exe 应该已经被正确设置了
    print(f"\n--- 尝试从 '{path_s}' 生成可执行文件: {path_exe} ---")
    cc_command = "gcc" 
    try:
        subprocess.run([cc_command, path_s, '-o', path_exe, '-no-pie'], check=True)
        print(f"可执行文件 '{path_exe}' 已成功生成！你可以尝试运行它。")
        # 例如在Linux/macOS上: ./{path_exe}
    except FileNotFoundError:
        print(f"错误: '{cc_command}' 命令未找到。请确保 C 编译器 (clang 或 gcc) 已正确安装并将其可执行文件路径加入到系统的 PATH 环境变量中。")
        return
    except subprocess.CalledProcessError as e:
        print(f"错误: '{cc_command}' 执行失败 (返回码 {e.returncode}): {e}")
        return

    # 如果 .s 是临时文件且不是用户通过-o指定的最终.s输出，可以考虑删除
    if path_s.endswith(".temp.s") and path_s != args.output: # 简单判断是否为临时s
        try:
            # print(f"  (清理临时汇编文件: {path_s})")
            # os.remove(path_s) # 注意：自动删除文件需谨慎
            pass # 暂时不自动删除
        except OSError as e:
            print(f"警告：无法删除临时文件 {path_s}: {e}")
            
    print("编译流程结束 (已生成可执行文件)。")


if __name__ == '__main__':
    main(sys.argv)
