import re
import os

""" Optimizador de Código Intermedio
Como el desarrollo del optimizador lo vamos a hacer de a poco, vamos a comentar bien
todo para cuando volvamos a leer el codigo acordarnos que hicimos."""
class Optimizador:
    def __init__(self, ruta_entrada="./input_codigo.txt"):
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = "./output/archivoTemporalOptimizador.txt"
        self.bloques = []
        os.makedirs("./output", exist_ok=True)


    def leer_archivo(self):
        try:
            with open(self.ruta_entrada, "r") as archivo:
                lineas = archivo.readlines()
                print("ARCHIVO LEIDO\n")
                for linea in lineas:
                    print(linea.strip())
                return lineas
        except FileNotFoundError:
            print("no se encontro el archivo")
            return []

    def acomodar_entrada(self):
        #Limpia lineas vacías y agrega espacios
        lineas = self.leer_archivo()
        if not lineas:
            return

        operadores = ['>=', '<=', '==', '!=', '+', '-', '*', '/', '=', '%', '>', '<']
        lineas_limpias = [linea.strip() for linea in lineas if linea.strip() != ""]

        patron = '|'.join(map(re.escape, operadores))
        regex = re.compile(rf'\s*({patron})\s*')

        lineas_con_espacios = []
        for linea in lineas_limpias:
            nueva = regex.sub(r' \1 ', linea)
            nueva = ' '.join(nueva.split())  # quita espacios dobles
            lineas_con_espacios.append(nueva + '\n')

        with open(self.ruta_salida, "w") as f:
            f.writelines(lineas_con_espacios)

        print("Archivo limpio generado en:", self.ruta_salida)

    def generar_bloques(self):
        # aca detectamos bloques basicos en el codigo intermedio limpio
        try:
            with open(self.ruta_salida, "r") as f:
                lineas = f.readlines()
        except FileNotFoundError:
            print("ERROR")
            return
        
        bloques = []
        lideres = set()

        # REALIZAMOS ESTO POR REGLAS

        # Regla 1: La primera instrucción es un lider
        if lineas:
            lideres.add(0)

        # Primera pasada: identificar todos los labels y sus posiciones
        label_positions = {}
        for i, linea in enumerate(lineas):
            tokens = linea.split()
            if tokens and tokens[0] == "label" and len(tokens) > 1:
                label_name = tokens[1]
                label_positions[label_name] = i    

        # Regla 2 y 3: label y saltos
        for i, linea in enumerate(lineas):
            tokens = linea.strip().split()
            if not tokens:
                continue
            op = tokens[0]

            if op == "label":
                lideres.add(i)

            if op in ("jump", "ifntjmp"):
                if i + 1 < len(lineas):
                    lideres.add(i + 1)
            
                # Buscamos el destino del salto
                if len(tokens) > 1:
                    target_label = tokens[-1] 
                    if target_label in label_positions:
                        lideres.add(label_positions[target_label])

        lideres = sorted(lideres)

           # CONSTRUIMOS BLOQES
        for idx in range(len(lideres)):
            inicio = lideres[idx]
        
            if idx + 1 < len(lideres):
                fin = lideres[idx + 1] - 1
            else:
                fin = len(lineas) - 1
        
            if inicio <= fin:
                bloques.append([inicio, fin])

        self.bloques = bloques

        print("Bloques Detectados:")
        for idx, (ini, fin) in enumerate(bloques):
            print(f"  Bloque {idx + 1}: líneas {ini}–{fin}")
            for l in lineas[ini:fin + 1]:
                print("    ", l.strip())
            print()
        # DEBUG
        print("Labels encontrados:", label_positions)
        print("Líderes identificados:", lideres)
        return bloques
    


    """    Optimización: Propagación de constantes
    Reemplazamos variables que tienen valores constantes conocidos
    EJEMPlo:
    t1 = 5
    t2 = t1 + 3  --> t2 = 5 + 3
    """
    def propagacion_constantes(self):
        with open(self.ruta_salida, "r") as f:
            lineas = f.readlines() #Lee el codigo limpio generado previamente

        optimizado = lineas.copy() # Lista de strings donde cada string es una linea del codigo intermedio

        for inicio, fin in self.bloques: #Iteramos bloque por bloque
            constantes = {} #Diccionario que almacena las variables que tienen valores constantes
                            #Ej: {"t1": "5", "t2": "10"}

            for i in range(inicio, fin + 1): #Iteramos linea por linea dentro del bloque


                partes = optimizado[i].split() #Separamos la linea en tokens
                # Si tenemos "t2 = t1 + 4" --> partes = ["t2", "=", "t1", "+", "4"]

                if len(partes) >= 3 and partes[1] == "=": #Si hay una asignacion
                    izquierda = partes[0]
                    derecha = partes[2:]

                    # Reemplaza variables por valores del diccionario
                    derecha = [constantes.get(tok, tok) for tok in derecha]

                    
                    expr = " ".join(derecha) # Juntamos la expresion nuevamente a string {"t1" + "4" --> "t1 + 4"}
                    if all(tok.isdigit() or tok in "+-*/%() " for tok in expr): # Evalua si la expresion tiene solo numeros o letras tamb
                        try:
                            valor = str(eval(expr)) #Si la exp es numerica, la evalua en compilacion
                            optimizado[i] = f"{izquierda} = {valor}\n" #Reemplaza la linea por la optimizada
                            constantes[izquierda] = valor #Agrega al diccionario
                        except:
                            pass
                    else:
                        optimizado[i] = f"{izquierda} = {' '.join(derecha)}\n" # Si hay letras no evalua, solo reemplaza
        
        with open("./CodigoIntermedioOptimizado.txt", "w") as f:
            f.writelines(optimizado)


    """ Reutiliza resultados de expresiones ya hechas dentro el mismo bloque
    EJEMPLO:
    t1 = a + b
    t2 = a + b  --> t2 = t1 
            """
    def exp_comunes(self):
        with open(self.ruta_salida, "r") as f:
                lineas = f.readlines()

        optimizado = lineas.copy()

        # Recorremos bloque por bloque
        for inicio, fin in self.bloques:
            expresiones = {}  # diccionario de expresiones vistas en el bloque
                    # Ej: {"a + b": "t1",...}
            expresiones_redef = []

            for i in range(inicio, fin + 1): # recorremos linea por linea dentro del bloque
                partes = optimizado[i].split() #Separamos la linea en tokens
                # Si tenemos "t2 = t1 + 4" --> partes = ["t2", "=", "t1", "+", "4"]

                # Si es una asignacion binaria
                if len(partes) == 5 and partes[1] == "=" and partes[3] in "+-*/":
                    izquierda = partes[0]
                    opizq =  partes[2]
                    op =  partes[3]
                    opder = partes[4]
                    expresion = f"{opizq} {op} {opder}"
                    # Verificamos si la variable izquierda fue redefinida
                    redefinidas = [expr for expr in expresiones if izquierda in expr.split()]
                    # Recorre las expresiones y busca si la variable izquierda aparece en alguna
                    if redefinidas:
                        print(f"[Línea {i}] Variable {izquierda} fue redefinida. Invalidando expresiones: {redefinidas}")
                        for expr in redefinidas:
                            if expr in expresiones:
                                del expresiones[expr]

                    # Si la expresion esta en el diccionario, la reutilizamos
                    if expresion in expresiones:
                        anterior = expresiones[expresion] #Agarramos la variable que ya tenia esa expresion
                        optimizado[i] = f"{izquierda} = {anterior}\n" #Reemplazamos la linea
                        print(f"  [Línea {i}] Reutilizando expresión común: {expresion} → {anterior}")
                    else: #Si no esta, es nueva entonces la guardamos
                        expresiones[expresion] = izquierda
                        print(f"  [Línea {i}] Nueva expresión: {expresion} → {izquierda}")

        # Guardamos resultado optimizado
        with open("./output/CodigoIntermedioOptimizado.txt", "w") as f:
            f.writelines(optimizado)

        print("Optimización de expresiones comunes completada.")

    """ Elimina instrucciones que no afectanal reesultado final del programa
    EJEMPLO:
    t1 = c + d
    No se usa mas t1, por lo tanto no tiene efecto en el resultado, es CODGIO MUERTO  
            """
    
    def eliminar_codigo_muerto(self):
        with open(self.ruta_salida, "r") as f:
            lineas = f.readlines()

        optimizado = lineas.copy()

        for inicio, fin in reversed(self.bloques):  # Recorremos los bloques de abajo hacia arriba
            usadas = set() # Es un conjunto que se construye a medida que recorremos de abajo hacia ariba
            nuevo_bloque = []
        
            # RECORRE BLOQUE DE ABAJO HACIA ARRIBA
            for i in range(final, inicio, -1, -1):
                # por ej si teneemos t2 = t1 + 3

                partes = optimizado[i].split()
                # partes = ["t2", "=", "t1", "+", "3"]
                
                #SI ES UNA ASIGNACION
                if len(partes) >= 3 and partes[1] == "=":
                    izquierda = partes[0]
                    derecha = partes[2:]

                    # VARIABLES QUE SE USAN EN ESTA LINEA 
                    # var_usadas va a tener ["t1"]
                    var_usadas = [ tok for tok in derecha if tok.isidentifier() and not tok.isdigit()]

                    if izquierda not in usadas:
                        #SI NO SE USA LA VARIABLE LA ELIMINAMOS

                        print(f"  [Línea {i}] Eliminada: codigo muerto: {optimizado[i].strip()}")
                        opotimizado[i] = f"// eliminado: {optimizado[i]}"
                    
                    else:
                        #SI SE USA, SE MANTIENE Y ACTUALIZAMOS VARIABLES USADAS

                        usadas.discard(izquierda)  
                        usadas.update(var_usadas)
                        print(f"  [Línea {i}] Mantiene {izquierda}, usa {var_usadas}")

                        

