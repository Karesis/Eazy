# Generated from EazyLanguage.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .EazyLanguageParser import EazyLanguageParser
else:
    from EazyLanguageParser import EazyLanguageParser

# This class defines a complete listener for a parse tree produced by EazyLanguageParser.
class EazyLanguageListener(ParseTreeListener):

    # Enter a parse tree produced by EazyLanguageParser#program.
    def enterProgram(self, ctx:EazyLanguageParser.ProgramContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#program.
    def exitProgram(self, ctx:EazyLanguageParser.ProgramContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#statement.
    def enterStatement(self, ctx:EazyLanguageParser.StatementContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#statement.
    def exitStatement(self, ctx:EazyLanguageParser.StatementContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#labelDefinition.
    def enterLabelDefinition(self, ctx:EazyLanguageParser.LabelDefinitionContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#labelDefinition.
    def exitLabelDefinition(self, ctx:EazyLanguageParser.LabelDefinitionContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#printStatement.
    def enterPrintStatement(self, ctx:EazyLanguageParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#printStatement.
    def exitPrintStatement(self, ctx:EazyLanguageParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#ifGotoStatement.
    def enterIfGotoStatement(self, ctx:EazyLanguageParser.IfGotoStatementContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#ifGotoStatement.
    def exitIfGotoStatement(self, ctx:EazyLanguageParser.IfGotoStatementContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#boxStatement.
    def enterBoxStatement(self, ctx:EazyLanguageParser.BoxStatementContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#boxStatement.
    def exitBoxStatement(self, ctx:EazyLanguageParser.BoxStatementContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#assignStatement.
    def enterAssignStatement(self, ctx:EazyLanguageParser.AssignStatementContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#assignStatement.
    def exitAssignStatement(self, ctx:EazyLanguageParser.AssignStatementContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#commonExpression.
    def enterCommonExpression(self, ctx:EazyLanguageParser.CommonExpressionContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#commonExpression.
    def exitCommonExpression(self, ctx:EazyLanguageParser.CommonExpressionContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#relationalExpression.
    def enterRelationalExpression(self, ctx:EazyLanguageParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#relationalExpression.
    def exitRelationalExpression(self, ctx:EazyLanguageParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:EazyLanguageParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:EazyLanguageParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:EazyLanguageParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:EazyLanguageParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#NumberAtom.
    def enterNumberAtom(self, ctx:EazyLanguageParser.NumberAtomContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#NumberAtom.
    def exitNumberAtom(self, ctx:EazyLanguageParser.NumberAtomContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#IdAtom.
    def enterIdAtom(self, ctx:EazyLanguageParser.IdAtomContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#IdAtom.
    def exitIdAtom(self, ctx:EazyLanguageParser.IdAtomContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#ParensExpr.
    def enterParensExpr(self, ctx:EazyLanguageParser.ParensExprContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#ParensExpr.
    def exitParensExpr(self, ctx:EazyLanguageParser.ParensExprContext):
        pass


    # Enter a parse tree produced by EazyLanguageParser#UnaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:EazyLanguageParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by EazyLanguageParser#UnaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:EazyLanguageParser.UnaryMinusExprContext):
        pass



del EazyLanguageParser