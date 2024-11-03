from Contexto import Contexto
from ID import ID

class TablaSimbolos(object) :
    
    __instance = None
    contextos = []

    def __new__(cls):
        if TablaSimbolos.__instance is None:
            TablaSimbolos.__instance = object.__new__(cls)
        return TablaSimbolos.__instance
    
    def __init__(self) :
        contextoGlobal = Contexto()
        self.contextos.append(contextoGlobal)

    def addContexto(self, contexto) :
        self.contextos.append(contexto)
        print("largo de la lista de contextos: "+ str(len(self.contextos)))

    def delContexto(self) :
        if len(self.contextos) > 1: #Verifica si hay o no contextos antes de eliminar
            self.contextos.pop()
        else:
            print("No hay contextos para eliminar.")

    def addIdentificador(self, nombre, tipoDato) :
        contexto = self.contextos[-1]
        id = ID(nombre, tipoDato, 1, 0, 0) #declarado,inicialidado,usado
        contexto.tabla.update({nombre:id})
        # print("SE ANADIO UN IDENTIFICADOR")

    def buscarLocal(self, nombre) : 
        if (self.contextos[-1].traerVariable(nombre)) != None:
        #    print('"' + nombre + '" se esta usando a nivel LOCAL\n') 
            variable = self.contextos[-1].traerVariable(nombre)
            return variable  # Retorna la instancia
        return None # Retorna None si no existe
        
    def buscarGlobal(self, nombre) :
        if(self.contextos[0].traerVariable(nombre)) != None:
        #    print('"' + nombre + " ya esta siendo usada globalmente\n")
            variable = self.contextos[0].traerVariable(nombre)
            return variable  # Retorna la instancia
        return None # Retorna None si no existe
    
    def buscarFuncionGlobal(self, nombre) :
        if(self.contextos[0].traerVariable(nombre)) != None:
            print('"' + nombre + '" esta declarada, se puede usar\n')
            return 1
        return 0

    # def controlarUsadosTabla(self):
    #     self.contextos[-1].controlarUsados()

    # def controlarUsados(self):
    #     print("Estado de uso de las variables:")
    #     for nombre, id in self.tabla.items():
    #         if id.usado == 0:
    #             print('WARNING(error semantico): La variable: ' + nombre + ' esta declarada pero no usada')
    
    def controlarUsados(self):
        noUsados=[]
        noInit=[]
        print("Estado de uso de las variables:")
        contexto_actual = self.contextos[-1]  # Obtener el contexto actual
        for nombre, id in contexto_actual.tabla.items():  # Acceder a la tabla del contexto actual
            print(f'Variable: {nombre}, Estado Uso: {id.usado}, Estado Inicializado: {id.inicializado}')
            if id.usado == 0:
                noUsados.append(nombre)
            if id.inicializado == 0:
                noInit.append(nombre)    
        print("\n\n")
        for i in noUsados:
            print(f'WARNING(error semantico): La variable: {i} esta declarada pero no usada')
        print("\n")
        for j in noInit:
            print(f'WARNING(error semantico): La variable: {j} no esta incializada, no puedes usarla')
              
