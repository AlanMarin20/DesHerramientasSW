import sys
from antlr4 import *
from compiladoresLexer import compiladoresLexer
from compiladoresParser import compiladoresParser
from Visitor import Visitor
from Walker import Walker
from Optimizador import Optimizador

def main(argv):
    archivo = "input/entrada.txt"
    if len(argv) > 1:
        archivo = argv[1]
    
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    tree = parser.programa()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("Error de sintaxis detectado")
        print("Compilación cancelada - No se generó código")
        return

    # PRIMERO: Análisis semántico
    print("=== ANÁLISIS SEMÁNTICO ===")
    visitor = Visitor()
    visitor.visitPrograma(tree)
    
    if visitor.errores:
        print("Hubo errores semánticos. No se genera código.")
        return 

    # SEGUNDO: Generación de código intermedio
    print("\n=== GENERACIÓN CÓDIGO INTERMEDIO ===")
    walker = Walker()
    walker.visitPrograma(tree)
    # El walker genera el archivo en: "./output/codigoIntermedio.txt"

    # TERCERO: Optimización de código
    print("\n=== OPTIMIZACIÓN DE CÓDIGO ===")
    
    # 1. Le decimos al optimizador que lea el archivo que acaba de crear el Walker
    ruta_generada_por_walker = "./output/codigoIntermedio.txt"
    opt = Optimizador(ruta_generada_por_walker)
    
    # 2. Ejecutamos el Pipeline COMPLETO (en orden)
    opt.acomodar_entrada()           # Limpia espacios y carga en memoria
    opt.generar_bloques()            # Detecta bloques básicos
    
    opt.propagacion_constantes()     # Fase 1: Matemática
    opt.exp_comunes()                # Fase 2: Reducción de lógica
    opt.eliminar_codigo_muerto()     # Fase 3: Limpieza final

    print(f"\nProceso finalizado. Código optimizado en: {opt.ruta_optimizada}")

if __name__ == '__main__':
    main(sys.argv)