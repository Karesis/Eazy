// grammar/Nyan.g4
grammar Nyan;
options { tokenVocab=NyanLexer; }
import Definitions, Statements, Expressions;

// A program is a sequence of top-level definitions and statements
program: (top_level_def | statement)? (NEWLINE (top_level_def | statement)?)* EOF;
