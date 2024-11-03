from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from ID import ID
import re

class Escucha (compiladoresListener) :
    tablaDeSimbolos = TablaSimbolos()

    numTokensTotal = 0
    numNodosTotal = 0

    numTokens = 0
    numNodos = 0

    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Comienza la compilacion")
    
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print('Fin compilacion\n')
        # print('Se encontraron: \n')
        # print('Nodos: ' + str(self.numNodosTotal) + "\n")
        # print('Tokens: ' + str(self.numTokensTotal) + "\n")

#----INSTRUCCIONES----
    def enterInstruccion(self, ctx: compiladoresParser.InstruccionContext):
        pass

    def exitInstruccion(self, ctx: compiladoresParser.InstruccionContext):
        # Verificamos si es un tipo de instrucción que lleva ; al final
        if ctx.declaracion() or ctx.asignacion() or ctx.callFunction() or ctx.RETURN():
            numHijos = ctx.getChildCount()# Obtenemos el número total de hijos
            # Verificamos si hay hijos y si el último hijo no es un punto y coma
            if numHijos > 0:  # Verificamos si hay uno o mas hijos
                ultimoHijo = ctx.getChild(numHijos - 1)  # Accedemos al último hijo
                if ultimoHijo.getText() != ';': 
                    print('ERROR: se espera un ;')
                  

    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        #print('####Declaracion####')
        # if isinstance(ctx, compiladoresParser.FuncionContext): #QUE ES ESTO?
        #     print('Funcion')
        pass

    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):            
        #print('####Sali de declaracion####')
        tipoVariable = ctx.getChild(0).getText()
        print ('tipo de dato: ' + tipoVariable + '\n')
        nombreVariables = []
        for i in range(1, ctx.getChildCount(), 2):
            if ctx.getChild(i).getText() == ';' or ctx.getChild(i).getText() == ',' or ctx.getChild(i).getText() == '<missing ID>':
                print('+++ERROR SINTACTICO: Formato para declarar incorrecto+++')
                return None
            elif ctx.getChild(i).getSymbol().type == compiladoresParser.ID:
                nombreVariables.append(ctx.getChild(i).getText()) 
            else:
               print("+++ERROR SINTACTICO: Falta un ID+++") 
               return None    
            #int x , y , z; --> hacemos que el for arranque en la segunda variable y salte de a dos
        for nombreVariable in nombreVariables:
            if (self.tablaDeSimbolos.buscarGlobal(nombreVariable)) is not None:
                print('+++ERROR SEMANTICO: La variable' + nombreVariable + 'ya existe a nivel global+++')
            elif (self.tablaDeSimbolos.buscarLocal(nombreVariable)) is not None:
               print('+++ERROR SEMANTICO: La variable' + nombreVariable + 'ya existe a nivel local+++')
            else:
               print('La variable "' + nombreVariable + '" se agregó correctamente a la tabla de símbolos.')
               self.tablaDeSimbolos.addIdentificador(nombreVariable, tipoVariable)
        
    def enterAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        pass
        #print('### ASIGNACION ###')

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        nombreVariable = ctx.getChild(0).getText()
        print('Analizando variable: "' + nombreVariable + '"\n')
        numHijos = ctx.getChildCount()
        variableGlobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable) 
        variableLocal = self.tablaDeSimbolos.buscarLocal(nombreVariable) 
        tipoDatoIzq = None
        tipoDatoDer = None
        if variableLocal is not None:
            print('La variable "' + nombreVariable + '" se encontró a nivel local')
            variableLocal.inicializado = 1  # Acceso directo al objeto
            tipoDatoIzq = variableLocal.tipoDato
        elif variableGlobal is not None:
            print('La variable "' + nombreVariable + '" se encontró a nivel global')
            variableGlobal.inicializado = 1  # Acceso directo al objeto
            tipoDatoIzq = variableGlobal.tipoDato
        else:
            print('+++ERROR SEMANTICO: La variable "' + nombreVariable + '" no esta declarada+++')
        #CAMBIAR ATRIBUTO USADO A 1
        nombreVariableUsada = ctx.getChild(2).getText()
        partes = re.split("[+\-*]",nombreVariableUsada)
        for i in partes:
            if i.isdigit(): #Si es un numero
                print(str(tipoDatoIzq))
                tipoDatoDer ='TipoDato.INT'
                if tipoDatoDer != str(tipoDatoIzq):
                    if str(tipoDatoIzq) != 'TipoDato.FLOAT':
                        print("Error Semantico: Formato de variable incompatible")
                        if variableGlobal is not None: 
                            variableGlobal.inicializado=0
                        elif variableLocal is not None: 
                            variableLocal.inicializado=0
            # elif i.isalpha() and "'" in i: #Si es un char
            #     tipoDatoDer='TipoDato.CHAR'
            #     if tipoDatoDer != str(tipoDatoIzq):
            #         print("Error Semantico: Formato de variable incompatible")
            #         if variableGlobal is not None: 
            #                 variableGlobal.inicializado=0
            #         elif variableLocal is not None: 
            #                 variableLocal.inicializado=0
            else:  # Si es una variable
                variableUsadaGlobal = self.tablaDeSimbolos.buscarGlobal(i)
                variableUsadaLocal = self.tablaDeSimbolos.buscarLocal(i)
                # Si encontramos la variable del lado derecho del ASIG, cambiar 'usada' a 1
                if variableUsadaLocal is not None:
                    if variableUsadaLocal.inicializado == 1:
                        variableUsadaLocal.usado = 1
                        tipoDatoDer = variableUsadaLocal.tipoDato
                    else:
                        print('ERROR SEMANTICO: La variable: "'+i+'" no esta inicializada')
                        tipoDatoDer = variableUsadaLocal.tipoDato
                elif variableUsadaGlobal is not None:
                    if variableUsadaGlobal.inicializado == 1:        
                        variableUsadaGlobal.usado = 1
                        tipoDatoDer = variableUsadaGlobal.tipoDato
                    else:
                        print('ERROR SEMANTICO: La variable: "'+i+'" no esta inicializada')
                        tipoDatoDer=variableUsadaGlobal.tipoDato       
                if tipoDatoDer != tipoDatoIzq:
                    if variableUsadaGlobal is not None:
                        variableUsadaGlobal.usado = 0
                        variableGlobal.inicializado = 0
                    elif variableUsadaLocal is not None:
                        variableUsadaLocal.usado = 0
                        variableLocal.inicializado = 0
                    print("ERROR SEMANTICO: Incompatibilidad de datos")
        self.tablaDeSimbolos.controlarUsados()
    
    # def enterDeclAsig(self, ctx: compiladoresParser.DeclAsigContext):
    #    print("### Entrando a una declaración de asignación ###\n")
  
    # def exitDeclAsig(self, ctx: compiladoresParser.DeclAsigContext):
    #    #nombre = ctx.getChild(0).getText()
    #    #nombreVariable = nombre [3:]
    #    #tipo = ctx.getChild(0).getText()
    #    #tipoVariable=tipo[0:3]
    #    if self.tablaDeSimbolos.buscarGlobal(nombreVariable)==1:
    #        print("La variable "+nombreVariable+" ya esta usada a nivel GLOBAL, debes escoger  otro nombre")
    #    elif self.tablaDeSimbolos.buscarLocal(nombreVariable)==1:
    #        print("La variable "+nombreVariable+" ya esta usada a nivel LOCAL, debes escoger  otro nombre")   
    #    else:
    #        print("La variable "+nombreVariable+" se agrego correctamente a la tabla de simbolos")
    #        self.tablaDeSimbolos.addIdentificador(nombreVariable, tipoVariable) 

