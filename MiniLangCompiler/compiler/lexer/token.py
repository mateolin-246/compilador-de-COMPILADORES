"""Representación de un token de MiniLang."""

from dataclasses import dataclass
from typing import Any

from compiler.lexer.token_type import TokenType


@dataclass(frozen=True, slots=True)
class Token:
    """Unidad léxica con ubicación exacta en el código fuente."""

    tipo: TokenType
    valor: Any
    linea: int
    columna: int
    lexema: str

    def __str__(self) -> str:
        return f"{self.tipo.name:<18} {self.lexema}"
