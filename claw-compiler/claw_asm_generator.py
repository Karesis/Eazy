# claw-compiler/claw_asm_generator.py
import sys
# 导入你定义的 AST 节点和 Token 类型
from claw_ast import Program, BlockDefinition, BackBlock, GenericLineBlock, GotoBlock, BlockContent
from claw_lexer import Token, TokenType # 假设 Token 和 TokenType 在 claw_lexer.py 中

class AssemblyGenerator:
    def __init__(self):
        self.assembly_code = []
        # 暂时还不需要管理局部变量或复杂标签
        # self.current_function_locals = {}
        # self.next_local_offset = -8
        # self.label_count = 0

    def add_instruction(self, instruction, comment=None):
        """Helper function to add an assembly instruction."""
        indent = "    "
        if comment:
            self.assembly_code.append(f"{indent}{instruction.ljust(30)} # {comment}")
        else:
            self.assembly_code.append(f"{indent}{instruction}")

    def generate_program(self, program_node: Program):
        """Generates assembly code for the entire Eazy program AST."""
        self.add_instruction(".text", "Code section")
        self.add_instruction(".global _start", "Make _start visible to linker")

        main_block_node = None
        for block_def in program_node.block_definitions:
            if isinstance(block_def, BlockDefinition) and block_def.name == "main":
                main_block_node = block_def
                break # 找到 @main 就停止

        if main_block_node is None:
            raise ValueError("Compiler Error: Entry point '@main:' block not found in the program.")

        # Generate code for the @main block mapped to _start
        self.generate_main_block_as_start(main_block_node)

        # Later, you would loop through other block_definitions
        # and generate regular functions for them here.

        return "\n".join(self.assembly_code) + "\n"

    def generate_main_block_as_start(self, block_node: BlockDefinition):
        """Generates assembly for the @main block, mapping it to _start."""
        self.assembly_code.append("_start:") # Program entry label

        # Process the statements inside the @main block
        last_stmt_was_back = False
        for content_node in block_node.inner_content:
            last_stmt_was_back = self.generate_block_content(content_node)
            # If a back statement was generated, it handled the exit.
            # We might stop processing further statements in _start after back,
            # or let it run but the exit syscall means they won't execute.

        # If the @main block finished without an explicit 'back', exit with code 0.
        if not last_stmt_was_back:
            self.add_instruction("movq $0, %rdi", "Default exit code 0 (no explicit back)")
            self.add_instruction("movq $60, %rax", "syscall number for exit")
            self.add_instruction("syscall", "Exit the program")


    def generate_block_content(self, content_node: BlockContent) -> bool:
        """
        Generates code for a node within a block's inner_content.
        Returns True if a 'back' statement was handled (which includes exit), False otherwise.
        """
        if isinstance(content_node, BackBlock):
            # Handle 'back [value, ...]'
            if content_node.return_values:
                # For now, only handle single return value for exit code
                if len(content_node.return_values) > 1:
                    print(f"Warning: 'back' with multiple values in @main not yet fully supported for exit code. Using the first value.", file=sys.stderr)

                value_token = content_node.return_values[0]

                # Generate code to get the value into %rax (standard return place)
                value_reg = self.generate_value_expression(value_token) # Gets value into a register (e.g., %rax)

                # Move the result from value_reg to %rdi for the exit syscall
                if value_reg != "rdi":
                    self.add_instruction(f"movq %{value_reg}, %rdi", f"Move return value from {value_reg} to exit code register (%rdi)")
                # If value_reg *was* %rdi, it's already there.
            else:
                # Handle 'back' (no value) -> exit with 0
                self.add_instruction("movq $0, %rdi", "Set exit code 0 for back without value")

            # Generate the exit syscall
            self.add_instruction("movq $60, %rax", "syscall number for exit")
            self.add_instruction("syscall", "Exit the program")
            return True # Indicate that a back/exit was handled

        elif isinstance(content_node, GenericLineBlock):
            # TODO: Implement handling for generic lines (assignments, print, etc.)
            # For now, just print a warning or skip.
            line_text = ' '.join(t.lexeme for t in content_node.line_tokens)
            print(f"Warning: Skipping GenericLineBlock: '{line_text}' - Not yet implemented in ASM generator.", file=sys.stderr)
            self.add_instruction(f"# Skipping: {line_text}") # Add as assembly comment
            return False

        elif isinstance(content_node, GotoBlock):
            # TODO: Implement handling for goto (will become 'call' later)
            print(f"Warning: Skipping GotoBlock targeting '{content_node.target_block_name}' - Not yet implemented.", file=sys.stderr)
            self.add_instruction(f"# Skipping: goto {content_node.target_block_name}")
            return False

        # Add elif for other BlockContent types as needed
        else:
            print(f"Warning: Unsupported BlockContent type: {type(content_node)}", file=sys.stderr)
            return False


    def generate_value_expression(self, value_token: Token) -> str:
        """
        Generates code for a simple value (constant or identifier)
        and returns the register holding the result.
        (Simplified: always uses %rax for now)
        """
        target_reg = "rax" # Simplification: All intermediate results go to rax

        if value_token.type == TokenType.NUMBER:
            self.add_instruction(f"movq ${value_token.value}, %{target_reg}", f"Load constant {value_token.value} into %{target_reg}")
            return target_reg
        elif value_token.type == TokenType.IDENTIFIER:
            # TODO: Implement variable loading
            # Need to look up variable's location (e.g., stack offset)
            # variable_location = self.lookup_variable(value_token.lexeme) # Needs symbol table / local var tracking
            # self.add_instruction(f"movq {variable_location}, %{target_reg}", f"Load variable {value_token.lexeme} into %{target_reg}")
            raise NotImplementedError(f"Loading variables ('{value_token.lexeme}') not yet implemented.")
            # return target_reg
        else:
            # Later, handle more complex expressions (binary ops, etc.)
            raise TypeError(f"Unsupported value token type for expression generation: {value_token.type}")