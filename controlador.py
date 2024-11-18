import curses
from modelo import Paciente, Medico, Habitacion, Cama

def validar_rut(rut):
    """Valida el RUT chileno."""
    rut = rut.replace(".", "").replace("-", "")
    cuerpo = rut[:-1]
    dv = rut[-1].upper()

    try:
        cuerpo_int = int(cuerpo)
    except ValueError:
        return False

    suma = 0
    multiplicador = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 9 if multiplicador == 7 else multiplicador + 1

    calculado = 11 - (suma % 11)
    dv_calculado = "K" if calculado == 10 else "0" if calculado == 11 else str(calculado)

    return dv == dv_calculado

def crear_habitacion(base_datos, stdscr):
    """Crea una nueva habitación en la base de datos."""
    curses.echo()
    stdscr.clear()
    stdscr.addstr("Ingrese el nombre de la habitación: ")
    nombre = stdscr.getstr().decode('utf-8').strip()

    if not nombre:
        stdscr.addstr("Nombre inválido. El nombre no puede estar vacío.\n")
        stdscr.getch()
        return

    nombre = nombre.replace(" ", ".")

    stdscr.addstr("Ingrese el número de la habitación: ")
    numero = stdscr.getstr().decode('utf-8').strip()
    if not numero or not numero.isdigit():
        stdscr.addstr("Número inválido. Debe ser un número entero.\n")
        stdscr.getch()
        return

    # Construcción del ID de la habitación
    id_habitacion = f"{nombre}_{numero}"
    habitacion = Habitacion(id_habitacion, numero, nombre)
    habitacion.guardar(base_datos)

    stdscr.addstr(f"Habitación {id_habitacion} creada exitosamente.\n")
    stdscr.getch()

def mostrar_pacientes(base_datos, stdscr):
    """Muestra todos los pacientes registrados."""
    stdscr.clear()
    pacientes = Paciente.obtener_todos(base_datos)
    if not pacientes:
        stdscr.addstr("No hay pacientes registrados.\n")
        stdscr.getch()
        return

    stdscr.addstr(f"{'RUT':<15} {'Nombre':<20} {'Diagnóstico':<20} "
                  f"{'Médico Tratante':<20} {'Habitación':<10}\n")
    stdscr.addstr("-" * 85 + "\n")
    for paciente in pacientes:
        stdscr.addstr(f"{paciente['rut']:<15} {paciente['nombre']:<20} {paciente['diagnostico']:<20} "
                      f"{paciente['medico_tratante']:<20} {paciente['habitacion']:<10}\n")
    stdscr.addstr("\nPresione cualquier tecla para volver al menú.")
    stdscr.getch()

def mostrar_detalle_paciente(base_datos, stdscr):
    """Muestra el detalle de un paciente seleccionado por RUT."""
    stdscr.clear()
    pacientes = Paciente.obtener_todos(base_datos)
    if not pacientes:
        stdscr.addstr("No hay pacientes registrados.\n")
        stdscr.getch()
        return

    seleccionado = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione un paciente para ver los detalles:\n")
        for idx, paciente in enumerate(pacientes):
            if idx == seleccionado:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {paciente['rut']} - {paciente['nombre']}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {paciente['rut']} - {paciente['nombre']}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado = (seleccionado - 1) % len(pacientes)
        elif key == curses.KEY_DOWN:
            seleccionado = (seleccionado + 1) % len(pacientes)
        elif key == curses.KEY_RIGHT:
            paciente_seleccionado = pacientes[seleccionado]
            break
        elif key == curses.KEY_LEFT:
            return

    stdscr.clear()
    stdscr.addstr("Detalles del paciente:\n")
    stdscr.addstr(f"{'RUT':<15} {'Nombre':<20} {'Diagnóstico':<20} {'Médico Tratante':<20} "
                  f"{'Último Examen':<20} {'Habitación':<10} {'Cama':<10}\n")
    stdscr.addstr("-" * 115 + "\n")
    stdscr.addstr(f"{paciente_seleccionado['rut']:<15} {paciente_seleccionado['nombre']:<20} "
                  f"{paciente_seleccionado['diagnostico']:<20} {paciente_seleccionado['medico_tratante']:<20} "
                  f"{paciente_seleccionado['ultimo_examen']:<20} {paciente_seleccionado['habitacion']:<10} "
                  f"{paciente_seleccionado['cama']:<10}\n")
    stdscr.addstr("\nPresione cualquier tecla para volver al menú.")
    stdscr.getch()

