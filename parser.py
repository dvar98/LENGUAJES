# parser.py
from lexer import Token, Lexer

# Diccionario que mapea tipos de token a sus símbolos
SYMBOLS = {
    "RPAR": ")",
    "LPAR": "(",
    "LSQB": "[",
    "RSQB": "]",
    "COLON": ":",
    "COMMA": ",",
    "SEMI": ";",
    "PLUS": "+",
    "MINUS": "-",
    "STAR": "*",
    "SLASH": "/",
    "VBAR": "|",
    "AMPER": "&",
    "LESS": "<",
    "GREATER": ">",
    "EQUAL": "=",
    "DOT": ".",
    "PERCENT": "%",
    "LBRACE": "{",
    "RBRACE": "}",
    "EQEQUAL": "==",
    "NOTEQUAL": "!=",
    "LESSEQUAL": "<=",
    "GREATEREQUAL": ">=",
    "TILDE": "~",
    "CIRCUMFLEX": "^",
    "LEFTSHIFT": "<<",
    "RIGHTSHIFT": ">>",
    "DOUBLESTAR": "**",
    "PLUSEQUAL": "+=",
    "MINEQUAL": "-=",
    "STAREQUAL": "*=",
    "SLASHEQUAL": "/=",
    "PERCENTEQUAL": "%=",
    "AMPEREQUAL": "&=",
    "VBAREQUAL": "|=",
    "CIRCUMFLEXEQUAL": "^=",
    "LEFTSHIFTEQUAL": "<<=",
    "RIGHTSHIFTEQUAL": ">>=",
    "DOUBLESTAREQUAL": "**=",
    "DOUBLESLASH": "//",
    "DOUBLESLASHEQUAL": "//=",
    "AT": "@",
    "ATEQUAL": "@=",
    "RARROW": "->",
    "ELLIPSIS": "...",
    "COLONEQUAL": ":=",
    "EXCLAMATION": "!"
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]

    def advance(self):
        """Avanza al siguiente token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token("EOF", None, -1, -1)

    def parse(self):
        """Inicia el análisis sintáctico a partir de la regla inicial `file`."""
        try:
            ast = self.file()
            # print("AST generado exitosamente:", ast)
            return ast
        except SyntaxError as e:
            print(e)
            return None

    def file(self):
        """Regla de inicio `file`: maneja un archivo completo de declaraciones."""
        statements = []
        while self.current_token.type != "EOF":
            statement = self.statement()
            if statement:
                statements.append(statement)
            self.advance()
        return {"type": "file", "statements": statements}

    def statement(self):
        """Identifica y procesa una sentencia (declaración)."""
        if self.current_token.type == "KEYWORD" and self.current_token.value == "class":
            return self.class_def()
        elif self.current_token.type == "KEYWORD" and self.current_token.value == "def":
            return self.function_def()
        elif self.current_token.type == "KEYWORD" and self.current_token.value == "return":
            return self.return_stmt()
        elif self.current_token.type == "KEYWORD" and self.current_token.value in {"if", "while", "for"}:
            return self.control_flow()
        elif self.current_token.type == "KEYWORD" and self.current_token.value == "pass":
            return self.pass_stmt()
        else:
            return self.expression()

    def class_def(self):
        """Regla para definir una clase."""
        self.match("KEYWORD", "class")
        class_name = self.current_token.value
        self.match("NAME")
        self.match("COLON")
        body = self.block()
        return {"type": "class_def", "name": class_name, "body": body}

    def function_def(self):
        """Regla para definir una función con anotaciones de tipo."""
        self.match("KEYWORD", "def")
        func_name = self.current_token.value
        self.match("NAME")
        self.match("LPAR")
        params = self.parameters()
        self.match("RPAR")
        self.match("COLON")
        # Espera un salto de línea después de los dos puntos
        if self.current_token.type == "NEWLINE":
            self.match("NEWLINE")
            body = self.block()
        else:
            # Maneja una función de una sola línea como "pass"
            body = [self.statement()]
        return {"type": "function_def", "name": func_name, "params": params, "body": body}

    def parameters(self):
        """Manejo de parámetros de función, incluyendo anotaciones de tipo."""
        params = []
        while self.current_token.type != "RPAR":
            param_name = self.current_token.value
            self.match("NAME")
            if self.current_token.type == "COLON":
                self.match("COLON")
                param_type = self.type_annotation()
                params.append({"name": param_name, "type": param_type})
            else:
                params.append({"name": param_name, "type": None})

            if self.current_token.type == "COMMA":
                self.match("COMMA")
        return params

    def type_annotation(self):
        """Procesa anotaciones de tipo como parte de los parámetros de una función."""
        if self.current_token.type == "LSQB":
            self.match("LSQB")
            type_name = self.current_token.value
            self.match("NAME")
            self.match("RSQB")
            return {"type": "list", "subtype": type_name}
        else:
            type_name = self.current_token.value
            self.match("NAME")
            return {"type": type_name}

    def pass_stmt(self):
        """Regla para una sentencia `pass`."""
        self.match("KEYWORD", "pass")
        return {"type": "pass_stmt"}

    def return_stmt(self):
        """Regla para una sentencia de retorno."""
        self.match("KEYWORD", "return")
        expr = self.expression()
        return {"type": "return_stmt", "expression": expr}

    def control_flow(self):
        """Manejo de estructuras de control (if, while, for)."""
        if self.current_token.value == "if":
            return self.if_stmt()
        elif self.current_token.value == "while":
            return self.while_stmt()
        elif self.current_token.value == "for":
            return self.for_stmt()

    def if_stmt(self):
        """Regla para una declaración if."""
        self.match("KEYWORD", "if")
        condition = self.expression()
        self.match("COLON")
        then_branch = self.block()
        else_branch = None
        if self.current_token.value == "else":
            self.match("KEYWORD", "else")
            self.match("COLON")
            else_branch = self.block()
        return {"type": "if_stmt", "condition": condition, "then": then_branch, "else": else_branch}

    def expression(self):
        """Manejo básico de expresiones (literals, identifiers)."""
        if self.current_token.type == "NUMBER":
            value = self.current_token.value
            self.advance()
            return {"type": "literal", "value": value}
        elif self.current_token.type == "NAME":
            name = self.current_token.value
            self.advance()
            return {"type": "identifier", "name": name}
        else:
            self.syntax_error("expression")

    def block(self):
        """Manejo de un bloque de código (series de sentencias)."""
        statements = []
        self.match("NEWLINE")
        self.match("INDENT")
        while self.current_token.type != "DEDENT":
            statements.append(self.statement())
        self.match("DEDENT")
        return {"type": "block", "statements": statements}

    def match(self, expected_type, expected_value=None):
        """Verifica el tipo y valor del token actual y avanza."""
        if self.current_token.type == expected_type and (expected_value is None or self.current_token.value == expected_value):
            self.advance()
        else:
            found = SYMBOLS.get(self.current_token.type, self.current_token.value or self.current_token.type)
            expected = SYMBOLS.get(expected_type, expected_value or expected_type)
            self.syntax_error(expected, found)

    def syntax_error(self, expected, found=None):
        """Lanza un error de sintaxis con un mensaje detallado en el formato solicitado."""
        found = found or self.current_token.value
        error_msg = f"<{self.current_token.line},{self.current_token.column}> Error sintactico: se encontro: '{found}'; se esperaba: '{expected}'."
        raise SyntaxError(error_msg)
