"""Tipos de token reconocidos por MiniLang."""

from enum import Enum, auto


class TokenType(Enum):
    """Catálogo único y consistente de tokens del lenguaje."""

    IDENTIFICADOR = auto()
    NUMERO = auto()
    CADENA = auto()
    SI = auto()

    SUMA = auto()
    RESTA = auto()
    MULTIPLICACION = auto()
    DIVISION = auto()
    ASIGNACION = auto()
    IGUAL = auto()
    DIFERENTE = auto()
    MAYOR = auto()
    MENOR = auto()
    MAYOR_IGUAL = auto()
    MENOR_IGUAL = auto()

    PARENTESIS_IZQ = auto()
    PARENTESIS_DER = auto()
    LLAVE_IZQ = auto()
    LLAVE_DER = auto()
    PUNTO_COMA = auto()

    EOF = auto()
