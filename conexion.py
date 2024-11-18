from pymongo import MongoClient

def conectar_mongodb():
    """Establece la conexión con la base de datos MongoDB."""
    try:
        uri = "mongodb+srv://borispuentes:UTNHhGYonlO9gtuA@cluster0.vr57f.mongodb.net"
        cliente = MongoClient(uri)
        base_datos = cliente["Lab04Biblioteca"]
        return base_datos
    except Exception:
        return None
