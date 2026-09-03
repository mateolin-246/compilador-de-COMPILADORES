"""Punto de entrada de la aplicación MiniLang Compiler."""

import tkinter as tk

from ui.compiler_window import CompilerWindow


def main() -> None:
    root = tk.Tk()
    CompilerWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
