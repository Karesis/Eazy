// grammar/Definitions.g4
parser grammar Definitions;
options { tokenVocab=NyanLexer; }
import Statements, Expressions;

top_level_def:
    use_def
    | block_def
    | trait_def
    | extern_def;

block_def:
    AT ID (LT generic_params GT)? (LPAREN func_params? RPAREN)? 
    (
        COLON inheritance (WHERE where_clause)? block
    |   (WHERE where_clause)? block 
    )
    ;

func_params: typed_param (COMMA typed_param)*;
typed_param: type_spec ID;

generic_params: ID (COMMA ID)*;
inheritance: type_spec;
where_clause: type_spec COLON type_spec (COMMA type_spec COLON type_spec)*;

trait_def: TRAIT ID block;

use_def: USE path (
    DOUBLE_COLON (
        MUL
        | ID (AS ID)?
        | INDENT use_members DEDENT
    )
)?;
path: ID (DOUBLE_COLON ID)*;
use_members: use_member (COMMA use_member)*;
use_member: ID (AS ID)?;

extern_def: EXTERN STRING_LITERAL block;