#-------------------------------------------
#----FUNCION----

    def enterPrototipoFuncion(self, ctx: compiladoresParser.PrototipoFuncionContext):
        #print('### Encontre un prototipo ###\n')
        pass

    def exitPrototipoFuncion(self, ctx: compiladoresParser.PrototipoFuncionContext):
        #Verificacion ; al final
        numHijos = ctx.getChildCount()
        # Verificamos si hay hijos y si el último hijo no es un punto y coma
        if numHijos > 0:  # Verificamos si hay uno o mas hijos
            ultimoHijo = ctx.getChild(numHijos - 1)  # Accedemos al último hijo
            if ultimoHijo.getText() != ';': 
                print('ERROR: se espera un ;')
        #Verificacion parentesis
        if ctx.getChild(2).getText() != '(':
            print('ERROR SINTACTICO: Falta parentesis de apertura')
            return None
        if ctx.getChild(numHijos-2).getText() != ')':
            print('ERROR SINTACTICO: Falta parentesis de cierre')
            return None          
        
        tipoRetorno = ctx.tipodato().getText()
        nombreFuncion = ctx.ID().getText()
        if self.tablaDeSimbolos.buscarGlobal(nombreFuncion):
            print('La funcion"' + nombreFuncion + '"ya esta definida a nivel global.')
            return None
        
        # Imprimir el nombre de la funcion y el tipo de retorno
        print(f'Prototipo de función encontrado, nombre: "' + nombreFuncion + ' " tipo de dato de retorno: ' + tipoRetorno)

        # Obtener los parámetros de la función, si existen
        parametros = ctx.parFunc()  #Iguala los parametros que le pasaron a la variable parametros
        listaParametros = [] #Hace lista para luego imprimir
        if parametros and parametros.getChildCount() > 0: #Se fija si tiene parametros
            numHijos = parametros.getChildCount()
            i = 0
            #print(f"Número de hijos en 'parametros': {numHijos}")
            # for j in range(numHijos):                                   #Este for imprime todos los hijos
            #     print(f"Hijo {j}: {parametros.getChild(j).getText()}")  
            while i < numHijos:
                tipoParametro = parametros.getChild(i).getText()  # Tipo de dato del parámetro
                nombreParametro = parametros.getChild(i+1).getText()  # Nombre del parámetro
                listaParametros.append(f"{tipoParametro} {nombreParametro}")#Agrega los parametros a la lista para mostrarlos
                                                                            #pero no los agrega a la tabla de simbolos
                self.tablaDeSimbolos.addIdentificador(nombreParametro, tipoParametro)
                # Aumentar el índice en 3 para saltar tipo, nombre y la coma
                if i + 2 < numHijos and parametros.getChild(i + 2).getText() == ',': 
                #Esta comprobacion sirve para ver si hay otro parametro o si es el ultimo
                    i += 3  # Saltamos tipo, nombre y coma
                else:
                    break  # No hay más parámetros
        else:
            pass#print('No hay parametros')
        if listaParametros: 
            print('La funcion "' + nombreFuncion + '" necesita los siguientes parametros: ' )
            print(listaParametros)# Agregue esto para que imprima la lista de parametros
        else:
            print('La funcion no tiene parametros')
        
        self.tablaDeSimbolos.addIdentificador(nombreFuncion, tipoRetorno)#Agrega el nombre de la funcion y el tipo de retorno a la tabla de simbolos
        print("------------------------------------------------")

    def enterFunction(self, ctx:compiladoresParser.FuncionContext):
        #print('### Entrando a una funcion ###\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
    
    def exitFuncion(self, ctx: compiladoresParser.FuncionContext):
        tipoRetorno = ctx.prototSpyc().tipodato().getText()
        nombreFuncion = ctx.prototSpyc().ID().getText()
        if (self.tablaDeSimbolos.buscarFuncionGlobal(nombreFuncion)) == 0: #Busca si la funcion esta declarada
            print('La funcion "' + nombreFuncion + '" no esta declarada pero será agregada.\n')
            self.tablaDeSimbolos.addIdentificador(nombreFuncion, tipoRetorno)
            # return None
        # Imprimir la función encontrada para fines de depuración
        print(f'Función encontrada: "' + nombreFuncion + '" con tipo de retorno: ' + tipoRetorno)

        # Obtener los parámetros de la función, si existen
        parametros = ctx.prototSpyc().parFunc()  #Aca se fija si hay parametros
        listaParametros = [] #hacemos lista para luego imprimir
        if parametros and parametros.getChildCount() > 0: #modifique esto para que se fije si tiene parametros
            numHijos = parametros.getChildCount()
            i = 0
            print(f'Número de hijos en "parametros": {numHijos}')
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
                    # print('hay mas parametros')
                    i += 3  # Saltamos tipo, nombre y coma
                else:
                    break  # No hay más parámetros
            # self.tablaDeSimbolos.imprimirTabla()   
        else:
            pass#print('No hay parametros')
        if listaParametros: 
            print('La funcion "' + nombreFuncion + '" tiene los siguientes parametros: ' )
            print(listaParametros)# Agregue esto para que imprima la lista
        else:
            print('La funcion "' + nombreFuncion + '" NO tiene parametros')

        print('En la funcion "' + nombreFuncion + '" se encontro lo siguiente: ')
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()  
        self.tablaDeSimbolos.delContexto()
        print('------------------------------------------------')
