import re
import os

class Optimizador:
    def __init__(self, ruta_entrada="./input_codigo.txt"):
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = "./output/archivoTemporalOptimizador.txt"
        self.ruta_optimizada = "./output/CodigoIntermedioOptimizado.txt" 
        self.bloques = []
        self.lineas_actuales = [] 
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
        lineas = self.leer_archivo()
        if not lineas: return

        operadores = ['>=', '<=', '==', '!=', '+', '-', '*', '/', '=', '%', '>', '<']
        lineas_limpias = [linea.strip() for linea in lineas if linea.strip() != ""]

        patron = '|'.join(map(re.escape, operadores))
        regex = re.compile(rf'\s*({patron})\s*')

        lineas_con_espacios = []
        for linea in lineas_limpias:
            nueva = regex.sub(r' \1 ', linea)
            nueva = ' '.join(nueva.split()) 
            lineas_con_espacios.append(nueva + '\n')

        self.lineas_actuales = lineas_con_espacios 
        
        with open(self.ruta_salida, "w") as f:
            f.writelines(lineas_con_espacios)
        print("Archivo limpio generado en:", self.ruta_salida)

    def generar_bloques(self):
        if not self.lineas_actuales:
            try:
                with open(self.ruta_salida, "r") as f:
                    self.lineas_actuales = f.readlines()
            except FileNotFoundError:
                print("ERROR: No hay código cargado")
                return

        lineas = self.lineas_actuales 
        n = len(lineas)
        self.funciones = {}           
        self.bloques_por_funcion = {} 
        bloques_flat = []

        func_heads = []    
        labels_pos = {}    

        for idx, linea in enumerate(lineas):
            tok = linea.strip().split()
            if not tok: continue

            if tok[0].endswith(':') and not tok[0].startswith('L'):
                func_name = tok[0][:-1]
                func_heads.append((func_name, idx))

            elif tok[0].startswith('L') and tok[0].endswith(':'):
                labels_pos[tok[0][:-1]] = idx

        if not func_heads:
            func_heads = [("main", 0)]

        for i, (func_name, func_start) in enumerate(func_heads):
            func_end = (func_heads[i+1][1] - 1) if (i+1 < len(func_heads)) else (n - 1)
            for j in range(func_start, func_end + 1):
                tok = lineas[j].strip().split()
                if tok and tok[0] == "retornar":
                    func_end = j
                    break
            self.funciones[func_name] = (func_start, func_end)

        for fname, (iniF, finF) in self.funciones.items():
            lideres = set()
            first_lider = iniF + 1
            if first_lider <= finF: lideres.add(first_lider)

            for L, pos in labels_pos.items():
                if iniF <= pos <= finF: lideres.add(pos)

            for i in range(iniF, finF + 1):
                tok = lineas[i].strip().split()
                if not tok: continue
                if tok[0] == "siFalso":
                    if i + 1 <= finF: lideres.add(i + 1)
                    dest = tok[-1]
                    if dest in labels_pos: lideres.add(labels_pos[dest])
                elif tok[0] == "ir" and len(tok) >= 3 and tok[1] == "a":
                    if i + 1 <= finF: lideres.add(i + 1)
                    dest = tok[-1]
                    if dest in labels_pos: lideres.add(labels_pos[dest])

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

        print("\n=== DETECCIÓN DE FUNCIONES Y BLOQUES ===")
        print("Funciones detectadas y rangos (lineas):")
        for fn, (a, b) in self.funciones.items():
            print(f"  - {fn}: {a}..{b}")
        return self.bloques

    def propagacion_constantes(self):
        optimizado = self.lineas_actuales.copy()
        for inicio, fin in self.bloques: 
            constantes = {} 
            for i in range(inicio, fin + 1): 
                partes = optimizado[i].split() 
                if len(partes) >= 3 and partes[1] == "=": 
                    izquierda = partes[0]
                    derecha = partes[2:]
                    derecha_nueva = [str(constantes.get(tok, tok)) for tok in derecha]
                    expr = " ".join(derecha_nueva) 
                    valor_calculado = None
                    caracteres_permitidos = set("0123456789.+-*/%() =<>!")
                    es_seguro = set(expr).issubset(caracteres_permitidos)

                    if es_seguro:
                        try:
                            valor_calculado = str(eval(expr)) 
                        except:
                            valor_calculado = None
                    
                    if valor_calculado is not None:
                        optimizado[i] = f"{izquierda} = {valor_calculado}\n"
                        constantes[izquierda] = valor_calculado
                    else:
                        optimizado[i] = f"{izquierda} = {expr}\n"
                        if izquierda in constantes:
                            del constantes[izquierda]
        
        with open(self.ruta_optimizada, "w") as f:
            f.writelines(optimizado)

    def exp_comunes(self):
            print(">>> Ejecutando Expresiones Comunes (Conmutativo)...")
            optimizado = self.lineas_actuales.copy()
            for inicio, fin in self.bloques:
                expresiones = {}  
                for i in range(inicio, fin + 1):
                    partes = optimizado[i].split()
                    if len(partes) >= 3 and partes[1] == "=":
                        izquierda = partes[0] 
                        claves_a_borrar = [k for k in expresiones if izquierda in k.split()]
                        for k in claves_a_borrar: del expresiones[k]
                        claves_por_valor = [k for k, v in expresiones.items() if v == izquierda]
                        for k in claves_por_valor: del expresiones[k]

                    if len(partes) == 5 and partes[1] == "=" and partes[3] in "+-*/%":
                        izquierda = partes[0]
                        op1 = partes[2]
                        op = partes[3]
                        op2 = partes[4]
                        
                        expr_original = f"{op1} {op} {op2}"
                        expr_conmutativa = f"{op2} {op} {op1}" 
                        
                        encontrada = None
                        if expr_original in expresiones:
                            encontrada = expresiones[expr_original]
                        elif op in "+*" and expr_conmutativa in expresiones:
                            encontrada = expresiones[expr_conmutativa]
                            print(f"  [Smart] Conmutatividad detectada: {expr_original} es igual a {expr_conmutativa}")

                        if encontrada:
                            optimizado[i] = f"{izquierda} = {encontrada}\n"
                            expresiones[expr_original] = izquierda
                        else:
                            expresiones[expr_original] = izquierda

            self.lineas_actuales = optimizado
            with open(self.ruta_optimizada, "w") as f:
                f.writelines(optimizado)

    # ---> AQUÍ ESTABA EL ERROR: AHORA ESTÁ INDENTADO DENTRO DE LA CLASE <---
    def eliminar_codigo_muerto(self):
            print(">>> Ejecutando Eliminación de Código Muerto (Backwards)...")
            src = self.lineas_actuales.copy()
            optimizado = src.copy()

            keywords = ["ir", "a", "goto", "if", "siFalso", "call", "retornar", "label", "+", "-", "*", "/", "=", "==", "<", ">", "<=", ">="]

            for bloquen in self.bloques:
                inicio, fin = bloquen
                variables_vivas = set()

                for i in range(fin, inicio - 1, -1):
                    linea = optimizado[i].strip()
                    if not linea or linea.startswith("//") or linea.endswith(":"):
                        continue

                    partes = linea.split()

                    if "call" in partes:
                        for k in range(10): 
                            variables_vivas.add(f"vf{k}")

                    if len(partes) >= 3 and partes[1] == "=":
                        izquierda = partes[0]
                        derecha = partes[2:]

                        es_temporal = izquierda.startswith("t") or izquierda.startswith("vf") or izquierda.startswith("aux")

                        if es_temporal and izquierda not in variables_vivas:
                            optimizado[i] = f"// eliminado: {linea}\n"
                        else:
                            if izquierda in variables_vivas:
                                variables_vivas.remove(izquierda)
                            for tok in derecha:
                                if tok.isidentifier() and tok not in keywords and not tok[0].isdigit():
                                    variables_vivas.add(tok)
                    else:
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
            print("Eliminacion de código muerto completada.")