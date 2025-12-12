import re
import os

class Optimizador:
    # Constructor de la clase
    def __init__(self, ruta_entrada="./input_codigo.txt"):
        self.ruta_entrada = ruta_entrada # La ruta del codigo intermedio sucio (salida del walker)
        self.ruta_salida = "./output/archivoTemporalOptimizador.txt" # Aca se guarda el codigo limpio
        self.ruta_optimizada = "./output/CodigoIntermedioOptimizado.txt" # La salida final optimizada
        self.bloques = [] # Lista donde guardamos los bloques basicos detectados
        self.lineas_actuales = [] # Aca se carga el codigo en memoria para procesar
        os.makedirs("./output", exist_ok=True) # Crea la carpeta 'output' si no existe

    def leer_archivo(self):
        # lee el archivo de entrada y lo muestra en consola
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
        # Esta funcion limpia el codigo intermedio (quita espacios dobles, lineas vacias)
        lineas = self.leer_archivo()
        if not lineas: return

        operadores = ['>=', '<=', '==', '!=', '+', '-', '*', '/', '=', '%', '>', '<']
        lineas_limpias = [linea.strip() for linea in lineas if linea.strip() != ""] # Quita lineas vacias

        # Define el patron regex para separar operadores con espacios
        patron = '|'.join(map(re.escape, operadores))
        regex = re.compile(rf'\s*({patron})\s*')

        lineas_con_espacios = []
        for linea in lineas_limpias:
            nueva = regex.sub(r' \1 ', linea) # Agrega espacios alrededor de operadores
            nueva = ' '.join(nueva.split()) # Quita espacios dobles
            lineas_con_espacios.append(nueva + '\n')

        self.lineas_actuales = lineas_con_espacios # Guarda el codigo limpio en memoria
        
        with open(self.ruta_salida, "w") as f:
            f.writelines(lineas_con_espacios) # Guarda el archivo limpio en disco
        print("Archivo limpio generado en:", self.ruta_salida)

    def generar_bloques(self):
        # Detecta los bloques basicos (trozos de codigo sin saltos en el medio)
        if not self.lineas_actuales:
            # Manejo de error si no se cargo el codigo
            try:
                with open(self.ruta_salida, "r") as f:
                    self.lineas_actuales = f.readlines()
            except FileNotFoundError:
                print("ERROR: No hay codigo cargado")
                return

        lineas = self.lineas_actuales 
        n = len(lineas)
        self.funciones = {}           
        self.bloques_por_funcion = {} 
        bloques_flat = []

        func_heads = []    
        labels_pos = {}    

        # Primero, detectamos todas las funciones y etiquetas (labels)
        for idx, linea in enumerate(lineas):
            tok = linea.strip().split()
            if not tok: continue

            if tok[0].endswith(':') and not tok[0].startswith('L'):
                func_name = tok[0][:-1]
                func_heads.append((func_name, idx)) # funcion nueva es un lider
            elif tok[0].startswith('L') and tok[0].endswith(':'):
                labels_pos[tok[0][:-1]] = idx # La etiqueta es un lider

        if not func_heads:
            func_heads = [("main", 0)]

        # Delimitamos el inicio y fin de cada funcion
        for i, (func_name, func_start) in enumerate(func_heads):
            func_end = (func_heads[i+1][1] - 1) if (i+1 < len(func_heads)) else (n - 1)
            # Buscamos 'retornar' como el fin de la funcion
            for j in range(func_start, func_end + 1):
                tok = lineas[j].strip().split()
                if tok and tok[0] == "retornar":
                    func_end = j
                    break
            self.funciones[func_name] = (func_start, func_end)

        # Ahora, en cada funcion, encontramos los lideres y definimos los bloques
        for fname, (iniF, finF) in self.funciones.items():
            lideres = set()
            first_lider = iniF + 1
            if first_lider <= finF: lideres.add(first_lider) # La primera instruccion despues del nombre de la funcion es lider

            for L, pos in labels_pos.items():
                if iniF <= pos <= finF: lideres.add(pos) # Las etiquetas dentro de la funcion son lideres

            for i in range(iniF, finF + 1):
                tok = lineas[i].strip().split()
                if not tok: continue
                
                # Despues de un salto (siFalso o ir a), la siguiente linea es un lider
                if tok[0] == "siFalso":
                    if i + 1 <= finF: lideres.add(i + 1)
                    dest = tok[-1]
                    if dest in labels_pos: lideres.add(labels_pos[dest]) # El destino del salto es un lider
                elif tok[0] == "ir" and len(tok) >= 3 and tok[1] == "a":
                    if i + 1 <= finF: lideres.add(i + 1)
                    dest = tok[-1]
                    if dest in labels_pos: lideres.add(labels_pos[dest]) # El destino del salto es un lider

            # Ordenamos los lideres y creamos las tuplas [inicio, fin] de cada bloque
            lideres = sorted(lideres)
            bloques_fun = []
            for k in range(len(lideres)):
                b_ini = lideres[k]
                b_fin = (lideres[k+1] - 1) if (k+1 < len(lideres)) else finF
                if b_ini <= b_fin:
                    bloques_fun.append([b_ini, b_fin])
                    bloques_flat.append([b_ini, b_fin])

            self.bloques_por_funcion[fname] = bloques_fun
                
        self.bloques = bloques_flat # Lista final de todos los bloques en el codigo

        print("\n=== DETECCION DE FUNCIONES Y BLOQUES ===")
        print("Funciones detectadas y rangos (lineas):")
        for fn, (a, b) in self.funciones.items():
            print(f"  - {fn}: {a}..{b}")
        return self.bloques

    def propagacion_constantes(self):
        # Fase 1: Resuelve las cuentas matematicas que solo tienen numeros
        optimizado = self.lineas_actuales.copy()
        for inicio, fin in self.bloques: 
            constantes = {} # Diccionario para guardar variables con valores conocidos (t1: "5")
            for i in range(inicio, fin + 1): 
                partes = optimizado[i].split() 
                if len(partes) >= 3 and partes[1] == "=": 
                    izquierda = partes[0]
                    derecha = partes[2:]
                    
                    # 1. Reemplazamos variables conocidas por sus valores constantes (propagacion)
                    derecha_nueva = [str(constantes.get(tok, tok)) for tok in derecha]
                    expr = " ".join(derecha_nueva) 
                    valor_calculado = None
                    
                    # 2. Comprobamos si la expresion es solo numeros y operadores (seguridad para eval)
                    caracteres_permitidos = set("0123456789.+-*/%() =<>! ")
                    es_solo_constante = all(c in caracteres_permitidos for c in set(expr))

                    if es_solo_constante:
                        try:
                            # Intentamos calcular el valor (constant folding)
                            expr_limpia = expr.replace("true", "1").replace("false", "0")
                            valor_calculado = str(eval(expr_limpia)) 
                            
                        except Exception:
                            valor_calculado = None # Fallo la evaluacion (ej. division por cero)
                    
                    # 3. Aplicamos el resultado
                    if valor_calculado is not None:
                        optimizado[i] = f"{izquierda} = {valor_calculado}\n" # Reemplazamos t1 = 5 + 2 por t1 = 7
                        constantes[izquierda] = valor_calculado # Guardamos el nuevo valor en el diccionario
                    else:
                        optimizado[i] = f"{izquierda} = {expr}\n" # Si no pudimos calcular, dejamos la expresion
                        if izquierda in constantes:
                            del constantes[izquierda] # Si redefinimos la variable (x=y), ya no es constante
        
        self.lineas_actuales = optimizado
        with open(self.ruta_optimizada, "w") as f:
            f.writelines(optimizado)
            
    def exp_comunes(self):
        # Fase 2: Reutiliza resultados de expresiones ya calculadas (ej: t2 = t1)
        print(">>> Ejecutando Expresiones Comunes (Conmutativo)...")
        optimizado = self.lineas_actuales.copy()
        for inicio, fin in self.bloques:
            expresiones = {}  # Diccionario: {"a + b": "t1"}
            for i in range(inicio, fin + 1):
                partes = optimizado[i].split()
                
                # 1. Invalidacion: Si asignamos a una variable, borramos las expresiones que dependian de ella
                if len(partes) >= 3 and partes[1] == "=":
                    izquierda = partes[0] 
                    claves_a_borrar = [k for k in expresiones if izquierda in k.split()]
                    for k in claves_a_borrar: del expresiones[k]
                    claves_por_valor = [k for k, v in expresiones.items() if v == izquierda]
                    for k in claves_por_valor: del expresiones[k]

                # 2. Busqueda: Si la linea es una operacion binaria (ej: t1 = a + b)
                if len(partes) == 5 and partes[1] == "=" and partes[3] in "+-*/%":
                    izquierda = partes[0]
                    op1 = partes[2]
                    op = partes[3]
                    op2 = partes[4]
                    
                    expr_original = f"{op1} {op} {op2}"
                    expr_conmutativa = f"{op2} {op} {op1}" # Para el caso de x * y y luego y * x
                    
                    encontrada = None
                    if expr_original in expresiones:
                        encontrada = expresiones[expr_original]
                    elif op in "+*" and expr_conmutativa in expresiones: # Solo + y * son conmutativos
                        encontrada = expresiones[expr_conmutativa]
                        print(f"Conmutatividad detectada: {expr_original} es igual a {expr_conmutativa}")

                    if encontrada:
                        optimizado[i] = f"{izquierda} = {encontrada}\n" # Optimizamos: t2 = t1
                        expresiones[expr_original] = izquierda
                    else:
                        expresiones[expr_original] = izquierda # Guardamos la nueva expresion

        self.lineas_actuales = optimizado
        with open(self.ruta_optimizada, "w") as f:
            f.writelines(optimizado)

    
    def eliminar_codigo_muerto(self):
        # Fase 3: Elimina los calculos cuyos resultados nunca se usan (analisis hacia atras)
        print("Ejecutando Eliminacion de Codigo Muerto (Backwards)...")
        src = self.lineas_actuales.copy()
        optimizado = src.copy()

        keywords = ["ir", "a", "goto", "if", "siFalso", "call", "retornar", "label", "+", "-", "*", "/", "=", "==", "<", ">", "<=", ">="]

        for bloquen in self.bloques:
            inicio, fin = bloquen
            variables_vivas = set() # Conjunto de variables que se usaran en el futuro

            for i in range(fin, inicio - 1, -1): # Recorremos del final al principio
                linea = optimizado[i].strip()
                if not linea or linea.startswith("//") or linea.endswith(":"):
                    continue

                partes = linea.split()

                # Seguridad para llamadas a funcion (protegemos vf0, vf1...)
                if "call" in partes:
                    for k in range(10): 
                        variables_vivas.add(f"vf{k}")

                # Si es una asignacion (t1 = ...)
                if len(partes) >= 3 and partes[1] == "=":
                    izquierda = partes[0]
                    derecha = partes[2:]

                    es_temporal = izquierda.startswith("t") or izquierda.startswith("vf") or izquierda.startswith("aux")

                    # Si es temporal Y nadie la necesita (no esta en variables_vivas) -> ELIMINAMOS
                    if es_temporal and izquierda not in variables_vivas:
                        optimizado[i] = f"// eliminado: {linea}\n"
                    else:
                        # Si la variable 'izquierda' esta viva: la definimos aqui, ya no es viva hacia arriba
                        if izquierda in variables_vivas:
                            variables_vivas.remove(izquierda)
                        
                        # Las variables de la 'derecha' pasan a ser vivas
                        for tok in derecha:
                            if tok.isidentifier() and tok not in keywords and not tok[0].isdigit():
                                variables_vivas.add(tok)
                # Si es una instruccion de control (retornar, siFalso, etc)
                else:
                    # Todas las variables que aparecen son vivas
                    for tok in partes:
                        if tok.isidentifier() and tok not in keywords:
                            try:
                                float(tok) 
                            except ValueError:
                                variables_vivas.add(tok)

            self.lineas_actuales = optimizado
            with open(self.ruta_optimizada, "w") as destino:
                for linea in optimizado:
                    if linea.strip() == "": continue 
                    destino.write(linea)
            #print("Eliminacion de codigo muerto completada.")