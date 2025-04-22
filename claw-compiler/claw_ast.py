from dataclasses import dataclass, field
from typing import List, Optional
from claw_lexer import Token 
@dataclass
class ASTNode: # 基类
    pass

# --- Top Level ---
@dataclass
class Program(ASTNode):
    # 程序由顶层命名块定义组成
    block_definitions: List['BlockDefinition'] = field(default_factory=list)

# --- Block Definition ---
@dataclass
class BlockDefinition(ASTNode): # Represents a @name: block
    name: str
    parameters: Optional[str] = field(default_factory=list)
    # 块内部的内容列表，这些内容都是 BlockContent 的子类
    inner_content: List['BlockContent'] = field(default_factory=list)

# --- Block Content (Base class for things inside a BlockDefinition) ---
@dataclass
class BlockContent(ASTNode):
    pass # No common fields needed for all inner content types

# --- Specific Block Content Types ---

# 代表一行将被“直接翻译”的普通代码块 (例如：a = 10, b = a * 5 + 2, print b)
# Parser 只需要识别这是一行，并存储这行的内容
@dataclass
class GenericLineBlock(BlockContent):
    # 存储这行的原始 tokens (不包括行首的缩进和行尾的 NEWLINE)
    line_tokens: List[Token] = field(default_factory=list)
    # 可以可选地存储行的原始文本，有时候比 tokens 更方便生成代码
    # raw_text: str = ""


# 代表 goto 控制流块
@dataclass
class GotoBlock(BlockContent):
    target_block_name: str # 目标块的名字
    arguments: Optional[Token] = field(default_factory=list)


# 代表 back 控制流块
@dataclass
class BackBlock(BlockContent):
    output: Optional[Token]
    pass

