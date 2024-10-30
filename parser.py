from lexer import Token, Lexer  # Necesario tener implementado un Lexer para obtener tokens

# Diccionario que mapea tipos de token a sus símbolos para mensajes de error
SYMBOLS = {
    "RPAR": ")", "LPAR": "(", "LSQB": "[", "RSQB": "]", "COLON": ":",
    "COMMA": ",", "SEMI": ";", "PLUS": "+", "MINUS": "-", "STAR": "*",
    "SLASH": "/", "VBAR": "|", "AMPER": "&", "LESS": "<", "GREATER": ">",
    "EQUAL": "=", "DOT": ".", "PERCENT": "%", "LBRACE": "{", "RBRACE": "}",
    "EQEQUAL": "==", "NOTEQUAL": "!=", "LESSEQUAL": "<=", "GREATEREQUAL": ">=",
    "TILDE": "~", "CIRCUMFLEX": "^", "LEFTSHIFT": "<<", "RIGHTSHIFT": ">>",
    "DOUBLESTAR": "**", "PLUSEQUAL": "+=", "MINEQUAL": "-=", "STAREQUAL": "*=",
    "SLASHEQUAL": "/=", "PERCENTEQUAL": "%=", "AMPEREQUAL": "&=", "VBAREQUAL": "|=",
    "CIRCUMFLEXEQUAL": "^=", "LEFTSHIFTEQUAL": "<<=", "RIGHTSHIFTEQUAL": ">>=",
    "DOUBLESTAREQUAL": "**=", "DOUBLESLASH": "//", "DOUBLESLASHEQUAL": "//=",
    "AT": "@", "ATEQUAL": "@=", "RARROW": "->", "ELLIPSIS": "...", "COLONEQUAL": ":=",
    "EXCLAMATION": "!"
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]
        self.indent_stack = [0]  # Pila para manejar el nivel de indentación

    def advance(self):
        """Avanza al siguiente token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token("EOF", None, -1, -1)

    def parse(self):
        """Inicia el análisis sintáctico."""
        try:
            ast = self.file()
            print("AST generado exitosamente:", ast)
            return ast
        except SyntaxError as e:
            print(e)
            return None

    def file(self):
        """Regla de inicio `file`."""
        statements = []
        while self.current_token.type != "EOF":
            statements.append(self.statement())
            self.advance()
        return {"type": "file", "statements": statements}

    def statement(self):
        """Procesa diferentes tipos de sentencias."""
        if self.current_token.type == "KEYWORD" and self.current_token.value == "def":
            return self.function_def()
        elif self.current_token.type == "KEYWORD" and self.current_token.value in {"if", "else", "while", "for"}:
            return self.control_flow()
        elif self.current_token.type == "KEYWORD" and self.current_token.value == "pass":
            return self.pass_stmt()
        else:
            return self.expression()

    def function_def(self):
        """Definición de función con manejo de indentación."""
        self.match("KEYWORD", "def")
        func_name = self.current_token.value
        self.match("NAME")
        self.match("LPAR")
        params = self.parameters()
        self.match("RPAR")
        self.match("COLON")
        
        # Verificar y manejar indentación del bloque de la función
        if self.current_token.type == "NEWLINE":
            self.match("NEWLINE")
            if self.current_token.type != "INDENT":
                self.indentation_error()
            self.match("INDENT")
            body = self.block()
            self.match("DEDENT")
        else:
            body = [self.statement()]
        
        return {"type": "function_def", "name": func_name, "params": params, "body": body}

    def control_flow(self):
        """Manejo de estructuras de control con indentación."""
        if self.current_token.value == "if":
            return self.if_stmt()
        elif self.current_token.value == "while":
            return self.while_stmt()
        elif self.current_token.value == "for":
            return self.for_stmt()

    def if_stmt(self):
        """Declaración `if` con manejo de indentación."""
        self.match("KEYWORD", "if")
        condition = self.expression()
        self.match("COLON")
        
        # Verificar indentación después de `if`:
        if self.current_token.type == "NEWLINE":
            self.match("NEWLINE")
            if self.current_token.type != "INDENT":
                self.indentation_error()
            self.match("INDENT")
            then_branch = self.block()
            self.match("DEDENT")
        else:
            then_branch = [self.statement()]

        else_branch = None
        if self.current_token.value == "else":
            self.match("KEYWORD", "else")
            self.match("COLON")
            if self.current_token.type == "NEWLINE":
                self.match("NEWLINE")
                if self.current_token.type != "INDENT":
                    self.indentation_error()
                self.match("INDENT")
                else_branch = self.block()
                self.match("DEDENT")
            else:
                else_branch = [self.statement()]

        return {"type": "if_stmt", "condition": condition, "then": then_branch, "else": else_branch}

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
        """Regla para `pass`."""
        self.match("KEYWORD", "pass")
        return {"type": "pass_stmt"}

    def match(self, expected_type, expected_value=None):
        """Verifica y consume tokens, lanza error si no coincide."""
        if self.current_token.type == expected_type and (expected_value is None or self.current_token.value == expected_value):
            self.advance()
        else:
            found = SYMBOLS.get(self.current_token.type, self.current_token.value or self.current_token.type)
            expected = SYMBOLS.get(expected_type, expected_value or expected_type)
            self.syntax_error(expected, found)

    def syntax_error(self, expected, found=None):
        """Genera un mensaje de error de sintaxis detallado."""
        found = found or self.current_token.value
        error_msg = f"<{self.current_token.line},{self.current_token.column}> Error sintactico: se encontro: '{found}'; se esperaba: '{expected}'."
        raise SyntaxError(error_msg)

    def indentation_error(self):
        """Lanza un error de sintaxis específico de indentación."""
        error_msg = f"<{self.current_token.line},{self.current_token.column}> Error sintactico: falla de indentacion"
        raise SyntaxError(error_msg)

    def block(self):
        """Manejo de un bloque de código (series de sentencias)."""
        statements = []
        while self.current_token.type != "DEDENT" and self.current_token.type != "EOF":
            statements.append(self.statement())
            self.advance()
        return {"type": "block", "statements": statements}

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
