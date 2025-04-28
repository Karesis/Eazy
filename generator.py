# generator.py
# Contains the CodeGenerator for translating Eazy AST to C code.

import sys
# Import AST node definitions
from eazy_ast import *

# --- Symbol Table ---
class Symbol:
    """Represents an entry in the symbol table."""
    def __init__(self, name, type, kind, node=None): # kind='var', 'struct_instance', 'image_snapshot', 'block', 'param'
        self.name = name
        self.type = type # Eazy type ('int', 'char', StructInstanceNode, image_struct_c_name)
        self.kind = kind
        self.node = node # Reference to the defining AST node if useful
        self.c_name = name # C variable/function name (might differ later)
        self.struct_type_name = None # For struct instances, store the C typedef name
        self.image_struct_name = None # For image snapshots, store the C struct name

class SymbolTable:
    """Manages scopes and symbols."""
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []

    def define(self, symbol):
        """Define a new symbol in the current scope."""
        # if symbol.name in self.symbols:
        #     print(f"Warning: Redefining symbol '{symbol.name}' in the same scope.", file=sys.stderr)
        self.symbols[symbol.name] = symbol

    def resolve(self, name):
        """Find a symbol by name, searching current and parent scopes."""
        symbol = self.symbols.get(name)
        if symbol: return symbol
        if self.parent: return self.parent.resolve(name)
        return None

    def create_child_scope(self):
        """Create a new nested scope."""
        child = SymbolTable(parent=self)
        self.children.append(child)
        return child

