// grammar/NyanLexer.g4

// 声明必须在第一行
lexer grammar NyanLexer;

options {
    superClass = NyanLexerBase;
}

// @header 和 @members 必须在声明之后
@lexer::header {
from .nyan_lexer_base import NyanLexerBase
}

@lexer::members {
    # This empty block ensures that the lexer class body is not empty
    # and the inheritance from NyanLexerBase is correctly placed.
}

tokens {
    INDENT,
    DEDENT
}

// --- Keywords (from Spec Section 2 & others) ---
AT: '@'; TRAIT: 'trait'; STRUCT: 'struct'; EXTERN: 'extern'; USE: 'use';
AS: 'as'; SUPER: 'super'; IF: 'if'; ELIF: 'elif'; ELSE: 'else'; FOR: 'for';
IN: 'in'; MATCH: 'match'; CASE: 'case'; DEFAULT: 'default'; RET: 'ret';
SPAWN: 'spawn'; CHAN: 'chan'; TYPE: 'type'; NAME: 'name'; SIZE: 'size';
COUNT: 'count'; ERR: 'err'; MOVE: 'move'; REL: 'rel'; UNSAFE: 'unsafe';
WHERE: 'where';

// --- Primitive Type Keywords (from Spec Section 3.1) ---
TYPE_INT: 'int'; TYPE_FLOAT: 'float'; TYPE_CHAR: 'char'; TYPE_BOOL: 'bool';

// --- Literals (from Spec Section 3.2) ---
BOOL_LITERAL: 'true' | 'false';
INT_LITERAL: [0-9]+;
FLOAT_LITERAL: [0-9]+ '.' [0-9]+;
CHAR_LITERAL: '\'' . '\'';
STRING_LITERAL: '"' (~["\r\n])* '"'; // For extern "C" etc.
NAME_LITERAL: '/' [a-zA-Z_] [a-zA-Z0-9_]* '/';

// --- Operators and Punctuation (from Spec Section 2) ---
ARROW: '<-';      // Concurrency
QUESTION: '?';     // Error propagation
DOT: '.';         // Access
DOUBLE_COLON: '::'; // Namespace access
AMPERSAND: '&';   // Pointer
TILDE: '~';       // Move shorthand

ASSIGN: '=';
PLUS: '+'; MINUS: '-'; MUL: '*'; DIV: '/'; MOD: '%';

EQUAL: '=='; NOT_EQUAL: '!='; LT: '<'; GT: '>'; LTE: '<='; GTE: '>=';
AND: 'and'; OR: 'or'; NOT: 'not';

LPAREN: '('; RPAREN: ')'; LBRACE: '{'; RBRACE: '}';
COMMA: ','; COLON: ':';

// --- Identifier ---
ID: [a-zA-Z_] [a-zA-Z0-9_]*;

// --- Whitespace, Comments, Newlines ---
COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t]+ -> skip;
// NEWLINE is handled by the Python superclass to inject INDENT/DEDENT tokens.
NEWLINE: ( '\r'? '\n' | '\r' );
