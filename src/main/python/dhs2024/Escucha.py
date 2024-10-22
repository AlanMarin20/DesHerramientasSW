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

    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("Encontre WHILE\n")

    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("FIN del WHILE")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + str(ctx.getText())+"\n")

    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("####Declaracion####")

    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("####Sali de declaracion####")
        tipoDeDato = ctx.getChild(0).getText()
        print ("tipo de dato: " + tipoDeDato + "\n")
        NombreVariable = ctx.getChild(1).getText()
        print ("variable: " + NombreVariable + "\n") 
            
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

    def enterFunction(self, ctx:compiladoresParser.FuncionContext):
        print(' ### Entrando a una funcion ###')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitFunction(self, ctx:compiladoresParser.FuncionContext):
        nombreFuncion = ctx.prototSpyc.getChild(1).getText() #esto no se si esta bien
        Tiporetorno = ctx.prototSpyc.getChild(0).getText() #esto no se si esta bien
        
        if self.tablaDeSimbolos.buscarGlobal(nombreFuncion)==1 or self.tablaDeSimbolos.buscarLocal(nombreFuncion)==1:
            print("Este nombre de funcion ya esta definida a nivel global")
            return None
        
        print("Parametros Encontrados")
        parametros = ctx.parFuncion.getChild(0) #esto no se si esta bien
        if parametros: #en caso de que hayan parametros
            numHijos = parametros.getChildCount()
            i=0
            while(i < numHijos):
                tipoParametro = parametros.getChild(i).getText() #accede al i porque el tipo va antes que el nombre
                nombreParametro = parametros.getChild(i+1).getText()
                self.tablaDeSimbolos.addIdentificador(tipoParametro,nombreParametro)
                if i+3 < numHijos: #si queda espacio para un proximo parametro
                    i+=3 #usamos +3 porque saltea tipo,nombre y coma
                else:
                    break 
         
        self.tablaDeSimbolos.addIdentificador(nombreFuncion, Tiporetorno)
        print("En esta funcion se encontro lo siguiente:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla() #imprime la tabla de simbolos del contexto actual
        self.tablaDeSimbolos.delContexto()
    