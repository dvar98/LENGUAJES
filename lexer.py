# lexer.py

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"<{self.type}, {self.value}, {self.line}, {self.column}>"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = code[self.pos] if code else None
        self.tokens = []  # Lista para almacenar tokens

    # Mapa de tokens para operadores y símbolos específicos
    token_map = {
        '(': 'LPAR', ')': 'RPAR', '[': 'LSQB', ']': 'RSQB', ':': 'COLON', ',': 'COMMA',
        ';': 'SEMI', '+': 'PLUS', '-': 'MINUS', '*': 'STAR', '/': 'SLASH', '|': 'VBAR',
        '&': 'AMPER', '<': 'LESS', '>': 'GREATER', '=': 'EQUAL', '.': 'DOT', '%': 'PERCENT',
        '{': 'LBRACE', '}': 'RBRACE', '==': 'EQEQUAL', '!=': 'NOTEQUAL', '<=': 'LESSEQUAL',
        '>=': 'GREATEREQUAL', '~': 'TILDE', '^': 'CIRCUMFLEX', '<<': 'LEFTSHIFT', '>>': 'RIGHTSHIFT',
        '**': 'DOUBLESTAR', '+=': 'PLUSEQUAL', '-=': 'MINEQUAL', '*=': 'STAREQUAL', '/=': 'SLASHEQUAL',
        '%=': 'PERCENTEQUAL', '&=': 'AMPEREQUAL', '|=': 'VBAREQUAL', '^=': 'CIRCUMFLEXEQUAL',
        '<<=': 'LEFTSHIFTEQUAL', '>>=': 'RIGHTSHIFTEQUAL', '**=': 'DOUBLESTAREQUAL', '//': 'DOUBLESLASH',
        '//=': 'DOUBLESLASHEQUAL', '@': 'AT', '@=': 'ATEQUAL', '->': 'RARROW', '...': 'ELLIPSIS',
        ':=': 'COLONEQUAL', '!': 'EXCLAMATION'
    }

    # Palabras reservadas de Python
    keywords = {
        "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class",
        "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global",
        "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
        "try", "while", "with", "yield"
    }

    def advance(self):
        """Avanza al siguiente carácter en el código y actualiza línea y columna."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.code[self.pos] if self.pos < len(self.code) else None

    def generate_tokens(self):
        """Genera tokens a partir del código fuente."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                self.tokens.append(self.make_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.make_identifier())
            elif self.current_char in self.token_map:
                self.tokens.append(self.make_operator())
            elif self.current_char == '#':  # Ignorar comentarios
                self.skip_comment()
            else:
                print(f"Error léxico en línea {self.line}, columna {self.column}")
                self.advance()
        return self.tokens

    def make_number(self):
        """Construye tokens de tipo número (entero o flotante)."""
        number = self.current_char
        start_column = self.column
        self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return Token("NUMBER", number, self.line, start_column)

    def make_identifier(self):
        """Construye tokens de tipo identificador o palabra clave."""
        identifier = self.current_char
        start_column = self.column
        self.advance()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        # Verificar si el identificador es una palabra clave
        token_type = "KEYWORD" if identifier in self.keywords else "NAME"
        return Token(token_type, identifier, self.line, start_column)

    def make_operator(self):
        """Construye tokens de operadores y símbolos especiales."""
        op = self.current_char
        start_column = self.column
        self.advance()
        # Verificar operadores de dos caracteres
        if self.current_char and op + self.current_char in self.token_map:
            op += self.current_char
            self.advance()
        return Token(self.token_map[op], op, self.line, start_column)

    def skip_comment(self):
        """Ignora comentarios hasta el final de la línea."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
