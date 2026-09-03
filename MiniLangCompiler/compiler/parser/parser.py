"""Parser descendente recursivo para MiniLang."""

from compiler.ast.nodes import (
    ASTNode,
    AssignmentNode,
    BinaryExpressionNode,
    ConditionalNode,
    LiteralNode,
    ProgramNode,
    VariableNode,
)
from compiler.errors.exceptions import ParserError
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType


class Parser:
    """Valida la gramática y construye un árbol de sintaxis abstracta."""

    OPERADORES_COMPARACION = {
        TokenType.IGUAL,
        TokenType.DIFERENTE,
        TokenType.MAYOR,
        TokenType.MENOR,
        TokenType.MAYOR_IGUAL,
        TokenType.MENOR_IGUAL,
    }

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.indice = 0

    def analizar(self) -> ProgramNode:
        sentencias: list[ASTNode] = []
        while not self._comprobar(TokenType.EOF):
            sentencias.append(self._sentencia())
        return ProgramNode(sentencias)

    def parse(self) -> ProgramNode:
        """Alias convencional del método principal del parser."""
        return self.analizar()

    def _sentencia(self) -> ASTNode:
        if self._comprobar(TokenType.SI):
            return self._condicional()
        if self._comprobar(TokenType.IDENTIFICADOR):
            return self._asignacion()
        raise ParserError(
            self._actual(),
            "un identificador o la palabra reservada 'si'",
            "Se esperaba el inicio de una sentencia.",
        )

    def _asignacion(self) -> AssignmentNode:
        identificador = self._consumir(
            TokenType.IDENTIFICADOR,
            "un identificador",
            "Se esperaba el nombre de la variable.",
        )
        self._consumir(
            TokenType.ASIGNACION,
            "'=' después del identificador",
            "Toda asignación debe incluir el operador '='.",
        )
        expresion = self._expresion()
        self._consumir(
            TokenType.PUNTO_COMA,
            "';' al final de la asignación",
            "Toda asignación debe terminar con punto y coma.",
        )
        return AssignmentNode(identificador.valor, expresion)

    def _condicional(self) -> ConditionalNode:
        self._consumir(TokenType.SI, "'si'")
        self._consumir(
            TokenType.PARENTESIS_IZQ,
            "'(' después de 'si'",
            "La condición debe comenzar entre paréntesis.",
        )
        condicion = self._condicion()
        self._consumir(
            TokenType.PARENTESIS_DER,
            "')' después de la condición",
            "La condición debe cerrarse con ')'.",
        )
        self._consumir(
            TokenType.LLAVE_IZQ,
            "'{' para iniciar el cuerpo del condicional",
            "El cuerpo de 'si' debe comenzar con una llave.",
        )

        cuerpo: list[ASTNode] = []
        while not self._comprobar(TokenType.LLAVE_DER) and not self._comprobar(
            TokenType.EOF
        ):
            cuerpo.append(self._sentencia())

        self._consumir(
            TokenType.LLAVE_DER,
            "'}' para cerrar el cuerpo del condicional",
            "El cuerpo de 'si' no fue cerrado.",
        )
        return ConditionalNode(condicion, cuerpo)

    def _condicion(self) -> BinaryExpressionNode:
        izquierda = self._expresion()
        operador = self._actual()
        if operador.tipo not in self.OPERADORES_COMPARACION:
            raise ParserError(
                operador,
                "un operador de comparación (==, !=, >, <, >= o <=)",
                "La condición necesita comparar dos expresiones.",
            )
        self._avanzar()
        derecha = self._expresion()
        return BinaryExpressionNode(izquierda, operador.lexema, derecha)

    def _expresion(self) -> ASTNode:
        nodo = self._termino()
        while self._coincidir(TokenType.SUMA, TokenType.RESTA):
            operador = self._anterior()
            derecha = self._termino()
            nodo = BinaryExpressionNode(nodo, operador.lexema, derecha)
        return nodo

    def _termino(self) -> ASTNode:
        nodo = self._factor()
        while self._coincidir(TokenType.MULTIPLICACION, TokenType.DIVISION):
            operador = self._anterior()
            derecha = self._factor()
            nodo = BinaryExpressionNode(nodo, operador.lexema, derecha)
        return nodo

    def _factor(self) -> ASTNode:
        if self._coincidir(TokenType.NUMERO):
            token = self._anterior()
            return LiteralNode(token.valor, "NUMERO")
        if self._coincidir(TokenType.CADENA):
            token = self._anterior()
            return LiteralNode(token.valor, "CADENA")
        if self._coincidir(TokenType.IDENTIFICADOR):
            return VariableNode(self._anterior().valor)
        if self._coincidir(TokenType.PARENTESIS_IZQ):
            expresion = self._expresion()
            self._consumir(
                TokenType.PARENTESIS_DER,
                "')' después de la expresión",
                "La expresión agrupada no fue cerrada.",
            )
            return expresion
        raise ParserError(
            self._actual(),
            "un número, una cadena, un identificador o '('",
            "Se esperaba una expresión válida.",
        )

    def _consumir(
        self,
        tipo: TokenType,
        esperado: str,
        detalle: str | None = None,
    ) -> Token:
        if self._comprobar(tipo):
            return self._avanzar()
        raise ParserError(self._actual(), esperado, detalle)

    def _coincidir(self, *tipos: TokenType) -> bool:
        if any(self._comprobar(tipo) for tipo in tipos):
            self._avanzar()
            return True
        return False

    def _comprobar(self, tipo: TokenType) -> bool:
        return self._actual().tipo == tipo

    def _avanzar(self) -> Token:
        if not self._comprobar(TokenType.EOF):
            self.indice += 1
        return self._anterior()

    def _actual(self) -> Token:
        return self.tokens[self.indice]

    def _anterior(self) -> Token:
        return self.tokens[self.indice - 1]
