import curses
from menu import menu_principal
from conexion import conectar_mongodb


def main(stdscr):
    """Función principal que inicia el programa."""
    base_datos = conectar_mongodb()
    if base_datos is not None:
        menu_principal(base_datos, stdscr)
    else:
        stdscr.addstr("No se pudo establecer la conexión con la base de datos.\n")
        stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
