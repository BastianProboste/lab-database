
# Proyecto: Lab04 - Biblioteca

Este repositorio contiene el código necesario para trabajar con la base de datos **Lab04Biblioteca**, diseñada para gestionar colecciones y documentos relacionados con un laboratorio de biblioteca. A continuación, se describen las instrucciones para configurar el entorno y ejecutar el proyecto.

---

## 📂 Conexión a la Base de Datos

La base de datos está alojada en un clúster de MongoDB Atlas. A continuación, se muestra la URI de conexión:

```
mongodb+srv://borispuentes:UTNHhGYonlO9gtuA@cluster0.vr57f.mongodb.net/Lab04Biblioteca?retryWrites=true&w=majority&appName=Cluster0
```

Esta conexión permite acceder directamente a la base de datos `Lab04Biblioteca`, que contiene todas las colecciones y documentos necesarios para este laboratorio. 

> **Nota:** El código está preparado para desplegarse sin necesidad de modificar esta URI de conexión.

---

## ⚙️ Configuración del Entorno

Siga los pasos a continuación para configurar el entorno y ejecutar el proyecto:

1. **Crear y activar un entorno virtual con Conda:**
   ```bash
   conda create -n database python=3.9
   conda activate database
   ```

2. **Instalar las dependencias necesarias:**
   ```bash
   pip install windows-curses
   pip install pymongo
   ```

3. **Clonar este repositorio y acceder a la carpeta del código:**
   ```bash
   cd "ruta_del_codigo"
   ```

4. **Ejecutar el proyecto:**
   ```bash
   python main.py
   ```

---

## 🛠️ Requisitos del Sistema

- **Python:** Versión 3.9
- **Administrador de paquetes:** Conda y pip
- **Sistema operativo:** Windows

---

## 📝 Notas Adicionales

- Este proyecto está configurado para ejecutarse directamente, siempre que las credenciales de la base de datos sean válidas.
- Las credenciales vienen integradas en el codigo.

---

