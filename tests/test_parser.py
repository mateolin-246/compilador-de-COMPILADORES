"""Pruebas unitarias del parser descendente recursivo."""

import pytest

from compiler.ast.nodes import (
    AssignmentNode,
    BinaryExpressionNode,
    ConditionalNode,
    LiteralNode,
    ProgramNode,
)
from compiler.errors.exceptions import ParserError
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


def analizar(codigo: str) -> ProgramNode:
    return Parser(Lexer(codigo).analizar()).analizar()


def test_asignacion_valida() -> None:
    arbol = analizar("x = 10;")
    assert isinstance(arbol.sentencias[0], AssignmentNode)


def test_suma_valida() -> None:
    arbol = analizar("x = 10 + 5;")
    asignacion = arbol.sentencias[0]
    assert isinstance(asignacion, AssignmentNode)
    assert isinstance(asignacion.expresion, BinaryExpressionNode)
    assert asignacion.expresion.operador == "+"


def test_parentesis_y_multiplicacion_validos() -> None:
    arbol = analizar("resultado = (10 + 5) * 2;")
    expresion = arbol.sentencias[0].expresion
    assert isinstance(expresion, BinaryExpressionNode)
    assert expresion.operador == "*"
    assert isinstance(expresion.izquierda, BinaryExpressionNode)


def test_varias_asignaciones_validas() -> None:
    arbol = analizar("x = 10;\ny = 20;\nresultado = x + y;")
    assert len(arbol.sentencias) == 3
    assert all(isinstance(nodo, AssignmentNode) for nodo in arbol.sentencias)


def test_condicional_valido() -> None:
    arbol = analizar("si (x > 10) { y = 20; }")
    condicional = arbol.sentencias[0]
    assert isinstance(condicional, ConditionalNode)
    assert condicional.condicion.operador == ">"
    assert len(condicional.cuerpo) == 1


def test_error_si_falta_asignacion() -> None:
    with pytest.raises(ParserError) as error:
        analizar("x 10;")
    assert "'=' después del identificador" in str(error.value)


def test_error_si_falta_expresion() -> None:
    with pytest.raises(ParserError) as error:
        analizar("x = ;")
    assert "Se esperaba una expresión válida" in str(error.value)


def test_error_si_operacion_esta_incompleta() -> None:
    with pytest.raises(ParserError) as error:
        analizar("x = 10 + ;")
    assert error.value.encontrado == ";"


def test_error_si_falta_parentesis_del_condicional() -> None:
    with pytest.raises(ParserError) as error:
        analizar("si (x > 10 {")
    assert "')' después de la condición" in str(error.value)


def test_precedencia_multiplicacion_antes_que_suma() -> None:
    arbol = analizar("x = 2 + 3 * 4;")
    expresion = arbol.sentencias[0].expresion
    assert isinstance(expresion, BinaryExpressionNode)
    assert expresion.operador == "+"
    assert isinstance(expresion.derecha, BinaryExpressionNode)
    assert expresion.derecha.operador == "*"
    assert isinstance(expresion.derecha.izquierda, LiteralNode)


def test_condicional_anidado() -> None:
    codigo = "si (x > 0) { si (x <= 10) { y = 1; } }"
    arbol = analizar(codigo)
    exterior = arbol.sentencias[0]
    assert isinstance(exterior, ConditionalNode)
    assert isinstance(exterior.cuerpo[0], ConditionalNode)
