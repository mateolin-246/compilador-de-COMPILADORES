"""Excepciones con mensajes descriptivos y ubicación en el código."""

from compiler.lexer.token import Token


class MiniLangError(Exception):
    """Clase base para errores controlados del compilador."""


class LexicalError(MiniLangError):
    """Error producido al encontrar una secuencia léxica inválida."""

    def __init__(self, linea: int, columna: int, detalle: str) -> None:
        self.linea = linea
        self.columna = columna
        self.detalle = detalle
        super().__init__(str(self))

    def __str__(self) -> str:
        return (
            f"Error léxico en línea {self.linea}, columna {self.columna}:\n"
            f"{self.detalle}"
        )


class ParserError(MiniLangError):
    """Error producido cuando los tokens no cumplen la gramática."""

    def __init__(self, token: Token, esperado: str, detalle: str | None = None) -> None:
        self.token = token
        self.linea = token.linea
        self.columna = token.columna
        self.esperado = esperado
        self.encontrado = "fin de archivo" if token.tipo.name == "EOF" else token.lexema
        self.detalle = detalle or "La secuencia de tokens no cumple la gramática."
        super().__init__(str(self))

    def __str__(self) -> str:
        return (
            f"Error sintáctico en línea {self.linea}, columna {self.columna}:\n"
            f"{self.detalle}\n"
            f"Se esperaba: {self.esperado}.\n"
            f"Se encontró: {self.encontrado!r} ({self.token.tipo.name})."
        )
