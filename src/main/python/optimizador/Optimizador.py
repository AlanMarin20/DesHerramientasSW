import re
import os

""" Optimizador de Código Intermedio
Como el desarrollo del optimizador lo vamos a hacer de a poco, vamos a comentar bien
todo para cuando volvamos a leer el codigo acordarnos que hicimos."""
class Optimizador:
    def __init__(self, ruta_entrada="./input_codigo.txt"):
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = "./output/archivoTemporalOptimizador.txt"
        self.ruta_optimizada = "./output/CodigoIntermedioOptimizado.txt" # Unifiqué la salida aquí
        self.bloques = []
        self.lineas_actuales = [] # <--- NUEVO: Aquí guardamos el código en memoria para pasarlo entre funciones
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

        # CAMBIO: Guardamos en disco Y en memoria para que siga el flujo
        self.lineas_actuales = lineas_con_espacios 
        
        with open(self.ruta_salida, "w") as f:
            f.writelines(lineas_con_espacios)

        print("Archivo limpio generado en:", self.ruta_salida)

    def generar_bloques(self):
        # aca detectamos bloques basicos en el codigo intermedio limpio
        
        # CAMBIO: Usamos lo que está en memoria en vez de leer archivo
        if not self.lineas_actuales:
            # Por si acaso alguien llama a generar_bloques sin llamar a acomodar antes
            try:
                with open(self.ruta_salida, "r") as f:
                    self.lineas_actuales = f.readlines()
            except FileNotFoundError:
                print("ERROR: No hay código cargado")
                return

        lineas = self.lineas_actuales 
        
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
        # (Dejé tus prints tal cual)
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
        # CAMBIO: Usamos self.lineas_actuales en vez de leer archivo
        optimizado = self.lineas_actuales.copy()

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
                    derecha_nueva = [str(constantes.get(tok, tok)) for tok in derecha]


                    expr = " ".join(derecha_nueva) # Juntamos la expresion nuevamente a string {"t1" + "4" --> "t1 + 4"}
                    
                    valor_calculado = None

                    # Valudamos caracteres permitidos 
                    #Validamos caracteres permitidos para evaluar
                    caracteres_permitidos = set("0123456789.+-*/%() =<>!")
                    es_seguro = set(expr).issubset(caracteres_permitidos)

                    if es_seguro:
                        try:
                            # eval resuelve la cuenta matemática
                            valor_calculado = str(eval(expr)) 
                        except:
                            # Puede fallar por división por cero, sintaxis, etc.
                            valor_calculado = None
                    
                    if valor_calculado is not None:
                        # Se pudo reducir una constante
                        optimizado[i] = f"{izquierda} = {valor_calculado}\n"
                        constantes[izquierda] = valor_calculado
                    
                    else:
                        # No se pudo reducir
                        optimizado[i] = f"{izquierda} = {expr}\n"

                        #Si la variable izquierda se redefinio, debemos sacar el valor antiguo

                        if izquierda in constantes:
                            del constantes[izquierda]
                        
                    
        # Guardamos cambios
        self.lineas_actuales = optimizado       
                    
                    
                    
                    
                    
                    
                    
                    #if all(tok.isdigit() or tok in "+-*/%() " for tok in expr): # Evalua si la expresion tiene solo numeros o letras tamb
                     #   try:
                      #      valor = str(eval(expr)) #Si la exp es numerica, la evalua en compilacion
                       #     optimizado[i] = f"{izquierda} = {valor}\n" #Reemplaza la linea por la optimizada
                        #    constantes[izquierda] = valor #Agrega al diccionario
                        #except:
                        #    pass
                    #else:
                     #   optimizado[i] = f"{izquierda} = {' '.join(derecha)}\n" # Si hay letras no evalua, solo reemplaza
        
        # CAMBIO: Actualizamos la memoria Y escribimos el archivo
        #self.lineas_actuales = optimizado
        
        with open(self.ruta_optimizada, "w") as f:
            f.writelines(optimizado)


    """ Reutiliza resultados de expresiones ya hechas dentro el mismo bloque
    EJEMPLO:
    t1 = a + b
    t2 = a + b  --> t2 = t1 
            """
    def exp_comunes(self):
            print(">>> Ejecutando Expresiones Comunes (Conmutativo)...")
            optimizado = self.lineas_actuales.copy()

            for inicio, fin in self.bloques:
                expresiones = {}  # Diccionario: {"a + b": "t1"}
                
                for i in range(inicio, fin + 1):
                    partes = optimizado[i].split()
                    
                    # Antes de procesar, borramos del diccionario lo que se rompe en esta linea
                    if len(partes) >= 3 and partes[1] == "=":
                        izquierda = partes[0] 
                        
                        #Si cambio una variable usada en una ya existente (Ej a = 99 rompe "a + b")
                        claves_a_borrar = [k for k in expresiones if izquierda in k.split()]
                        for k in claves_a_borrar:
                            del expresiones[k]
                            
                        #Si piso la variable que guardaba el resultado (Ej t1 = 0 rompe {"a+b": "t1"})
                        claves_por_valor = [k for k, v in expresiones.items() if v == izquierda]
                        for k in claves_por_valor:
                            del expresiones[k]

                    if len(partes) == 5 and partes[1] == "=" and partes[3] in "+-*/%":
                        izquierda = partes[0]
                        op1 = partes[2]
                        op = partes[3]
                        op2 = partes[4]
                        
                        expr_original = f"{op1} {op} {op2}"
                        expr_conmutativa = f"{op2} {op} {op1}" # El push anterior no tenia en cuenta esto
                        
                        encontrada = None
                        
                        #Buscamos coincidencia exacta
                        if expr_original in expresiones:
                            encontrada = expresiones[expr_original]
                            
                        #Buscamos coincidencia conmutativa (Solo para + y *)
                        elif op in "+*" and expr_conmutativa in expresiones:
                            encontrada = expresiones[expr_conmutativa]
                            print(f"  [Smart] Conmutatividad detectada: {expr_original} es igual a {expr_conmutativa}")

                        if encontrada:
                            #optimizamos
                            optimizado[i] = f"{izquierda} = {encontrada}\n"
                            # Actualizamos el diccionario
                            expresiones[expr_original] = izquierda
                        else:
                            # guardamos la nueva expresion
                            expresiones[expr_original] = izquierda

            # Guardamos cambios
            self.lineas_actuales = optimizado
            
            with open(self.ruta_optimizada, "w") as f:
                f.writelines(optimizado)

    #La logica es recorrer hacia atras porque asi sabemos que variables
    # van a ser usadas en el futuro y cuales no
    def eliminar_codigo_muerto(self):
            print("CODIGO MUERTO")
            src = self.lineas_actuales.copy()
            optimizado = src.copy()

            # Palabras clave que NO son variables (para evitar agregarlas a variables_vivas)
            keywords = ["ir", "a", "goto", "if", "siFalso", "call", "retornar", "label", "+", "-", "*", "/", "=", "==", "<", ">", "<=", ">="]

            for bloquen in self.bloques:
                inicio, fin = bloquen
                
                # Variables que necesitaremos en el futuro
                # Al final del bloque, asumimos que las temporales (t...) mueren, 
                # pero las de usuario (a, b, x...) pueden estar vivas en otro bloque.
                # Por seguridad, empezamos vacío y protegemos las NO temporales al momento de borrar.
                variables_vivas = set()

                # RECORREMOS DE ATRAS PARA ADELANTE 
                for i in range(fin, inicio - 1, -1):
                    linea = optimizado[i].strip()
                    
                    # Ignorar comentarios o lineas vacías
                    if not linea or linea.startswith("//") or linea.endswith(":"):
                        continue

                    partes = linea.split()

                    # primer caso: asignaciones
                    if len(partes) >= 3 and partes[1] == "=":
                        izquierda = partes[0]
                        derecha = partes[2:]

                        # CRITERIO
                        # 1. La variable izquierda NO esta en 'variables_vivas' (nadie la necesita abajo)
                        # 2. Es una variable temporal 
                        es_temporal = izquierda.startswith("t") or izquierda.startswith("vf") or izquierda.startswith("aux")

                        if es_temporal and izquierda not in variables_vivas:
                            # La borramos 
                            optimizado[i] = f"// eliminado: {linea}\n"
                        else:
                            # no borramos
                            # 1. Como se define aca, 'izquierda' ya no se necesita hacia arriba.
                            if izquierda in variables_vivas:
                                variables_vivas.remove(izquierda)
                            
                            # 2. Las variables de la derecha las necesitamos, son vivqs
                            for tok in derecha:
                                if tok.isidentifier() and tok not in keywords and not tok[0].isdigit():
                                    variables_vivas.add(tok)

                    # segundo caso: instrucciones de control
                    # Ej siFalso t1 ir a L1  o  retornar x  o  push t1
                    else:
                        # Cualq variable que aparezca aca es viva
                        for tok in partes:
                            if tok.isidentifier() and tok not in keywords:
                                # Chequeo extra que dio error antes, porque a veces venian numeros
                                try:
                                    float(tok) # Si es numero, lo ignoramos
                                except ValueError:
                                    variables_vivas.add(tok)

            # Guardamos resultado
            self.lineas_actuales = optimizado
            
            with open(self.ruta_optimizada, "w") as destino:
                for linea in optimizado:
                    if linea.strip() == "": continue 
                    destino.write(linea)
            
            print("Eliminacion de código muerto completada.")