// Generated from /home/alan/dhs/dhs2024/src/main/python/dhs2024/compiladores.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link compiladoresParser}.
 */
public interface compiladoresListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#tipodato}.
	 * @param ctx the parse tree
	 */
	void enterTipodato(compiladoresParser.TipodatoContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#tipodato}.
	 * @param ctx the parse tree
	 */
	void exitTipodato(compiladoresParser.TipodatoContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#opComp}.
	 * @param ctx the parse tree
	 */
	void enterOpComp(compiladoresParser.OpCompContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#opComp}.
	 * @param ctx the parse tree
	 */
	void exitOpComp(compiladoresParser.OpCompContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#programa}.
	 * @param ctx the parse tree
	 */
	void enterPrograma(compiladoresParser.ProgramaContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#programa}.
	 * @param ctx the parse tree
	 */
	void exitPrograma(compiladoresParser.ProgramaContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#instrucciones}.
	 * @param ctx the parse tree
	 */
	void enterInstrucciones(compiladoresParser.InstruccionesContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#instrucciones}.
	 * @param ctx the parse tree
	 */
	void exitInstrucciones(compiladoresParser.InstruccionesContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void enterInstruccion(compiladoresParser.InstruccionContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#instruccion}.
	 * @param ctx the parse tree
	 */
	void exitInstruccion(compiladoresParser.InstruccionContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#declaracion}.
	 * @param ctx the parse tree
	 */
	void enterDeclaracion(compiladoresParser.DeclaracionContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#declaracion}.
	 * @param ctx the parse tree
	 */
	void exitDeclaracion(compiladoresParser.DeclaracionContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#declAsig}.
	 * @param ctx the parse tree
	 */
	void enterDeclAsig(compiladoresParser.DeclAsigContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#declAsig}.
	 * @param ctx the parse tree
	 */
	void exitDeclAsig(compiladoresParser.DeclAsigContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#prototipoFuncion}.
	 * @param ctx the parse tree
	 */
	void enterPrototipoFuncion(compiladoresParser.PrototipoFuncionContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#prototipoFuncion}.
	 * @param ctx the parse tree
	 */
	void exitPrototipoFuncion(compiladoresParser.PrototipoFuncionContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#prototSpyc}.
	 * @param ctx the parse tree
	 */
	void enterPrototSpyc(compiladoresParser.PrototSpycContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#prototSpyc}.
	 * @param ctx the parse tree
	 */
	void exitPrototSpyc(compiladoresParser.PrototSpycContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#parFunc}.
	 * @param ctx the parse tree
	 */
	void enterParFunc(compiladoresParser.ParFuncContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#parFunc}.
	 * @param ctx the parse tree
	 */
	void exitParFunc(compiladoresParser.ParFuncContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#funcion}.
	 * @param ctx the parse tree
	 */
	void enterFuncion(compiladoresParser.FuncionContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#funcion}.
	 * @param ctx the parse tree
	 */
	void exitFuncion(compiladoresParser.FuncionContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#callFunction}.
	 * @param ctx the parse tree
	 */
	void enterCallFunction(compiladoresParser.CallFunctionContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#callFunction}.
	 * @param ctx the parse tree
	 */
	void exitCallFunction(compiladoresParser.CallFunctionContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#envPar}.
	 * @param ctx the parse tree
	 */
	void enterEnvPar(compiladoresParser.EnvParContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#envPar}.
	 * @param ctx the parse tree
	 */
	void exitEnvPar(compiladoresParser.EnvParContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#lista_envPar}.
	 * @param ctx the parse tree
	 */
	void enterLista_envPar(compiladoresParser.Lista_envParContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#lista_envPar}.
	 * @param ctx the parse tree
	 */
	void exitLista_envPar(compiladoresParser.Lista_envParContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#asignacion}.
	 * @param ctx the parse tree
	 */
	void enterAsignacion(compiladoresParser.AsignacionContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#asignacion}.
	 * @param ctx the parse tree
	 */
	void exitAsignacion(compiladoresParser.AsignacionContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#opal}.
	 * @param ctx the parse tree
	 */
	void enterOpal(compiladoresParser.OpalContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#opal}.
	 * @param ctx the parse tree
	 */
	void exitOpal(compiladoresParser.OpalContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#or}.
	 * @param ctx the parse tree
	 */
	void enterOr(compiladoresParser.OrContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#or}.
	 * @param ctx the parse tree
	 */
	void exitOr(compiladoresParser.OrContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#o}.
	 * @param ctx the parse tree
	 */
	void enterO(compiladoresParser.OContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#o}.
	 * @param ctx the parse tree
	 */
	void exitO(compiladoresParser.OContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#and}.
	 * @param ctx the parse tree
	 */
	void enterAnd(compiladoresParser.AndContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#and}.
	 * @param ctx the parse tree
	 */
	void exitAnd(compiladoresParser.AndContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#a}.
	 * @param ctx the parse tree
	 */
	void enterA(compiladoresParser.AContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#a}.
	 * @param ctx the parse tree
	 */
	void exitA(compiladoresParser.AContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#comp}.
	 * @param ctx the parse tree
	 */
	void enterComp(compiladoresParser.CompContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#comp}.
	 * @param ctx the parse tree
	 */
	void exitComp(compiladoresParser.CompContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#c}.
	 * @param ctx the parse tree
	 */
	void enterC(compiladoresParser.CContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#c}.
	 * @param ctx the parse tree
	 */
	void exitC(compiladoresParser.CContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#exp}.
	 * @param ctx the parse tree
	 */
	void enterExp(compiladoresParser.ExpContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#exp}.
	 * @param ctx the parse tree
	 */
	void exitExp(compiladoresParser.ExpContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(compiladoresParser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(compiladoresParser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#e}.
	 * @param ctx the parse tree
	 */
	void enterE(compiladoresParser.EContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#e}.
	 * @param ctx the parse tree
	 */
	void exitE(compiladoresParser.EContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#t}.
	 * @param ctx the parse tree
	 */
	void enterT(compiladoresParser.TContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#t}.
	 * @param ctx the parse tree
	 */
	void exitT(compiladoresParser.TContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(compiladoresParser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(compiladoresParser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#iwhile}.
	 * @param ctx the parse tree
	 */
	void enterIwhile(compiladoresParser.IwhileContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#iwhile}.
	 * @param ctx the parse tree
	 */
	void exitIwhile(compiladoresParser.IwhileContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#bloque}.
	 * @param ctx the parse tree
	 */
	void enterBloque(compiladoresParser.BloqueContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#bloque}.
	 * @param ctx the parse tree
	 */
	void exitBloque(compiladoresParser.BloqueContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#ifor}.
	 * @param ctx the parse tree
	 */
	void enterIfor(compiladoresParser.IforContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#ifor}.
	 * @param ctx the parse tree
	 */
	void exitIfor(compiladoresParser.IforContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#init}.
	 * @param ctx the parse tree
	 */
	void enterInit(compiladoresParser.InitContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#init}.
	 * @param ctx the parse tree
	 */
	void exitInit(compiladoresParser.InitContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#cond}.
	 * @param ctx the parse tree
	 */
	void enterCond(compiladoresParser.CondContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#cond}.
	 * @param ctx the parse tree
	 */
	void exitCond(compiladoresParser.CondContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#iter}.
	 * @param ctx the parse tree
	 */
	void enterIter(compiladoresParser.IterContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#iter}.
	 * @param ctx the parse tree
	 */
	void exitIter(compiladoresParser.IterContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#incremento}.
	 * @param ctx the parse tree
	 */
	void enterIncremento(compiladoresParser.IncrementoContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#incremento}.
	 * @param ctx the parse tree
	 */
	void exitIncremento(compiladoresParser.IncrementoContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#decremento}.
	 * @param ctx the parse tree
	 */
	void enterDecremento(compiladoresParser.DecrementoContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#decremento}.
	 * @param ctx the parse tree
	 */
	void exitDecremento(compiladoresParser.DecrementoContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#iif}.
	 * @param ctx the parse tree
	 */
	void enterIif(compiladoresParser.IifContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#iif}.
	 * @param ctx the parse tree
	 */
	void exitIif(compiladoresParser.IifContext ctx);
	/**
	 * Enter a parse tree produced by {@link compiladoresParser#ielse}.
	 * @param ctx the parse tree
	 */
	void enterIelse(compiladoresParser.IelseContext ctx);
	/**
	 * Exit a parse tree produced by {@link compiladoresParser#ielse}.
	 * @param ctx the parse tree
	 */
	void exitIelse(compiladoresParser.IelseContext ctx);
}