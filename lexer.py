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

    # Mapa de tokens
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

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.code[self.pos] if self.pos < len(self.code) else None

    def generate_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.make_identifier())
            elif self.current_char in self.token_map:
                tokens.append(self.make_operator())
            else:
                print(f"Error léxico en línea {self.line}, columna {self.column}")
                self.advance()
        return tokens

    def make_number(self):
        number = self.current_char
        start_column = self.column
        self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return Token("NUMBER", number, self.line, start_column)

    def make_identifier(self):
        identifier = self.current_char
        start_column = self.column
        self.advance()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        if identifier in {"if", "else", "class", "def", "return"}:
            return Token("KEYWORD", identifier, self.line, start_column)
        return Token("NAME", identifier, self.line, start_column)

    def make_operator(self):
        op = self.current_char
        start_column = self.column
        self.advance()
        if self.current_char and op + self.current_char in self.token_map:
            op += self.current_char
            self.advance()
        return Token(self.token_map[op], op, self.line, start_column)
