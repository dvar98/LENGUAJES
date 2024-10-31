# main.py
import ctypes
from lexer import Lexer
from parser import Parser

# Cargar la biblioteca compartida
try:
    lib = ctypes.CDLL('./libparser.so')  # Cambia a 'parser.dll' en Windows si es necesario
except OSError:
    raise Exception("No se pudo cargar la biblioteca compartida. Asegúrate de compilar 'grammar.c'.")

# Definir la estructura de C para `Parser`
class CParser(ctypes.Structure):
    _fields_ = [
        ("start_rule", ctypes.c_int),
        ("input_code", ctypes.c_char_p),
        ("keywords", ctypes.POINTER(ctypes.c_char_p)),
        ("n_keyword_lists", ctypes.c_int),
        ("soft_keywords", ctypes.POINTER(ctypes.c_char_p))
    ]

# Configuración de argumentos y tipo de retorno para _PyPegen_parse
lib._PyPegen_parse.argtypes = [ctypes.POINTER(CParser)]
lib._PyPegen_parse.restype = ctypes.c_void_p

# Enum para las reglas de inicio en `grammar.c`
RULES = {
    "file_input": 0,
    "single_input": 1,
    "eval_input": 2,
    "func_type_input": 3
}

def initialize_cparser(input_code, rule="file_input"):
    """Inicializa y retorna una estructura `CParser` en C."""
    parser = CParser()
    parser.start_rule = RULES[rule]
    parser.input_code = input_code.encode('utf-8')

    # Palabras clave en C
    keywords = [
        "False", "None", "True", "and", "as", "assert", "async", "await", "break",
        "class", "continue", "def", "del", "elif", "else", "except", "finally",
        "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
        "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"
    ]
    soft_keywords = ["match", "case"]

    # Convertir palabras clave a ctypes
    c_keywords = (ctypes.c_char_p * len(keywords))(*[k.encode('utf-8') for k in keywords])
    c_soft_keywords = (ctypes.c_char_p * len(soft_keywords))(*[k.encode('utf-8') for k in soft_keywords])

    parser.keywords = c_keywords
    parser.n_keyword_lists = len(keywords)
    parser.soft_keywords = c_soft_keywords

    return parser

def parse_code(filename):
    """
    Main function to analyze source code from a file.

    Args:
        filename (str): The path to the source code file to be analyzed.

    This function performs the following steps:
    1. Lexical Analysis: Reads the source code from the file and generates tokens.
    2. Syntactic Analysis in Python: Parses the tokens to generate an Abstract Syntax Tree (AST) in Python.
    3. Syntactic Analysis in C (if necessary): Uses a C parser to further analyze the code.

    The function prints the generated tokens, the AST, and the result of the C analysis.
    If a syntax error occurs during the Python parsing step, it prints the error message and stops further analysis.
    """
    
    """Función principal para analizar código fuente desde un archivo."""
    # Leer el código desde el archivo
    with open(filename, 'r') as file:
        input_code = file.read()

    # Paso 1: Análisis léxico
    lexer = Lexer(input_code)
    tokens = lexer.generate_tokens()
    #print("Tokens generados:", tokens)

    # Paso 2: Análisis sintáctico en Python
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast is not None:
            # print("AST generado exitosamente:", ast)
            print("El análisis sintáctico ha finalizado exitosamente.")
        else:
            print("Error en el análisis sintáctico.")
    except SyntaxError as e:
        print(e)

'''
    # Paso 3: Análisis en C (si es necesario)
    cparser = initialize_cparser(input_code, "eval_input")
    result = lib._PyPegen_parse(ctypes.byref(cparser))

    if result is None:
        print("Error de análisis en C.")
    else:
        print("Análisis exitoso en C.")

    lib.free_parser(ctypes.byref(cparser))
'''

# Ejemplo de uso
if __name__ == "__main__":
    parse_code("entrada.py")# Lee el código desde el archivo entrada.txt
