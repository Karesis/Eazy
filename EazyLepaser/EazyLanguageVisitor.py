# Generated from EazyLanguage.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .EazyLanguageParser import EazyLanguageParser
else:
    from EazyLanguageParser import EazyLanguageParser

# This class defines a complete generic visitor for a parse tree produced by EazyLanguageParser.

class EazyLanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by EazyLanguageParser#program.
    def visitProgram(self, ctx:EazyLanguageParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#statement.
    def visitStatement(self, ctx:EazyLanguageParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#labelDefinition.
    def visitLabelDefinition(self, ctx:EazyLanguageParser.LabelDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#printStatement.
    def visitPrintStatement(self, ctx:EazyLanguageParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#ifGotoStatement.
    def visitIfGotoStatement(self, ctx:EazyLanguageParser.IfGotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#boxStatement.
    def visitBoxStatement(self, ctx:EazyLanguageParser.BoxStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#assignStatement.
    def visitAssignStatement(self, ctx:EazyLanguageParser.AssignStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#commonExpression.
    def visitCommonExpression(self, ctx:EazyLanguageParser.CommonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#relationalExpression.
    def visitRelationalExpression(self, ctx:EazyLanguageParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:EazyLanguageParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:EazyLanguageParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#NumberAtom.
    def visitNumberAtom(self, ctx:EazyLanguageParser.NumberAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#IdAtom.
    def visitIdAtom(self, ctx:EazyLanguageParser.IdAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#ParensExpr.
    def visitParensExpr(self, ctx:EazyLanguageParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EazyLanguageParser#UnaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:EazyLanguageParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)



del EazyLanguageParser