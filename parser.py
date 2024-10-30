# parser.py
from lexer import Token, Lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token("EOF", None, -1, -1)

    def parse(self):
        return self.file()

    def file(self):
        statements = []
        while self.current_token.type != "EOF":
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == "KEYWORD" and self.current_token.value == "class":
            return self.class_def()
        elif self.current_token.type == "KEYWORD" and self.current_token.value == "def":
            return self.function_def()
        elif self.current_token.type == "KEYWORD" and self.current_token.value == "return":
            return self.return_stmt()
        else:
            return self.expression()

    def class_def(self):
        self.match("KEYWORD", "class")
        class_name = self.current_token.value
        self.match("NAME")
        self.match("COLON")
        body = self.block()
        return {"type": "class_def", "name": class_name, "body": body}

    def function_def(self):
        self.match("KEYWORD", "def")
        func_name = self.current_token.value
        self.match("NAME")
        self.match("LPAR")
        self.match("RPAR")
        self.match("COLON")
        body = self.block()
        return {"type": "function_def", "name": func_name, "body": body}

    def return_stmt(self):
        self.match("KEYWORD", "return")
        expr = self.expression()
        return {"type": "return_stmt", "expression": expr}

    def expression(self):
        if self.current_token.type == "NUMBER":
            value = self.current_token.value
            self.advance()
            return {"type": "literal", "value": value}
        self.error("Expected expression")

    def block(self):
        statements = []
        while self.current_token.type != "EOF" and self.current_token.value != "DEDENT":
            statements.append(self.statement())
        return statements

    def match(self, type_, value=None):
        if self.current_token.type == type_ and (value is None or self.current_token.value == value):
            self.advance()
        else:
            self.error(f"Expected {type_} {value}")

    def error(self, message):
        raise SyntaxError(f"{message} at line {self.current_token.line}, column {self.current_token.column}")
