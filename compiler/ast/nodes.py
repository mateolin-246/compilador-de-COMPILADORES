"""Clases que representan el AST de MiniLang."""

from dataclasses import dataclass, field
from typing import Any


class ASTNode:
    """Clase base de todos los nodos del árbol."""


@dataclass(slots=True)
class ProgramNode(ASTNode):
    sentencias: list[ASTNode] = field(default_factory=list)


@dataclass(slots=True)
class AssignmentNode(ASTNode):
    nombre: str
    expresion: ASTNode


@dataclass(slots=True)
class BinaryExpressionNode(ASTNode):
    izquierda: ASTNode
    operador: str
    derecha: ASTNode


@dataclass(slots=True)
class LiteralNode(ASTNode):
    valor: Any
    tipo: str


@dataclass(slots=True)
class VariableNode(ASTNode):
    nombre: str


@dataclass(slots=True)
class ConditionalNode(ASTNode):
    condicion: ASTNode
    cuerpo: list[ASTNode] = field(default_factory=list)


def format_ast(nodo: ASTNode) -> str:
    """Devuelve una representación legible del AST usando ramas Unicode."""
    lineas: list[str] = []
    _agregar_nodo(nodo, "", True, lineas, raiz=True)
    return "\n".join(lineas)


def _agregar_nodo(
    nodo: ASTNode,
    prefijo: str,
    ultimo: bool,
    lineas: list[str],
    raiz: bool = False,
) -> None:
    conector = "" if raiz else ("└── " if ultimo else "├── ")
    lineas.append(f"{prefijo}{conector}{_etiqueta(nodo)}")
    hijos = _hijos(nodo)
    nuevo_prefijo = prefijo if raiz else prefijo + ("    " if ultimo else "│   ")

    for indice, hijo in enumerate(hijos):
        es_ultimo = indice == len(hijos) - 1
        if isinstance(hijo, ASTNode):
            _agregar_nodo(hijo, nuevo_prefijo, es_ultimo, lineas)
        else:
            conector_hijo = "└── " if es_ultimo else "├── "
            lineas.append(f"{nuevo_prefijo}{conector_hijo}{hijo}")


def _etiqueta(nodo: ASTNode) -> str:
    if isinstance(nodo, ProgramNode):
        return "Programa"
    if isinstance(nodo, AssignmentNode):
        return "Asignación"
    if isinstance(nodo, BinaryExpressionNode):
        return f"Operación: {nodo.operador}"
    if isinstance(nodo, LiteralNode):
        if nodo.tipo == "CADENA":
            return f"Cadena: {nodo.valor!r}"
        return f"Número: {nodo.valor}"
    if isinstance(nodo, VariableNode):
        return f"Variable: {nodo.nombre}"
    if isinstance(nodo, ConditionalNode):
        return "Condicional: si"
    return nodo.__class__.__name__


def _hijos(nodo: ASTNode) -> list[ASTNode | str]:
    if isinstance(nodo, ProgramNode):
        return list(nodo.sentencias)
    if isinstance(nodo, AssignmentNode):
        return [f"Variable: {nodo.nombre}", nodo.expresion]
    if isinstance(nodo, BinaryExpressionNode):
        return [nodo.izquierda, nodo.derecha]
    if isinstance(nodo, ConditionalNode):
        return ["Condición", nodo.condicion, "Cuerpo", *nodo.cuerpo]
    return []
