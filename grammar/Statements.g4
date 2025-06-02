// grammar/Statements.g4
parser grammar Statements;
options { tokenVocab=NyanLexer; }
import Expressions;

statement:
    simple_stmt
    | compound_stmt;

simple_stmt:
    variable_decl
    | expression
    | return_stmt;

compound_stmt:
    if_stmt
    | for_stmt
    | match_stmt
    | unsafe_block; // Added unsafe block here

block: INDENT statement+ DEDENT;

variable_decl: type_spec ID (ASSIGN expression)?;
return_stmt: RET expression?;
unsafe_block: UNSAFE block;

if_stmt: IF expression block (ELIF expression block)* (ELSE block)?;
for_stmt: FOR ID IN expression block;

match_stmt: MATCH expression INDENT case_clause+ DEDENT;
case_clause:
    CASE pattern (IF expression)? block
    | DEFAULT block;
pattern:
    literal
    | type_spec ID?;
