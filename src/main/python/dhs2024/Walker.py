from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from antlr4.tree.Tree import TerminalNodeImpl

class Walker (compiladoresVisitor):
    #---- Generador de código intermedio ----

    contadorTemporales = 0
    contadorEtiquetas = 0
    
    def __init__(self):
        # Abre archivo
        self.archivoCodigoIntermedio = open("./output/codigoIntermedio.txt", "w")
    
    def __del__(self):
        # Cierra archivo (por si hay errores en el codigo C)
        if hasattr(self, 'archivoCodigoIntermedio'):
            self.archivoCodigoIntermedio.close()

    def getTemporal(self):
        # Genera nombres únicos para variables temporales: t1, t2, t3...
        self.contadorTemporales += 1
        return f"t{self.contadorTemporales}"
    
    def getEtiqueta(self):
        # Genera nombres únicos para etiquetas: L1, L2, L3... estas etiquetas se usan para saltos
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
        # Procesa la definición de una función
        prototipo = ctx.prototSpyc()
        nombre_funcion = prototipo.getChild(1).getText()
        # Escribe el encabezado de la función en el intermedio
        self.archivoCodigoIntermedio.write(f"\n{nombre_funcion}:\n")
        # Procesa el cuerpo de la función
        self.visit(ctx.bloque())
        # Agrega retorno automático en el intermedio si no es main
        if nombre_funcion != "main":
            self.archivoCodigoIntermedio.write("retornar\n")

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
        # Procesa llamada a función: funcion(param1, param2)
        nombre_funcion = ctx.getChild(0).getText()
        # Recolecta parámetros del prototipo
        parametros = []
        env_par = ctx.envPar()
        if env_par and env_par.opal():
            param1 = self.visitOperacionSimple(env_par.opal())
            parametros.append(param1)
            # Procesa parámetros internos de la funcion
            lista_env = env_par.lista_envPar()
            while lista_env and lista_env.opal():
                param_extra = self.visitOperacionSimple(lista_env.opal())
                parametros.append(param_extra)
                lista_env = lista_env.lista_envPar()
        # Pasa parámetros usando variables vf0, vf1, vf2... (variable funcion)
        for i, param in enumerate(parametros):
            vf_name = f"vf{i}"
            self.archivoCodigoIntermedio.write(f"{vf_name} = {param}\n")
        # Genera llamada y almacena resultado
        temporal_resultado = self.getTemporal()
        self.archivoCodigoIntermedio.write(f"{temporal_resultado} = call {nombre_funcion}\n")
        
        return temporal_resultado

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
        # Procesa declaración de variables: int x, y, z;
        for i in range(1, ctx.getChildCount()):
            child = ctx.getChild(i)
            if hasattr(child, 'symbol') and child.symbol.type == compiladoresParser.ID:
                variable = child.getText()
                # Inicializa todas las variables con 0
                self.archivoCodigoIntermedio.write(f"{variable} = 0\n")

    def visitIwhile(self, ctx):
        # Procesa while(condicion) {...}
        etiqueta_inicio = self.getEtiqueta()
        etiqueta_fin = self.getEtiqueta()
        # Etiqueta de inicio del bucle
        self.archivoCodigoIntermedio.write(f"{etiqueta_inicio}:\n")
        # Procesa condición
        if ctx.cond():
            condicion_result = self.visitOperacionSimple(ctx.cond().opal())
            if condicion_result:
                self.archivoCodigoIntermedio.write(f"siFalso {condicion_result} ir a {etiqueta_fin}\n")
        # Procesa cuerpo del bucle
        self.visit(ctx.bloque())
        # Salto al inicio y etiqueta de fin
        self.archivoCodigoIntermedio.write(f"ir a {etiqueta_inicio}\n")
        self.archivoCodigoIntermedio.write(f"{etiqueta_fin}:\n")

    def visitIif(self, ctx):
        # Procesa if(condicion) {...}
        etiqueta_fin = self.getEtiqueta()
        # Procesa condición
        condicion_result = self.visitOperacionSimple(ctx.opal())
        if condicion_result:
            self.archivoCodigoIntermedio.write(f"siFalso {condicion_result} ir a {etiqueta_fin}\n")
        # Procesa cuerpo del if
        if ctx.bloque():
            self.visit(ctx.bloque())
        elif ctx.instruccion():
            self.visit(ctx.instruccion())
        # Etiqueta de fin del if
        self.archivoCodigoIntermedio.write(f"{etiqueta_fin}:\n")

    def visitIelse(self, ctx):
        # Procesa else
        self.visitChildren(ctx)

    def visitIfor(self, ctx):
        # Procesa for(init; cond; iter) {...}
        etiqueta_inicio = self.getEtiqueta()
        etiqueta_fin = self.getEtiqueta()
        # Inicialización
        if ctx.getChildCount() > 2:
            self.visit(ctx.getChild(2))
        # Etiqueta de inicio
        self.archivoCodigoIntermedio.write(f"{etiqueta_inicio}:\n")
        # Condición
        if ctx.getChildCount() > 4:
            condicion_result = self.visitOperacionSimple(ctx.getChild(4).opal())
            if condicion_result:
                self.archivoCodigoIntermedio.write(f"siFalso {condicion_result} ir a {etiqueta_fin}\n")
        
        # Cuerpo del bucle
        if ctx.getChildCount() > 8:
            self.visit(ctx.getChild(8))
        # Iteración
        if ctx.getChildCount() > 6:
            self.visit(ctx.getChild(6))
        
        # Salto al inicio y etiqueta de fin
        self.archivoCodigoIntermedio.write(f"ir a {etiqueta_inicio}\n")
        self.archivoCodigoIntermedio.write(f"{etiqueta_fin}:\n")

    def visitInit(self, ctx):
        # Procesa inicialización de for
        return self.visitChildren(ctx)

    def visitIter(self, ctx):
        # Procesa iteración de for
        return self.visitChildren(ctx)

    def visitCond(self, ctx):
        # Procesa condición de bucle/condicional
        return self.visitOperacionSimple(ctx.opal())

    def visitReturn(self, ctx):
        # Procesa return
        if ctx.opal():
            valor_retorno = self.visitOperacionSimple(ctx.opal())
            if valor_retorno:
                self.archivoCodigoIntermedio.write(f"retornar {valor_retorno}\n")
        else:
            self.archivoCodigoIntermedio.write("retornar\n")

    #---- Metodos de Procesamiento de Operaciones ----

    def visitOperacionSimple(self, ctx):
        # Metodo para todas las operaciones
        if ctx is None:
            return "0"
        # Operaciones simples
        if hasattr(ctx, 'NUMERO') and ctx.NUMERO():
            return ctx.NUMERO().getText()
        elif hasattr(ctx, 'ID') and ctx.ID():
            return ctx.ID().getText()
        # Operaciones complejas
        return self.procesarOperacionIterativa(ctx)

    def procesarOperacionIterativa(self, ctx):
        # Procesador iterativo de operaciones
        if ctx is None:
            return "0"
        texto = ctx.getText()
        # Comparaciones (x > 0, y == 5, etc.)
        if any(op in texto for op in ['>', '<', '>=', '<=', '==', '!=']):
            for op in ['>=', '<=', '==', '!=', '>', '<']:
                if op in texto:
                    partes = texto.split(op)
                    if len(partes) == 2:
                        izquierda = self.procesarSubOperacion(partes[0].strip())
                        derecha = self.procesarSubOperacion(partes[1].strip())
                        temporal = self.getTemporal()
                        self.archivoCodigoIntermedio.write(f"{temporal} = {izquierda} {op} {derecha}\n")
                        return temporal
        
        # Operaciones Aritmeticas (x + 1, y * 2, etc.)
        for op in ['+', '-', '*', '/', '%']:
            if op in texto:
                partes = texto.split(op)
                if len(partes) == 2:
                    izquierda = self.procesarSubOperacion(partes[0].strip())
                    derecha = self.procesarSubOperacion(partes[1].strip())
                    temporal = self.getTemporal()
                    self.archivoCodigoIntermedio.write(f"{temporal} = {izquierda} {op} {derecha}\n")
                    return temporal
    
        # Entre Parentesis
        if texto.startswith('(') and texto.endswith(')'):
            return self.visitOperacionSimple(ctx.getChild(1) if ctx.getChildCount() > 1 else None)
        
        # Valor
        return texto

    def procesarSubOperacion(self, operacion):
        # Procesa y descompone operaciones complejas
        for op in ['*', '/', '%', '+', '-']:
            if op in operacion:
                partes = operacion.split(op)
                if len(partes) == 2:
                    izquierda = partes[0].strip()
                    derecha = partes[1].strip()
                    temporal = self.getTemporal()
                    self.archivoCodigoIntermedio.write(f"{temporal} = {izquierda} {op} {derecha}\n")
                    return temporal
        # Si no hay operaciones, retornar la operacion tal cual
        return operacion

    #---- Metodos para de "paso" ----
    def visitOpal(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitOr(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitAnd(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitComp(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitExp(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitTerm(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitFactor(self, ctx):
        return self.visitOperacionSimple(ctx)
    def visitC(self, ctx):
        return ctx.getText()
    def visitChildren(self, ctx):
        # Método para procesar hijos de un nodo
        if ctx.getChildCount() > 0:
            return self.visit(ctx.getChild(0))
        return None
    def visitPrototipoFuncion(self, ctx):
        # Procesa prototipos de función 
        pass
