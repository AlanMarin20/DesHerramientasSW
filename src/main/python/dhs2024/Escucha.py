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

    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("####Declaracion####")
        if isinstance(ctx, compiladoresParser.FuncionContext):
            print("Funcion")

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
        # print("----> Token: " + node.getText())
        self.numTokens += 1
        self.numTokensTotal += 1

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
    
    def exitFuncion(self, ctx: compiladoresParser.FuncionContext):        
        tipoRetorno = ctx.prototSpyc().tipodato().getText()
        nombreFuncion = ctx.prototSpyc().ID().getText()
        if self.tablaDeSimbolos.buscarGlobal(nombreFuncion):
            print("La funcion" + nombreFuncion + "ya esta definida a nivel global.")
            return None
        
        # Imprimir la función encontrada para fines de depuración
        print(f"Función encontrada: "+nombreFuncion+" con tipo de retorno: "+tipoRetorno)

        # Obtener los parámetros de la función, si existen
        parametros = ctx.prototSpyc().parFunc()  #Aca se fija si hay parametros
        listaParametros=[] #hacemos lista para luego imprimir
        if parametros and parametros.getChildCount() > 0 : #modifique esto para que se fije si tiene parametros
            numHijos = parametros.getChildCount()
            i = 0
            print(f"Número de hijos en 'parametros': {numHijos}")
            # for j in range(numHijos):                                   #Esto es para imprimir todos los hijos
            #     print(f"Hijo {j}: {parametros.getChild(j).getText()}")  #pero ya esta solucionado creo
            while i < numHijos:
                tipoParametro = parametros.getChild(i).getText()  # Tipo de dato del parámetro
                nombreParametro = parametros.getChild(i+1).getText()  # Nombre del parámetro
                self.tablaDeSimbolos.addIdentificador(nombreParametro, tipoParametro)
                listaParametros.append(f"{tipoParametro} {nombreParametro}")
                
                # Aumentar el índice en 3 para saltar tipo, nombre y la coma
                if i + 2 < numHijos and parametros.getChild(i + 2).getText() == ',': 
                #Esta comprobacion sirve para ver si hay otro parametro o si es el ultimo
                    print("hay mas parametros")
                    i += 3  # Saltamos tipo, nombre y coma
               
                else:
                    break  # No hay más parámetros

        else:
            print("No hay parametros")
        if listaParametros: 
            print("La funcion " + nombreFuncion + " tiene los siguientes parametros: " )
            print(listaParametros)#agregue esto para que imprima la lista
        else:
            print("La funcion no tiene parametros")

        self.tablaDeSimbolos.addIdentificador(nombreFuncion, tipoRetorno)

        print("########En esta función se encontró lo siguiente########")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()  
        self.tablaDeSimbolos.delContexto()
#Agregue estos bucles y pase el while junto
    def enterIif(self, ctx: compiladoresParser.IifContext) :
        print(' ### Entrando a un if ###\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
    
    def exitIif(self, ctx: compiladoresParser.IifContext) :
        print('### Saliendo del if ###\n')
        #COMPLETAR
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

    def enterIfor(self, ctx: compiladoresParser.IforContext) :
        print("### Entrando a un for ###\n")
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitIfor(self, ctx: compiladoresParser.IforContext) :
        print("### Saliendo del for ###\n")
        #COMPLETAR
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos
        

    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("Encontre WHILE\n")

    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("FIN del WHILE")
        print("\tCantidad hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + str(ctx.getText())+"\n")
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

    def enterIelse(self, ctx: compiladoresParser.IelseContext):
        print("### Entrando a un else ###\n")
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitIelse(self, ctx: compiladoresParser.IelseContext):
        print("### Saliendo del else ###\n")
        #COMPLETAR
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

