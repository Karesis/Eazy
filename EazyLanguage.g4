grammar EazyLanguage;

// --- 语法规则 (Parser Rules) ---
program : statement* EOF ;

statement
    : labelDefinition
    | printStatement
    | ifGotoStatement
    | variableDeclarationStatement // 通用变量声明 (用于 int a; Point p;)
    | boxDefinitionStatement       // Box 类型定义 (例如: Point {int x, int y})
    | assignStatement
    | NEWLINE                      // 允许空行
    ;

labelDefinition
    : ID ':' NEWLINE
    ;

printStatement
    : PRINT commonExpression NEWLINE
    ;

ifGotoStatement
    : IF commonExpression GOTO ID NEWLINE
    ;

// Box 类型定义 (例如: Point {int x, int y})
// 注意：这里我们叫它 boxDefinitionStatement，但源码中是以 ID (类型名) 开头，而不是 "box" 关键字
boxDefinitionStatement
    : ID LBRACE memberDefinitionList RBRACE NEWLINE?
    ;

memberDefinitionList
    : typedMember (COMMA typedMember)*
    ;

// Box 中的成员定义
typedMember
    : typeSpecifier ID    # NamedMemberDefinition   // 例如: int x
    | typeSpecifier       # AnonymousMemberDefinition // 例如: int (匿名成员)
    ;

// 通用变量声明 (例如: int count NEWLINE  或  Point p1 NEWLINE)
variableDeclarationStatement
    : typeSpecifier ID NEWLINE
    ;

// 类型说明符，可以是基本类型 INT 或用户定义的 Box 类型名 (ID)
typeSpecifier
    : INT
    | ID  // 例如 Point, Color 等 Box 类型名
    ;

// 赋值语句
assignStatement
    : assignTarget ASSIGN commonExpression NEWLINE
    ;

// 赋值目标 (L-value)
assignTarget
    : ID                                                           # AssignToId         // a = ...
    | primaryExpression DOT ID                                     # AssignToMember     // p.x = ...
    | primaryExpression LBRACKET commonExpression RBRACKET         # AssignToIndex      // p[0] = ...
    ;

// 表达式规则
commonExpression
    : relationalExpression
    ;

relationalExpression
    : additiveExpression ( (ABOVE | UNDER | EQUAL) additiveExpression )?
    ;

additiveExpression
    : multiplicativeExpression ( (ADD | SUB) multiplicativeExpression )*
    ;

multiplicativeExpression
    : primaryExpression ( (MUL | DIV) primaryExpression )*
    ;

primaryExpression
    : NUMBER                                                     # NumberAtom
    | ID                                                         # IdAtom        // 单独的变量名
    | primaryExpression DOT ID                                   # MemberAccessExpr // 读取 p.x
    | primaryExpression LBRACKET commonExpression RBRACKET       # IndexAccessExpr  // 读取 p[0]
    | LPAREN commonExpression RPAREN                             # ParensExpr
    | SUB primaryExpression                                      # UnaryMinusExpr
    ;

// --- 词法规则 (Lexer Rules) ---
// Keywords
PRINT   : 'print';
IF      : 'if';
GOTO    : 'goto';
INT     : 'int'; // "int" 本身是一个类型关键字

// Identifiers
ID      : [a-zA-Z_] [a-zA-Z0-9_]* ; // 用于变量名、Box类型名、标签名、成员名

// Immediates (Literals)
NUMBER  : [0-9]+ ;

// Operators and Delimiters
MUL     : '*' ;
DIV     : '/' ;
ADD     : '+' ;
SUB     : '-' ;
ABOVE   : '>' ;
UNDER   : '<' ;
EQUAL   : '==' ;
ASSIGN  : '=' ;
LPAREN  : '(' ;
RPAREN  : ')' ;
COLON   : ':' ;
LBRACE  : '{' ; // {
RBRACE  : '}' ; // }
LBRACKET: '[' ; // [
RBRACKET: ']' ; // ]
COMMA   : ',' ; // ,
DOT     : '.' ; // .

// Newlines (Not skipped, used as statement terminator and for labelDefinition)
NEWLINE : ( '\r'? '\n' )+ ;

// Comments and Skips
LINE_COMMENT  : '#' ~[\r\n]* -> skip ;
WS            : [ \t]+ -> skip ;