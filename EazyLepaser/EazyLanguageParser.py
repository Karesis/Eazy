# Generated from EazyLanguage.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,20,97,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,5,0,26,8,0,10,
        0,12,0,29,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,3,1,39,8,1,1,2,1,2,
        1,2,1,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,
        1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,8,1,8,1,8,3,8,69,8,8,1,9,1,9,1,9,5,
        9,74,8,9,10,9,12,9,77,9,9,1,10,1,10,1,10,5,10,82,8,10,10,10,12,10,
        85,9,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,95,8,11,1,11,
        0,0,12,0,2,4,6,8,10,12,14,16,18,20,22,0,3,1,0,11,13,1,0,9,10,1,0,
        7,8,96,0,27,1,0,0,0,2,38,1,0,0,0,4,40,1,0,0,0,6,44,1,0,0,0,8,48,
        1,0,0,0,10,54,1,0,0,0,12,58,1,0,0,0,14,63,1,0,0,0,16,65,1,0,0,0,
        18,70,1,0,0,0,20,78,1,0,0,0,22,94,1,0,0,0,24,26,3,2,1,0,25,24,1,
        0,0,0,26,29,1,0,0,0,27,25,1,0,0,0,27,28,1,0,0,0,28,30,1,0,0,0,29,
        27,1,0,0,0,30,31,5,0,0,1,31,1,1,0,0,0,32,39,3,4,2,0,33,39,3,6,3,
        0,34,39,3,8,4,0,35,39,3,10,5,0,36,39,3,12,6,0,37,39,5,18,0,0,38,
        32,1,0,0,0,38,33,1,0,0,0,38,34,1,0,0,0,38,35,1,0,0,0,38,36,1,0,0,
        0,38,37,1,0,0,0,39,3,1,0,0,0,40,41,5,5,0,0,41,42,5,17,0,0,42,43,
        5,18,0,0,43,5,1,0,0,0,44,45,5,1,0,0,45,46,3,14,7,0,46,47,5,18,0,
        0,47,7,1,0,0,0,48,49,5,2,0,0,49,50,3,14,7,0,50,51,5,3,0,0,51,52,
        5,5,0,0,52,53,5,18,0,0,53,9,1,0,0,0,54,55,5,4,0,0,55,56,5,5,0,0,
        56,57,5,18,0,0,57,11,1,0,0,0,58,59,5,5,0,0,59,60,5,14,0,0,60,61,
        3,14,7,0,61,62,5,18,0,0,62,13,1,0,0,0,63,64,3,16,8,0,64,15,1,0,0,
        0,65,68,3,18,9,0,66,67,7,0,0,0,67,69,3,18,9,0,68,66,1,0,0,0,68,69,
        1,0,0,0,69,17,1,0,0,0,70,75,3,20,10,0,71,72,7,1,0,0,72,74,3,20,10,
        0,73,71,1,0,0,0,74,77,1,0,0,0,75,73,1,0,0,0,75,76,1,0,0,0,76,19,
        1,0,0,0,77,75,1,0,0,0,78,83,3,22,11,0,79,80,7,2,0,0,80,82,3,22,11,
        0,81,79,1,0,0,0,82,85,1,0,0,0,83,81,1,0,0,0,83,84,1,0,0,0,84,21,
        1,0,0,0,85,83,1,0,0,0,86,95,5,6,0,0,87,95,5,5,0,0,88,89,5,15,0,0,
        89,90,3,14,7,0,90,91,5,16,0,0,91,95,1,0,0,0,92,93,5,10,0,0,93,95,
        3,22,11,0,94,86,1,0,0,0,94,87,1,0,0,0,94,88,1,0,0,0,94,92,1,0,0,
        0,95,23,1,0,0,0,6,27,38,68,75,83,94
    ]

