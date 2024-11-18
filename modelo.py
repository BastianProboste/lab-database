from pymongo.collection import Collection

class Paciente:
    """Clase que representa a un paciente."""

    def __init__(self, rut, nombre, diagnostico, medico_tratante, habitacion, cama, ultimo_examen):
        self.rut = rut
        self.nombre = nombre
        self.diagnostico = diagnostico
        self.medico_tratante = medico_tratante
        self.habitacion = habitacion
        self.cama = cama
        self.ultimo_examen = ultimo_examen

    @staticmethod
    def obtener_todos(base_datos):
        """Obtiene todos los pacientes de la base de datos."""
        return list(base_datos.pacientes.find())

    @staticmethod
    def obtener_por_rut(base_datos, rut):
        """Obtiene un paciente por su RUT."""
        return base_datos.pacientes.find_one({"rut": rut})

    def guardar(self, base_datos):
        """Guarda el paciente en la base de datos."""
        base_datos.pacientes.insert_one(self.__dict__)

    @staticmethod
    def actualizar(base_datos, rut, campos):
        """Actualiza los campos de un paciente."""
        base_datos.pacientes.update_one({"rut": rut}, {"$set": campos})


class Medico:
    """Clase que representa a un médico."""

    def __init__(self, id_medico, nombre, especialidad):
        self.id_medico = id_medico
        self.nombre = nombre
        self.especialidad = especialidad

    @staticmethod
    def obtener_todos(base_datos):
        """Obtiene todos los médicos de la base de datos."""
        return list(base_datos.medicos.find())

    def guardar(self, base_datos):
        """Guarda el médico en la base de datos."""
        base_datos.medicos.insert_one(self.__dict__)

    @staticmethod
    def obtener_por_nombre(base_datos, nombre):
        """Obtiene un médico por su nombre."""
        return base_datos.medicos.find_one({"nombre": nombre})


class Habitacion:
    """Clase que representa una habitación."""

    def __init__(self, id_habitacion, numero, nombre):
        self.id_habitacion = id_habitacion
        self.numero = numero
        self.nombre = nombre

    @staticmethod
    def obtener_todas(base_datos):
        """Obtiene todas las habitaciones de la base de datos."""
        return list(base_datos.habitaciones.find())

    def guardar(self, base_datos):
        """Guarda la habitación en la base de datos."""
        base_datos.habitaciones.insert_one(self.__dict__)


class Cama:
    """Clase que representa una cama."""

    def __init__(self, id_cama, habitacion, ocupada=False, paciente=None):
        self.id_cama = id_cama
        self.habitacion = habitacion
        self.ocupada = ocupada
        self.paciente = paciente

    @staticmethod
    def obtener_disponibles(base_datos):
        """Obtiene todas las camas disponibles."""
        return list(base_datos.camas.find({"ocupada": False}))

    @staticmethod
    def obtener_por_id(base_datos, id_cama):
        """Obtiene una cama por su ID."""
        return base_datos.camas.find_one({"id_cama": id_cama})

    def guardar(self, base_datos):
        """Guarda la cama en la base de datos."""
        base_datos.camas.insert_one(self.__dict__)

    @staticmethod
    def actualizar(base_datos, id_cama, campos):
        """Actualiza los campos de una cama."""
        base_datos.camas.update_one({"id_cama": id_cama}, {"$set": campos})
