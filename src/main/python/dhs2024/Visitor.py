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

        return self.visitChildren(ctx)

    def visitOr(self, ctx):
        print("Llama al visitOr")
        if isinstance(ctx.getChild(0), compiladoresParser.OContext):
            print("Entra a un O")
            return self.visitO(ctx.getChild(0))  # Devuelve el resultado
        else:
            return self.visitChildren(ctx)
    
    def visitO(self, ctx):
        print("Llama al visitO")
        if isinstance(ctx.getChild(0), compiladoresParser.ExpContext):
            print("Entra a una exp")
            return self.visitExp(ctx.getChild(0))  # Devuelve el resultado
        else:
            return self.visitChildren(ctx)
    
    def visitExp(self, ctx):
        print("Llama al visitExp")
        if isinstance(ctx.getChild(0), compiladoresParser.TermContext):
            print("Entra a un term")
            return self.visitTerm(ctx.getChild(0))  # Devuelve el resultado
        else:
            return self.visitChildren(ctx)
    
    def visitTerm(self, ctx):
        print("Llama al visitTerm")
        if isinstance(ctx.getChild(0), compiladoresParser.FactorContext):
            print("Entra a un factor")
            return self.visitFactor(ctx.getChild(0))  # Devuelve el resultado
        else:
            return self.visitChildren(ctx)
    
    def visitFactor(self, ctx):
        print("Llego al factor")
        return super().visitFactor(ctx)
    

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
  
