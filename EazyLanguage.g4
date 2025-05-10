grammar EazyLanguage;

// --- 语法规则 (Parser Rules) ---
program : statement* EOF ;

statement
    : labelDefinition      // 新增：标签定义语句
    | printStatement
    | ifGotoStatement
    | boxStatement
    | assignStatement
    | NEWLINE              // 允许空行
    ;

labelDefinition
    : ID ':' NEWLINE       // 例如: myLabel: NEWLINE
    ;

printStatement
    : PRINT commonExpression NEWLINE
    ;

ifGotoStatement
    : IF commonExpression GOTO ID NEWLINE // commonExpression 现在可以包含比较了
    ;

boxStatement
    : INT ID NEWLINE // INT 是 'int' 关键字
    ;

assignStatement 
    : ID ASSIGN commonExpression NEWLINE
    ;

// 表达式规则
commonExpression
    : relationalExpression // 表达式的顶层是关系表达式
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
    : NUMBER             # NumberAtom
    | ID                 # IdAtom
    | LPAREN commonExpression RPAREN # ParensExpr
    | SUB primaryExpression # UnaryMinusExpr
    ;

// --- 词法规则 (Lexer Rules) ---
// Keywords
PRINT   : 'print';
IF      : 'if';
GOTO    : 'goto';
INT     : 'int'; // 关键字 "int"

// Identifiers
ID      : [a-zA-Z_] [a-zA-Z0-9_]* ;

// Immediates (Literals)
NUMBER  : [0-9]+ ;

// Operators
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

// Newlines (Not skipped, used as statement terminator and for labelDefinition)
NEWLINE : ( '\r'? '\n' )+ ;

// Comments and Skips
LINE_COMMENT  : '#' ~[\r\n]* -> skip ;
WS            : [ \t]+ -> skip ;

