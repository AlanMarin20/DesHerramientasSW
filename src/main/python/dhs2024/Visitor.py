from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos


#Primero tenemos dos clases, Temporal y Etiqueta
#Temporal genera los t0,t1,etc, incrementando el contador cada vez que solicitamos una nueva
#Etiqueta genera l0,l1,etc para gestion de control de flujo, para los for,while,etc.
class Temporal(): #Temporales t0,t1,t2,...,
    def __init__(self):
        self.contador = -1
  
    def getTemporal(self):
        self.contador += 1
        print(f"Generando temporal: t{self.contador}")
        return f't{self.contador}'
  
class Etiqueta(): #Labels para control de flujo
    def __init__(self):
        self.contador = -1


    def getEtiqueta(self):
        self.contador += 1
        return f'l{self.contador}'


class Visitor (compiladoresVisitor):
    def __init__(self):
      
        self.file = None
        self.ruta = './output/codigoIntermedio.txt' #Donde se guarda el archivo con el cod intermedio
        self.temporales = [] #Almacena los temporales generados
        self.etiquetas = [] #Almacena las etiquetas generadas
        self.generadorDeTemporales = Temporal() #Instancia de la clase Temporal, se encarga de generar los nuevos temporales
        self.generadorDeEtiquetas = Etiqueta()
        self.tablaDeSimbolos = TablaSimbolos()


        self.operando1 = None
        self.operando2 = None
        self.operador = None
        self.isSumador = False #Para saber si la operacion actual esta relacionada con una suma
        self.isFuncion = False #Para saber si el codigo q se esta procesando corresponde a una funcion
        
        self.etiquetaFuncion = {}
        self.funcionInvocada = {}
        self.isReturn = False #Indica si el codigo actual genera un instruccion de return


        # Constantes Codigo Intermedio de Tres Direcciones
        self.etiqueta = 'label'
        self.b = 'jmp'
        self.bneq = 'ifnjmp'


    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("------------------------")
        print("Se empieza a generar el codigo intermedio")
        self.file = open(self.ruta, "w") #Abrimos el archivo especificado en ruta para que se escriba el codigo intermedio
        self.visitInstrucciones(ctx.getChild(0)) #Visitamos las intrucciones del programa
        self.file.close() #Cerramos el archivo
        print("Se termino de generar el codigo intermedio")
        print("------------------------")

    def visitInstrucciones(self, ctx: compiladoresParser.InstruccionesContext):
        for instruccion in ctx.getChildren():
            self.visit(instruccion)
        return

    def visitInstruccion(self, ctx: compiladoresParser.InstruccionContext):
        return self.visitChildren(ctx)

    def visitBloque(self, ctx: compiladoresParser.BloqueContext):
        return self.visitChildren(ctx)
  
    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        primer_id = ctx.getChild(1).getText()
        self.file.write(f"{primer_id}\n")  # Inicializar la variable (opcional)
        for i in range(3, ctx.getChildCount(), 2):
            id_actual = ctx.getChild(i).getText()
            self.file.write(f"{id_actual}\n") 

    def visitOpal(self, ctx):
        print("Entra al Opal")
        print(f"Cantidad de hijos en Opal: {ctx.getChildCount()}")

        if isinstance(ctx.getChild(0), compiladoresParser.OrContext):  
            print("Entra a un Or")
            return self.visitOr(ctx.getChild(0))  
        else:
            resultado = self.visitChildren(ctx)
            if resultado is None:
                print(f"+++ Advertencia: visit{ctx.__class__.__name__} devolvió None +++")
            return resultado

    def visitOr(self, ctx):
        print("Llama al visitOr")
        if isinstance(ctx.getChild(0), compiladoresParser.OContext):
            print("Entra a un O")
            return self.visitO(ctx.getChild(0))  # Devuelve el resultado
        elif isinstance(ctx.getChild(0), compiladoresParser.AndContext):
            print("Entra a un And")
            return self.visitAnd(ctx.getChild(0))  # Devuelve el resultado
        else:
            resultado = self.visitChildren(ctx)
            if resultado is None:
                print(f"+++ Advertencia: visit{ctx.__class__.__name__} devolvió None +++")
            return resultado
                
    def visitO(self, ctx):
        print("Llama al visitO")
        if ctx is None or ctx.getChildCount() == 0:
            print("+++ ERROR: ctx en visitO es None o no tiene hijos +++")
        else: 
            if isinstance(ctx.getChild(0), compiladoresParser.ExpContext):
                print("Entra a una exp")
                return self.visitExp(ctx.getChild(0))  # Devuelve el resultado
            else:
                resultado = self.visitChildren(ctx)
                if resultado is None:
                    print(f"+++ Advertencia: visit{ctx.__class__.__name__} devolvió None +++")
                return resultado
    
    def visitAnd(self, ctx):
        print(f"Cantidad de hijos en And: {ctx.getChildCount()}")
        for i in range(ctx.getChildCount()):
            print(f"  Hijo {i}: {ctx.getChild(i).getText()}")

        resultado = self.visit(ctx.getChild(0))

        i = 1
        while i < ctx.getChildCount():
            if i+1 >= ctx.getChildCount():
                print("+++ ERROR: Se intentó acceder a un hijo fuera de rango en visitAnd +++")
                break
            
            operador = ctx.getChild(i).getText()
            siguiente_exp = self.visit(ctx.getChild(i+1))
            
            if siguiente_exp is None:
                print(f"+++ ERROR: visitExp devolvió None en visitAnd +++")
                break

            print(f"Operación: {resultado} {operador} {siguiente_exp}")
            resultado = f"{resultado} {operador} {siguiente_exp}"

            i += 2

        return resultado

    def visitExp(self, ctx):
        print("Llama al visitExp")
        if isinstance(ctx.getChild(0), compiladoresParser.TermContext):
            print("Entra a un term")
            return self.visitTerm(ctx.getChild(0))  # Devuelve el resultado
        else:
            resultado = self.visitChildren(ctx)
            if resultado is None:
                print(f"+++ Advertencia: visit{ctx.__class__.__name__} devolvió None +++")
            return resultado
    
    def visitTerm(self, ctx):
        print(f"Cantidad de hijos en Term: {ctx.getChildCount()}")
        for i in range(ctx.getChildCount()):
            print(f"  Hijo {i}: {ctx.getChild(i).getText()}")

        if ctx.getChildCount() == 0:
            print("+++ ERROR: visitTerm recibió un nodo vacío +++")
            return ""

        resultado = self.visit(ctx.getChild(0))  # Visita el primer factor

        i = 1
        while i < ctx.getChildCount():
            if i+1 >= ctx.getChildCount():
                print("+++ ERROR: Se intentó acceder a un hijo fuera de rango en visitTerm +++")
                break  # Salimos del bucle si no hay suficientes hijos
            
            operador = ctx.getChild(i).getText()  # Puede ser "*" o "/"
            siguiente_factor = self.visit(ctx.getChild(i+1))
            
            if siguiente_factor is None:
                print(f"+++ ERROR: visitFactor devolvió None en visitTerm +++")
                break

            print(f"Operación: {resultado} {operador} {siguiente_factor}")
            resultado = f"{resultado} {operador} {siguiente_factor}"

            i += 2  # Saltar al siguiente operador

        return resultado
    
    def visitFactor(self, ctx):
        print("Entra a un factor")
        
        if ctx.getChildCount() == 1:  # Si el factor es un número o una variable
            valor = ctx.getChild(0).getText()
            print(f"Factor encontrado: {valor}")
            return valor  # Devuelve el valor del número o variable

        elif ctx.getChildCount() == 3:  # Si es una expresión entre paréntesis (expr)
            return self.visit(ctx.getChild(1))  # Evalúa lo que hay dentro

        print("+++ ERROR: No se pudo reconocer el factor +++")
        return ""
            

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        nombreVariable = ctx.getChild(0).getText()
        print(f'Asignando a la variable: "{nombreVariable}"\n')
        resultado = self.visitOpal(ctx.getChild(2))
        print("resultado = " + resultado)
        self.file.write(f"{nombreVariable} = {resultado}\n")


   # def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
   #     # Nombre de la variable de la asignación
   #     nombreVariable = ctx.getChild(0).getText()
   #     print(f'Asignando a la variable: "{nombreVariable}"\n')
      
   #     # La expresión a la derecha de la asignación
   #     expDerecha = ctx.getChild(2)
   #     print(expDerecha.getChildCount()) #ESTE ES EL PROBLEMA, SIEMPRE VA A TIRAR COMO QUE ES 1
   #     # Verificamos si hay más de un child, lo que indicaría que hay una operación
   #     if expDerecha.getChildCount() > 1:  # Es una opal
   #         print("ENTRA AL IF OPAL")
   #         operando1 = self.visit(expDerecha.getChild(0))  # Primer operando
   #         operador = expDerecha.getChild(1).getText()  # Operador (+, -, *, /, etc.)
   #         operando2 = self.visit(expDerecha.getChild(2))  # Segundo operando


   #         # Generamos el temporal
   #         temporal = self.generadorDeTemporales.getTemporal()


   #         # Hacemos la operacion y escribimos el codigo intermedio
   #         if operador == "+":
   #             self.file.write(f"{temporal} = {operando1} + {operando2}\n")
   #         elif operador == "-":
   #             self.file.write(f"{temporal} = {operando1} - {operando2}\n")
   #         elif operador == "*":
   #             self.file.write(f"{temporal} = {operando1} * {operando2}\n")
   #         elif operador == "/":
   #             self.file.write(f"{temporal} = {operando1} / {operando2}\n")
   #         else:
   #             print(f"+++ERROR: Operador '{operador}' no reconocido+++")
   #             return


   #         # Finalmente, asignamos el resultado al temporal
   #         self.file.write(f"{nombreVariable} = {temporal}\n")
   #     else:
   #         # Si no es una operación, simplemente asignamos el valor directo
   #         print("ENTRA AL ELSE VALOR DIRECTO")
          
   #         valorDerecha = self.visit(expDerecha)  # Valor directo (puede ser una variable, número, etc.)
   #         self.file.write(f"{nombreVariable} = {valorDerecha}\n")


   #     expDerecha = ctx.getChild(2)  # `opal`
   #     valorDerecha = self.obtenerFactor(expDerecha)
   #     print(f"Valor derecha: {valorDerecha}")
   #     self.file.write(f"{nombreVariable} = {valorDerecha}\n")
  
