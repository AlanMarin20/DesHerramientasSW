# Generated from /home/alan/dhs/dhs2024/src/main/python/dhs2024/compiladores.g4 by ANTLR 4.13.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,40,228,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,
        1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,
        1,12,1,12,1,13,1,13,1,14,1,14,1,14,1,15,1,15,1,15,1,16,1,16,1,17,
        1,17,1,17,1,18,1,18,1,18,1,19,1,19,1,20,1,20,1,20,1,21,1,21,1,21,
        1,22,1,22,1,23,1,23,1,23,1,24,1,24,1,25,1,25,1,26,1,26,1,26,1,27,
        1,27,1,27,1,28,4,28,152,8,28,11,28,12,28,153,1,29,1,29,1,29,1,29,
        1,30,1,30,1,30,1,30,1,30,1,31,1,31,1,31,1,31,1,31,1,31,1,32,1,32,
        1,32,1,32,1,32,1,33,1,33,1,33,1,33,1,33,1,33,1,33,1,34,1,34,1,34,
        1,34,1,34,1,35,1,35,1,35,1,35,1,35,1,35,1,35,1,36,1,36,1,36,1,36,
        1,36,1,36,1,37,1,37,1,37,1,37,1,38,1,38,1,38,1,39,1,39,1,39,1,39,
        1,39,1,40,1,40,1,40,1,40,1,41,1,41,3,41,219,8,41,1,41,1,41,1,41,
        5,41,224,8,41,10,41,12,41,227,9,41,0,0,42,1,0,3,0,5,1,7,2,9,3,11,
        4,13,5,15,6,17,7,19,8,21,9,23,10,25,11,27,12,29,13,31,14,33,15,35,
        16,37,17,39,18,41,19,43,20,45,21,47,22,49,23,51,24,53,25,55,26,57,
        27,59,28,61,29,63,30,65,31,67,32,69,33,71,34,73,35,75,36,77,37,79,
        38,81,39,83,40,1,0,3,2,0,65,90,97,122,1,0,48,57,3,0,9,10,13,13,32,
        32,230,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,
        0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,
        0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,
        0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,
        0,0,0,45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,
        0,0,0,55,1,0,0,0,0,57,1,0,0,0,0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,
        0,0,0,65,1,0,0,0,0,67,1,0,0,0,0,69,1,0,0,0,0,71,1,0,0,0,0,73,1,0,
        0,0,0,75,1,0,0,0,0,77,1,0,0,0,0,79,1,0,0,0,0,81,1,0,0,0,0,83,1,0,
        0,0,1,85,1,0,0,0,3,87,1,0,0,0,5,89,1,0,0,0,7,91,1,0,0,0,9,93,1,0,
        0,0,11,95,1,0,0,0,13,97,1,0,0,0,15,99,1,0,0,0,17,101,1,0,0,0,19,
        103,1,0,0,0,21,105,1,0,0,0,23,107,1,0,0,0,25,109,1,0,0,0,27,111,
        1,0,0,0,29,113,1,0,0,0,31,116,1,0,0,0,33,119,1,0,0,0,35,121,1,0,
        0,0,37,124,1,0,0,0,39,127,1,0,0,0,41,129,1,0,0,0,43,132,1,0,0,0,
        45,135,1,0,0,0,47,137,1,0,0,0,49,140,1,0,0,0,51,142,1,0,0,0,53,144,
        1,0,0,0,55,147,1,0,0,0,57,151,1,0,0,0,59,155,1,0,0,0,61,159,1,0,
        0,0,63,164,1,0,0,0,65,170,1,0,0,0,67,175,1,0,0,0,69,182,1,0,0,0,
        71,187,1,0,0,0,73,194,1,0,0,0,75,200,1,0,0,0,77,204,1,0,0,0,79,207,
        1,0,0,0,81,212,1,0,0,0,83,218,1,0,0,0,85,86,7,0,0,0,86,2,1,0,0,0,
        87,88,7,1,0,0,88,4,1,0,0,0,89,90,5,40,0,0,90,6,1,0,0,0,91,92,5,41,
        0,0,92,8,1,0,0,0,93,94,5,123,0,0,94,10,1,0,0,0,95,96,5,125,0,0,96,
        12,1,0,0,0,97,98,5,59,0,0,98,14,1,0,0,0,99,100,5,44,0,0,100,16,1,
        0,0,0,101,102,5,43,0,0,102,18,1,0,0,0,103,104,5,45,0,0,104,20,1,
        0,0,0,105,106,5,42,0,0,106,22,1,0,0,0,107,108,5,47,0,0,108,24,1,
        0,0,0,109,110,5,37,0,0,110,26,1,0,0,0,111,112,5,61,0,0,112,28,1,
        0,0,0,113,114,5,43,0,0,114,115,5,43,0,0,115,30,1,0,0,0,116,117,5,
        45,0,0,117,118,5,45,0,0,118,32,1,0,0,0,119,120,5,62,0,0,120,34,1,
        0,0,0,121,122,5,62,0,0,122,123,5,61,0,0,123,36,1,0,0,0,124,125,5,
        60,0,0,125,126,5,61,0,0,126,38,1,0,0,0,127,128,5,60,0,0,128,40,1,
        0,0,0,129,130,5,61,0,0,130,131,5,61,0,0,131,42,1,0,0,0,132,133,5,
        38,0,0,133,134,5,38,0,0,134,44,1,0,0,0,135,136,5,38,0,0,136,46,1,
        0,0,0,137,138,5,124,0,0,138,139,5,124,0,0,139,48,1,0,0,0,140,141,
        5,124,0,0,141,50,1,0,0,0,142,143,5,94,0,0,143,52,1,0,0,0,144,145,
        5,60,0,0,145,146,5,60,0,0,146,54,1,0,0,0,147,148,5,62,0,0,148,149,
        5,62,0,0,149,56,1,0,0,0,150,152,3,3,1,0,151,150,1,0,0,0,152,153,
        1,0,0,0,153,151,1,0,0,0,153,154,1,0,0,0,154,58,1,0,0,0,155,156,5,
        105,0,0,156,157,5,110,0,0,157,158,5,116,0,0,158,60,1,0,0,0,159,160,
        5,99,0,0,160,161,5,104,0,0,161,162,5,97,0,0,162,163,5,114,0,0,163,
        62,1,0,0,0,164,165,5,102,0,0,165,166,5,108,0,0,166,167,5,111,0,0,
        167,168,5,97,0,0,168,169,5,116,0,0,169,64,1,0,0,0,170,171,5,98,0,
        0,171,172,5,111,0,0,172,173,5,111,0,0,173,174,5,108,0,0,174,66,1,
        0,0,0,175,176,5,100,0,0,176,177,5,111,0,0,177,178,5,117,0,0,178,
        179,5,98,0,0,179,180,5,108,0,0,180,181,5,101,0,0,181,68,1,0,0,0,
        182,183,5,118,0,0,183,184,5,111,0,0,184,185,5,105,0,0,185,186,5,
        100,0,0,186,70,1,0,0,0,187,188,5,114,0,0,188,189,5,101,0,0,189,190,
        5,116,0,0,190,191,5,117,0,0,191,192,5,114,0,0,192,193,5,110,0,0,
        193,72,1,0,0,0,194,195,5,119,0,0,195,196,5,104,0,0,196,197,5,105,
        0,0,197,198,5,108,0,0,198,199,5,101,0,0,199,74,1,0,0,0,200,201,5,
        102,0,0,201,202,5,111,0,0,202,203,5,114,0,0,203,76,1,0,0,0,204,205,
        5,105,0,0,205,206,5,102,0,0,206,78,1,0,0,0,207,208,5,101,0,0,208,
        209,5,108,0,0,209,210,5,115,0,0,210,211,5,101,0,0,211,80,1,0,0,0,
        212,213,7,2,0,0,213,214,1,0,0,0,214,215,6,40,0,0,215,82,1,0,0,0,
        216,219,3,1,0,0,217,219,5,95,0,0,218,216,1,0,0,0,218,217,1,0,0,0,
        219,225,1,0,0,0,220,224,3,1,0,0,221,224,3,3,1,0,222,224,5,95,0,0,
        223,220,1,0,0,0,223,221,1,0,0,0,223,222,1,0,0,0,224,227,1,0,0,0,
        225,223,1,0,0,0,225,226,1,0,0,0,226,84,1,0,0,0,227,225,1,0,0,0,5,
        0,153,218,223,225,1,6,0,0
    ]

class compiladoresLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    PA = 1
    PC = 2
    LLA = 3
    LLC = 4
    PYC = 5
    COMA = 6
    SUMA = 7
    RESTA = 8
    MULT = 9
    DIV = 10
    MOD = 11
    ASIG = 12
    INCR = 13
    DECR = 14
    MAYOR = 15
    MAYOREQ = 16
    MENOREQ = 17
    MENOR = 18
    IGUAL = 19
    AND = 20
    ANDsim = 21
    OR = 22
    ORsim = 23
    POT = 24
    DESPizq = 25
    DESPder = 26
    NUMERO = 27
    INT = 28
    CHAR = 29
    FLOAT = 30
    BOOLEAN = 31
    DOUBLE = 32
    VOID = 33
    RETURN = 34
    WHILE = 35
    FOR = 36
    IF = 37
    ELSE = 38
    WS = 39
    ID = 40

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'{'", "'}'", "';'", "','", "'+'", "'-'", "'*'", 
            "'/'", "'%'", "'='", "'++'", "'--'", "'>'", "'>='", "'<='", 
            "'<'", "'=='", "'&&'", "'&'", "'||'", "'|'", "'^'", "'<<'", 
            "'>>'", "'int'", "'char'", "'float'", "'bool'", "'double'", 
            "'void'", "'return'", "'while'", "'for'", "'if'", "'else'" ]

    symbolicNames = [ "<INVALID>",
            "PA", "PC", "LLA", "LLC", "PYC", "COMA", "SUMA", "RESTA", "MULT", 
            "DIV", "MOD", "ASIG", "INCR", "DECR", "MAYOR", "MAYOREQ", "MENOREQ", 
            "MENOR", "IGUAL", "AND", "ANDsim", "OR", "ORsim", "POT", "DESPizq", 
            "DESPder", "NUMERO", "INT", "CHAR", "FLOAT", "BOOLEAN", "DOUBLE", 
            "VOID", "RETURN", "WHILE", "FOR", "IF", "ELSE", "WS", "ID" ]

    ruleNames = [ "LETRA", "DIGITO", "PA", "PC", "LLA", "LLC", "PYC", "COMA", 
                  "SUMA", "RESTA", "MULT", "DIV", "MOD", "ASIG", "INCR", 
                  "DECR", "MAYOR", "MAYOREQ", "MENOREQ", "MENOR", "IGUAL", 
                  "AND", "ANDsim", "OR", "ORsim", "POT", "DESPizq", "DESPder", 
                  "NUMERO", "INT", "CHAR", "FLOAT", "BOOLEAN", "DOUBLE", 
                  "VOID", "RETURN", "WHILE", "FOR", "IF", "ELSE", "WS", 
                  "ID" ]

    grammarFileName = "compiladores.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


