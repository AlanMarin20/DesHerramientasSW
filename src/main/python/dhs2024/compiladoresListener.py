# Generated from /home/alan/dhs/dhs2024/src/main/python/dhs2024/compiladores.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .compiladoresParser import compiladoresParser
else:
    from compiladoresParser import compiladoresParser

# This class defines a complete listener for a parse tree produced by compiladoresParser.
class compiladoresListener(ParseTreeListener):

    # Enter a parse tree produced by compiladoresParser#tipodato.
    def enterTipodato(self, ctx:compiladoresParser.TipodatoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#tipodato.
    def exitTipodato(self, ctx:compiladoresParser.TipodatoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#opComp.
    def enterOpComp(self, ctx:compiladoresParser.OpCompContext):
        pass

    # Exit a parse tree produced by compiladoresParser#opComp.
    def exitOpComp(self, ctx:compiladoresParser.OpCompContext):
        pass


    # Enter a parse tree produced by compiladoresParser#programa.
    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        pass

    # Exit a parse tree produced by compiladoresParser#programa.
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        pass


    # Enter a parse tree produced by compiladoresParser#instrucciones.
    def enterInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
        pass

    # Exit a parse tree produced by compiladoresParser#instrucciones.
    def exitInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
        pass


    # Enter a parse tree produced by compiladoresParser#instruccion.
    def enterInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#instruccion.
    def exitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#declaracion.
    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#declaracion.
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#declaracionArreglos.
    def enterDeclaracionArreglos(self, ctx:compiladoresParser.DeclaracionArreglosContext):
        pass

    # Exit a parse tree produced by compiladoresParser#declaracionArreglos.
    def exitDeclaracionArreglos(self, ctx:compiladoresParser.DeclaracionArreglosContext):
        pass


    # Enter a parse tree produced by compiladoresParser#declAsig.
    def enterDeclAsig(self, ctx:compiladoresParser.DeclAsigContext):
        pass

    # Exit a parse tree produced by compiladoresParser#declAsig.
    def exitDeclAsig(self, ctx:compiladoresParser.DeclAsigContext):
        pass


    # Enter a parse tree produced by compiladoresParser#prototipoFuncion.
    def enterPrototipoFuncion(self, ctx:compiladoresParser.PrototipoFuncionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#prototipoFuncion.
    def exitPrototipoFuncion(self, ctx:compiladoresParser.PrototipoFuncionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#prototSpyc.
    def enterPrototSpyc(self, ctx:compiladoresParser.PrototSpycContext):
        pass

    # Exit a parse tree produced by compiladoresParser#prototSpyc.
    def exitPrototSpyc(self, ctx:compiladoresParser.PrototSpycContext):
        pass


    # Enter a parse tree produced by compiladoresParser#parFunc.
    def enterParFunc(self, ctx:compiladoresParser.ParFuncContext):
        pass

    # Exit a parse tree produced by compiladoresParser#parFunc.
    def exitParFunc(self, ctx:compiladoresParser.ParFuncContext):
        pass


    # Enter a parse tree produced by compiladoresParser#funcion.
    def enterFuncion(self, ctx:compiladoresParser.FuncionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#funcion.
    def exitFuncion(self, ctx:compiladoresParser.FuncionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#callFunction.
    def enterCallFunction(self, ctx:compiladoresParser.CallFunctionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#callFunction.
    def exitCallFunction(self, ctx:compiladoresParser.CallFunctionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#envPar.
    def enterEnvPar(self, ctx:compiladoresParser.EnvParContext):
        pass

    # Exit a parse tree produced by compiladoresParser#envPar.
    def exitEnvPar(self, ctx:compiladoresParser.EnvParContext):
        pass


    # Enter a parse tree produced by compiladoresParser#lista_envPar.
    def enterLista_envPar(self, ctx:compiladoresParser.Lista_envParContext):
        pass

    # Exit a parse tree produced by compiladoresParser#lista_envPar.
    def exitLista_envPar(self, ctx:compiladoresParser.Lista_envParContext):
        pass


    # Enter a parse tree produced by compiladoresParser#asignacion.
    def enterAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#asignacion.
    def exitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#arreglo.
    def enterArreglo(self, ctx:compiladoresParser.ArregloContext):
        pass

    # Exit a parse tree produced by compiladoresParser#arreglo.
    def exitArreglo(self, ctx:compiladoresParser.ArregloContext):
        pass


    # Enter a parse tree produced by compiladoresParser#opal.
    def enterOpal(self, ctx:compiladoresParser.OpalContext):
        pass

    # Exit a parse tree produced by compiladoresParser#opal.
    def exitOpal(self, ctx:compiladoresParser.OpalContext):
        pass


    # Enter a parse tree produced by compiladoresParser#or.
    def enterOr(self, ctx:compiladoresParser.OrContext):
        pass

    # Exit a parse tree produced by compiladoresParser#or.
    def exitOr(self, ctx:compiladoresParser.OrContext):
        pass


    # Enter a parse tree produced by compiladoresParser#o.
    def enterO(self, ctx:compiladoresParser.OContext):
        pass

    # Exit a parse tree produced by compiladoresParser#o.
    def exitO(self, ctx:compiladoresParser.OContext):
        pass


    # Enter a parse tree produced by compiladoresParser#and.
    def enterAnd(self, ctx:compiladoresParser.AndContext):
        pass

    # Exit a parse tree produced by compiladoresParser#and.
    def exitAnd(self, ctx:compiladoresParser.AndContext):
        pass


    # Enter a parse tree produced by compiladoresParser#a.
    def enterA(self, ctx:compiladoresParser.AContext):
        pass

    # Exit a parse tree produced by compiladoresParser#a.
    def exitA(self, ctx:compiladoresParser.AContext):
        pass


    # Enter a parse tree produced by compiladoresParser#comp.
    def enterComp(self, ctx:compiladoresParser.CompContext):
        pass

    # Exit a parse tree produced by compiladoresParser#comp.
    def exitComp(self, ctx:compiladoresParser.CompContext):
        pass


    # Enter a parse tree produced by compiladoresParser#c.
    def enterC(self, ctx:compiladoresParser.CContext):
        pass

    # Exit a parse tree produced by compiladoresParser#c.
    def exitC(self, ctx:compiladoresParser.CContext):
        pass


    # Enter a parse tree produced by compiladoresParser#exp.
    def enterExp(self, ctx:compiladoresParser.ExpContext):
        pass

    # Exit a parse tree produced by compiladoresParser#exp.
    def exitExp(self, ctx:compiladoresParser.ExpContext):
        pass


    # Enter a parse tree produced by compiladoresParser#term.
    def enterTerm(self, ctx:compiladoresParser.TermContext):
        pass

    # Exit a parse tree produced by compiladoresParser#term.
    def exitTerm(self, ctx:compiladoresParser.TermContext):
        pass


    # Enter a parse tree produced by compiladoresParser#e.
    def enterE(self, ctx:compiladoresParser.EContext):
        pass

    # Exit a parse tree produced by compiladoresParser#e.
    def exitE(self, ctx:compiladoresParser.EContext):
        pass


    # Enter a parse tree produced by compiladoresParser#t.
    def enterT(self, ctx:compiladoresParser.TContext):
        pass

    # Exit a parse tree produced by compiladoresParser#t.
    def exitT(self, ctx:compiladoresParser.TContext):
        pass


    # Enter a parse tree produced by compiladoresParser#factor.
    def enterFactor(self, ctx:compiladoresParser.FactorContext):
        pass

    # Exit a parse tree produced by compiladoresParser#factor.
    def exitFactor(self, ctx:compiladoresParser.FactorContext):
        pass


    # Enter a parse tree produced by compiladoresParser#iwhile.
    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        pass

    # Exit a parse tree produced by compiladoresParser#iwhile.
    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        pass


    # Enter a parse tree produced by compiladoresParser#bloque.
    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        pass

    # Exit a parse tree produced by compiladoresParser#bloque.
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        pass


    # Enter a parse tree produced by compiladoresParser#ifor.
    def enterIfor(self, ctx:compiladoresParser.IforContext):
        pass

    # Exit a parse tree produced by compiladoresParser#ifor.
    def exitIfor(self, ctx:compiladoresParser.IforContext):
        pass


    # Enter a parse tree produced by compiladoresParser#init.
    def enterInit(self, ctx:compiladoresParser.InitContext):
        pass

    # Exit a parse tree produced by compiladoresParser#init.
    def exitInit(self, ctx:compiladoresParser.InitContext):
        pass


    # Enter a parse tree produced by compiladoresParser#cond.
    def enterCond(self, ctx:compiladoresParser.CondContext):
        pass

    # Exit a parse tree produced by compiladoresParser#cond.
    def exitCond(self, ctx:compiladoresParser.CondContext):
        pass


    # Enter a parse tree produced by compiladoresParser#iter.
    def enterIter(self, ctx:compiladoresParser.IterContext):
        pass

    # Exit a parse tree produced by compiladoresParser#iter.
    def exitIter(self, ctx:compiladoresParser.IterContext):
        pass


    # Enter a parse tree produced by compiladoresParser#incremento.
    def enterIncremento(self, ctx:compiladoresParser.IncrementoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#incremento.
    def exitIncremento(self, ctx:compiladoresParser.IncrementoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#decremento.
    def enterDecremento(self, ctx:compiladoresParser.DecrementoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#decremento.
    def exitDecremento(self, ctx:compiladoresParser.DecrementoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#iif.
    def enterIif(self, ctx:compiladoresParser.IifContext):
        pass

    # Exit a parse tree produced by compiladoresParser#iif.
    def exitIif(self, ctx:compiladoresParser.IifContext):
        pass


    # Enter a parse tree produced by compiladoresParser#ielse.
    def enterIelse(self, ctx:compiladoresParser.IelseContext):
        pass

    # Exit a parse tree produced by compiladoresParser#ielse.
    def exitIelse(self, ctx:compiladoresParser.IelseContext):
        pass



del compiladoresParser