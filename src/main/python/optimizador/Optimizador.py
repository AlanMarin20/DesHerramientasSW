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
        
        
        n = len(lineas)
        self.funciones = {}           # nombre -> (ini, fin)
        self.bloques_por_funcion = {} # nombre -> lista de [ini, fin]
        bloques_flat = []

        #DEFINIMOS CABECERAS DE FUNCIONES Y LABELS
        func_heads = []     # ("main", 0)
        labels_pos = {}     # 'L1' -> 0

        # RECORRE TODAS LAS LINEAS BUSCANDO FUNCIONES Y LABELS
        for idx, linea in enumerate(lineas):
            tok = linea.strip().split()
            if not tok:
                continue

            #Cabecera que termina con : y NO empieza con L es una funcion
            if tok[0].endswith(':') and not tok[0].startswith('L'):
                func_name = tok[0][:-1]
                func_heads.append((func_name, idx))

            #Label de control
            elif tok[0].startswith('L') and tok[0].endswith(':'):
                labels_pos[tok[0][:-1]] = idx

        # Si no hay funciones, asumimos que es todo un main ponele
        if not func_heads:
            func_heads = [("main", 0)]


        # HASTA AHORA DEFINIMOS FUNCIONES Y LABELS, AHORA DELIMITAMOS INICIO Y FIN DE CADA FUNCION

        for i, (func_name, func_start) in enumerate(func_heads):
            #Usamos como criterio, el incio es la cabecera y el fin es retornar o nombre de ota funcion
            # El fin es una linea antes del inicio de la sig funcion, en caso de ser la ultima, la ultima linea es el final.
            func_end = (func_heads[i+1][1] - 1) if (i+1 < len(func_heads)) else (n - 1)

            # buscamos retornar dentro de la funcion,
            for j in range(func_start, func_end + 1):
                tok = lineas[j].strip().split()
                if tok and tok[0] == "retornar":
                    func_end = j
                    break

            self.funciones[func_name] = (func_start, func_end)

        # PARA CADA FUNCION, CONSTRUIMOS BLOQUES BASICOS
        for fname, (iniF, finF) in self.funciones.items():
            lideres = set()

            # La PRIMERA instrucción dentro del cuerpo es lider
            first_lider = iniF + 1
            if first_lider <= finF:
                lideres.add(first_lider)

            # Cualquier label dentro de la funcion es lider
            for L, pos in labels_pos.items():
                if iniF <= pos <= finF:
                    lideres.add(pos)

            # Despues de cada salto, la siguiente instruccion es lider
            for i in range(iniF, finF + 1):
                tok = lineas[i].strip().split()
                if not tok:
                    continue

                # Usamos nomenclatura siFalso
                if tok[0] == "siFalso":
                    if i + 1 <= finF:
                        lideres.add(i + 1)
                    dest = tok[-1]
                    if dest in labels_pos:
                        lideres.add(labels_pos[dest])

                #Usamos nomenclatura ir
                elif tok[0] == "ir" and len(tok) >= 3 and tok[1] == "a":
                    if i + 1 <= finF:
                        lideres.add(i + 1)
                    dest = tok[-1]
                    if dest in labels_pos:
                        lideres.add(labels_pos[dest])

            # ORDENAMOS LOS LIDERES Y CREAMOS BLOQUES 
            lideres = sorted(lideres)
            bloques_fun = []
            for k in range(len(lideres)):
                b_ini = lideres[k]
                b_fin = (lideres[k+1] - 1) if (k+1 < len(lideres)) else finF
                if b_ini <= b_fin:
                    bloques_fun.append([b_ini, b_fin])
                    bloques_flat.append([b_ini, b_fin])

            self.bloques_por_funcion[fname] = bloques_fun

                
        self.bloques = bloques_flat

        #DEBUGEAMOS
        print("\n=== DETECCIÓN DE FUNCIONES Y BLOQUES ===")
        print("Funciones detectadas y rangos (lineas):")
        for fn, (a, b) in self.funciones.items():
            print(f"  - {fn}: {a}..{b}")

        print("\nLabels encontrados:")
        for L, pos in labels_pos.items():
            print(f"  - {L}: {pos}")

        print("\nBloques por funciOn:")
        for fn, bls in self.bloques_por_funcion.items():
            print(f"  {fn}:")
            for (a, b) in bls:
                frag = " | ".join(s.strip() for s in lineas[a:b+1])
                print(f"    [{a}-{b}]  {frag}")

        return self.bloques


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
        # Leer el archivo de entrada
        with open(self.ruta_salida, "r") as f:
            src = f.readlines()
        
        # Crear archivo de destino
        with open("./output/CodigoIntermedioOptimizado.txt", "w") as destino:
            definidas = set()
            usadas = set()
            optimizado = src.copy()

            for bloquen in self.bloques:
                inicio, fin = bloquen
                i = inicio

                while i <= fin:
                    linea = optimizado[i].split()
                    if len(linea) >= 3 and linea[1] == '=':
                        definidas.add(linea[0]) #miro el lado izquierdo y agrego a definidas
                        #ahora miramos el lado derecho para ver que variables estan siendo usadas
                        usadas.update([linea[j] for j in range(2, len(linea)) if linea[j].isidentifier()])
                    i += 1
                
                #vemos variables que no se esten usando
                innecesarias = definidas - usadas
                i = inicio
                while i <= fin:
                    partes = optimizado[i].split()
                    if len(partes) >= 3 and partes[1] == '=' and partes[0] in innecesarias:
                        # En lugar de eliminar, comentar la línea
                        print(f"  [Línea {i}] Eliminada: código muerto: {optimizado[i].strip()}")
                        optimizado[i] = f"// eliminado: {optimizado[i]}"
                    i += 1

            destino.seek(0)
            destino.truncate() #para escribir el archivo de cero
            for linea in optimizado:
                if linea == "":
                    continue  # saltar línea vacía
                if not linea.endswith('\n'):
                    linea += '\n'
                destino.write(linea)
        
        print("Eliminación de código muerto completada.")