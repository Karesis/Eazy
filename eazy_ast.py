# eazy_ast.py
# Defines the Abstract Syntax Tree nodes for the Eazy language.

class ASTNode:
    """Base class for all AST nodes."""
    pass

# --- Program Structure ---

class ProgramNode(ASTNode):
    """Root node for the entire program."""
    def __init__(self, blocks):
        self.blocks = blocks # List of BlockDefNode

class BlockDefNode(ASTNode):
    """Node representing a block definition (@name:)."""
    def __init__(self, name, params, body, line, column):
        self.name = name # Identifier token
        self.params = params # List of ParamNode or None
        self.body = body # List of statement nodes
        self.line = line
        self.column = column

class ParamNode(ASTNode):
    """Node representing a parameter in a block definition."""
    def __init__(self, type_token, name_token):
        self.type_token = type_token # Keyword token (e.g., 'int')
        self.name_token = name_token # Identifier token

# --- Statement Nodes ---

class VarDeclNode(ASTNode):
    """Node representing a variable declaration (e.g., int x)."""
    def __init__(self, type_token, name_token):
        self.type_token = type_token # Keyword token (e.g., 'int')
        self.name_token = name_token # Identifier token

class StructInstanceNode(ASTNode):
    """Node representing a struct instance creation."""
    def __init__(self, name_token, members):
        self.name_token = name_token # Identifier token for the instance
        self.members = members # List of StructMemberNode

class StructMemberNode(ASTNode):
    """Node representing a member within a struct definition."""
    def __init__(self, type_token, name_token):
        self.type_token = type_token # Keyword token
        self.name_token = name_token # Identifier token

class SetNode(ASTNode):
    """Node representing a set statement (assignment)."""
    def __init__(self, target, expression):
        self.target = target # IdentifierNode or MemberAccessNode
        self.expression = expression # Expression node

class BindingNode(ASTNode):
    """Node representing a binding statement (.name)."""
    def __init__(self, name_token):
        self.name_token = name_token # Identifier token

class ImageNode(ASTNode):
    """Node representing an image creation statement."""
    def __init__(self, image_name_token, template_name_token, args):
        self.image_name_token = image_name_token # Identifier
        self.template_name_token = template_name_token # Identifier
        self.args = args # List of expression nodes or None

class CallNode(ASTNode):
    """Node representing a call statement."""
    def __init__(self, result_container_token, target_block, args):
        self.result_container_token = result_container_token # Identifier
        self.target_block = target_block # IdentifierNode or MemberAccessNode (for path call)
        self.args = args # List of expression nodes or None

class RetNode(ASTNode):
    """Node representing a return statement."""
    def __init__(self, value):
        self.value = value # Expression node

class GotoNode(ASTNode):
    """Node representing a goto statement."""
    def __init__(self, label_token):
        self.label_token = label_token # Identifier token

class LabelNode(ASTNode):
    """Node representing a label definition (name:)."""
    def __init__(self, name_token):
        self.name_token = name_token # Identifier token

class IfNode(ASTNode):
    """Node representing an if statement."""
    def __init__(self, condition, statement):
        self.condition = condition # Expression node
        self.statement = statement # Single statement node executed if true

class PrintNode(ASTNode):
    """Node representing a print statement."""
    def __init__(self, value):
        self.value = value # Expression node

class ExitNode(ASTNode):
    """Node representing an exit statement."""
    pass

# --- Expression Nodes ---

class ExpressionNode(ASTNode):
    """Base class for all expression nodes."""
    pass

class IdentifierNode(ExpressionNode):
    """Node representing an identifier (variable, block name, etc.)."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class IntLiteralNode(ExpressionNode):
    """Node representing an integer literal."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class CharLiteralNode(ExpressionNode):
    """Node representing a character literal."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BinaryOpNode(ExpressionNode):
    """Node representing a binary operation (e.g., +, -, ==)."""
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

class MemberAccessNode(ExpressionNode):
    """Node representing member access (struct.member or image.binding)."""
    def __init__(self, base, member_token):
        self.base = base # Usually IdentifierNode or another MemberAccessNode
        self.member_token = member_token # Identifier token (the member/binding name)

# Note: ImageAccessNode might not be strictly necessary if MemberAccessNode
# is used and differentiated during semantic analysis or code generation.
# Keeping it separate might offer clarity if parsing logic can distinguish it.
# For now, MemberAccessNode handles both cases.
# class ImageAccessNode(ExpressionNode):
#     """Node specifically for image snapshot access (image_name.binding_name)."""
#     def __init__(self, image_name_token, binding_name_token):
#         self.image_name_token = image_name_token
#         self.binding_name_token = binding_name_token


