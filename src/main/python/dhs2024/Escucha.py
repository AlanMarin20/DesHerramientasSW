from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser

class Escucha (compiladoresListener) :
    numTokens = 0
    numNodos = 0

    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Comienza la compilacion")

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Fin de la compilacion")

    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("Encontre WHILE")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + str(ctx.getText()))

    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("FIN del WHILE")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + str(ctx.getText()))

    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("### Declaracion")

    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("Nombre Variable: " + ctx.getChild(1).getText())

    def visitTerminal(self, node: TerminalNode):
        #print("----> Token: " + node.getText())
        self.numTokens += 1

    def visitErrorNode(self, node: ErrorNode):
        print("----> Error: ")

    def enterEveryRule(self, ctx):
        self.numNodos += 1