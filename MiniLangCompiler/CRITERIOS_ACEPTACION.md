# Criterios de aceptación — MiniLang Compiler

| ID | Criterio | Resultado esperado |
|---|---|---|
| CA-01 | Recibir código fuente | El editor acepta código escrito en MiniLang. |
| CA-02 | Analizar identificadores | El lexer reconoce nombres de variables como `IDENTIFICADOR`. |
| CA-03 | Analizar números | El lexer reconoce enteros y decimales como un único token `NUMERO`. |
| CA-04 | Analizar cadenas | El lexer reconoce texto entre comillas dobles como `CADENA`. |
| CA-05 | Analizar operadores aritméticos | Reconoce `+`, `-`, `*` y `/`. |
| CA-06 | Analizar operadores de comparación | Reconoce `==`, `!=`, `>`, `<`, `>=` y `<=`. |
| CA-07 | Analizar símbolos | Reconoce paréntesis, llaves y punto y coma. |
| CA-08 | Ignorar comentarios | Los comentarios de una línea que empiezan con `//` no generan tokens. |
| CA-09 | Detectar error léxico | Informa el carácter inválido, la línea y la columna. |
| CA-10 | Ejecutar parser | Valida asignaciones y condicionales mediante descenso recursivo. |
| CA-11 | Respetar precedencia | Multiplicación y división tienen prioridad sobre suma y resta. |
| CA-12 | Detectar error sintáctico | Informa línea, columna, elemento esperado y elemento encontrado. |
| CA-13 | Generar AST | Representa programas, asignaciones, operaciones, literales, variables y condicionales. |
| CA-14 | Mostrar resultados | La interfaz presenta tokens, validación sintáctica y árbol AST. |
| CA-15 | Cargar ejemplo | El botón **Ejemplo** coloca un programa válido en el editor. |
| CA-16 | Limpiar interfaz | El botón **Limpiar** borra el editor y el resultado. |
| CA-17 | Ejecutar pruebas | `pytest` ejecuta correctamente toda la suite. |
| CA-18 | Ejecutar aplicación | `python main.py` abre la ventana **MiniLang Compiler**. |
| CA-19 | Mantener modularidad | Lexer, parser, AST, errores e interfaz están separados en paquetes. |
| CA-20 | Incluir ejemplos | El proyecto contiene un programa correcto y otro incorrecto. |
