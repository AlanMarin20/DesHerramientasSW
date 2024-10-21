import sys
from Escucha import Escucha
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from Walker import Walker


def main(argv):
    archivo = "input/opal.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo) #se encarga de leer la entrada
    lexer = compiladoresLexer(input) #genera tokens pidiendosele caracteres al archivo
    stream = CommonTokenStream(lexer) 
    parser = compiladoresParser(stream) #levanta tokens, es el que guia
    escucha = Escucha() 
    parser.addParseListener(escucha) 
    tree = parser.programa()
   # print(tree.toStringTree(recog=parser)) #esta linea impime el arbol 
    caminante = Walker()
    caminante.visitPrograma(tree)

if __name__ == '__main__':
    main(sys.argv)