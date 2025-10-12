from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Walker (compiladoresVisitor):

    contadorTemporales = 0
    contadorEtiquetas = 0
    
    archivoCodigoIntermedio = open("./output/codigoIntermedio.txt", "w")
    archivoCodigoIntermedioComentarios = open("./output/codigoIntermedioComentarios.txt", "w")

    def getTemporal(self):
        self.contadorTemporales += 1
        return f"t{self.contadorTemporales}"
    
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Generando codigo intermedio")
        self.visitInstrucciones(ctx.getChild(0))
        print("Codigo intermedio generado")
        self.archivoCodigoIntermedio.close()
        self.archivoCodigoIntermedioComentarios.close()
        
    def visitInstrucciones(self, ctx: compiladoresParser.InstruccionesContext):
        # Procesar todos los hijos que sean instrucciones individuales
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            # Si es una instrucción individual, procesarla
            if hasattr(child, 'getRuleIndex') and not isinstance(child, compiladoresParser.InstruccionesContext):
                print(f"Procesando instruccion: {child.getText()}")
                self.visit(child)
            # Si es más instrucciones, visitarlas recursivamente
            elif isinstance(child, compiladoresParser.InstruccionesContext):
                self.visit(child)

    def visitFuncion(self, ctx):
        print("Procesando funcion")
        self.visit(ctx.bloque())

    def visitBloque(self, ctx):
        if ctx.getChildCount() > 1:
            self.visit(ctx.getChild(1))

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print(f"Asignacion: {ctx.getText()}")
        variable = ctx.getChild(0).getText()
        
        # Obtener el primer opal de la lista
        opales = ctx.opal()
        if opales is not None:
            resultado = self.visitOpal(opales)
            self.archivoCodigoIntermedio.write(f"{variable} = {resultado}\n")
            print(f"Codigo: {variable} = {resultado}")

    def visitDeclAsig(self, ctx: compiladoresParser.DeclAsigContext):
        print(f"DeclAsig: {ctx.getText()}")
        
        if ctx.declaracion():
            # Obtener la primera variable
            for i in range(1, ctx.declaracion().getChildCount()):
                child = ctx.declaracion().getChild(i)
                if hasattr(child, 'symbol') and child.symbol.type == compiladoresParser.ID:
                    variable = child.getText()
                    print(f"Variable encontrada: {variable}")
                    
                    # Obtener el primer opal de la lista
                    opales = ctx.opal()
                    if opales is not None:
                        resultado = self.visitOpal(opales)
                        self.archivoCodigoIntermedio.write(f"{variable} = {resultado}\n")
                        print(f"Codigo: {variable} = {resultado}")
                    break

    def visitOpal(self, ctx):
        # CORRECCIÓN: Manejar tanto listas como objetos contexto
        if isinstance(ctx, list):
            # Si es una lista, tomar el primer elemento
            if len(ctx) > 0:
                ctx = ctx[0]
            else:
                return "0"
        
        # Ahora ctx debería ser un objeto contexto, no una lista
        if ctx is None:
            return "0"
            
        print(f"visitOpal llamado con: {ctx.getText()}")
        
        if hasattr(ctx, 'getChildCount') and ctx.getChildCount() > 0:
            print(f"Opal tiene {ctx.getChildCount()} hijos")
            return self.visit(ctx.getChild(0))  # Usar visit en lugar de visitOr directo
        
        print("Opal sin hijos, retornando 0")
        return "0"

    def visitOr(self, ctx):
        if not hasattr(ctx, 'getChildCount') or ctx.getChildCount() == 0:
            return "0"
            
        left = self.visit(ctx.getChild(0))  # Usar visit en lugar de visitAnd
        
        if ctx.getChildCount() > 1 and ctx.getChild(1).getText() == '||':
            if ctx.getChildCount() > 2:
                right = self.visit(ctx.getChild(2))  # Usar visit en lugar de visitOr
                temporal = self.getTemporal()
                self.archivoCodigoIntermedio.write(f"{temporal} = {left} || {right}\n")
                return temporal
        return left

    def visitAnd(self, ctx):
        if not hasattr(ctx, 'getChildCount') or ctx.getChildCount() == 0:
            return "0"
            
        left = self.visit(ctx.getChild(0))  # Usar visit en lugar de visitComp
        
        if ctx.getChildCount() > 1 and ctx.getChild(1).getText() == '&&':
            if ctx.getChildCount() > 2:
                right = self.visit(ctx.getChild(2))  # Usar visit en lugar de visitAnd
                temporal = self.getTemporal()
                self.archivoCodigoIntermedio.write(f"{temporal} = {left} && {right}\n")
                return temporal
        return left

    def visitComp(self, ctx):
        if not hasattr(ctx, 'getChildCount') or ctx.getChildCount() == 0:
            return "0"
            
        left = self.visit(ctx.getChild(0))  # Usar visit en lugar de visitExp
        
        if ctx.getChildCount() > 1:
            op = ctx.getChild(1).getText()
            if ctx.getChildCount() > 2:
                right = self.visit(ctx.getChild(2))  # Usar visit en lugar de visitComp
                temporal = self.getTemporal()
                self.archivoCodigoIntermedio.write(f"{temporal} = {left} {op} {right}\n")
                return temporal
        return left

    def visitExp(self, ctx):
        if not hasattr(ctx, 'getChildCount') or ctx.getChildCount() == 0:
            return "0"
            
        left = self.visit(ctx.getChild(0))  # Usar visit en lugar de visitTerm
        
        i = 1
        while i < ctx.getChildCount():
            if i + 1 < ctx.getChildCount():
                op = ctx.getChild(i).getText()
                right = self.visit(ctx.getChild(i + 1))  # Usar visit en lugar de visitTerm
                temporal = self.getTemporal()
                self.archivoCodigoIntermedio.write(f"{temporal} = {left} {op} {right}\n")
                left = temporal
                i += 2
            else:
                break
        
        return left

    def visitTerm(self, ctx):
        if not hasattr(ctx, 'getChildCount') or ctx.getChildCount() == 0:
            return "0"
            
        left = self.visit(ctx.getChild(0))  # Usar visit en lugar de visitFactor
        
        i = 1
        while i < ctx.getChildCount():
            if i + 1 < ctx.getChildCount():
                op = ctx.getChild(i).getText()
                right = self.visit(ctx.getChild(i + 1))  # Usar visit en lugar de visitFactor
                temporal = self.getTemporal()
                self.archivoCodigoIntermedio.write(f"{temporal} = {left} {op} {right}\n")
                left = temporal
                i += 2
            else:
                break
        
        return left

    def visitFactor(self, ctx):
        if ctx.NUMERO():
            return ctx.NUMERO().getText()
        elif ctx.ID():
            return ctx.ID().getText()
        elif ctx.PA() and ctx.getChildCount() > 1:
            return self.visit(ctx.getChild(1))
        return "0"

    def visitDeclaracion(self, ctx):
        pass

