"""Pruebas de construcción y visualización del AST."""

from compiler.ast.nodes import (
    AssignmentNode,
    BinaryExpressionNode,
    ConditionalNode,
    LiteralNode,
    ProgramNode,
    VariableNode,
    format_ast,
)
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


def analizar(codigo: str) -> ProgramNode:
    return Parser(Lexer(codigo).analizar()).analizar()


def test_ast_de_asignacion() -> None:
    arbol = analizar("x = 10;")
    asignacion = arbol.sentencias[0]
    assert isinstance(asignacion, AssignmentNode)
    assert asignacion.nombre == "x"
    assert asignacion.expresion == LiteralNode(10, "NUMERO")


def test_ast_de_operacion_binaria() -> None:
    arbol = analizar("resultado = x + y;")
    operacion = arbol.sentencias[0].expresion
    assert operacion == BinaryExpressionNode(VariableNode("x"), "+", VariableNode("y"))


def test_ast_de_condicional() -> None:
    arbol = analizar('si (x >= 10) { mensaje = "ok"; }')
    condicional = arbol.sentencias[0]
    assert isinstance(condicional, ConditionalNode)
    assert condicional.condicion.operador == ">="
    assert isinstance(condicional.cuerpo[0], AssignmentNode)


def test_formato_visual_del_ast() -> None:
    texto = format_ast(analizar("x = 10 + 5;"))
    assert "Programa" in texto
    assert "Asignación" in texto
    assert "Variable: x" in texto
    assert "Operación: +" in texto
    assert "Número: 10" in texto
    assert "Número: 5" in texto
