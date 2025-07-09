from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QColor
from View.GuiMain import GuiMain
from controlers.Crud import mostrar_add_user_gui, mostrar_edit_user_gui, mostrar_delete_user_gui, list_users, get_user
from tinydb import where
import sys
from View.SetConexionGUI import SetConexionGUI
from controlers.Database import obtener_todas_conexiones
from View.DelConecGUI import DelConecGUI
from View.ViewRedGUI import ViewRedGUI
from View.ComunityGUI import ComunityGUI

class MainApp(GuiMain):
    def __init__(self):
        super().__init__()
        self.conectar_botones()
        self.actualizar_tabla()

    def conectar_botones(self):
        self.btn_agregar.clicked.connect(self.agregar_usuario)
        self.btn_editar.clicked.connect(self.editar_usuario)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        self.btn_establecer.clicked.connect(self.establecer_conexion)
        self.btn_eliminar_con.clicked.connect(self.eliminar_conexion)
        self.btn_visualizar.clicked.connect(self.visualizar_red)
        self.btn_calcular_distancia.clicked.connect(self.calcular_distancia)
        self.btn_comunidades.clicked.connect(self.mostrar_comunidades)

    def agregar_usuario(self):
        mostrar_add_user_gui()
        self.actualizar_tabla()

    def editar_usuario(self):
        mostrar_edit_user_gui()
        self.actualizar_tabla()

    def eliminar_usuario(self):
        mostrar_delete_user_gui()
        self.actualizar_tabla()

    def establecer_conexion(self):
        ventana = SetConexionGUI()
        ventana.exec_()
        self.actualizar_tabla()

    def eliminar_conexion(self):
        ventana = DelConecGUI()
        ventana.exec_()
        self.actualizar_tabla()

    def visualizar_red(self):
        ventana = ViewRedGUI()
        ventana.exec_()

    def calcular_distancia(self):
        from View.DistanceCalcGUI import DistanceCalcGUI
        ventana = DistanceCalcGUI()
        ventana.exec_()

    def mostrar_comunidades(self):
        ventana = ComunityGUI()
        ventana.exec_()

    def actualizar_tabla(self):
        self.table.setRowCount(0)
        usuarios = list_users()
        conexiones = obtener_todas_conexiones()
        for usuario in usuarios:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Calcular conexiones
            id_usuario = str(usuario.get('id', ''))
            total_conex = sum(1 for c in conexiones if str(c.get('id1')) == id_usuario or str(c.get('id2')) == id_usuario)
            
            # Crear items de tabla
            item_id = self._item(str(usuario.get('id', '')))
            item_nombre = self._item(usuario.get('nombre', ''))
            item_intereses = self._item(', '.join(usuario.get('intereses', [])))
            item_conexiones = self._item(str(total_conex))
            
            # Aplicar colores según el número de conexiones
            if total_conex >= 15:  # Influencer (rojo)
                color_fondo = QColor(255, 200, 200)  # Rojo claro
                for item in [item_id, item_nombre, item_intereses, item_conexiones]:
                    item.setBackground(color_fondo)
            elif total_conex >= 4:  # Usuario influyente (verde)
                color_fondo = QColor(200, 255, 200)  # Verde claro
                for item in [item_id, item_nombre, item_intereses, item_conexiones]:
                    item.setBackground(color_fondo)
            
            # Insertar items en la tabla
            self.table.setItem(row, 0, item_id)
            self.table.setItem(row, 1, item_nombre)
            self.table.setItem(row, 2, item_intereses)
            self.table.setItem(row, 3, item_conexiones)

    def _item(self, text):
        return QTableWidgetItem(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
