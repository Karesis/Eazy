# claw.py
import sys
import os
import argparse
import subprocess

from antlr4 import InputStream, CommonTokenStream
from llvmlite import ir
from EazyLepaser.EazyLanguageLexer import EazyLanguageLexer
from EazyLepaser.EazyLanguageParser import EazyLanguageParser
from EazyLanguageCompiler import EazyTreeWalker 

# --- 阶段一函数：从 EazyLanguage 源码字符串生成 LLVM Module 对象 ---
def source_to_llvm_module(eazy_source_string: str, verbose: bool = False) -> ir.Module | None:
    """
    Parses EazyLanguage source string and generates an LLVM IR Module object.
    Returns the llvmlite.ir.Module object on success, None on failure.
    """
    if verbose: print("阶段 1: 从源码字符串生成 LLVM IR Module...")
    
    try:
        if verbose: print("  正在创建输入流和词法分析器...")
        input_stream = InputStream(eazy_source_string) # 使用 InputStream 处理内存中的字符串
        lexer = EazyLanguageLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = EazyLanguageParser(stream)
        
        if verbose: print("  开始构建解析树...")
        tree = parser.program()
        if verbose: print("  解析树构建成功！")

        if verbose: print("  开始用 Visitor 生成 LLVM IR...")
        walker = EazyTreeWalker() 
        walker.visit(tree) # Visitor 会构建并填充 walker.module
        if verbose: print("  Visitor 遍历完成。")
        return walker.module # 返回构建好的 LLVM Module 对象
    except Exception as e:
        print(f"错误：编译器前端（解析或IR生成）失败: {e}")
        # import traceback; traceback.print_exc() # 调试时打开
        return None

# --- 阶段二函数：从 LLVM Module 对象生成汇编字符串 ---
def llvm_module_to_asm_string(llvm_module: ir.Module, verbose: bool = False) -> str | None:
    """
    Compiles an LLVM IR Module object to an assembly string using llc.
    Returns the assembly string on success, None on failure.
    """
    llvm_ir_code = str(llvm_module) # 获取模块的文本表示
    target_triple = llvm_module.triple # 从模块获取目标三元组

    if verbose: print(f"\n阶段 2: 从 LLVM IR (目标: {target_triple}) 编译到汇编字符串...")
    try:
        llc_command = ['llc', '-relocation-model=pic']
        # 当从 stdin 读取时，llc 通常能从 IR 文本中识别 target triple
        # 如果 IR 文本中没有 triple，或者想更明确，可以加 -mtriple=<triple_str>
        # llc_command.extend(['-mtriple', target_triple]) # 可选

        process = subprocess.run(
            llc_command,
            input=llvm_ir_code, # 将 IR 字符串作为输入传递给 llc
            capture_output=True,  # 捕获 llc 的输出
            text=True,            # 将输出解码为文本
            encoding='utf-8',
            check=True            # 如果 llc 返回非零退出码，则抛出 CalledProcessError
        )
        if verbose: print("  汇编代码已在内存中生成。")
        return process.stdout # 返回 llc 生成的汇编代码字符串
    except FileNotFoundError:
        print("错误: 'llc' 命令未找到。请确保 LLVM 已正确安装并将其可执行文件路径加入到系统的 PATH 环境变量中。")
        return None
    except subprocess.CalledProcessError as e:
        print(f"错误: 'llc' 执行失败 (返回码 {e.returncode}):\n标准错误输出:\n{e.stderr}")
        return None
    except Exception as e:
        print(f"错误: 生成汇编时发生未知错误: {e}")
        return None

