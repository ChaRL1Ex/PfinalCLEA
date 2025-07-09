from tinydb import TinyDB, Query
import os

# Ruta de la base de datos (puedes cambiarla si lo deseas)
db_path = os.path.join(os.path.dirname(__file__), 'red_usuarios_db.json')
db = TinyDB(db_path)

# Tablas
usuarios_table = db.table('usuarios')
conexiones_table = db.table('conexiones')

# Funciones básicas para usuarios
def agregar_usuario(usuario):
    """usuario debe ser un dict con campos: id, nombre, intereses (lista)"""
    if not usuario.get('id') or not usuario.get('nombre'):
        return {'ok': False, 'error': 'Faltan campos obligatorios (id, nombre)'}
    Usuario = Query()
    if usuarios_table.contains(Usuario.id == usuario['id']):
        return {'ok': False, 'error': 'El usuario con ese ID ya existe'}
    return {'ok': True, 'id': usuarios_table.insert(usuario)}

def editar_usuario(id_usuario, nuevos_datos):
    """nuevos_datos es un dict con los campos a actualizar"""
    Usuario = Query()
    if not usuarios_table.contains(Usuario.id == id_usuario):
        return {'ok': False, 'error': 'Usuario no encontrado'}
    usuarios_table.update(nuevos_datos, Usuario.id == id_usuario)
    return {'ok': True}

def obtener_usuario(id_usuario):
    Usuario = Query()
    usuario = usuarios_table.get(Usuario.id == id_usuario)
    if usuario:
        return {'ok': True, 'usuario': usuario}
    else:
        return {'ok': False, 'error': 'Usuario no encontrado'}

def obtener_todos_usuarios():
    return usuarios_table.all()

# Funciones básicas para conexiones
def agregar_conexion(conexion):
    """conexion debe ser un dict con campos: id1, id2 (IDs de usuarios conectados)"""
    if not conexion.get('id1') or not conexion.get('id2'):
        return {'ok': False, 'error': 'Faltan campos obligatorios (id1, id2)'}
    if conexion['id1'] == conexion['id2']:
        return {'ok': False, 'error': 'No se puede conectar un usuario consigo mismo'}
    Usuario = Query()
    # Comparar como str para evitar problemas de tipo
    usuarios = usuarios_table.all()
    ids_existentes = set(str(u['id']) for u in usuarios)
    if str(conexion['id1']) not in ids_existentes or str(conexion['id2']) not in ids_existentes:
        return {'ok': False, 'error': 'Uno o ambos usuarios no existen'}
    Conexion = Query()
    if conexiones_table.contains((Conexion.id1 == conexion['id1']) & (Conexion.id2 == conexion['id2'])) or \
        conexiones_table.contains((Conexion.id1 == conexion['id2']) & (Conexion.id2 == conexion['id1'])):
        return {'ok': False, 'error': 'La conexión ya existe'}
    return {'ok': True, 'id': conexiones_table.insert(conexion)}

def editar_conexion(id1, id2, nuevos_datos):
    Conexion = Query()
    if not (conexiones_table.contains((Conexion.id1 == id1) & (Conexion.id2 == id2)) or \
            conexiones_table.contains((Conexion.id1 == id2) & (Conexion.id2 == id1))):
        return {'ok': False, 'error': 'Conexión no encontrada'}
    conexiones_table.update(nuevos_datos, ((Conexion.id1 == id1) & (Conexion.id2 == id2)) | ((Conexion.id1 == id2) & (Conexion.id2 == id1)))
    return {'ok': True}

def obtener_conexion(id1, id2):
    Conexion = Query()
    conexion = conexiones_table.get(((Conexion.id1 == id1) & (Conexion.id2 == id2)) | ((Conexion.id1 == id2) & (Conexion.id2 == id1)))
    if conexion:
        return {'ok': True, 'conexion': conexion}
    else:
        return {'ok': False, 'error': 'Conexión no encontrada'}

def obtener_todas_conexiones():
    return conexiones_table.all()