def cambiar_cama_paciente(base_datos, stdscr):
    """Cambia la cama asignada a un paciente."""
    stdscr.clear()
    pacientes = Paciente.obtener_todos(base_datos)
    if not pacientes:
        stdscr.addstr("No hay pacientes disponibles.\n")
        stdscr.getch()
        return

    seleccionado_paciente = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione un paciente para cambiar la cama:\n")
        for idx, paciente in enumerate(pacientes):
            if idx == seleccionado_paciente:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {paciente['rut']} - {paciente['nombre']}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {paciente['rut']} - {paciente['nombre']}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado_paciente = (seleccionado_paciente - 1) % len(pacientes)
        elif key == curses.KEY_DOWN:
            seleccionado_paciente = (seleccionado_paciente + 1) % len(pacientes)
        elif key == curses.KEY_RIGHT:
            paciente_seleccionado = pacientes[seleccionado_paciente]
            break
        elif key == curses.KEY_LEFT:
            return

    camas_disponibles = Cama.obtener_disponibles(base_datos)
    if not camas_disponibles:
        stdscr.addstr("No hay camas disponibles.\n")
        stdscr.getch()
        return

    seleccionado_cama = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione una cama disponible para asignar al paciente:\n")
        for idx, cama in enumerate(camas_disponibles):
            # Obtener el tamaño de la ventana
            height, width = stdscr.getmaxyx()

            # Formatear la cadena de manera segura
            linea = f"  Cama ID: {cama['id_cama']} - Habitación: {cama['habitacion']}"
            if len(linea) > width - 1:
                linea = linea[:width - 4] + "..."

            if idx == seleccionado_cama:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {linea}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {linea}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado_cama = (seleccionado_cama - 1) % len(camas_disponibles)
        elif key == curses.KEY_DOWN:
            seleccionado_cama = (seleccionado_cama + 1) % len(camas_disponibles)
        elif key == curses.KEY_RIGHT:
            cama_seleccionada = camas_disponibles[seleccionado_cama]
            break
        elif key == curses.KEY_LEFT:
            return

    # Liberar la cama anterior
    if paciente_seleccionado.get("cama"):
        Cama.actualizar(base_datos, paciente_seleccionado["cama"], {"ocupada": False, "paciente": None})

    # Actualizar el paciente
    Paciente.actualizar(base_datos, paciente_seleccionado["rut"], {
        "cama": cama_seleccionada["id_cama"],
        "habitacion": cama_seleccionada["habitacion"]
    })

    # Ocupar la nueva cama
    Cama.actualizar(base_datos, cama_seleccionada["id_cama"], {"ocupada": True, "paciente": paciente_seleccionado["rut"]})

    stdscr.addstr(f"La cama del paciente {paciente_seleccionado['nombre']} ha sido cambiada exitosamente a la cama "
                  f"{cama_seleccionada['id_cama']} en la habitación {cama_seleccionada['habitacion']}.\n")
    stdscr.getch()

def cambiar_medico_paciente(base_datos, stdscr):
    """Cambia el médico tratante de un paciente."""
    stdscr.clear()
    pacientes = Paciente.obtener_todos(base_datos)
    if not pacientes:
        stdscr.addstr("No hay pacientes disponibles.\n")
        stdscr.getch()
        return

    seleccionado_paciente = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione un paciente para cambiar el médico tratante:\n")
        for idx, paciente in enumerate(pacientes):
            if idx == seleccionado_paciente:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {paciente['rut']} - {paciente['nombre']}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {paciente['rut']} - {paciente['nombre']}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado_paciente = (seleccionado_paciente - 1) % len(pacientes)
        elif key == curses.KEY_DOWN:
            seleccionado_paciente = (seleccionado_paciente + 1) % len(pacientes)
        elif key == curses.KEY_RIGHT:
            paciente_seleccionado = pacientes[seleccionado_paciente]
            break
        elif key == curses.KEY_LEFT:
            return

    medicos = Medico.obtener_todos(base_datos)
    if not medicos:
        stdscr.addstr("No hay médicos disponibles para asignar.\n")
        stdscr.getch()
        return

    seleccionado_medico = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione un nuevo médico tratante para el paciente:\n")
        for idx, medico in enumerate(medicos):
            if idx == seleccionado_medico:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {medico['nombre']} - {medico['especialidad']}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {medico['nombre']} - {medico['especialidad']}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado_medico = (seleccionado_medico - 1) % len(medicos)
        elif key == curses.KEY_DOWN:
            seleccionado_medico = (seleccionado_medico + 1) % len(medicos)
        elif key == curses.KEY_RIGHT:
            medico_seleccionado = medicos[seleccionado_medico]
            break
        elif key == curses.KEY_LEFT:
            return

    # Actualizar el médico en la base de datos
    Paciente.actualizar(base_datos, paciente_seleccionado["rut"], {
        "medico_tratante": medico_seleccionado["nombre"]
    })

    stdscr.addstr(f"El médico del paciente {paciente_seleccionado['nombre']} ha sido cambiado exitosamente a "
                  f"{medico_seleccionado['nombre']}.\n")
    stdscr.getch()

