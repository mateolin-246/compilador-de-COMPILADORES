"""Pruebas unitarias del analizador léxico."""

import pytest

from compiler.errors.exceptions import LexicalError
from compiler.lexer.lexer import Lexer
from compiler.lexer.token_type import TokenType


def tipos(codigo: str) -> list[TokenType]:
    return [token.tipo for token in Lexer(codigo).analizar()]


def test_asignacion() -> None:
    assert tipos("x = 10;") == [
        TokenType.IDENTIFICADOR,
        TokenType.ASIGNACION,
        TokenType.NUMERO,
        TokenType.PUNTO_COMA,
        TokenType.EOF,
    ]


def test_operacion() -> None:
    assert tipos("x = 10 + 5;") == [
        TokenType.IDENTIFICADOR,
        TokenType.ASIGNACION,
        TokenType.NUMERO,
        TokenType.SUMA,
        TokenType.NUMERO,
        TokenType.PUNTO_COMA,
        TokenType.EOF,
    ]


def test_parentesis_y_multiplicacion() -> None:
    assert tipos("resultado = (10 + 5) * 2;") == [
        TokenType.IDENTIFICADOR,
        TokenType.ASIGNACION,
        TokenType.PARENTESIS_IZQ,
        TokenType.NUMERO,
        TokenType.SUMA,
        TokenType.NUMERO,
        TokenType.PARENTESIS_DER,
        TokenType.MULTIPLICACION,
        TokenType.NUMERO,
        TokenType.PUNTO_COMA,
        TokenType.EOF,
    ]


def test_decimal_es_un_solo_numero() -> None:
    tokens = Lexer("x = 3.14;").analizar()
    assert tokens[2].tipo == TokenType.NUMERO
    assert tokens[2].valor == 3.14
    assert tokens[2].lexema == "3.14"


def test_cadena() -> None:
    tokens = Lexer('nombre = "Mateo";').analizar()
    assert tokens[2].tipo == TokenType.CADENA
    assert tokens[2].valor == "Mateo"


def test_comentarios_se_ignoran() -> None:
    tokens = Lexer("// comentario\nx = 10;").analizar()
    assert [token.tipo for token in tokens] == [
        TokenType.IDENTIFICADOR,
        TokenType.ASIGNACION,
        TokenType.NUMERO,
        TokenType.PUNTO_COMA,
        TokenType.EOF,
    ]
    assert tokens[0].linea == 2


def test_error_lexico_por_caracter_invalido() -> None:
    with pytest.raises(LexicalError) as error:
        Lexer("x = 10 @ 5;").analizar()
    assert error.value.linea == 1
    assert error.value.columna == 8
    assert "@" in str(error.value)


def test_operadores_de_comparacion() -> None:
    codigo = "x == 1 != 2 > 3 < 4 >= 5 <= 6"
    tokens = Lexer(codigo).analizar()
    comparadores = [
        token.tipo
        for token in tokens
        if token.tipo
        in {
            TokenType.IGUAL,
            TokenType.DIFERENTE,
            TokenType.MAYOR,
            TokenType.MENOR,
            TokenType.MAYOR_IGUAL,
            TokenType.MENOR_IGUAL,
        }
    ]
    assert comparadores == [
        TokenType.IGUAL,
        TokenType.DIFERENTE,
        TokenType.MAYOR,
        TokenType.MENOR,
        TokenType.MAYOR_IGUAL,
        TokenType.MENOR_IGUAL,
    ]


def test_linea_y_columna() -> None:
    tokens = Lexer("x = 10;\n  resultado = x;").analizar()
    resultado = tokens[4]
    assert resultado.lexema == "resultado"
    assert resultado.linea == 2
    assert resultado.columna == 3


def test_error_por_cadena_sin_cerrar() -> None:
    with pytest.raises(LexicalError) as error:
        Lexer('mensaje = "hola').analizar()
    assert "Cadena sin cerrar" in str(error.value)
