class Contexto():

    def __init__(self) :
        self.tabla = {}

    def traerVariable(self, nombre) :
        if nombre in self.tabla:
            return nombre
        else:
            return None
        
    def imprimirTabla(self):
        for clave, valor in self.tabla.items():
            print(f"{clave}: {valor}")