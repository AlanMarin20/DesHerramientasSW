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
        4,0,44,244,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,
        45,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,
        7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,1,12,1,13,1,13,1,14,1,
        14,1,15,1,15,1,16,1,16,1,17,1,17,1,18,1,18,1,18,1,19,1,19,1,19,1,
        20,1,20,1,21,1,21,1,21,1,22,1,22,1,22,1,23,1,23,1,24,1,24,1,24,1,
        25,1,25,1,25,1,26,1,26,1,27,1,27,1,27,1,28,1,28,1,29,1,29,1,30,1,
        30,1,30,1,31,1,31,1,31,1,32,4,32,168,8,32,11,32,12,32,169,1,33,1,
        33,1,33,1,33,1,34,1,34,1,34,1,34,1,34,1,35,1,35,1,35,1,35,1,35,1,
        35,1,36,1,36,1,36,1,36,1,36,1,37,1,37,1,37,1,37,1,37,1,37,1,37,1,
        38,1,38,1,38,1,38,1,38,1,39,1,39,1,39,1,39,1,39,1,39,1,39,1,40,1,
        40,1,40,1,40,1,40,1,40,1,41,1,41,1,41,1,41,1,42,1,42,1,42,1,43,1,
        43,1,43,1,43,1,43,1,44,1,44,1,44,1,44,1,45,1,45,3,45,235,8,45,1,
        45,1,45,1,45,5,45,240,8,45,10,45,12,45,243,9,45,0,0,46,1,0,3,0,5,
        1,7,2,9,3,11,4,13,5,15,6,17,7,19,8,21,9,23,10,25,11,27,12,29,13,
        31,14,33,15,35,16,37,17,39,18,41,19,43,20,45,21,47,22,49,23,51,24,
        53,25,55,26,57,27,59,28,61,29,63,30,65,31,67,32,69,33,71,34,73,35,
        75,36,77,37,79,38,81,39,83,40,85,41,87,42,89,43,91,44,1,0,3,2,0,
        65,90,97,122,1,0,48,57,3,0,9,10,13,13,32,32,246,0,5,1,0,0,0,0,7,
        1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,
        1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,
        1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,
        1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,0,47,
        1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,0,55,1,0,0,0,0,57,
        1,0,0,0,0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,0,0,0,0,67,
        1,0,0,0,0,69,1,0,0,0,0,71,1,0,0,0,0,73,1,0,0,0,0,75,1,0,0,0,0,77,
        1,0,0,0,0,79,1,0,0,0,0,81,1,0,0,0,0,83,1,0,0,0,0,85,1,0,0,0,0,87,
        1,0,0,0,0,89,1,0,0,0,0,91,1,0,0,0,1,93,1,0,0,0,3,95,1,0,0,0,5,97,
        1,0,0,0,7,99,1,0,0,0,9,101,1,0,0,0,11,103,1,0,0,0,13,105,1,0,0,0,
        15,107,1,0,0,0,17,109,1,0,0,0,19,111,1,0,0,0,21,113,1,0,0,0,23,115,
        1,0,0,0,25,117,1,0,0,0,27,119,1,0,0,0,29,121,1,0,0,0,31,123,1,0,
        0,0,33,125,1,0,0,0,35,127,1,0,0,0,37,129,1,0,0,0,39,132,1,0,0,0,
        41,135,1,0,0,0,43,137,1,0,0,0,45,140,1,0,0,0,47,143,1,0,0,0,49,145,
        1,0,0,0,51,148,1,0,0,0,53,151,1,0,0,0,55,153,1,0,0,0,57,156,1,0,
        0,0,59,158,1,0,0,0,61,160,1,0,0,0,63,163,1,0,0,0,65,167,1,0,0,0,
        67,171,1,0,0,0,69,175,1,0,0,0,71,180,1,0,0,0,73,186,1,0,0,0,75,191,
        1,0,0,0,77,198,1,0,0,0,79,203,1,0,0,0,81,210,1,0,0,0,83,216,1,0,
        0,0,85,220,1,0,0,0,87,223,1,0,0,0,89,228,1,0,0,0,91,234,1,0,0,0,
        93,94,7,0,0,0,94,2,1,0,0,0,95,96,7,1,0,0,96,4,1,0,0,0,97,98,5,40,
        0,0,98,6,1,0,0,0,99,100,5,41,0,0,100,8,1,0,0,0,101,102,5,123,0,0,
        102,10,1,0,0,0,103,104,5,125,0,0,104,12,1,0,0,0,105,106,5,91,0,0,
        106,14,1,0,0,0,107,108,5,93,0,0,108,16,1,0,0,0,109,110,5,39,0,0,
        110,18,1,0,0,0,111,112,5,34,0,0,112,20,1,0,0,0,113,114,5,59,0,0,
        114,22,1,0,0,0,115,116,5,44,0,0,116,24,1,0,0,0,117,118,5,43,0,0,
        118,26,1,0,0,0,119,120,5,45,0,0,120,28,1,0,0,0,121,122,5,42,0,0,
        122,30,1,0,0,0,123,124,5,47,0,0,124,32,1,0,0,0,125,126,5,37,0,0,
        126,34,1,0,0,0,127,128,5,61,0,0,128,36,1,0,0,0,129,130,5,43,0,0,
        130,131,5,43,0,0,131,38,1,0,0,0,132,133,5,45,0,0,133,134,5,45,0,
        0,134,40,1,0,0,0,135,136,5,62,0,0,136,42,1,0,0,0,137,138,5,62,0,
        0,138,139,5,61,0,0,139,44,1,0,0,0,140,141,5,60,0,0,141,142,5,61,
        0,0,142,46,1,0,0,0,143,144,5,60,0,0,144,48,1,0,0,0,145,146,5,61,
        0,0,146,147,5,61,0,0,147,50,1,0,0,0,148,149,5,38,0,0,149,150,5,38,
        0,0,150,52,1,0,0,0,151,152,5,38,0,0,152,54,1,0,0,0,153,154,5,124,
        0,0,154,155,5,124,0,0,155,56,1,0,0,0,156,157,5,124,0,0,157,58,1,
        0,0,0,158,159,5,94,0,0,159,60,1,0,0,0,160,161,5,60,0,0,161,162,5,
        60,0,0,162,62,1,0,0,0,163,164,5,62,0,0,164,165,5,62,0,0,165,64,1,
        0,0,0,166,168,3,3,1,0,167,166,1,0,0,0,168,169,1,0,0,0,169,167,1,
        0,0,0,169,170,1,0,0,0,170,66,1,0,0,0,171,172,5,105,0,0,172,173,5,
        110,0,0,173,174,5,116,0,0,174,68,1,0,0,0,175,176,5,99,0,0,176,177,
        5,104,0,0,177,178,5,97,0,0,178,179,5,114,0,0,179,70,1,0,0,0,180,
        181,5,102,0,0,181,182,5,108,0,0,182,183,5,111,0,0,183,184,5,97,0,
        0,184,185,5,116,0,0,185,72,1,0,0,0,186,187,5,98,0,0,187,188,5,111,
        0,0,188,189,5,111,0,0,189,190,5,108,0,0,190,74,1,0,0,0,191,192,5,
        100,0,0,192,193,5,111,0,0,193,194,5,117,0,0,194,195,5,98,0,0,195,
        196,5,108,0,0,196,197,5,101,0,0,197,76,1,0,0,0,198,199,5,118,0,0,
        199,200,5,111,0,0,200,201,5,105,0,0,201,202,5,100,0,0,202,78,1,0,
        0,0,203,204,5,114,0,0,204,205,5,101,0,0,205,206,5,116,0,0,206,207,
        5,117,0,0,207,208,5,114,0,0,208,209,5,110,0,0,209,80,1,0,0,0,210,
        211,5,119,0,0,211,212,5,104,0,0,212,213,5,105,0,0,213,214,5,108,
        0,0,214,215,5,101,0,0,215,82,1,0,0,0,216,217,5,102,0,0,217,218,5,
        111,0,0,218,219,5,114,0,0,219,84,1,0,0,0,220,221,5,105,0,0,221,222,
        5,102,0,0,222,86,1,0,0,0,223,224,5,101,0,0,224,225,5,108,0,0,225,
        226,5,115,0,0,226,227,5,101,0,0,227,88,1,0,0,0,228,229,7,2,0,0,229,
        230,1,0,0,0,230,231,6,44,0,0,231,90,1,0,0,0,232,235,3,1,0,0,233,
        235,5,95,0,0,234,232,1,0,0,0,234,233,1,0,0,0,235,241,1,0,0,0,236,
        240,3,1,0,0,237,240,3,3,1,0,238,240,5,95,0,0,239,236,1,0,0,0,239,
        237,1,0,0,0,239,238,1,0,0,0,240,243,1,0,0,0,241,239,1,0,0,0,241,
        242,1,0,0,0,242,92,1,0,0,0,243,241,1,0,0,0,5,0,169,234,239,241,1,
        6,0,0
    ]

class compiladoresLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    PA = 1
    PC = 2
    LLA = 3
    LLC = 4
    CA = 5
    CC = 6
    COMs = 7
    COMd = 8
    PYC = 9
    COMA = 10
    SUMA = 11
    RESTA = 12
    MULT = 13
    DIV = 14
    MOD = 15
    ASIG = 16
    INCR = 17
    DECR = 18
    MAYOR = 19
    MAYOREQ = 20
    MENOREQ = 21
    MENOR = 22
    IGUAL = 23
    AND = 24
    ANDsim = 25
    OR = 26
    ORsim = 27
    POT = 28
    DESPizq = 29
    DESPder = 30
    NUMERO = 31
    INT = 32
    CHAR = 33
    FLOAT = 34
    BOOLEAN = 35
    DOUBLE = 36
    VOID = 37
    RETURN = 38
    WHILE = 39
    FOR = 40
    IF = 41
    ELSE = 42
    WS = 43
    ID = 44

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'{'", "'}'", "'['", "']'", "'''", "'\"'", "';'", 
            "','", "'+'", "'-'", "'*'", "'/'", "'%'", "'='", "'++'", "'--'", 
            "'>'", "'>='", "'<='", "'<'", "'=='", "'&&'", "'&'", "'||'", 
            "'|'", "'^'", "'<<'", "'>>'", "'int'", "'char'", "'float'", 
            "'bool'", "'double'", "'void'", "'return'", "'while'", "'for'", 
            "'if'", "'else'" ]

    symbolicNames = [ "<INVALID>",
            "PA", "PC", "LLA", "LLC", "CA", "CC", "COMs", "COMd", "PYC", 
            "COMA", "SUMA", "RESTA", "MULT", "DIV", "MOD", "ASIG", "INCR", 
            "DECR", "MAYOR", "MAYOREQ", "MENOREQ", "MENOR", "IGUAL", "AND", 
            "ANDsim", "OR", "ORsim", "POT", "DESPizq", "DESPder", "NUMERO", 
            "INT", "CHAR", "FLOAT", "BOOLEAN", "DOUBLE", "VOID", "RETURN", 
            "WHILE", "FOR", "IF", "ELSE", "WS", "ID" ]

    ruleNames = [ "LETRA", "DIGITO", "PA", "PC", "LLA", "LLC", "CA", "CC", 
                  "COMs", "COMd", "PYC", "COMA", "SUMA", "RESTA", "MULT", 
                  "DIV", "MOD", "ASIG", "INCR", "DECR", "MAYOR", "MAYOREQ", 
                  "MENOREQ", "MENOR", "IGUAL", "AND", "ANDsim", "OR", "ORsim", 
                  "POT", "DESPizq", "DESPder", "NUMERO", "INT", "CHAR", 
                  "FLOAT", "BOOLEAN", "DOUBLE", "VOID", "RETURN", "WHILE", 
                  "FOR", "IF", "ELSE", "WS", "ID" ]

    grammarFileName = "compiladores.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


