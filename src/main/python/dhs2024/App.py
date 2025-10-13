import sys
from antlr4 import *
from compiladoresLexer import compiladoresLexer
from compiladoresParser import compiladoresParser
from Visitor import Visitor
from Walker import Walker
from Optimizador import Optimizador

def main(argv):
    archivo = "input/opal.txt"
    if len(argv) > 1:
        archivo = argv[1]
    
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    tree = parser.programa()
    
    # PRIMERO: Análisis semántico
    print("=== ANÁLISIS SEMÁNTICO ===")
    visitor = Visitor()
    visitor.visitPrograma(tree)
    
    # SEGUNDO: Generación de código intermedio
    print("\n=== GENERACIÓN CÓDIGO INTERMEDIO ===")
    walker = Walker()
    walker.visitPrograma(tree)

    # TERCERO: Optimización de código
    opt = Optimizador()
    opt.acomodar_entrada()
    opt.generar_bloques()
 
if __name__ == '__main__':
    main(sys.argv)
