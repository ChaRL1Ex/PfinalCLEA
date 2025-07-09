from View.AddUserGui import AddUserGui
from View.EditUserGUI import EditUserGui
from View.DeleteUserGui import DeleteUserGui
from controlers.Database import agregar_usuario, editar_usuario, obtener_usuario, obtener_todos_usuarios, usuarios_table, conexiones_table, obtener_todas_conexiones
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from tinydb import where

# Obtener el siguiente ID disponible (el mayor + 1)
def id_disponible():
    usuarios = obtener_todos_usuarios()
    if not usuarios:
        return 1
    ids = [int(u['id']) for u in usuarios if str(u['id']).isdigit()]
    return max(ids) + 1 if ids else 1

# Crear usuario desde GUI
def mostrar_add_user_gui():
    app = QApplication.instance() or QApplication(sys.argv)
    id_disp = id_disponible()
    ventana = AddUserGui(id_disp)
    if ventana.exec_() == 1:
        nombre = ventana.input_nombre.text()
        intereses = ventana.get_intereses()
        res = agregar_usuario({'id': id_disp, 'nombre': nombre, 'intereses': intereses})
        if not res['ok']:
            QMessageBox.warning(ventana, 'Error', str(res['error']))
        else:
            QMessageBox.information(ventana, 'Éxito', 'Usuario agregado correctamente')
    ventana.close()

# Editar usuario desde GUI
def mostrar_edit_user_gui():
    app = QApplication.instance() or QApplication(sys.argv)
    ventana = EditUserGui()
    if ventana.exec_() == 1:
        id_usuario = ventana.combo_id.currentText()
        # Forzar tipo correcto para TinyDB
        if id_usuario.isdigit():
            id_usuario = int(id_usuario)
        nombre = ventana.input_nombre.text()
        intereses = ventana.get_intereses()
        res = editar_usuario(id_usuario, {'nombre': nombre, 'intereses': intereses})
        if not res['ok']:
            QMessageBox.warning(ventana, 'Error', str(res['error']))
        else:
            QMessageBox.information(ventana, 'Éxito', 'Usuario editado correctamente')
    ventana.close()

# Obtener usuario por ID
def get_user(id_usuario):
    return obtener_usuario(id_usuario)

# Listar todos los usuarios
def list_users():
    return obtener_todos_usuarios()

def mostrar_delete_user_gui():
    app = QApplication.instance() or QApplication(sys.argv)
    ventana = DeleteUserGui()
    if ventana.exec_() == 1:
        id_usuario = ventana.combo_id.currentText()
        # Forzar tipo correcto para TinyDB
        if id_usuario.isdigit():
            id_usuario = int(id_usuario)
        # Eliminar usuario
        usuarios_table.remove(where('id') == id_usuario)
        # Eliminar conexiones asociadas
        conexiones = obtener_todas_conexiones()
        for c in conexiones:
            if str(c.get('id1')) == str(id_usuario) or str(c.get('id2')) == str(id_usuario):
                conexiones_table.remove(doc_ids=[c.doc_id])
        QMessageBox.information(ventana, 'Éxito', f'Usuario {id_usuario} y sus conexiones eliminados correctamente')
    ventana.close()


