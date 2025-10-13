import re

class Optimizador:
    def __init__(self):
        print("=== OPTIMIZADOR DE CÓDIGO ACTIVADO ===")
        self.ruta_entrada = "./output/codigoIntermedioPrueba.txt"
        self.ruta_salida = "./output/archivoTemporalOptimizador.txt"

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