# --- Code Generator ---
class CodeGenerator:
    """Walks the AST and generates C code."""
    def __init__(self):
        self.c_code_globals = "" # For #includes, global struct defs, function prototypes
        self.c_code_funcs = ""   # For function implementations
        self.current_scope = SymbolTable()
        self.struct_typedefs = {} # Keep track of generated typedefs for struct types: { type_name: True }
        self.image_structs = {} # Keep track of generated structs for image snapshots: { c_struct_name: True }
        self.block_bindings = {} # block_name -> [binding_name1, binding_name2]
        self.current_block_c_func_name = None
        self.indent_level = 0
        self._add_globals("#include <stdio.h>\n")
        self._add_globals("#include <stdlib.h> // For malloc, exit\n")
        self._add_globals("#include <string.h> // For potential string ops later\n\n")

    def _indent(self):
        return "    " * self.indent_level

    def _add_globals(self, code_line):
        self.c_code_globals += code_line

    def _add_func_code(self, code_line):
        self.c_code_funcs += self._indent() + code_line

    def _enter_scope(self):
        self.current_scope = self.current_scope.create_child_scope()

    def _exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        else:
            print("Error: Cannot exit global scope.", file=sys.stderr) # Should not happen

    def generate(self, node):
        """Generate C code for the given AST node (should be ProgramNode)."""
        self.visit(node)
        # Ensure main function is standard int main(void) or int main(int argc, char *argv[])
        # For now, replace 'main' function definition if found
        self.c_code_funcs = self.c_code_funcs.replace("int main(void)", "int eazy_main(void)", 1) # Rename original main if exists
        self.c_code_funcs = self.c_code_funcs.replace("int main(ImageSnapshot_main* _image_out)", "int eazy_main(ImageSnapshot_main* _image_out)", 1) # Handle case with bindings

        # Add the standard C main entry point that calls our Eazy main
        main_call = "eazy_main()" if "eazy_main(void)" in self.c_code_globals else \
                    "eazy_main(NULL)" if "eazy_main(ImageSnapshot_main* _image_out)" in self.c_code_globals else \
                    "main()" # Fallback if main block had different name/params

        # Check if eazy_main exists before adding the wrapper
        if "eazy_main(" in self.c_code_globals:
             self._add_func_code("\nint main(int argc, char *argv[]) {\n")
             self.indent_level += 1
             self._add_func_code(f"return {main_call};\n") # Call the Eazy main function
             self.indent_level -= 1
             self._add_func_code("}\n")
        elif "main(" in self.c_code_globals: # If user named block something else but it's the entry point
             print("Warning: No '@main:' block found. Assuming first block is entry point.", file=sys.stderr)
             # This case is complex, requires knowing which block is the entry point.
             # For now, we assume '@main:' exists for standard C main generation.


        return self.c_code_globals + "\n" + self.c_code_funcs

    def visit(self, node):
        """Dispatch to the appropriate visit method for the node type."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        # print(f"Visiting {type(node).__name__}") # Debug print
        return visitor(node)

    def generic_visit(self, node):
        """Handle visiting nodes with no specific method."""
        print(f"Warning: No specific visit method for {type(node).__name__}", file=sys.stderr)

    def visit_ProgramNode(self, node):
        """Visit the root ProgramNode."""
        # First pass: Define block symbols and find bindings
        for block_node in node.blocks:
            block_name = block_node.name.value
            symbol = Symbol(block_name, 'block', 'block', block_node)
            self.current_scope.define(symbol)
            bindings = [stmt.name_token.value for stmt in block_node.body if isinstance(stmt, BindingNode)]
            if bindings: self.block_bindings[block_name] = bindings

        # Define Image Snapshot structs globally based on bindings found
        for block_name, bindings in self.block_bindings.items():
             image_struct_c_name = f"ImageSnapshot_{block_name}"
             if image_struct_c_name not in self.image_structs:
                 self.image_structs[image_struct_c_name] = True
                 struct_def = f"typedef struct {{\n"
                 # *** Assumption: All bound variables are int for now ***
                 # TODO: Use semantic analysis results for accurate types
                 bound_var_types = {} # Placeholder for actual types
                 block_sym = self.current_scope.resolve(block_name)
                 if block_sym and block_sym.node:
                     temp_scope = SymbolTable() # Temporary scope to find var decls
                     for stmt in block_sym.node.body:
                         if isinstance(stmt, VarDeclNode):
                             bound_var_types[stmt.name_token.value] = stmt.type_token.value
                         # Could also check params if they can be bound

                 for binding_name in bindings:
                     eazy_type = bound_var_types.get(binding_name, 'int') # Default to int if not found
                     c_type = self.eazy_type_to_c(eazy_type)
                     struct_def += f"    {c_type} {binding_name};\n"
                 struct_def += f"}} {image_struct_c_name};\n\n"
                 self._add_globals(struct_def)

        # Generate function prototypes first
        for block_node in node.blocks:
            self._generate_function_prototype(block_node)

        # Second pass: Generate function bodies
        for block_node in node.blocks:
            self.visit(block_node)

    def _generate_function_prototype(self, node):
         """Helper to generate only the C function prototype."""
         block_name = node.name.value
         c_func_name = block_name # Simple mapping

         # Determine return type (assuming int for now)
         # TODO: Refine based on 'ret' statements in semantic analysis
         return_type = "int"

         params_c_list = []
         if node.params:
             for param in node.params:
                 c_type = self.eazy_type_to_c(param.type_token.value)
                 params_c_list.append(f"{c_type} {param.name_token.value}")

         image_struct_c_name = f"ImageSnapshot_{block_name}"
         if block_name in self.block_bindings:
              params_c_list.append(f"{image_struct_c_name}* _image_out")

         params_c_str = ", ".join(params_c_list) if params_c_list else "void"
         self._add_globals(f"{return_type} {c_func_name}({params_c_str});\n")


    def visit_BlockDefNode(self, node):
        """Visit a BlockDefNode and generate its C function body."""
        block_name = node.name.value
        self.current_block_c_func_name = block_name # Used by nested visits

        # Get prototype info again (could be stored from first pass)
        return_type = "int" # Assumption
        params_c_list = []
        if node.params:
            for param in node.params:
                c_type = self.eazy_type_to_c(param.type_token.value)
                params_c_list.append(f"{c_type} {param.name_token.value}")
        image_struct_c_name = f"ImageSnapshot_{block_name}"
        if block_name in self.block_bindings:
             params_c_list.append(f"{image_struct_c_name}* _image_out")
        params_c_str = ", ".join(params_c_list) if params_c_list else "void"

        # Start function definition
        self.c_code_funcs += f"\n{return_type} {self.current_block_c_func_name}({params_c_str}) {{\n"
        self.indent_level += 1
        self._enter_scope()

        # Define parameter symbols in the new scope
        if node.params:
            for param in node.params:
                 param_sym = Symbol(param.name_token.value, param.type_token.value, 'param', param)
                 self.current_scope.define(param_sym)

        # --- Generate Function Body ---
        local_vars_code = ""
        struct_alloc_code = ""
        # Hoist variable and struct declarations
        for stmt in node.body:
            if isinstance(stmt, VarDeclNode):
                c_type = self.eazy_type_to_c(stmt.type_token.value)
                var_name = stmt.name_token.value
                local_vars_code += f"{self._indent()}{c_type} {var_name};\n"
                sym = Symbol(var_name, stmt.type_token.value, 'var', stmt)
                self.current_scope.define(sym)
            elif isinstance(stmt, StructInstanceNode):
                instance_name = stmt.name_token.value
                struct_c_type_name = f"StructType_{instance_name}" # Unique type name per instance
                if struct_c_type_name not in self.struct_typedefs:
                     self.struct_typedefs[struct_c_type_name] = True
                     typedef_code = f"typedef struct {{\n"
                     for member in stmt.members:
                         member_c_type = self.eazy_type_to_c(member.type_token.value)
                         typedef_code += f"    {member_c_type} {member.name_token.value};\n"
                     typedef_code += f"}} {struct_c_type_name};\n\n"
                     self._add_globals(typedef_code) # Add typedef globally

                local_vars_code += f"{self._indent()}{struct_c_type_name}* {instance_name} = NULL;\n" # Declare and init pointer
                struct_alloc_code += f"{self._indent()}{instance_name} = ({struct_c_type_name}*)malloc(sizeof({struct_c_type_name}));\n"
                struct_alloc_code += f"{self._indent()}if ({instance_name} == NULL) {{ fprintf(stderr, \"E: Memory allocation failed for '{instance_name}'\\n\"); exit(1); }}\n"
                sym = Symbol(instance_name, stmt, 'struct_instance', stmt)
                sym.struct_type_name = struct_c_type_name
                self.current_scope.define(sym)

        self.c_code_funcs += local_vars_code
        self.c_code_funcs += struct_alloc_code

        # Generate code for executable statements
        has_explicit_return = False
        for stmt in node.body:
            if not isinstance(stmt, (VarDeclNode, StructInstanceNode, BindingNode, LabelNode)):
                 self.visit(stmt)
                 if isinstance(stmt, (RetNode, ExitNode)):
                     has_explicit_return = True
            elif isinstance(stmt, LabelNode):
                 self.indent_level -= 1 # Dedent for label
                 self._add_func_code(f"{self.visit(stmt)}:\n")
                 self.indent_level += 1

        # --- Handle Bindings ---
        if image_struct_c_name:
             self._add_func_code(f"if (_image_out != NULL) {{\n") # Check if called via image
             self.indent_level += 1
             for binding_name in self.block_bindings[block_name]:
                 bound_sym = self.current_scope.resolve(binding_name)
                 if bound_sym and bound_sym.kind in ('var', 'param'):
                     # TODO: Handle binding struct members if needed
                     self._add_func_code(f"_image_out->{binding_name} = {binding_name};\n")
                 elif bound_sym and bound_sym.kind == 'struct_instance':
                     print(f"Warning: Binding struct instance '{binding_name}' directly is not supported. Bind members instead.", file=sys.stderr)
                 else:
                      print(f"Warning: Cannot bind '{binding_name}' (kind: {bound_sym.kind if bound_sym else 'not found'}) in block '{block_name}'.", file=sys.stderr)
             self.indent_level -= 1
             self._add_func_code(f"}}\n")

        # Add default return if necessary
        if not has_explicit_return and return_type == "int":
            # Check if last statement is goto, which might imply no return needed, but complex to track.
            is_last_goto = isinstance(node.body[-1], GotoNode) if node.body else False
            if not is_last_goto: # Add return if last statement wasn't ret, exit, or goto
                 self._add_func_code(f"return 0; // Default return\n")

        self._exit_scope()
        self.indent_level -= 1
        self._add_func_code("}\n") # Close function brace

    # --- Visit Methods for Statements and Expressions ---
    # (Keep implementations for visit_VarDeclNode, visit_StructInstanceNode,
    # visit_SetNode, visit_BindingNode, visit_ImageNode, visit_CallNode,
    # visit_RetNode, visit_GotoNode, visit_LabelNode, visit_IfNode,
    # visit_PrintNode, visit_ExitNode, visit_IdentifierNode, visit_IntLiteralNode,
    # visit_CharLiteralNode, visit_BinaryOpNode, visit_MemberAccessNode,
    # and helper eazy_type_to_c from the previous version. Ensure they use
    # self._add_func_code correctly.)

    def visit_VarDeclNode(self, node): pass # Handled in BlockDefNode
    def visit_StructInstanceNode(self, node): pass # Handled in BlockDefNode
    def visit_BindingNode(self, node): pass # Handled in BlockDefNode / ImageNode

    def visit_SetNode(self, node):
        target_c = self.visit(node.target)
        expr_c = self.visit(node.expression)
        self._add_func_code(f"{target_c} = {expr_c};\n")

    def visit_ImageNode(self, node):
        image_var_name = node.image_name_token.value
        template_name = node.template_name_token.value
        template_block_sym = self.current_scope.resolve(template_name) # Resolve in global scope?
        if not template_block_sym or template_block_sym.kind != 'block':
             print(f"Error (L{node.template_name_token.line}): Cannot find block '{template_name}' for image creation.", file=sys.stderr)
             return

        image_struct_c_name = f"ImageSnapshot_{template_name}"
        # Ensure the struct type is defined (should be from ProgramNode visit)
        if template_name not in self.block_bindings and image_struct_c_name not in self.image_structs:
             print(f"Warning (L{node.template_name_token.line}): Creating image from block '{template_name}' which has no bindings. Defining empty snapshot struct.", file=sys.stderr)
             self._add_globals(f"typedef struct {{ /* No bindings */ }} {image_struct_c_name};\n\n")
             self.image_structs[image_struct_c_name] = True # Mark as defined globally

        # Declare the image snapshot variable locally (on stack)
        self._add_func_code(f"{image_struct_c_name} {image_var_name};\n")

        # Define the symbol for the image snapshot variable in the current scope
        img_sym = Symbol(image_var_name, image_struct_c_name, 'image_snapshot', node)
        img_sym.image_struct_name = image_struct_c_name
        self.current_scope.define(img_sym)

        # Prepare arguments for the function call
        args_c = []
        if node.args:
            args_c = [self.visit(arg) for arg in node.args]
        # Add the image struct pointer argument if the target expects it
        if template_name in self.block_bindings:
            args_c.append(f"&{image_var_name}")
        elif node.args is None: # Handle case where block has no params AND no bindings
             pass # No arguments needed
        # Else: Block has params but no bindings - args_c already populated

        args_c_str = ", ".join(args_c)
        # Call the function, ignore return value for image creation
        self._add_func_code(f"{template_name}({args_c_str}); // Call for image\n")


    def visit_CallNode(self, node):
        result_var_name = node.result_container_token.value
        target_node = node.target_block
        target_c_func_name = ""
        target_block_sym = None # To store resolved symbol

        if isinstance(target_node, IdentifierNode):
             target_name = target_node.value
             target_block_sym = self.current_scope.resolve(target_name) # Resolve in global scope?
             if not target_block_sym or target_block_sym.kind != 'block':
                 print(f"Error (L{target_node.token.line}): Cannot find block '{target_name}' for call.", file=sys.stderr)
                 return
             target_c_func_name = target_name
        elif isinstance(target_node, MemberAccessNode):
             # TODO: Implement path call logic
             print(f"Error (L{node.target_block.base.token.line}): Path calls (e.g., parent.child) not yet implemented.", file=sys.stderr)
             return
        else:
             print(f"Error (L{node.result_container_token.line}): Invalid target for call.", file=sys.stderr)
             return

        result_sym = self.current_scope.resolve(result_var_name)
        if not result_sym or result_sym.kind not in ('var', 'param'):
             print(f"Error (L{node.result_container_token.line}): Result container '{result_var_name}' for call not found or not a variable.", file=sys.stderr)
             return

        args_c = []
        if node.args:
            args_c = [self.visit(arg) for arg in node.args]

        # Add NULL for the image struct pointer if the target function expects one
        if target_c_func_name in self.block_bindings:
             args_c.append("NULL")
        elif node.args is None and target_c_func_name not in self.block_bindings:
             # Handle case where block has no params AND no bindings
             pass # No arguments needed

        args_c_str = ", ".join(args_c)
        self._add_func_code(f"{result_var_name} = {target_c_func_name}({args_c_str}); // Call for result\n")

    def visit_RetNode(self, node):
        value_c = self.visit(node.value)
        self._add_func_code(f"return {value_c};\n")

    def visit_GotoNode(self, node):
        label_name = node.label_token.value
        self._add_func_code(f"goto {label_name};\n")

    def visit_LabelNode(self, node):
        return node.name_token.value # Return name, handled in BlockDefNode

    def visit_IfNode(self, node):
        condition_c = self.visit(node.condition)
        self._add_func_code(f"if ({condition_c}) {{\n")
        self.indent_level += 1
        self.visit(node.statement) # Generate the single statement
        self.indent_level -= 1
        self._add_func_code(f"}}\n")

    def visit_PrintNode(self, node):
        value_c = self.visit(node.value)
        format_spec = "%d" # Default assumption
        # Basic type inference for print
        value_type = 'int' # Default
        if isinstance(node.value, CharLiteralNode): value_type = 'char'
        elif isinstance(node.value, IdentifierNode):
            sym = self.current_scope.resolve(node.value.value)
            if sym: value_type = sym.type # Use declared Eazy type
        elif isinstance(node.value, MemberAccessNode):
             # Need more complex type inference based on struct member type
             pass # Keep default for now

        if value_type == 'char': format_spec = "%c"
        # Add other format specifiers if needed (%f, %s, etc.)

        self._add_func_code(f'printf("{format_spec}\\n", {value_c});\n')

    def visit_ExitNode(self, node):
        # Check if we are inside the function generated for @main block
        if self.current_block_c_func_name == 'main':
             self._add_func_code("return 0; // Exit from main\n")
        else:
             self._add_func_code("exit(0); // Exit from non-main block\n")

    def visit_IdentifierNode(self, node):
        sym = self.current_scope.resolve(node.value)
        if not sym:
             print(f"Error (L{node.token.line} C{node.token.column}): Undefined identifier '{node.value}'.", file=sys.stderr)
             return f"/* Undefined: {node.value} */" # Avoid crash
        return node.value # Return C name (assuming it's same as Eazy name for now)

    def visit_IntLiteralNode(self, node):
        return str(node.value)

    def visit_CharLiteralNode(self, node):
        # Handle C escapes
        c_val = node.value
        if c_val == '\n': c_val = '\\n'
        elif c_val == '\t': c_val = '\\t'
        elif c_val == "'": c_val = "\\'"
        elif c_val == '\\': c_val = '\\\\'
        # Add others if needed
        return f"'{c_val}'"

    def visit_BinaryOpNode(self, node):
        left_c = self.visit(node.left)
        right_c = self.visit(node.right)
        op = node.op_token.value
        return f"({left_c} {op} {right_c})"

    def visit_MemberAccessNode(self, node):
        # This needs to handle nested access like a.b.c correctly
        # We traverse the base first. If the base itself is a MemberAccess,
        # its visit method will return the C code for accessing *its* member.
        base_c = self.visit(node.base)
        member_name = node.member_token.value

        # Determine the type/kind of the immediate base of *this* access
        immediate_base_node = node.base
        base_sym = None
        current_node = node.base
        struct_type_name_for_member = None # Store the C type of the struct containing the member

        # Find the original identifier for symbol lookup in nested access (a.b.c -> find 'a')
        temp_node = node.base
        while isinstance(temp_node, MemberAccessNode):
            temp_node = temp_node.base
        if isinstance(temp_node, IdentifierNode):
             original_base_sym = self.current_scope.resolve(temp_node.value)
             if not original_base_sym:
                 print(f"Error (L{temp_node.token.line}): Base identifier '{temp_node.value}' for member access not found.", file=sys.stderr)
                 return "/* Invalid Base */"

             # Now, determine the type of the *immediate* base (e.g., for a.b.c, find type of 'b')
             # This requires type inference or storing member types in symbol table.
             # Simplified approach: Assume we know the type of the direct base symbol.
             if isinstance(node.base, IdentifierNode): # Simple case: a.b
                 base_sym = self.current_scope.resolve(node.base.value)
                 if base_sym and base_sym.kind == 'struct_instance':
                     struct_type_name_for_member = base_sym.struct_type_name
                 elif base_sym and base_sym.kind == 'image_snapshot':
                     struct_type_name_for_member = base_sym.image_struct_name # Not really needed for '.' access
                 # else: error handled below or in identifier visit

             # TODO: Handle nested case a.b.c - need type of 'b'
             # This part requires proper type tracking during semantic analysis.
             # For now, we'll rely on the base_sym check below.

        else:
             print(f"Error (L{node.member_token.line}): Cannot determine base identifier for member access.", file=sys.stderr)
             return "/* Invalid Base */"


        # Now decide between '.' and '->' based on the *original* base kind
        if original_base_sym:
            if original_base_sym.kind == 'struct_instance':
                 # Base was a pointer, so all access is via ->
                 # base_c already contains the code to access the member *before* this one
                 # e.g., for a.b.c, base_c might be "a->b"
                 return f"{base_c}->{member_name}"
            elif original_base_sym.kind == 'image_snapshot':
                 # Base was a value type (struct on stack), access is via .
                 return f"{base_c}.{member_name}"
            else:
                  print(f"Error (L{node.member_token.line}): Member access '.' or '->' applied to non-struct/image '{original_base_sym.name}' (kind: {original_base_sym.kind}).", file=sys.stderr)
                  return f"/* Invalid Member Access on {original_base_sym.name} */"
        else:
             # Error already printed or base wasn't identifier
             return "/* Invalid Member Access */"


    def eazy_type_to_c(self, eazy_type):
        """Map Eazy type names to C type names."""
        if eazy_type == 'int': return 'int'
        if eazy_type == 'char': return 'char'
        # Add mappings for float, bool, etc. if added to Eazy
        print(f"Warning: Unknown Eazy type '{eazy_type}', mapping to 'int'.", file=sys.stderr)
        return 'int' # Default fallback


# --- Example Usage (Optional: Keep for testing this file) ---
# if __name__ == "__main__":
#     # Assume ast is an AST generated by the parser
#     # Example:
#     # from leparser import Lexer, Parser, Token # Assuming Token is also in leparser
#     # int_tok = Token(TT_KEYWORD, 'int')
#     # x_tok = Token(TT_IDENTIFIER, 'x')
#     # main_tok = Token(TT_IDENTIFIER, 'main')
#     # ten_tok = Token(TT_INT, 10)
#     # print_tok = Token(TT_KEYWORD, 'print')
#     # exit_tok = Token(TT_KEYWORD, 'exit')
#     # ast = ProgramNode(blocks=[
#     #     BlockDefNode(name=main_tok, params=None, line=1, column=1, body=[
#     #         VarDeclNode(int_tok, x_tok),
#     #         SetNode(IdentifierNode(x_tok), IntLiteralNode(ten_tok)),
#     #         PrintNode(IdentifierNode(x_tok)),
#     #         ExitNode()
#     #     ])
#     # ])

#     # generator = CodeGenerator()
#     # c_code = generator.generate(ast)
#     # print("\n--- Generated C Code ---")
#     # print(c_code)
#     pass # Add test code here if running standalone