def crear_cama_y_asignar(base_datos, stdscr):
    """Crea nuevas camas y las asigna a una habitación existente."""
    stdscr.clear()
    habitaciones = Habitacion.obtener_todas(base_datos)
    if not habitaciones:
        stdscr.addstr("No hay habitaciones disponibles.\n")
        stdscr.getch()
        return

    seleccionado_habitacion = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione una habitación para asignar las camas:\n")
        for idx, habitacion in enumerate(habitaciones):
            if idx == seleccionado_habitacion:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> Habitación {habitacion['numero']} (ID: {habitacion['id_habitacion']})\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  Habitación {habitacion['numero']} (ID: {habitacion['id_habitacion']})\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado_habitacion = (seleccionado_habitacion - 1) % len(habitaciones)
        elif key == curses.KEY_DOWN:
            seleccionado_habitacion = (seleccionado_habitacion + 1) % len(habitaciones)
        elif key == curses.KEY_RIGHT:
            habitacion_seleccionada = habitaciones[seleccionado_habitacion]
            break
        elif key == curses.KEY_LEFT:
            return

    curses.echo()
    try:
        stdscr.addstr("¿Cuántas camas desea agregar? ")
        num_camas = int(stdscr.getstr().decode('utf-8'))
        if num_camas < 1:
            stdscr.addstr("El número de camas debe ser un número positivo.\n")
            stdscr.getch()
            return
    except ValueError:
        stdscr.addstr("Entrada no válida. Ingrese un número entero.\n")
        stdscr.getch()
        return

    id_habitacion = habitacion_seleccionada['id_habitacion']
    numero_habitacion = habitacion_seleccionada['numero']
    camas_creadas = []

    for i in range(1, num_camas + 1):
        id_cama = f"{numero_habitacion}{str(i).zfill(2)}"
        cama = Cama(id_cama, id_habitacion)
        cama.guardar(base_datos)
        camas_creadas.append(id_cama)

    stdscr.addstr("Camas creadas y asignadas a la habitación:\n")
    for cama_id in camas_creadas:
        stdscr.addstr(f"- Cama ID: {cama_id}\n")
    stdscr.getch()

def agregar_paciente(base_datos, stdscr):
    """Agrega un nuevo paciente al sistema."""
    stdscr.clear()
    medicos = Medico.obtener_todos(base_datos)
    if not medicos:
        stdscr.addstr("No hay médicos disponibles.\n")
        stdscr.getch()
        return

    seleccionado_medico = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Seleccione un médico tratante:\n")
        for idx, medico in enumerate(medicos):
            if idx == seleccionado_medico:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"> {medico['nombre']} - {medico['especialidad']}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"  {medico['nombre']} - {medico['especialidad']}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            seleccionado_medico = (seleccionado_medico - 1) % len(medicos)
        elif key == curses.KEY_DOWN:
            seleccionado_medico = (seleccionado_medico + 1) % len(medicos)
        elif key == curses.KEY_RIGHT:
            medico_tratante = medicos[seleccionado_medico]['nombre']
            break
        elif key == curses.KEY_LEFT:
            return

    # Obtención de una cama disponible desde MongoDB
    cama_disponible = base_datos.camas.find_one({"ocupada": False})
    if not cama_disponible:
        stdscr.addstr("No hay camas disponibles.\n")
        stdscr.getch()
        return

    curses.echo()
    stdscr.addstr("Ingrese el RUT del paciente: ")
    rut = stdscr.getstr().decode('utf-8').strip()
    stdscr.addstr("Ingrese el nombre del paciente: ")
    nombre = stdscr.getstr().decode('utf-8').strip()
    stdscr.addstr("Ingrese el diagnóstico inicial: ")
    diagnostico = stdscr.getstr().decode('utf-8').strip()
    stdscr.addstr("Ingrese el nombre del último examen realizado: ")
    ultimo_examen = stdscr.getstr().decode('utf-8').strip()

    paciente = {
        "rut": rut,
        "nombre": nombre,
        "diagnostico": diagnostico,
        "medico_tratante": medico_tratante,
        "habitacion": cama_disponible['habitacion'],
        "cama": cama_disponible['id_cama'],
        "ultimo_examen": ultimo_examen
    }
    # Inserción del paciente en MongoDB
    base_datos.pacientes.insert_one(paciente)
    stdscr.addstr(f"Paciente {nombre} agregado exitosamente.\n")

    # Actualización de la cama en MongoDB
    base_datos.camas.update_one(
        {"id_cama": cama_disponible['id_cama']},
        {"$set": {"ocupada": True, "paciente": rut}}
    )
    stdscr.getch()

def agregar_medico(base_datos, stdscr):
    """Agrega un nuevo médico al sistema."""
    while True:
        stdscr.clear()
        curses.echo()
        stdscr.addstr("Ingrese el nombre del médico: ")
        nombre = stdscr.getstr().decode('utf-8').strip()
        stdscr.addstr("Ingrese el RUT del médico: ")
        rut = stdscr.getstr().decode('utf-8').strip()
        stdscr.addstr("Ingrese la especialidad del médico: ")
        especialidad = stdscr.getstr().decode('utf-8').strip()

        medico = Medico(id_medico=rut, nombre=nombre, especialidad=especialidad)
        medico.guardar(base_datos)

        stdscr.addstr(f"Médico {nombre} agregado exitosamente.\n")

        stdscr.addstr("¿Desea agregar otro médico? (S/N): ")
        continuar = stdscr.getstr().decode('utf-8').strip().upper()
        if continuar != "S":
            break
