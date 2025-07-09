from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controlers.Database import obtener_todos_usuarios, obtener_todas_conexiones

class DelConecGUI(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general
    color6 = '#ffffff'  # Texto blanco
    color7 = '#c97c7c'  # Botón eliminar
    color8 = '#a85a5a'  # Hover eliminar

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Eliminar Conexión')
        self.setMinimumSize(900, 500)
        self.setStyleSheet(f'background-color: {self.color5};')
        self.usuarios = []
        self.conexiones = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título
        titulo = QLabel('Eliminar Conexión')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont('Arial', 20, QFont.Bold))
        titulo.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(titulo)

        # Layout principal
        main_layout = QHBoxLayout()
        layout.addLayout(main_layout)

        # Columna izquierda (ID, Nombre, Intereses)
        col_izq = QVBoxLayout()
        main_layout.addLayout(col_izq)

        # ID
        label_id = QLabel('ID:')
        label_id.setStyleSheet(f'color: {self.color1}; background: none;')
        col_izq.addWidget(label_id)
        self.combo_id = QComboBox()
        self.combo_id.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color6}; padding: 6px;')
        col_izq.addWidget(self.combo_id)
        self.combo_id.currentIndexChanged.connect(self.on_id_selected)

        # Nombre
        label_nombre = QLabel('Nombre:')
        label_nombre.setStyleSheet(f'color: {self.color1}; background: none;')
        col_izq.addWidget(label_nombre)
        self.input_nombre = QLineEdit()
        self.input_nombre.setReadOnly(True)
        self.input_nombre.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color6}; padding: 6px;')
        col_izq.addWidget(self.input_nombre)

        # Intereses
        label_intereses = QLabel('Intereses')
        label_intereses.setStyleSheet(f'color: {self.color1}; background: none;')
        col_izq.addWidget(label_intereses)
        self.lista_intereses = QListWidget()
        self.lista_intereses.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color6};')
        self.lista_intereses.setMinimumHeight(120)
        col_izq.addWidget(self.lista_intereses)

        # Columna derecha (Conexiones)
        col_der = QVBoxLayout()
        main_layout.addLayout(col_der)

        label_conex = QLabel('Conexiones')
        label_conex.setStyleSheet(f'color: {self.color1}; background: none;')
        col_der.addWidget(label_conex)
        self.lista_conex = QListWidget()
        self.lista_conex.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color6};')
        self.lista_conex.setMinimumHeight(180)
        col_der.addWidget(self.lista_conex)

        # Botón eliminar
        self.btn_eliminar = QPushButton('Eliminar conexion')
        self.btn_eliminar.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.color7};
                color: {self.color6};
                border: none;
                padding: 8px 40px;
                border-radius: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color8};
            }}
        ''')
        self.btn_eliminar.clicked.connect(self.eliminar_conexion)
        col_der.addWidget(self.btn_eliminar)
        col_der.addStretch(1)

        self.cargar_ids_con_conexiones()

    def cargar_ids_con_conexiones(self):
        self.usuarios = obtener_todos_usuarios()
        self.conexiones = obtener_todas_conexiones()
        ids_con_conex = set()
        for c in self.conexiones:
            ids_con_conex.add(str(c.get('id1')))
            ids_con_conex.add(str(c.get('id2')))
        self.id_map = {str(u['id']): u for u in self.usuarios if str(u['id']) in ids_con_conex}
        self.combo_id.clear()
        for id_str in self.id_map:
            self.combo_id.addItem(id_str)
        self.combo_id.setCurrentIndex(-1)

    def on_id_selected(self, idx):
        if idx < 0:
            self.input_nombre.setText("")
            self.lista_intereses.clear()
            self.lista_conex.clear()
            return
        id_str = self.combo_id.currentText()
        usuario = self.id_map.get(id_str)
        if usuario:
            self.input_nombre.setText(usuario.get('nombre', ''))
            self.lista_intereses.clear()
            for interes in usuario.get('intereses', []):
                self.lista_intereses.addItem(interes)
            # Mostrar conexiones de este usuario
            self.lista_conex.clear()
            for c in self.conexiones:
                if str(c.get('id1')) == id_str:
                    otro_id = str(c.get('id2'))
                elif str(c.get('id2')) == id_str:
                    otro_id = str(c.get('id1'))
                else:
                    continue
                otro_usuario = self.id_map.get(otro_id) or next((u for u in self.usuarios if str(u['id']) == otro_id), None)
                nombre_otro = otro_usuario.get('nombre', '') if otro_usuario else ''
                self.lista_conex.addItem(f"{otro_id}:{nombre_otro}")

    def eliminar_conexion(self):
        id_str = self.combo_id.currentText()
        item = self.lista_conex.currentItem()
        if not id_str or not item:
            QMessageBox.warning(self, 'Error', 'Selecciona un usuario y una conexión a eliminar.')
            return
        conexion_str = item.text()
        otro_id = conexion_str.split(':')[0]
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            f'¿Estás seguro de que quieres eliminar la conexión entre {id_str} y {otro_id}?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Eliminar la conexión de la base de datos
            from controlers.Database import conexiones_table
            for c in self.conexiones:
                if (str(c.get('id1')) == id_str and str(c.get('id2')) == otro_id) or (str(c.get('id2')) == id_str and str(c.get('id1')) == otro_id):
                    conexiones_table.remove(doc_ids=[c.doc_id])
            QMessageBox.information(self, 'Éxito', f'Conexión eliminada correctamente.')
            self.cargar_ids_con_conexiones()
            self.on_id_selected(self.combo_id.currentIndex())

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DelConecGUI()
    window.exec_()
