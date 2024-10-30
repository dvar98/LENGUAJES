import ctypes
from lexer import Lexer
from parser import Parser

def run_test(parser_class, code, description):
    print(f"Running test: {description}")
    lexer = Lexer(code)  # Asegúrate de tener un Lexer implementado para tokenizar `code`
    tokens = lexer.tokenize()
    parser = parser_class(tokens)
    result = parser.parse()
    print("Result:", result)
    print("-" * 40)


# Casos de prueba para el parser
tests = [
    {
        "description": "Función simple con parámetros y bloque correctamente indentado",
        "code": """
def is_even(x: int):
    if x % 2 == 0:
        return True
    else:
        return False
""",
        "expected": "AST sin errores"
    },
    {
        "description": "Error de sintaxis en palabra clave mal escrita ('DEF' en lugar de 'def')",
        "code": """
DEF is_even(x: int):
    return True
""",
        "expected": "<1,1> Error sintactico: se encontro: 'DEF'; se esperaba: 'expresion'"
    },
    {
        "description": "Error de indentación en el bloque de una función",
        "code": """
def is_odd(x: int):
if x % 2 != 0:
    return True
""",
        "expected": "<2,1> Error sintactico: falla de indentacion"
    },
    {
        "description": "Bloque `if-else` con indentación incorrecta en `else`",
        "code": """
def check_positive(x: int):
    if x > 0:
        return True
    else:
    return False
""",
        "expected": "<5,5> Error sintactico: falla de indentacion"
    },
    {
        "description": "Uso correcto de listas y anotaciones de tipo en parámetros",
        "code": """
def process_list(items: [int]):
    for item in items:
        print(item)
""",
        "expected": "AST sin errores"
    },
    {
        "description": "Error en parámetro de tipo faltante",
        "code": """
def process_data(data: ):
    pass
""",
        "expected": "<1,22> Error sintactico: se encontro: ')'; se esperaba: 'expression'"
    },
    {
        "description": "Expresión de retorno fuera de función",
        "code": """
return True
""",
        "expected": "<1,1> Error sintactico: 'return' fuera de una función"
    },
    {
        "description": "Error de indentación en bloque `if` dentro de función",
        "code": """
def is_even(x: int):
    if x % 2 == 0:
    return True
""",
        "expected": "<3,5> Error sintactico: falla de indentacion"
    },
    {
        "description": "Declaración `for` con expresión faltante",
        "code": """
def iterate_numbers(numbers: [int]):
    for in numbers:
        print(invalid)
""",
        "expected": "<2,9> Error sintactico: se encontro: 'in'; se esperaba: 'expression'"
    },
    {
        "description": "Función anidada con bloques correctamente indentados",
        "code": """
def outer(x: int):
    def inner(y: int):
        return y + x
    return inner
""",
        "expected": "AST sin errores"
    },
]

# Ejecutar los tests
for test in tests:
    run_test(Parser, test["code"], test["description"])
