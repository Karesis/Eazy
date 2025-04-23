# claw_ast.py (重构完成 - V2，包含 GotoNode)

from dataclasses import dataclass, field
from typing import List, Optional, Any

# --- 基础节点 ---
@dataclass
class ASTNode:
    """所有 AST 节点的基类。"""
    pass

@dataclass
class ExpressionNode(ASTNode):
    """所有代表“值”的节点的基类。"""
    pass

@dataclass
class StatementNode(ASTNode):
    """所有代表“动作”或“声明”的节点的基类。"""
    pass

# --- 表达式节点 ---

@dataclass
class ConstantNode(ExpressionNode):
    """代表一个字面常量值 (例如, 42)。"""
    value: Any # 实际的值 (目前主要是 int)
    # const_type: str = "int" # 可以明确类型

@dataclass
class IdentifierNode(ExpressionNode):
    """代表一个标识符 (变量名, 函数名, 标签名)。"""
    name: str

@dataclass
class BinaryOperationNode(ExpressionNode):
    """代表一个二元运算 (例如, +, -, *, /, ==, !=, >, <, <=, >=)。"""
    left: ExpressionNode
    operator: str # 存储操作符词素，例如 "+", "==", ">="
    right: ExpressionNode

@dataclass
class CallExpressionNode(ExpressionNode):
    """代表一个函数/块调用，可以用在表达式中或作为语句。"""
    callee_name: IdentifierNode
    arguments: List[ExpressionNode] = field(default_factory=list)

# --- 语句节点 ---

@dataclass
class VarDeclNode(StatementNode):
    """代表一个变量声明 (例如, int x; int y = 10)。"""
    var_name: IdentifierNode
    var_type: str # 目前是 "int"
    initializer: Optional[ExpressionNode] = None

@dataclass
class AssignmentNode(StatementNode):
    """代表一个赋值语句 (例如, x = y + 5)。"""
    target: IdentifierNode
    value: ExpressionNode

@dataclass
class ReturnNode(StatementNode):
    """代表一个 'return' 语句。"""
    value: Optional[ExpressionNode] = None # 要返回的表达式 (可选)

@dataclass
class CallStatementNode(StatementNode):
    """代表一个纯粹作为语句使用的调用。"""
    call_expression: CallExpressionNode

@dataclass
class ExpressionStatementNode(StatementNode):
    """包装一个被当作语句使用的表达式 (例如 print 调用)。"""
    expression: ExpressionNode

@dataclass
class IfNode(StatementNode):
    """代表一个 'if' 语句，必须包含 'then' 分支，可选包含 'else' 分支。"""
    condition: ExpressionNode          # if 后面的条件表达式
    then_body: List[StatementNode]     # 条件为真时执行的语句列表 ('then' 分支)
    else_body: Optional[List[StatementNode]] = None # 可选的 'else' 分支语句列表

@dataclass
class GotoNode(StatementNode):
    """代表一个 'goto' 语句，用于块内跳转。"""
    target_label: IdentifierNode # 跳转目标的标签名

@dataclass
class LabelNode(StatementNode):
    """Represents a label definition within a block (e.g., mylabel:)."""
    label_name: IdentifierNode

# (未来可以加 WhileNode, ForNode 等)
# (未来可能需要 LabelDeclarationNode 来明确定义标签)

# --- 顶层与块定义 ---

@dataclass
class ParameterNode(ASTNode):
    """代表块定义中的一个参数。"""
    name: str
    param_type: str # 例如 "int"

@dataclass
class BlockDefinition(ASTNode): # 代表一个 @name(...) 块 (函数定义)
    """代表一个顶层或嵌套的函数/块定义。"""
    name: str
    parameters: List[ParameterNode] = field(default_factory=list)
    body: List[StatementNode] = field(default_factory=list) # 函数体由语句构成

@dataclass
class Program(ASTNode):
    """代表整个 Eazy 程序。"""
    definitions: List[BlockDefinition] = field(default_factory=list) # 程序由块定义组成