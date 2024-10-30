import os
from Parcial import lexer  # Asegúrate de que la función lexer esté en Parcial.py

class AnalizadorSintactico:
    def __init__(self, entrada_path, salida_path):
        self.entrada_path = entrada_path
        self.salida_path = salida_path
        self.error = None
        self.funciones_definidas = set()  # Conjunto para almacenar funciones definidas

    def leer_archivo(self):
        try:
            with open(self.entrada_path, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except FileNotFoundError:
            self.error = f'Error: El archivo {self.entrada_path} no existe.'
            return None

    def extraer_info_token(self, token):
        partes = token.strip('<>').split(',')
        tipo = partes[0]
        texto = partes[1] if len(partes) > 1 else ''
        linea = partes[2] if len(partes) > 2 else ''
        columna = partes[3] if len(partes) > 3 else ''
        return tipo, texto, linea, columna

    def analizar_sintacticamente(self, tokens):
        try:
            print("Tokens:", tokens)  # Mensaje de depuración
            indent_level = 0
            expected_indent = 0

            for i, token in enumerate(tokens):
                tipo, texto, linea, columna = self.extraer_info_token(token)
                print(f"Analizando token: {token}")  # Mensaje de depuración

                if tipo == 'def':
                    if i + 1 < len(tokens):
                        nombre_funcion = self.extraer_info_token(tokens[i + 1])[1]
                        self.funciones_definidas.add(nombre_funcion)
                    indent_level += 1
                    expected_indent += 1

                elif tipo == 'return':
                    if indent_level < expected_indent:
                        raise SyntaxError(f"Error sintáctico: el 'return' no está correctamente indentado en la línea {linea}.")

                elif tipo == 'if':
                    indent_level += 1

                elif tipo == 'else':
                    if indent_level < expected_indent:
                        raise SyntaxError(f"Error sintáctico: el 'else' no está correctamente indentado en la línea {linea}.")

                elif tipo == 'id':
                    if texto not in self.funciones_definidas and texto == 'is_even':
                        raise SyntaxError(f"Error sintáctico: el identificador '{texto}' no se ha definido antes en la línea {linea}.")

                elif tipo == 'tk_dos_puntos':
                    if i == 0 or self.extraer_info_token(tokens[i - 1])[0] not in ('id', 'if', 'def', 'int'):
                        raise SyntaxError(f"Error sintáctico: se encontró ':' sin un identificador válido antes en la línea {linea}.")
                    # Mensaje de depuración adicional para el token anterior
                    print(f"Token anterior a ':': {tokens[i - 1]}")

                elif tipo == 'tk_coma':
                    if i == 0 or self.extraer_info_token(tokens[i - 1])[0] not in ('id', 'int'):
                        raise SyntaxError(f"Error sintáctico: se encontró ',' sin un identificador válido antes en la línea {linea}.")

                elif tipo == 'tk_par_der':
                    if i == 0 or self.extraer_info_token(tokens[i - 1])[0] not in ('id', 'int'):
                        raise SyntaxError(f"Error sintáctico: se encontró ')' sin un identificador válido antes en la línea {linea}.")

                elif tipo == 'end':
                    indent_level -= 1
                    expected_indent = max(0, indent_level)

            if indent_level > 0:
                raise SyntaxError("Error sintáctico: hay bloques de código sin cerrar.")

        except SyntaxError as e:
            self.error = f'<{linea},{columna}> Error sintáctico: se encontró: "{texto}"; se esperaba: {e.args[0]}.'
            print(self.error)  # Mensaje de depuración si ocurre un error

    def generar_reporte(self):
        with open(self.salida_path, 'w', encoding='utf-8') as salida:
            if self.error:
                salida.write(self.error + '\n')
            else:
                salida.write("**El análisis sintáctico ha finalizado exitosamente.**\n")

def main():
    carpeta_entradas = 'C:/Users/USUARIO/Downloads/LENGUAJES-Pruebas/LENGUAJES-Pruebas/entradas'
    carpeta_salidas = 'C:/Users/USUARIO/Downloads/LENGUAJES-Pruebas/LENGUAJES-Pruebas/salidas'
    os.makedirs(carpeta_salidas, exist_ok=True)
    for archivo in os.listdir(carpeta_entradas):
        if archivo.endswith('.py'):
            entrada = os.path.join(carpeta_entradas, archivo)
            salida = os.path.join(carpeta_salidas, f'salida_{archivo.split(".")[0]}.txt')
            analizador = AnalizadorSintactico(entrada, salida)
            code = analizador.leer_archivo()
            if code:
                tokens = lexer(code)
                print("Tokens generados:", tokens)  # Mensaje de depuración
                analizador.analizar_sintacticamente(tokens)
                analizador.generar_reporte()

if __name__ == '__main__':
    main()