# --- 阶段三函数：从汇编字符串编译链接到可执行文件 ---
def asm_string_to_executable(asm_string: str, output_exe_path: str, 
                             cc_command: str = "gcc", verbose: bool = False) -> bool:
    """
    Compiles an assembly string to a native executable using a C compiler.
    Returns True on success, False on failure.
    """
    if verbose: print(f"\n阶段 3: 从汇编字符串编译链接到可执行文件 '{output_exe_path}' (使用 {cc_command})")
    try:
        # 确保目标目录存在
        output_dir_exe = os.path.dirname(output_exe_path)
        if output_dir_exe and not os.path.exists(output_dir_exe):
            os.makedirs(output_dir_exe)
            if verbose: print(f"  创建目录: {output_dir_exe}")

        # 使用 '-x assembler -' 告诉 C 编译器从标准输入读取汇编代码
        subprocess.run(
            [cc_command, '-x', 'assembler', '-', '-o', output_exe_path, '-no-pie'],
            input=asm_string.encode('utf-8'), # 将汇编字符串作为输入
            check=True
        )
        print(f"可执行文件 '{output_exe_path}' 已成功生成!")
        return True
    except FileNotFoundError:
        print(f"错误: '{cc_command}' 命令未找到。请确保 C 编译器 (gcc 或 clang) 已正确安装并将其可执行文件路径加入到系统的 PATH 环境变量中。")
        return False
    except subprocess.CalledProcessError as e:
        print(f"错误: '{cc_command}' 执行失败 (返回码 {e.returncode}):\n标准错误输出:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"错误: 生成可执行文件时发生未知错误: {e}")
        return False

def main():
    # --- 命令行参数解析 (与你之前的版本基本一致) ---
    parser = argparse.ArgumentParser(
        prog="claw",
        description="Claw: EazyLanguage Compiler.",
        epilog="使用示例: python claw.py examples/test.ez -o my_program"
    )
    parser.add_argument("inputfile", help="EazyLanguage source file (.ez) to compile.")
    parser.add_argument("-o", "--output",
                        help="Specify the output file name/path for the final product.")
    output_type_group = parser.add_mutually_exclusive_group()
    output_type_group.add_argument("-ll", "--emit-llvm", dest="emit_llvm", action="store_true",
                                   help="Output LLVM IR (.ll) file and stop.")
    output_type_group.add_argument("-s", "--emit-asm", dest="emit_asm", action="store_true",
                                   help="Output Assembly (.s) file and stop.")
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Print verbose (detailed) compilation steps.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    # --- 获取输入文件内容 ---
    if not os.path.exists(args.inputfile):
        print(f"错误: 输入文件 '{args.inputfile}' 不存在。")
        sys.exit(1)
    if not args.inputfile.lower().endswith(".ez"):
        print(f"警告: 输入文件 '{args.inputfile}' 的后缀不是 .ez。")
    
    try:
        with open(args.inputfile, "r", encoding="utf-8") as f:
            eazy_source_code = f.read()
    except IOError as e:
        print(f"错误: 无法读取输入文件 '{args.inputfile}': {e}")
        sys.exit(1)

    # --- 决定最终输出文件名 ---
    base_input_name_for_defaults = os.path.splitext(os.path.basename(args.inputfile))[0]
    final_output_path = args.output # 用户通过 -o 指定的路径

    # --- 编译流程 ---
    # 阶段 1: Eazy 源码 -> LLVM Module 对象
    llvm_module = source_to_llvm_module(eazy_source_code, args.verbose)
    if llvm_module is None:
        print("编译中止：未能生成 LLVM IR Module。")
        sys.exit(1)
    
    llvm_ir_code_string = str(llvm_module) # 获取IR字符串，用于写入文件或传递

    # 处理 --emit-llvm 情况
    if args.emit_llvm:
        output_file = final_output_path if final_output_path else base_input_name_for_defaults + ".ll"
        try:
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir): os.makedirs(output_dir)
            with open(output_file, "w", encoding='utf-8') as f: f.write(llvm_ir_code_string)
            print(f"LLVM IR 已成功保存到文件: {output_file}")
            print("编译流程结束 (仅生成 LLVM IR)。")
        except IOError as e:
            print(f"错误: 无法写入 LLVM IR 到文件 '{output_file}': {e}")
        sys.exit(0)

    # 阶段 2: LLVM Module -> 汇编字符串
    asm_code_string = llvm_module_to_asm_string(llvm_module, args.verbose)
    if asm_code_string is None:
        print("编译中止：未能将 LLVM IR 转换为汇编代码。")
        sys.exit(1)

    # 处理 -s (--emit-asm) 情况
    if args.emit_asm:
        output_file = final_output_path if final_output_path else base_input_name_for_defaults + ".s"
        try:
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir): os.makedirs(output_dir)
            with open(output_file, "w", encoding='utf-8') as f: f.write(asm_code_string)
            print(f"汇编代码已成功保存到文件: {output_file}")
            print("编译流程结束 (已生成汇编文件)。")
        except IOError as e:
            print(f"错误: 无法写入汇编代码到文件 '{output_file}': {e}")
        sys.exit(0)

    # 默认情况：阶段 3: 汇编字符串 -> 可执行文件
    output_file = final_output_path if final_output_path else base_input_name_for_defaults
    if os.name == 'nt' and not output_file.lower().endswith('.exe'): output_file += '.exe'
    
    if not asm_string_to_executable(asm_code_string, output_file, verbose=args.verbose):
        print("编译中止：未能从汇编代码生成可执行文件。")
        sys.exit(1)
    
    print("编译流程成功结束 (已生成可执行文件)。")
    sys.exit(0)

if __name__ == "__main__":
    main()
