# MiniLang Compiler

Aplicación educativa que implementa las primeras etapas de un compilador para un lenguaje pequeño llamado **MiniLang**. Recibe código fuente, realiza análisis léxico y sintáctico, detecta errores con ubicación exacta y construye un árbol de sintaxis abstracta (AST).

## Objetivo

Demostrar de forma clara y funcional cómo un código fuente se transforma primero en tokens y después en una estructura sintáctica, mediante un lexer manual y un parser descendente recursivo.

## Características

- Identificadores y palabra reservada `si`.
- Números enteros y decimales.
- Cadenas entre comillas dobles.
- Operadores aritméticos y de comparación.
- Comentarios de una línea con `//`.
- Asignaciones y condicionales, incluidos condicionales anidados.
- Errores léxicos y sintácticos con línea y columna.
- AST para representar la estructura reconocida.
- Interfaz gráfica sencilla desarrollada con Tkinter.
- Suite independiente de pruebas con pytest.

## Tecnologías

- Python 3.10 o superior.
- Tkinter, incluido normalmente con Python.
- pytest, únicamente para las pruebas.

## Arquitectura

```text
Código fuente
     ↓
   Lexer
     ↓
   Tokens
     ↓
   Parser
     ↓
    AST
```

El **lexer** recorre cada carácter y crea tokens. El **parser** consume esos tokens, comprueba la gramática con descenso recursivo y crea los nodos del **AST**. La interfaz coordina el proceso y presenta sus resultados.

## Estructura del proyecto

```text
MiniLangCompiler/
├── main.py
├── README.md
├── CRITERIOS_ACEPTACION.md
├── requirements.txt
├── .gitignore
├── compiler/
│   ├── lexer/
│   │   ├── lexer.py
│   │   ├── token.py
│   │   └── token_type.py
│   ├── parser/
│   │   └── parser.py
│   ├── ast/
│   │   └── nodes.py
│   └── errors/
│       └── exceptions.py
├── ui/
│   └── compiler_window.py
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_ast.py
└── examples/
    ├── correcto.min
    └── incorrecto.min
```

Todos los paquetes incluyen su archivo `__init__.py`.

## Gramática final

```bnf
programa       → sentencia* EOF

sentencia      → asignacion
               | condicional

asignacion     → IDENTIFICADOR "=" expresion ";"

condicional    → "si" "(" condicion ")" "{" sentencia* "}"

condicion      → expresion operador_comparacion expresion

operador_comparacion
               → "==" | "!=" | ">" | "<" | ">=" | "<="

expresion      → termino (("+" | "-") termino)*

termino        → factor (("*" | "/") factor)*

factor         → NUMERO
               | CADENA
               | IDENTIFICADOR
               | "(" expresion ")"
```

La regla de `término` concede mayor precedencia a multiplicación y división que a suma y resta.

## Ejemplo de código

```minilang
x = 10;
y = 20;
resultado = x + y;

si (resultado > 20) {
    mensaje = "Resultado mayor que 20";
}
```

## Ejemplo de tokens

Para `x = 10 + 5;` se obtiene:

```text
IDENTIFICADOR    x
ASIGNACION       =
NUMERO           10
SUMA             +
NUMERO           5
PUNTO_COMA       ;
EOF
```

## Ejemplo de error léxico

Para `x = 10 @ 5;`:

```text
Error léxico en línea 1, columna 8:
Carácter no reconocido: '@'
```

## Ejemplo de error sintáctico

Para `x 10;`:

```text
Error sintáctico en línea 1, columna 3:
Toda asignación debe incluir el operador '='.
Se esperaba: '=' después del identificador.
Se encontró: '10' (NUMERO).
```

## Instalación

1. Comprueba la versión de Python:

   ```bash
   python --version
   ```

2. Opcionalmente, crea y activa un entorno virtual.

3. Instala la dependencia de pruebas:

   ```bash
   pip install -r requirements.txt
   ```

> En algunas distribuciones Linux, Tkinter se instala desde el gestor del sistema, por ejemplo con el paquete `python3-tk`. No se incluye en `requirements.txt` porque no es un paquete de pip.

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

La ventana incluye los botones **Analizar**, **Ejemplo** y **Limpiar**. También puede iniciarse el análisis con `Ctrl+Enter`.

## Pruebas

Ejecuta:

```bash
pytest
```

Resultado esperado:

```text
============================= 25 passed =============================
```

Las pruebas cubren el lexer, el parser, la precedencia de operadores, los mensajes de error y la estructura del AST.
