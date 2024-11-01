# main.py
from lexer import Lexer
from parser import Parser
import os

def parse_code(filename):
    """
    Main function to analyze source code from a file.

    Args:
        filename (str): The path to the source code file to be analyzed.

    This function performs the following steps:
    1. Lexical Analysis: Reads the source code from the file and generates tokens.
    2. Syntactic Analysis in Python: Parses the tokens to generate an Abstract Syntax Tree (AST) in Python.

    The function prints the generated tokens and the result of the parsing.
    If a syntax error occurs during the Python parsing step, it prints the error message and stops further analysis.
    """
    
    if not os.path.exists(filename):
        print(f"Error: El archivo '{filename}' no existe.")
        return

    # Leer el código desde el archivo
    with open(filename, 'r') as file:
        input_code = file.read()

    # Paso 1: Análisis léxico
    lexer = Lexer(input_code)
    tokens = lexer.generate_tokens()

    print("Tokens generados:")
    for token in tokens:
        print(token)

    # Paso 2: Análisis sintáctico en Python
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast is not None:
            print("El análisis sintáctico ha finalizado exitosamente.")
            # print("AST generado exitosamente:", ast)  # Descomentar si necesitas ver el AST
        else:
            print("Error en el análisis sintáctico.")
    except SyntaxError as e:
        print(e)


# Ejemplo de uso
if __name__ == "__main__":
    parse_code("entrada.py")  # Lee el código desde el archivo entrada.py
