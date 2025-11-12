from Optimizador import Optimizador

if __name__ == "__main__":
    opt = Optimizador("./input_codigo.txt")
    opt.acomodar_entrada()
    opt.generar_bloques()
    #opt.propagacion_constantes()
    #opt.exp_comunes()
    opt.eliminar_codigo_muerto()