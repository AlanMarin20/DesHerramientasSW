from Optimizador import Optimizador

if __name__ == "__main__":
    # Creamos instancia del optimizador
    opt = Optimizador("src/main/python/optimizador/input_codigo.txt")   # Asegurate de tener este archivo en la raíz del proyecto

    # Paso 1: Acomodar (limpiar) la entrada
    opt.acomodar_entrada()

    # Paso 2: Generar bloques básicos (y funciones)
    opt.generar_bloques()

    # Paso 3: Propagación de constantes
    print("\n=== PROPAGACIÓN DE CONSTANTES ===")
    opt.propagacion_constantes()

    # Paso 4: Detección y eliminación de expresiones comunes
    print("\n=== EXPRESIONES COMUNES ===")
    opt.exp_comunes()

    # Paso 5: Eliminación de código muerto
    #print("\n=== ELIMINACIÓN DE CÓDIGO MUERTO ===")
    opt.eliminar_codigo_muerto()

    print("\n=== OPTIMIZACIÓN FINALIZADA ===")
    print("Archivos generados en ./output/")
