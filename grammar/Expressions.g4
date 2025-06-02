// grammar/Expressions.g4
parser grammar Expressions;
options { tokenVocab=NyanLexer; }

expression: assignment_expr;

assignment_expr: channel_send_expr (ASSIGN assignment_expr)?;
channel_send_expr: logical_or_expr (ARROW logical_or_expr)?;
logical_or_expr: logical_and_expr (OR logical_and_expr)*;
logical_and_expr: equality_expr (AND equality_expr)*;
equality_expr: comparison_expr ((EQUAL | NOT_EQUAL) comparison_expr)*;
comparison_expr: additive_expr ((LT | GT | LTE | GTE) additive_expr)*;
additive_expr: multiplicative_expr ((PLUS | MINUS) multiplicative_expr)*;
multiplicative_expr: unary_expr ((MUL | DIV | MOD) unary_expr)*;

unary_expr:
    (PLUS | MINUS | NOT | AMPERSAND | MUL | TILDE | MOVE) unary_expr
    | postfix_expr;

postfix_expr:
    primary_expr (
          DOT ID
        | LPAREN call_args? RPAREN
        | QUESTION
        | LT type_args GT
    )*;

call_args: expression (COMMA expression)*;

primary_expr:
    LPAREN expression RPAREN
    | literal
    | ID
    | meta_function_call;

literal:
    INT_LITERAL | FLOAT_LITERAL | CHAR_LITERAL | BOOL_LITERAL
    | name_literal
    | type_literal;

name_literal: NAME_LITERAL;
type_literal: LT type_spec GT;

meta_function_call: (TYPE | SIZE | COUNT | NAME) LPAREN expression RPAREN;

type_spec: ID (LT type_args GT)?;
type_args: type_spec (COMMA type_spec)*;
