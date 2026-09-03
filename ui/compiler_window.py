"""Ventana Tkinter para analizar código MiniLang."""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from compiler.ast.nodes import format_ast
from compiler.errors.exceptions import LexicalError, ParserError
from compiler.lexer.lexer import Lexer
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType
from compiler.parser.parser import Parser


CODIGO_EJEMPLO = """// Programa de ejemplo
x = 10;
y = 20;
resultado = (x + y) * 2;

si (resultado > 20) {
    mensaje = "Resultado mayor que 20";
}
"""


class CompilerWindow:
    """Interfaz sencilla para mostrar tokens, validación sintáctica y AST."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MiniLang Compiler")
        self.root.geometry("1000x680")
        self.root.minsize(800, 560)
        self._configurar_estilos()
        self._crear_componentes()
        self.cargar_ejemplo()

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self.root)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10))
        estilo.configure("Accion.TButton", padding=(14, 7))

    def _crear_componentes(self) -> None:
        contenedor = ttk.Frame(self.root, padding=16)
        contenedor.pack(fill=tk.BOTH, expand=True)

        ttk.Label(contenedor, text="MiniLang Compiler", style="Titulo.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            contenedor,
            text="Analizador léxico, parser descendente recursivo y árbol AST",
            style="Subtitulo.TLabel",
        ).pack(anchor=tk.W, pady=(0, 12))

        paneles = ttk.PanedWindow(contenedor, orient=tk.HORIZONTAL)
        paneles.pack(fill=tk.BOTH, expand=True)

        panel_codigo = ttk.Frame(paneles, padding=(0, 0, 8, 0))
        panel_resultado = ttk.Frame(paneles, padding=(8, 0, 0, 0))
        paneles.add(panel_codigo, weight=1)
        paneles.add(panel_resultado, weight=1)

        ttk.Label(panel_codigo, text="Código fuente").pack(anchor=tk.W, pady=(0, 5))
        self.editor = ScrolledText(
            panel_codigo,
            wrap=tk.NONE,
            undo=True,
            font=("Consolas", 11),
            padx=10,
            pady=10,
        )
        self.editor.pack(fill=tk.BOTH, expand=True)

        ttk.Label(panel_resultado, text="Resultado").pack(anchor=tk.W, pady=(0, 5))
        self.salida = ScrolledText(
            panel_resultado,
            wrap=tk.NONE,
            state=tk.DISABLED,
            font=("Consolas", 10),
            padx=10,
            pady=10,
            background="#f6f8fa",
        )
        self.salida.pack(fill=tk.BOTH, expand=True)

        barra = ttk.Frame(contenedor)
        barra.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(
            barra,
            text="Analizar",
            command=self.analizar_codigo,
            style="Accion.TButton",
        ).pack(side=tk.LEFT)
        ttk.Button(
            barra,
            text="Ejemplo",
            command=self.cargar_ejemplo,
            style="Accion.TButton",
        ).pack(side=tk.LEFT, padx=8)
        ttk.Button(
            barra,
            text="Limpiar",
            command=self.limpiar,
            style="Accion.TButton",
        ).pack(side=tk.LEFT)
        self.estado = ttk.Label(barra, text="Listo")
        self.estado.pack(side=tk.RIGHT)

        self.root.bind("<Control-Return>", lambda _evento: self.analizar_codigo())

    def analizar_codigo(self) -> None:
        codigo = self.editor.get("1.0", tk.END).rstrip()
        if not codigo.strip():
            self._mostrar("Escribe código MiniLang o presiona el botón Ejemplo.")
            self.estado.configure(text="Sin código")
            return

        try:
            tokens = Lexer(codigo).analizar()
        except LexicalError as error:
            self._mostrar(f"✗ ERROR LÉXICO\n\n{error}")
            self.estado.configure(text="Error léxico")
            return

        seccion_lexica = self._formatear_tokens(tokens)
        try:
            arbol = Parser(tokens).analizar()
        except ParserError as error:
            self._mostrar(
                f"ANÁLISIS LÉXICO\n{'-' * 40}\n{seccion_lexica}\n\n"
                f"✗ ERROR SINTÁCTICO\n\n{error}"
            )
            self.estado.configure(text="Error sintáctico")
            return

        resultado = (
            f"ANÁLISIS LÉXICO\n{'-' * 40}\n{seccion_lexica}\n\n"
            f"ANÁLISIS SINTÁCTICO\n{'-' * 40}\n"
            "✓ Análisis sintáctico correcto\n\n"
            f"ÁRBOL AST\n{'-' * 40}\n{format_ast(arbol)}"
        )
        self._mostrar(resultado)
        self.estado.configure(text="Análisis correcto")

    @staticmethod
    def _formatear_tokens(tokens: list[Token]) -> str:
        filas: list[str] = []
        for token in tokens:
            valor = "" if token.tipo == TokenType.EOF else token.lexema
            filas.append(
                f"{token.tipo.name:<18} {valor:<24} "
                f"[línea {token.linea}, columna {token.columna}]"
            )
        return "\n".join(filas)

    def cargar_ejemplo(self) -> None:
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", CODIGO_EJEMPLO)
        self._mostrar("Presiona Analizar o Ctrl+Enter para procesar el ejemplo.")
        self.estado.configure(text="Ejemplo cargado")
        self.editor.focus_set()

    def limpiar(self) -> None:
        self.editor.delete("1.0", tk.END)
        self._mostrar("")
        self.estado.configure(text="Listo")
        self.editor.focus_set()

    def _mostrar(self, contenido: str) -> None:
        self.salida.configure(state=tk.NORMAL)
        self.salida.delete("1.0", tk.END)
        self.salida.insert("1.0", contenido)
        self.salida.configure(state=tk.DISABLED)
