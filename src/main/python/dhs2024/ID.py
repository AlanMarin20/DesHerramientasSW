from enum import Enum

class TipoDato(Enum) :
    VOID = 'void'
    INT = 'int'
    FLOAT = 'float'
    BOOLEAN = 'bool'
    DOUBLE = 'double'
    CHAR = 'char'

class ID() :

    def __init__(self, nombre, tD, declarado, inicializado, usado):
        self.nombre = nombre
        self.tipoDato = TipoDato(tD)
        self.declarado = declarado
        self.inicializado = inicializado
        self.usado = usado

    def __str__(self):
        return("ID: \t" + self.nombre + "\t" + str(self.tipoDato))
    
class Variable(ID) :
    def __init__(nombre, tipoDatoVariable, declarado, inicializado, usado):
        super.__init__(nombre, tipoDatoVariable, declarado, inicializado, usado)

class Funcion(ID) :
    def __init__(self, nombre, tipoDato, declarado,  inicializado, usado, args):
        super.__init__(nombre, tipoDato, declarado, inicializado, usado)
        self.args = args