class EazyLanguageParser ( Parser ):

    grammarFileName = "EazyLanguage.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "'if'", "'goto'", "'int'", 
                     "<INVALID>", "<INVALID>", "'*'", "'/'", "'+'", "'-'", 
                     "'>'", "'<'", "'=='", "'='", "'('", "')'", "':'" ]

    symbolicNames = [ "<INVALID>", "PRINT", "IF", "GOTO", "INT", "ID", "NUMBER", 
                      "MUL", "DIV", "ADD", "SUB", "ABOVE", "UNDER", "EQUAL", 
                      "ASSIGN", "LPAREN", "RPAREN", "COLON", "NEWLINE", 
                      "LINE_COMMENT", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_labelDefinition = 2
    RULE_printStatement = 3
    RULE_ifGotoStatement = 4
    RULE_boxStatement = 5
    RULE_assignStatement = 6
    RULE_commonExpression = 7
    RULE_relationalExpression = 8
    RULE_additiveExpression = 9
    RULE_multiplicativeExpression = 10
    RULE_primaryExpression = 11

    ruleNames =  [ "program", "statement", "labelDefinition", "printStatement", 
                   "ifGotoStatement", "boxStatement", "assignStatement", 
                   "commonExpression", "relationalExpression", "additiveExpression", 
                   "multiplicativeExpression", "primaryExpression" ]

    EOF = Token.EOF
    PRINT=1
    IF=2
    GOTO=3
    INT=4
    ID=5
    NUMBER=6
    MUL=7
    DIV=8
    ADD=9
    SUB=10
    ABOVE=11
    UNDER=12
    EQUAL=13
    ASSIGN=14
    LPAREN=15
    RPAREN=16
    COLON=17
    NEWLINE=18
    LINE_COMMENT=19
    WS=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(EazyLanguageParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EazyLanguageParser.StatementContext)
            else:
                return self.getTypedRuleContext(EazyLanguageParser.StatementContext,i)


        def getRuleIndex(self):
            return EazyLanguageParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = EazyLanguageParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 262198) != 0):
                self.state = 24
                self.statement()
                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 30
            self.match(EazyLanguageParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def labelDefinition(self):
            return self.getTypedRuleContext(EazyLanguageParser.LabelDefinitionContext,0)


        def printStatement(self):
            return self.getTypedRuleContext(EazyLanguageParser.PrintStatementContext,0)


        def ifGotoStatement(self):
            return self.getTypedRuleContext(EazyLanguageParser.IfGotoStatementContext,0)


        def boxStatement(self):
            return self.getTypedRuleContext(EazyLanguageParser.BoxStatementContext,0)


        def assignStatement(self):
            return self.getTypedRuleContext(EazyLanguageParser.AssignStatementContext,0)


        def NEWLINE(self):
            return self.getToken(EazyLanguageParser.NEWLINE, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = EazyLanguageParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 38
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 32
                self.labelDefinition()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 33
                self.printStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 34
                self.ifGotoStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 35
                self.boxStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 36
                self.assignStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 37
                self.match(EazyLanguageParser.NEWLINE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LabelDefinitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(EazyLanguageParser.ID, 0)

        def COLON(self):
            return self.getToken(EazyLanguageParser.COLON, 0)

        def NEWLINE(self):
            return self.getToken(EazyLanguageParser.NEWLINE, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_labelDefinition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabelDefinition" ):
                listener.enterLabelDefinition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabelDefinition" ):
                listener.exitLabelDefinition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLabelDefinition" ):
                return visitor.visitLabelDefinition(self)
            else:
                return visitor.visitChildren(self)




    def labelDefinition(self):

        localctx = EazyLanguageParser.LabelDefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_labelDefinition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(EazyLanguageParser.ID)
            self.state = 41
            self.match(EazyLanguageParser.COLON)
            self.state = 42
            self.match(EazyLanguageParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(EazyLanguageParser.PRINT, 0)

        def commonExpression(self):
            return self.getTypedRuleContext(EazyLanguageParser.CommonExpressionContext,0)


        def NEWLINE(self):
            return self.getToken(EazyLanguageParser.NEWLINE, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_printStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStatement" ):
                listener.enterPrintStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStatement" ):
                listener.exitPrintStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStatement" ):
                return visitor.visitPrintStatement(self)
            else:
                return visitor.visitChildren(self)




    def printStatement(self):

        localctx = EazyLanguageParser.PrintStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_printStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(EazyLanguageParser.PRINT)
            self.state = 45
            self.commonExpression()
            self.state = 46
            self.match(EazyLanguageParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfGotoStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(EazyLanguageParser.IF, 0)

        def commonExpression(self):
            return self.getTypedRuleContext(EazyLanguageParser.CommonExpressionContext,0)


        def GOTO(self):
            return self.getToken(EazyLanguageParser.GOTO, 0)

        def ID(self):
            return self.getToken(EazyLanguageParser.ID, 0)

        def NEWLINE(self):
            return self.getToken(EazyLanguageParser.NEWLINE, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_ifGotoStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfGotoStatement" ):
                listener.enterIfGotoStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfGotoStatement" ):
                listener.exitIfGotoStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfGotoStatement" ):
                return visitor.visitIfGotoStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifGotoStatement(self):

        localctx = EazyLanguageParser.IfGotoStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_ifGotoStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(EazyLanguageParser.IF)
            self.state = 49
            self.commonExpression()
            self.state = 50
            self.match(EazyLanguageParser.GOTO)
            self.state = 51
            self.match(EazyLanguageParser.ID)
            self.state = 52
            self.match(EazyLanguageParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoxStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(EazyLanguageParser.INT, 0)

        def ID(self):
            return self.getToken(EazyLanguageParser.ID, 0)

        def NEWLINE(self):
            return self.getToken(EazyLanguageParser.NEWLINE, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_boxStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoxStatement" ):
                listener.enterBoxStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoxStatement" ):
                listener.exitBoxStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoxStatement" ):
                return visitor.visitBoxStatement(self)
            else:
                return visitor.visitChildren(self)




    def boxStatement(self):

        localctx = EazyLanguageParser.BoxStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_boxStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.match(EazyLanguageParser.INT)
            self.state = 55
            self.match(EazyLanguageParser.ID)
            self.state = 56
            self.match(EazyLanguageParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(EazyLanguageParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(EazyLanguageParser.ASSIGN, 0)

        def commonExpression(self):
            return self.getTypedRuleContext(EazyLanguageParser.CommonExpressionContext,0)


        def NEWLINE(self):
            return self.getToken(EazyLanguageParser.NEWLINE, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_assignStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStatement" ):
                listener.enterAssignStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStatement" ):
                listener.exitAssignStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStatement" ):
                return visitor.visitAssignStatement(self)
            else:
                return visitor.visitChildren(self)




    def assignStatement(self):

        localctx = EazyLanguageParser.AssignStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_assignStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(EazyLanguageParser.ID)
            self.state = 59
            self.match(EazyLanguageParser.ASSIGN)
            self.state = 60
            self.commonExpression()
            self.state = 61
            self.match(EazyLanguageParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommonExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relationalExpression(self):
            return self.getTypedRuleContext(EazyLanguageParser.RelationalExpressionContext,0)


        def getRuleIndex(self):
            return EazyLanguageParser.RULE_commonExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommonExpression" ):
                listener.enterCommonExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommonExpression" ):
                listener.exitCommonExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommonExpression" ):
                return visitor.visitCommonExpression(self)
            else:
                return visitor.visitChildren(self)




    def commonExpression(self):

        localctx = EazyLanguageParser.CommonExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_commonExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.relationalExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EazyLanguageParser.AdditiveExpressionContext)
            else:
                return self.getTypedRuleContext(EazyLanguageParser.AdditiveExpressionContext,i)


        def ABOVE(self):
            return self.getToken(EazyLanguageParser.ABOVE, 0)

        def UNDER(self):
            return self.getToken(EazyLanguageParser.UNDER, 0)

        def EQUAL(self):
            return self.getToken(EazyLanguageParser.EQUAL, 0)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_relationalExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalExpression" ):
                listener.enterRelationalExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalExpression" ):
                listener.exitRelationalExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpression" ):
                return visitor.visitRelationalExpression(self)
            else:
                return visitor.visitChildren(self)




    def relationalExpression(self):

        localctx = EazyLanguageParser.RelationalExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_relationalExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.additiveExpression()
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0):
                self.state = 66
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 67
                self.additiveExpression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EazyLanguageParser.MultiplicativeExpressionContext)
            else:
                return self.getTypedRuleContext(EazyLanguageParser.MultiplicativeExpressionContext,i)


        def ADD(self, i:int=None):
            if i is None:
                return self.getTokens(EazyLanguageParser.ADD)
            else:
                return self.getToken(EazyLanguageParser.ADD, i)

        def SUB(self, i:int=None):
            if i is None:
                return self.getTokens(EazyLanguageParser.SUB)
            else:
                return self.getToken(EazyLanguageParser.SUB, i)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_additiveExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpression" ):
                listener.enterAdditiveExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpression" ):
                listener.exitAdditiveExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpression" ):
                return visitor.visitAdditiveExpression(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpression(self):

        localctx = EazyLanguageParser.AdditiveExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_additiveExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.multiplicativeExpression()
            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9 or _la==10:
                self.state = 71
                _la = self._input.LA(1)
                if not(_la==9 or _la==10):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 72
                self.multiplicativeExpression()
                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primaryExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(EazyLanguageParser.PrimaryExpressionContext)
            else:
                return self.getTypedRuleContext(EazyLanguageParser.PrimaryExpressionContext,i)


        def MUL(self, i:int=None):
            if i is None:
                return self.getTokens(EazyLanguageParser.MUL)
            else:
                return self.getToken(EazyLanguageParser.MUL, i)

        def DIV(self, i:int=None):
            if i is None:
                return self.getTokens(EazyLanguageParser.DIV)
            else:
                return self.getToken(EazyLanguageParser.DIV, i)

        def getRuleIndex(self):
            return EazyLanguageParser.RULE_multiplicativeExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpression" ):
                listener.enterMultiplicativeExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpression" ):
                listener.exitMultiplicativeExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpression" ):
                return visitor.visitMultiplicativeExpression(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpression(self):

        localctx = EazyLanguageParser.MultiplicativeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_multiplicativeExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.primaryExpression()
            self.state = 83
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7 or _la==8:
                self.state = 79
                _la = self._input.LA(1)
                if not(_la==7 or _la==8):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 80
                self.primaryExpression()
                self.state = 85
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return EazyLanguageParser.RULE_primaryExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NumberAtomContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EazyLanguageParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(EazyLanguageParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberAtom" ):
                listener.enterNumberAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberAtom" ):
                listener.exitNumberAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberAtom" ):
                return visitor.visitNumberAtom(self)
            else:
                return visitor.visitChildren(self)


    class ParensExprContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EazyLanguageParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(EazyLanguageParser.LPAREN, 0)
        def commonExpression(self):
            return self.getTypedRuleContext(EazyLanguageParser.CommonExpressionContext,0)

        def RPAREN(self):
            return self.getToken(EazyLanguageParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParensExpr" ):
                listener.enterParensExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParensExpr" ):
                listener.exitParensExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParensExpr" ):
                return visitor.visitParensExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdAtomContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EazyLanguageParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(EazyLanguageParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdAtom" ):
                listener.enterIdAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdAtom" ):
                listener.exitIdAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdAtom" ):
                return visitor.visitIdAtom(self)
            else:
                return visitor.visitChildren(self)


    class UnaryMinusExprContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a EazyLanguageParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SUB(self):
            return self.getToken(EazyLanguageParser.SUB, 0)
        def primaryExpression(self):
            return self.getTypedRuleContext(EazyLanguageParser.PrimaryExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryMinusExpr" ):
                listener.enterUnaryMinusExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryMinusExpr" ):
                listener.exitUnaryMinusExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryMinusExpr" ):
                return visitor.visitUnaryMinusExpr(self)
            else:
                return visitor.visitChildren(self)



    def primaryExpression(self):

        localctx = EazyLanguageParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_primaryExpression)
        try:
            self.state = 94
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                localctx = EazyLanguageParser.NumberAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.match(EazyLanguageParser.NUMBER)
                pass
            elif token in [5]:
                localctx = EazyLanguageParser.IdAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.match(EazyLanguageParser.ID)
                pass
            elif token in [15]:
                localctx = EazyLanguageParser.ParensExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 88
                self.match(EazyLanguageParser.LPAREN)
                self.state = 89
                self.commonExpression()
                self.state = 90
                self.match(EazyLanguageParser.RPAREN)
                pass
            elif token in [10]:
                localctx = EazyLanguageParser.UnaryMinusExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 92
                self.match(EazyLanguageParser.SUB)
                self.state = 93
                self.primaryExpression()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





