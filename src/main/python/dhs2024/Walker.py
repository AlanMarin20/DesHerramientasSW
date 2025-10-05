from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class VarTemporal:
    contador = -1
    def __init__(self):
        self.nombre = "t" + self.contador
        self.contador = self.contador + 1
        self.proxOp = "" 
        self.prim = 0

class Walker (compiladoresVisitor) :

    contadorVarTemporales = 0 
    variablesTemporales = [] #Guarda el nombre de las variables temporales
    operadorSumaResta = [] #Guarda los signos + y -
    operadorMulDiv = [] #Guarda los signos * y /
    varAAsignar = '' #Guarda x si x = a+b

    argumentosFunciones = []
    varReturn = []

    archivoCodigoIntermedio = open("./output/codigoIntermedio.txt", "w") #Archivo codigo limpio

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        super().visitPrograma(ctx)
        self.archivoCodigoIntermedio.close()

    
    
#     def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
#         print(ctx.getChild(0).getText() + " - " +
#               ctx.getChild(1).getText())
#         #return super().visitDeclaracion(ctx)
#         return None 
    
#     def visitBloque(self, ctx: compiladoresParser.BloqueContext):
#         print("Nuevo contexto\n")
#         print(ctx.getText())
#         return super().visitIstrucciones(ctx.getChild(1))
    
#     def visitTerminal(self, node):
#         print("==>> Token " + node.getText())
#         return super().visitTerminal(node)
        
