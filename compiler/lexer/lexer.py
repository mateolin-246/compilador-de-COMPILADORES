"""Lexer manual para el lenguaje MiniLang."""

from compiler.errors.exceptions import LexicalError
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType


class Lexer:
    """Convierte código fuente MiniLang en una lista de tokens."""

    PALABRAS_RESERVADAS = {"si": TokenType.SI}

    TOKENS_DOBLES = {
        "==": TokenType.IGUAL,
        "!=": TokenType.DIFERENTE,
        ">=": TokenType.MAYOR_IGUAL,
        "<=": TokenType.MENOR_IGUAL,
    }

    TOKENS_SIMPLES = {
        "+": TokenType.SUMA,
        "-": TokenType.RESTA,
        "*": TokenType.MULTIPLICACION,
        "/": TokenType.DIVISION,
        "=": TokenType.ASIGNACION,
        ">": TokenType.MAYOR,
        "<": TokenType.MENOR,
        "(": TokenType.PARENTESIS_IZQ,
        ")": TokenType.PARENTESIS_DER,
        "{": TokenType.LLAVE_IZQ,
        "}": TokenType.LLAVE_DER,
        ";": TokenType.PUNTO_COMA,
    }

    def __init__(self, codigo_fuente: str) -> None:
        self.codigo_fuente = codigo_fuente
        self.indice = 0
        self.linea = 1
        self.columna = 1

    def analizar(self) -> list[Token]:
        """Recorre todo el código y devuelve sus tokens, incluido EOF."""
        tokens: list[Token] = []

        while not self._al_final():
            caracter = self._actual()

            if caracter in " \t\r":
                self._avanzar()
            elif caracter == "\n":
                self._avanzar()
            elif caracter == "/" and self._mirar() == "/":
                self._ignorar_comentario()
            elif caracter.isalpha() or caracter == "_":
                tokens.append(self._leer_identificador())
            elif caracter.isdigit():
                tokens.append(self._leer_numero())
            elif caracter == '"':
                tokens.append(self._leer_cadena())
            else:
                token = self._leer_operador_o_simbolo()
                if token is None:
                    raise LexicalError(
                        self.linea,
                        self.columna,
                        f"Carácter no reconocido: {caracter!r}",
                    )
                tokens.append(token)

        tokens.append(Token(TokenType.EOF, None, self.linea, self.columna, "EOF"))
        return tokens

    def scan_tokens(self) -> list[Token]:
        """Alias en inglés útil para integrar el lexer con otras herramientas."""
        return self.analizar()

    def _leer_identificador(self) -> Token:
        linea, columna = self.linea, self.columna
        inicio = self.indice

        while not self._al_final() and (
            self._actual().isalnum() or self._actual() == "_"
        ):
            self._avanzar()

        lexema = self.codigo_fuente[inicio : self.indice]
        tipo = self.PALABRAS_RESERVADAS.get(lexema, TokenType.IDENTIFICADOR)
        return Token(tipo, lexema, linea, columna, lexema)

    def _leer_numero(self) -> Token:
        linea, columna = self.linea, self.columna
        inicio = self.indice

        while not self._al_final() and self._actual().isdigit():
            self._avanzar()

        if (
            not self._al_final()
            and self._actual() == "."
            and self._mirar().isdigit()
        ):
            self._avanzar()
            while not self._al_final() and self._actual().isdigit():
                self._avanzar()

        lexema = self.codigo_fuente[inicio : self.indice]
        valor = float(lexema) if "." in lexema else int(lexema)
        return Token(TokenType.NUMERO, valor, linea, columna, lexema)

    def _leer_cadena(self) -> Token:
        linea, columna = self.linea, self.columna
        inicio = self.indice
        self._avanzar()
        caracteres: list[str] = []

        escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
        while not self._al_final() and self._actual() != '"':
            if self._actual() == "\n":
                raise LexicalError(
                    linea,
                    columna,
                    "Cadena sin cerrar antes del final de la línea.",
                )

            if self._actual() == "\\":
                self._avanzar()
                if self._al_final():
                    break
                escapado = self._actual()
                if escapado not in escapes:
                    raise LexicalError(
                        self.linea,
                        self.columna,
                        f"Secuencia de escape no reconocida: '\\{escapado}'",
                    )
                caracteres.append(escapes[escapado])
                self._avanzar()
            else:
                caracteres.append(self._actual())
                self._avanzar()

        if self._al_final():
            raise LexicalError(linea, columna, "Cadena sin cerrar al final del archivo.")

        self._avanzar()
        lexema = self.codigo_fuente[inicio : self.indice]
        return Token(TokenType.CADENA, "".join(caracteres), linea, columna, lexema)

    def _leer_operador_o_simbolo(self) -> Token | None:
        linea, columna = self.linea, self.columna
        doble = self._actual() + self._mirar()

        if doble in self.TOKENS_DOBLES:
            self._avanzar()
            self._avanzar()
            return Token(self.TOKENS_DOBLES[doble], doble, linea, columna, doble)

        simple = self._actual()
        if simple in self.TOKENS_SIMPLES:
            self._avanzar()
            return Token(self.TOKENS_SIMPLES[simple], simple, linea, columna, simple)

        return None

    def _ignorar_comentario(self) -> None:
        while not self._al_final() and self._actual() != "\n":
            self._avanzar()

    def _actual(self) -> str:
        return "\0" if self._al_final() else self.codigo_fuente[self.indice]

    def _mirar(self, desplazamiento: int = 1) -> str:
        posicion = self.indice + desplazamiento
        return "\0" if posicion >= len(self.codigo_fuente) else self.codigo_fuente[posicion]

    def _avanzar(self) -> str:
        caracter = self.codigo_fuente[self.indice]
        self.indice += 1
        if caracter == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        return caracter

    def _al_final(self) -> bool:
        return self.indice >= len(self.codigo_fuente)
