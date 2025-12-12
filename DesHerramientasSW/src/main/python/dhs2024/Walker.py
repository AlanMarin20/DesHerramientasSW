from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from antlr4.tree.Tree import TerminalNodeImpl

class Walker (compiladoresVisitor):
    #---- Generador de codigo intermedio ----

    contadorTemporales = 0
    contadorEtiquetas = 0
    
    def __init__(self):
        # Abre archivo
        self.archivoCodigoIntermedio = open("./output/codigoIntermedio.txt", "w")
        self.funcion_actual = ""
    
    def __del__(self):
        # Cierra archivo (por si hay errores en el codigo C)
        if hasattr(self, 'archivoCodigoIntermedio'):
            self.archivoCodigoIntermedio.close()

    def getTemporal(self):
        # Genera nombres para variables temporales: t1, t2, t3...
        self.contadorTemporales += 1
        return f"t{self.contadorTemporales}"
    
    def getEtiqueta(self):
        # Genera nombres para etiquetas: L1, L2, L3... estas etiquetas se usan para saltos
        self.contadorEtiquetas += 1
        return f"L{self.contadorEtiquetas}"
    
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        # Procesa todo el codigo C
        self.visitInstrucciones(ctx.getChild(0))
        # Cierra archivo y muestra que lo genero (esto si el codigo C correcto)
        self.archivoCodigoIntermedio.close()
        print("Codigo intermedio generado")
        
    def visitInstrucciones(self, ctx: compiladoresParser.InstruccionesContext):
        # Procesa una lista de instrucciones secuencialmente
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if hasattr(child, 'getRuleIndex') and not isinstance(child, compiladoresParser.InstruccionesContext):
                self.visit(child)
            elif isinstance(child, compiladoresParser.InstruccionesContext):
                self.visit(child)

    def visitFuncion(self, ctx):
        prototipo = ctx.prototSpyc()
        nombreFuncion = prototipo.getChild(1).getText()
        # Guardamos contexto actual
        self.funcion_actual = nombreFuncion
        # Escribimos la etiqueta de la función
        self.archivoCodigoIntermedio.write(f"\n{nombreFuncion}:\n")

        nombresArgumentos = [] #Esta es la pila de parametros que usa la funcion (int a,etc)
        
        # Verificamos si tiene la regla parFunc (parametros definidos)
        if prototipo.parFunc():
            pf = prototipo.parFunc()
            
            # Recorremos todos los hijos de parFunc buscando los que sean IDs
            for i in range(pf.getChildCount()):
                child = pf.getChild(i)
                # Verificamos si el token es un ID (usando el tipo de simbolo de ANTLR)
                if hasattr(child, 'getSymbol') and child.getSymbol().type == compiladoresParser.ID:
                    nombresArgumentos.append(child.getText())

        # Primero sacamos param2, despues param1.
        for arg in reversed(nombresArgumentos):
           self.archivoCodigoIntermedio.write(f"pop {arg}\n")
        # Procesamos el cuerpo de la función
        self.visit(ctx.bloque())
        # Limpiamos contexto al salir
        self.funcion_actual = ""

    def visitBloque(self, ctx):
        # Procesa un bloque de código entre llaves { }
        if ctx.getChildCount() > 1:
            self.visit(ctx.getChild(1))

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        # Procesa una asignación de variable: x = valor
        variable = ctx.getChild(0).getText()
        # Verifica si es llamada a función
        call_func = ctx.callFunction()
        if call_func is not None:
            resultado = self.visitCallFunction(call_func)
            self.archivoCodigoIntermedio.write(f"{variable} = {resultado}\n")
        else:
            # Si entra aca, es una operacion normal
            opales = ctx.opal()
            if opales is not None:
                resultado = self.visitOperacionSimple(opales)
                if resultado:
                    self.archivoCodigoIntermedio.write(f"{variable} = {resultado}\n")

    def visitCallFunction(self, ctx):

        nombreFuncion = ctx.getChild(0).getText()
        # Recolectamos los valores de los parámetros en una lista
        parametros = []
        env_par = ctx.envPar()
        
        # Verificamos si hay parámetros (envPar tiene opales)
        if env_par and env_par.opal():
            # Primer parámetro
            param1 = self.visitOperacionSimple(env_par.opal())
            parametros.append(param1)
            
            # Resto de parámetros (lista_envPar)
            lista_env = env_par.lista_envPar()
            while lista_env and lista_env.opal():
                param_extra = self.visitOperacionSimple(lista_env.opal())
                parametros.append(param_extra)
                lista_env = lista_env.lista_envPar()
        
        # Generamos los PUSH
        for param in parametros:
           self.archivoCodigoIntermedio.write(f"push {param}\n")
        
        # Generamos la llamada (CALL)
        temporalResultado = self.getTemporal()
        self.archivoCodigoIntermedio.write(f"{temporalResultado} = call {nombreFuncion}\n")
        
        return temporalResultado

    def visitDeclAsig(self, ctx: compiladoresParser.DeclAsigContext):
        # Procesa declaración con asignación: int x = valor
        if ctx.declaracion():
            for i in range(1, ctx.declaracion().getChildCount()):
                child = ctx.declaracion().getChild(i)
                if hasattr(child, 'symbol') and child.symbol.type == compiladoresParser.ID:
                    variable = child.getText()
                    # Si hay asignación, procesa la operacion
                    opales = ctx.opal()
                    if opales is not None:
                        resultado = self.visitOperacionSimple(ctx.opal())
                        if resultado:
                            self.archivoCodigoIntermedio.write(f"{variable} = {resultado}\n")
                    else:
                        # Inicializa con 0 por defecto
                        self.archivoCodigoIntermedio.write(f"{variable} = 0\n")
                    break

    def visitDeclaracion(self, ctx):
        # Al dejar esto vacio (pass), evitamos que se escriba "variable = 0"
        # cuando solo se declara "int x;"
        pass

    def visitIwhile(self, ctx):
        etiqueta_inicio = self.getEtiqueta()
        etiqueta_fin = self.getEtiqueta()

        self.archivoCodigoIntermedio.write(f"{etiqueta_inicio}:\n")

        if ctx.opal():
            condicion_result = self.visit(ctx.opal())
            
            if condicion_result:
                self.archivoCodigoIntermedio.write(f"siFalso {condicion_result} ir a {etiqueta_fin}\n")
            
        if ctx.instruccion():
            self.visit(ctx.instruccion())

        self.archivoCodigoIntermedio.write(f"ir a {etiqueta_inicio}\n")
        self.archivoCodigoIntermedio.write(f"{etiqueta_fin}:\n")

    def visitIif(self, ctx):
        etiqueta_else = self.getEtiqueta()
        etiqueta_fin = self.getEtiqueta()
        
        condicion_result = self.visitOperacionSimple(ctx.opal())
        
        # Detectar si hay ELSE
        nodo_ielse = ctx.ielse()
        tiene_else = nodo_ielse is not None

        destino_falso = etiqueta_else if tiene_else else etiqueta_fin
        
        self.archivoCodigoIntermedio.write(f"siFalso {condicion_result} ir a {destino_falso}\n")
            
        # Visitamos el cuerpo del if
        self.visit(ctx.instruccion())
        
        if tiene_else:
            # Al terminar el IF, debemos saltar al FIN 
            # para no "caer" en el código del else.
            self.archivoCodigoIntermedio.write(f"ir a {etiqueta_fin}\n")
            
            # Etiqueta donde comienza el else
            self.archivoCodigoIntermedio.write(f"{etiqueta_else}:\n")
            
            # Visitamos el cuerpo del else
            self.visit(nodo_ielse.instruccion())
            
        self.archivoCodigoIntermedio.write(f"{etiqueta_fin}:\n")

    def visitIfor(self, ctx):
        etiqueta_inicio = self.getEtiqueta()
        etiqueta_fin = self.getEtiqueta()
        
        if ctx.init():
            self.visit(ctx.init()) 

        self.archivoCodigoIntermedio.write(f"{etiqueta_inicio}:\n")

        if ctx.cond():
            condicion_result = self.visit(ctx.cond())
            if condicion_result:
                self.archivoCodigoIntermedio.write(f"siFalso {condicion_result} ir a {etiqueta_fin}\n")
        
        # Cuerpo del for
        if ctx.instruccion():
            self.visit(ctx.instruccion())
            
        if ctx.iter_():       
            self.visit(ctx.iter_()) 
        
        self.archivoCodigoIntermedio.write(f"ir a {etiqueta_inicio}\n")
        self.archivoCodigoIntermedio.write(f"{etiqueta_fin}:\n")

    def visitInit(self, ctx):
        variable = ctx.ID().getText()
        valor = ctx.NUMERO().getText()
        
        self.archivoCodigoIntermedio.write(f"{variable} = {valor}\n")
        return None

    def visitIter(self, ctx):
        return self.visitChildren(ctx)

    def visitCond(self, ctx):
        return self.visitOperacionSimple(ctx.opal())

    def visitIreturn(self, ctx):
        # Si tiene hijos (además de la palabra 'return')
            # Visitamos el hijo 1 que contiene la expresión
            if self.funcion_actual == "main":
                return  # Salimos del método sin escribir nada
            
            if ctx.getChildCount() > 1:
                valor = self.visitOperacionSimple(ctx.getChild(1))
                self.archivoCodigoIntermedio.write(f"retornar {valor}\n")
            else:
            # Si no tiene expresión, solo return
                self.archivoCodigoIntermedio.write("retornar\n")

    def visitOperacionSimple(self, ctx):
        # Delega la tarea a (Opal, Exp, Term, etc.)
        if ctx is None:
            return "0"
        return self.visit(ctx)

    def visitOpal(self, ctx):
        # Solo pasa el control a la regla de abajo ('or')
        return self.visit(ctx.or_()) 

    def visitOr(self, ctx):
        # Obtener el primer valor (hijo izquierdo)
        resultado = self.visit(ctx.getChild(0)) # Visitamos 'and'

        i = 1
        while i < ctx.getChildCount():
            operador = ctx.getChild(i).getText()
            siguiente_nodo = ctx.getChild(i+1)   
            siguiente_val = self.visit(siguiente_nodo)

            nuevo_temporal = self.getTemporal()
            self.archivoCodigoIntermedio.write(f"{nuevo_temporal} = {resultado} {operador} {siguiente_val}\n")
            
            resultado = nuevo_temporal
            i += 2 # Saltamos el operador y el operando
            
        return resultado

    def visitAnd(self, ctx):

        resultado = self.visit(ctx.getChild(0)) 

        i = 1
        while i < ctx.getChildCount():
            operador = ctx.getChild(i).getText() 
            siguiente_nodo = ctx.getChild(i+1)  
            siguiente_val = self.visit(siguiente_nodo)

            nuevo_temporal = self.getTemporal()
            self.archivoCodigoIntermedio.write(f"{nuevo_temporal} = {resultado} {operador} {siguiente_val}\n")
            
            resultado = nuevo_temporal
            i += 2
            
        return resultado

    def visitComp(self, ctx):
        
        izq = self.visit(ctx.exp(0)) 

        # Si hay más de 1 hijo (exp operador exp), entonces hay comparación
        if ctx.getChildCount() > 1:
            operador = ctx.getChild(1).getText() 
            der = self.visit(ctx.exp(1))         
            
            temporal = self.getTemporal()
            self.archivoCodigoIntermedio.write(f"{temporal} = {izq} {operador} {der}\n")
            return temporal
            
        # Si no hubo comparación, devolvemos solo la expresión
        return izq

    def visitExp(self, ctx):
        resultado = self.visit(ctx.getChild(0)) 
        i = 1
        while i < ctx.getChildCount():
            operador = ctx.getChild(i).getText()       
            siguiente_nodo = ctx.getChild(i+1)         
            siguiente_val = self.visit(siguiente_nodo)
            
            # Generamos t...
            nuevo_temporal = self.getTemporal()
            self.archivoCodigoIntermedio.write(f"{nuevo_temporal} = {resultado} {operador} {siguiente_val}\n")
            
            # El resultado acumulado ahora es este temporal
            resultado = nuevo_temporal
            
            i += 2
            
        return resultado

    def visitTerm(self, ctx):
        resultado = self.visit(ctx.getChild(0)) 

        i = 1
        while i < ctx.getChildCount():
            operador = ctx.getChild(i).getText()
            siguiente_nodo = ctx.getChild(i+1)
            siguiente_val = self.visit(siguiente_nodo)
            
            nuevo_temporal = self.getTemporal()
            self.archivoCodigoIntermedio.write(f"{nuevo_temporal} = {resultado} {operador} {siguiente_val}\n")
            
            resultado = nuevo_temporal
            i += 2
            
        return resultado

    def visitFactor(self, ctx):
        # Paréntesis (PA exp PC)
        # Si tiene 3 hijos y el primero es '(', visitamos la expresión del medio
        if ctx.getChildCount() == 3 and ctx.PA():
            return self.visit(ctx.exp())

        # Numero o Variable
        return ctx.getText()
    
    def visitChildren(self, ctx):
        # Método para procesar hijos de un nodo
        if ctx.getChildCount() > 0:
            return self.visit(ctx.getChild(0))
        return None
    
    def visitPrototipoFuncion(self, ctx):
        # Procesa prototipos de función 
        pass
