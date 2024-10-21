from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from ID import ID

class Escucha (compiladoresListener) :
    tablaDeSimbolos = TablaSimbolos()

    numTokensTotal = 0
    numNodosTotal = 0

    numTokens = 0
    numNodos = 0

    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Comienza la compilacion")

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Fin de la compilacion")

    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("Encontre WHILE\n")

    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("FIN del WHILE")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + str(ctx.getText())+"\n")

    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("### Declaracion")

    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        tipoDeDato = ctx.getChild(0).getText()
        NombreVariable = ctx.getChild(1).getText()

        if(self.tablaDeSimbolos.buscarGlobal(NombreVariable) != 1):
            self.tablaDeSimbolos.buscarLocal(NombreVariable)

        self.tablaDeSimbolos.addIdentificador(NombreVariable, tipoDeDato)

    def enterAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("### ASIGNACION ###")

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("ya no hay variables que asignar\n")


    def visitTerminal(self, node: TerminalNode):
        #print("----> Token: " + node.getText())
        self.numTokens += 1

    def visitErrorNode(self, node: ErrorNode):
        print("----> Error: ")

    def enterEveryRule(self, ctx):
        self.numNodos += 1
        self.numNodosTotal += 1

    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        print('***Entre a un CONTEXTO***\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)


    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        print('***Sali de un CONTEXTO***')
        print('Cantidad de hijos: ' + str(ctx.getChildCount()))
        print('TOKENS: ' + ctx.getText())

        print("En este contesto se encontro: ")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 20 + "\n")
        self.tablaDeSimbolos.delContexto()

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print('Fin compilacion\n')
        print('Se encontraron: \n')
        print('Nodos: ' + str(self.numNodosTotal) + "\n")
        print('Tokens: ' + str(self.numTokensTotal) + "\n")