#----FIN FUNCION----
#-------------------------------------------
    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        #print('### Entrando a un contexto ###\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        # print('### Saliendo del contexto ###\n')
        # print('Cantidad de hijos: ' + str(ctx.getChildCount()))
        # print('TOKENS: ' + ctx.getText())

        print("En este contesto se encontro: ")
        # self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 20 + "\n")
        # self.tablaDeSimbolos.contextos[-1].controlarUsados()
        self.tablaDeSimbolos.delContexto()
#-------------------------------------------
#----BUCLES----

    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print('### Entrando a un while ###\n')
        # pass

    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        # if ctx.PA is None:
        #     print('ERROR: Falta parentesis de apertura')
        #     return None
        # if ctx.PC is None:
        #     print('ERROR: Falta parentesis de cierre')
        #     return None
        if ctx.getChild(1).getText() != '(':
            print('ERROR SINTACTICO: Falta parentesis de apertura')
            return None
        if ctx.getChild(3).getText() != ')':
            print('ERROR SINTACTICO: Falta parentesis de cierre')
            return None
        
        # print('### Saliendo del while ###\n')
        # print("\tCantidad hijos: " + str(ctx.getChildCount()))
        # print("\tTokens: " + str(ctx.getText())+"\n")
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

    def enterIfor(self, ctx: compiladoresParser.IforContext) :
        # print('### Entrando a un for ###\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitIfor(self, ctx: compiladoresParser.IforContext) :
        if ctx.getChild(1).getText() != '(':
            print(ctx.getChild(1).getText())
            print('ERROR SINTACTICO: Falta parentesis de apertura')
            return None
        if ctx.getChild(7).getText() != ')':
            print(ctx.getChild(7).getText())
            print('ERROR SINTACTICO: Falta parentesis de cierre')
            return None
        if ctx.getChild(3).getText() != ';' or ctx.getChild(5).getText() != ';':
            print('ERROR SINTACTICO: Falta ;')
            return None
        # print('### Saliendo del for ###\n')
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

    def enterIif(self, ctx: compiladoresParser.IifContext) :
        # print('### Entrando a un if ###\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
    
    def exitIif(self, ctx: compiladoresParser.IifContext) :
        if ctx.getChild(1).getText() != '(':
            print('ERROR SINTACTICO: Falta parentesis de apertura')
            return None
        if ctx.getChild(3).getText() != ')':
            print('ERROR SINTACTICO: Falta parentesis de cierre')
            return None
        # print('### Saliendo del if ###\n')
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

    def enterIelse(self, ctx: compiladoresParser.IelseContext):
        # print('### Entrando a un else ###\n')
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitIelse(self, ctx: compiladoresParser.IelseContext):
        # print('### Saliendo del else ###\n')
        self.tablaDeSimbolos.delContexto() #Esto elimina el ultimo contexto agregado a tablaDeSimbolos

#----FIN BUCLES----
#-------------------------------------------
    def visitTerminal(self, node: TerminalNode):
        # print("----> Token: " + node.getText())
        self.numTokens += 1
        self.numTokensTotal += 1

    def visitErrorNode(self, node: ErrorNode):
        print("----> Error: ")

    def enterEveryRule(self, ctx):
        self.numNodos += 1
        self.numNodosTotal += 1
    