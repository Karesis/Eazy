from enum import Enum, auto
from dataclasses import dataclass

# --- Structure ---
# Token Category
class TokenCategory(Enum):
    OPERATOR = auto()        # General operators like +, -, *, /
    LOGICAL_OP = auto()      # Logical operators like ==, !=, <, >
    KEYWORD = auto()         # Language keywords like if, else, while
    IDENTIFIER = auto()      # Variable names, function names, etc.
    LITERAL = auto()         # Concrete values like numbers, strings
    SEPARATOR = auto()       # Punctuation like (), {}, ;, ,
    ASSIGNMENT = auto()      # Assignment operators like =
    BOL = auto()             # Begin of A Line
    EOF = auto()             # End of File marker
    UNKNOWN = auto()         # For unrecognized characters/tokens

# Token Type
class TokenType(Enum):
    def __init__(self, value, display: str, category: TokenCategory):
        self.display: str = display
        self.category: TokenCategory = category

    # -- Member Definitions --

    # Literals
    literal_int = (auto(), '<integer>', TokenCategory.literal)
    literal_float = (auto(), '<float>', TokenCategory.literal) 
    LITERAL_STR = (auto(), '<string>', TokenCategory.LITERAL)

    # Identifiers 
    IDENTIFIER = (auto(), '<identifier>', TokenCategory.IDENTIFIER)

    # Keywords 
    KEYWORD_IF = (auto(), 'if', TokenCategory.KEYWORD)
    KEYWORD_ELIF = (auto(), 'elif', TokenCategory.KEYWORD)
    KEYWORD_ELSE = (auto(), 'else', TokenCategory.KEYWORD)
    KEYWORD_WHILE = (auto(), 'while', TokenCategory.KEYWORD)
    KEYWORD_PRINT = (auto(), 'print', TokenCategory.KEYWORD)
    KEYWORD_GOTO = (auto(), 'goto', TokenCategory.KEYWORD)
    KEYWORD_RET = (auto(), 'ret', TokenCategory.KEYWORD)

    # Operators
    OP_PLUS = (auto(), '+', TokenCategory.OPERATOR)
    OP_MINUS = (auto(), '-', TokenCategory.OPERATOR)
    OP_MULTIPLY= (auto(), '*', TokenCategory.OPERATOR)
    OP_DIVIDE  = (auto(), '/', TokenCategory.OPERATOR)
    OP_SHIFTLEFT = (auto(), '<<', TokenCategory.OPERATOR)
    OP_SHIFTRIGHT = (auto(), '>>', TokenCategory.OPERATOR)
    OP_AND = (auto(), '&', TokenCategory.OPERATOR)
    OP_OR = (auto(), '|', TokenCategory.OPERATOR)
    OP_XOR = (auto(), '^', TokenCategory.OPERATOR)
    OP_POWER = (auto(), '**', TokenCategory.OPERATOR)
    OP_MOD = (auto(), '%', TokenCategory.OPERATOR)

    # Logical Operators
    OP_EQ = (auto(), '==', TokenCategory.LOGICAL_OP) 
    OP_LT = (auto(), '<', TokenCategory.LOGICAL_OP)
    OP_LTE = (auto(), '<=', TokenCategory.LOGICAL_OP)
    OP_GT = (auto(), '>', TokenCategory.LOGICAL_OP) 
    OP_GTE = (auto(), '>=', TokenCategory.LOGICAL_OP)
    OP_ANDAND = (auto(), '&&', TokenCategory.LOGICAL_OP)
    OP_OROR = (auto(), '||', TokenCategory.LOGICAL_OP)

    # Assignment
    ASSIGN = (auto(), '=', TokenCategory.ASSIGNMENT)

    # Separators / Punctuation
    LPAREN = (auto(), '(', TokenCategory.SEPARATOR)
    RPAREN = (auto(), ')', TokenCategory.SEPARATOR)
    LBRACE = (auto(), '{', TokenCategory.SEPARATOR)
    RBRACE = (auto(), '}', TokenCategory.SEPARATOR)
    COMMA = (auto(), ',', TokenCategory.SEPARATOR)

    # End of File
    EOF = (auto(), '<EOF>', TokenCategory.EOF)
    # Begin of Line
    BOL = (auto(), '<BOL>', TokenCategory.BOL)

    # Unknown / Error Token
    UNKNOWN = (auto(), '<unknown>', TokenCategory.UNKNOWN)

# Token Class
@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return (f"Token(type={self.type.name}, lexeme='{self.lexeme}', "
                f"value={repr(self.value)}, line={self.line}, col={self.column}, "
                f"cat='{self.type.category.name}')")

