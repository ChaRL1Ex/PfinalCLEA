from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QApplication, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controlers.Database import obtener_todos_usuarios, obtener_usuario, obtener_todas_conexiones

class DeleteUserGui(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Eliminar usuario')
        self.setMinimumSize(400, 500)
        self.setStyleSheet(f'background-color: {self.color5};')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        titulo = QLabel('Eliminar usuario')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont('Arial', 14))
        titulo.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(titulo)

        # ID
        label_id = QLabel('ID:')
        label_id.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_id)
        self.combo_id = QComboBox()
        self.combo_id.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        layout.addWidget(self.combo_id)
        self.combo_id.currentIndexChanged.connect(self.on_id_selected)

        # Nombre
        label_nombre = QLabel('Nombre:')
        label_nombre.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_nombre)
        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_nombre.setEnabled(False)
        layout.addWidget(self.input_nombre)

        # Intereses
        label_intereses = QLabel('Intereses:')
        label_intereses.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_intereses)
        self.input_intereses = QLineEdit()
        self.input_intereses.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_intereses.setEnabled(False)
        layout.addWidget(self.input_intereses)

        # Conexiones
        label_conex = QLabel('Conexiones')
        label_conex.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_conex)
        self.list_conex = QListWidget()
        self.list_conex.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        self.list_conex.setEnabled(False)
        layout.addWidget(self.list_conex)

        layout.addStretch(1)

        # Botón Eliminar
        self.btn_eliminar = QPushButton('Eliminar')
        self.btn_eliminar.setStyleSheet(f'background: #c97c7c; color: {self.color1}; border-radius: 16px; padding: 8px 20px; font-weight: bold;')
        self.btn_eliminar.clicked.connect(self.confirmar_eliminar)
        layout.addWidget(self.btn_eliminar, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.cargar_ids()

    def cargar_ids(self):
        self.combo_id.clear()
        usuarios = obtener_todos_usuarios()
        self.id_map = {}
        for usuario in usuarios:
            id_str = str(usuario.get('id', ''))
            self.combo_id.addItem(id_str)
            self.id_map[id_str] = usuario
        self.combo_id.setCurrentIndex(-1)

    def on_id_selected(self, idx):
        if idx < 0:
            self.input_nombre.setText("")
            self.input_intereses.setText("")
            self.list_conex.clear()
            return
        id_str = self.combo_id.currentText()
        usuario = self.id_map.get(id_str)
        if usuario:
            self.input_nombre.setText(usuario.get('nombre', ''))
            self.input_intereses.setText(','.join(usuario.get('intereses', [])))
            self.cargar_conexiones(id_str)
        else:
            self.input_nombre.setText("")
            self.input_intereses.setText("")
            self.list_conex.clear()

    def cargar_conexiones(self, id_str):
        self.list_conex.clear()
        conexiones = obtener_todas_conexiones()
        conexiones_usuario = []
        for c in conexiones:
            if str(c.get('id1')) == id_str:
                conexiones_usuario.append(str(c.get('id2')))
            elif str(c.get('id2')) == id_str:
                conexiones_usuario.append(str(c.get('id1')))
        if conexiones_usuario:
            self.list_conex.addItems(conexiones_usuario)
        else:
            self.list_conex.addItem('No existen conexiones con este Usuario')

    def confirmar_eliminar(self):
        id_str = self.combo_id.currentText()
        if not id_str:
            QMessageBox.warning(self, 'Error', 'Debes seleccionar un usuario')
            return
        confirm = QMessageBox.question(self, 'Confirmar eliminación', f'¿Estás seguro de que deseas eliminar el usuario {id_str}?',
                                        QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.accept()  # Puedes manejar la eliminación real desde fuera

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = DeleteUserGui()
    if window.exec_() == QDialog.Accepted:
        print('Eliminado:', window.combo_id.currentText())
    else:
        print('Cancelado')
