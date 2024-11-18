import curses
from controlador import (
    crear_habitacion,
    crear_cama_y_asignar,
    agregar_paciente,
    agregar_medico,
    mostrar_pacientes,
    mostrar_detalle_paciente,
    cambiar_cama_paciente,
    cambiar_medico_paciente,
)
from conexion import conectar_mongodb


def menu_principal(base_datos, stdscr):
    """Despliega el menú principal del sistema."""
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    opciones = [
        "Mostrar todos los pacientes",
        "Mostrar detalle de un paciente por RUT",
        "Cambiar cama de un paciente",
        "Cambiar médico de un paciente",
        "Crear habitación",
        "Crear cama y asignar a habitación",
        "Agregar paciente",
        "Agregar médico",
        "Salir"
    ]
    seleccionado = 0

    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, "=== Sistema de Gestión Clínica ===\n")
        for idx, opcion in enumerate(opciones):
            if idx == seleccionado:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {opcion}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {opcion}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado = (seleccionado - 1) % len(opciones)
        elif key == curses.KEY_DOWN:
            seleccionado = (seleccionado + 1) % len(opciones)
        elif key in (curses.KEY_RIGHT, ord('\n')):  # Seleccionar opción
            if opciones[seleccionado] == "Mostrar todos los pacientes":
                mostrar_pacientes(base_datos, stdscr)
            elif opciones[seleccionado] == "Mostrar detalle de un paciente por RUT":
                mostrar_detalle_paciente(base_datos, stdscr)
            elif opciones[seleccionado] == "Cambiar cama de un paciente":
                cambiar_cama_paciente(base_datos, stdscr)
            elif opciones[seleccionado] == "Cambiar médico de un paciente":
                cambiar_medico_paciente(base_datos, stdscr)
            elif opciones[seleccionado] == "Crear habitación":
                crear_habitacion(base_datos, stdscr)
            elif opciones[seleccionado] == "Crear cama y asignar a habitación":
                crear_cama_y_asignar(base_datos, stdscr)
            elif opciones[seleccionado] == "Agregar paciente":
                agregar_paciente(base_datos, stdscr)
            elif opciones[seleccionado] == "Agregar médico":
                agregar_medico(base_datos, stdscr)
            elif opciones[seleccionado] == "Salir":
                break
        elif key == curses.KEY_LEFT:  # Salir del menú
            break
