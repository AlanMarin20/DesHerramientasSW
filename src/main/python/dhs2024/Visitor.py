from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from antlr4.tree.Tree import TerminalNodeImpl

class Visitor(compiladoresVisitor):
    def __init__(self):
        self.tablaDeSimbolos = TablaSimbolos()
        self.errores = []

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Iniciando análisis semántico...")
        self.visitInstrucciones(ctx.getChild(0))
        
        # Al final del programa, controlar variables no usadas
        self.tablaDeSimbolos.controlarUsados()
        
        if self.errores:
            print("Se encontraron errores semánticos:")
            for error in self.errores:
                print(f" - {error}")
        else:
            print("Análisis semántico completado sin errores")

    def visitInstrucciones(self, ctx: compiladoresParser.InstruccionesContext):
        for instruccion in ctx.getChildren():
            if instruccion and not isinstance(instruccion, compiladoresParser.InstruccionesContext):
                self.visit(instruccion)

    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        # int x, y, z;
        tipo = ctx.getChild(0).getText()
        
        # Procesar todas las variables en la declaración
        for i in range(1, ctx.getChildCount()):
            child = ctx.getChild(i)
            # Solo procesar IDs, ignorar comas
            if hasattr(child, 'symbol') and child.symbol.type == compiladoresParser.ID:
                variable = child.getText()
                
                # Verificar si la variable ya existe
                if self.tablaDeSimbolos.buscarLocal(variable) or self.tablaDeSimbolos.buscarGlobal(variable):
                    self.errores.append(f"Variable '{variable}' ya declarada")
                else:
                    self.tablaDeSimbolos.addIdentificador(variable, tipo)
                    print(f"Variable declarada: {tipo} {variable}")

    def visitDeclAsig(self, ctx: compiladoresParser.DeclAsigContext):
        # int x = 5;
        if ctx.declaracion():
            tipo = ctx.declaracion().getChild(0).getText()
            # Obtener la primera variable de la declaración
            for i in range(1, ctx.declaracion().getChildCount()):
                child = ctx.declaracion().getChild(i)
                if hasattr(child, 'symbol') and child.symbol.type == compiladoresParser.ID:
                    variable = child.getText()
                    
                    # Verificar si la variable ya existe
                    if self.tablaDeSimbolos.buscarLocal(variable) or self.tablaDeSimbolos.buscarGlobal(variable):
                        self.errores.append(f"Variable '{variable}' ya declarada")
                    else:
                        self.tablaDeSimbolos.addIdentificador(variable, tipo)
                        # Marcar como inicializada
                        id_obj = self.tablaDeSimbolos.buscarLocal(variable)
                        if id_obj:
                            id_obj.inicializado = 1
                        print(f"Variable declarada y asignada: {tipo} {variable}")
                    break  # Solo procesar la primera variable

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        # x = 5;
        variable = ctx.getChild(0).getText()
        
        # Verificar que la variable exista
        id_obj = self.tablaDeSimbolos.buscarLocal(variable) or self.tablaDeSimbolos.buscarGlobal(variable)
        if not id_obj:
            self.errores.append(f"Variable '{variable}' no declarada")
        else:
            # Marcar como usada e inicializada
            id_obj.usado = 1
            id_obj.inicializado = 1
            print(f"Asignación válida a variable: {variable}")

    def visitOpal(self, ctx):
        # Análisis de expresiones - verificar que las variables usadas existan
        return self.visitChildren(ctx)

    def visitFactor(self, ctx):
        if ctx.ID():
            variable = ctx.ID().getText()
            id_obj = self.tablaDeSimbolos.buscarLocal(variable) or self.tablaDeSimbolos.buscarGlobal(variable)
            if not id_obj:
                self.errores.append(f"Variable '{variable}' no declarada")
            else:
                # Marcar como usada
                id_obj.usado = 1
        return None

    def visitIif(self, ctx):
        print("Analizando estructura if")
        # Evaluar la condición
        self.visitOpal(ctx.getChild(2))
        # Procesar el cuerpo
        self.visit(ctx.getChild(4))
        return None

    def visitIwhile(self, ctx):
        print("Analizando estructura while")
        # Evaluar la condición
        self.visitOpal(ctx.getChild(2))
        # Procesar el cuerpo
        self.visit(ctx.bloque())
        return None

    def visitIfor(self, ctx):
        print("Analizando estructura for")
        
        # Crear nuevo contexto para el for
        from Contexto import Contexto
        nuevo_contexto = Contexto()
        self.tablaDeSimbolos.addContexto(nuevo_contexto)
        
        # Procesar inicialización
        if ctx.init():
            self.visitInit(ctx.init())
        
        # Procesar condición
        if ctx.cond():
            self.visitCond(ctx.cond())
        
        # Procesar iteración
        if ctx.iter():
            self.visitIter(ctx.iter())
        
        # Procesar cuerpo
        self.visit(ctx.bloque())
        
        # Salir del contexto del for
        self.tablaDeSimbolos.delContexto()
        
        return None

    def visitInit(self, ctx):
        # x = 5 (en for)
        variable = ctx.getChild(0).getText()
        
        # Verificar que la variable exista
        id_obj = self.tablaDeSimbolos.buscarLocal(variable) or self.tablaDeSimbolos.buscarGlobal(variable)
        if not id_obj:
            self.errores.append(f"Variable '{variable}' no declarada en for")
        else:
            id_obj.usado = 1
            id_obj.inicializado = 1

    def visitFuncion(self, ctx):
        prototipo = ctx.prototSpyc()
        
        # Obtener tipo de retorno y nombre según tu gramática
        if prototipo.getChild(0).getText() == 'void':
            tipo_retorno = 'void'
            nombre_funcion = prototipo.getChild(1).getText()
        else:
            tipo_retorno = prototipo.getChild(0).getText()
            nombre_funcion = prototipo.getChild(1).getText()
        
        print(f"Analizando función: {tipo_retorno} {nombre_funcion}()")
        
        # Agregar nuevo contexto para la función
        from Contexto import Contexto
        nuevo_contexto = Contexto()
        self.tablaDeSimbolos.addContexto(nuevo_contexto)
        
        # Procesar parámetros si existen
        if prototipo.parFunc():
            self.visitParFunc(prototipo.parFunc())
        
        # Procesar cuerpo de la función
        self.visit(ctx.bloque())
        
        # Salir del contexto de la función
        self.tablaDeSimbolos.delContexto() 

    def visitParFunc(self, ctx):
        # Procesar parámetros de función: int x, int y
        i = 0
        while i < ctx.getChildCount():
            child = ctx.getChild(i)
            # Si es un tipo de dato, procesar el siguiente como ID
            if isinstance(child, compiladoresParser.TipodatoContext):
                tipo_param = child.getText()
                if i + 1 < ctx.getChildCount():
                    next_child = ctx.getChild(i + 1)
                    if hasattr(next_child, 'symbol') and next_child.symbol.type == compiladoresParser.ID:
                        nombre_param = next_child.getText()
                        
                        # Agregar parámetro a la tabla de símbolos
                        self.tablaDeSimbolos.addIdentificador(nombre_param, tipo_param)
                        print(f"Parámetro: {tipo_param} {nombre_param}")
                        i += 2
                        continue
            i += 1

    def visitReturn(self, ctx):
        print("Analizando return")
        if ctx.opal():
            self.visitOpal(ctx.opal())
        return None

    def visitBloque(self, ctx: compiladoresParser.BloqueContext):
        # Los bloques crean nuevo contexto
        from Contexto import Contexto
        nuevo_contexto = Contexto()
        self.tablaDeSimbolos.addContexto(nuevo_contexto)
        
        # Procesar instrucciones dentro del bloque
        self.visitChildren(ctx)
        
        # Salir del contexto del bloque
        self.tablaDeSimbolos.delContexto()
        
        return None


    # Métodos para reglas que no requieren lógica especial
    def visitPartesumaresta(self, ctx):
        return self.visitChildren(ctx)

    def visitPartemuldivmod(self, ctx):
        return self.visitChildren(ctx)

    def visitParteigualdad(self, ctx):
        return self.visitChildren(ctx)

    def visitParterelacion(self, ctx):
        return self.visitChildren(ctx)

    def visitParteand(self, ctx):
        return self.visitChildren(ctx)

    def visitParteor(self, ctx):
        return self.visitChildren(ctx)
    

