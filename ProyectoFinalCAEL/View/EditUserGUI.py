from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QApplication, QComboBox,
    QHBoxLayout, QPushButton, QListWidget, QGroupBox, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controlers.Database import obtener_todos_usuarios, obtener_usuario

class EditUserGui(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Editar usuario')
        self.setMinimumSize(500, 700)
        self.setStyleSheet(f'background-color: {self.color5};')
        self.intereses = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        titulo = QLabel('Editar usuario')
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

        # Sección de Intereses
        grupo_intereses = QGroupBox('Gestión de Intereses')
        grupo_intereses.setStyleSheet(f'''
            QGroupBox {{
                font-weight: bold;
                color: {self.color1};
                border: 2px solid {self.color2};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        ''')
        layout_intereses = QVBoxLayout(grupo_intereses)
        
        # Campo para agregar nuevo interés
        label_nuevo_interes = QLabel('Agregar nuevo interés:')
        label_nuevo_interes.setStyleSheet(f'color: {self.color1}; background: none;')
        layout_intereses.addWidget(label_nuevo_interes)
        
        input_layout = QHBoxLayout()
        self.input_nuevo_interes = QLineEdit()
        self.input_nuevo_interes.setPlaceholderText('Escribe un nuevo interés...')
        self.input_nuevo_interes.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        input_layout.addWidget(self.input_nuevo_interes)
        
        self.btn_agregar_interes = QPushButton('Agregar')
        self.btn_agregar_interes.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.color2};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color3};
            }}
        ''')
        self.btn_agregar_interes.clicked.connect(self.agregar_interes)
        input_layout.addWidget(self.btn_agregar_interes)
        layout_intereses.addLayout(input_layout)
        
        # Gestión de intereses existentes
        label_gestion = QLabel('Gestionar intereses existentes:')
        label_gestion.setStyleSheet(f'color: {self.color1}; background: none;')
        layout_intereses.addWidget(label_gestion)
        
        gestion_layout = QHBoxLayout()
        
        # Dropdown para seleccionar interés
        self.combo_intereses = QComboBox()
        self.combo_intereses.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        gestion_layout.addWidget(self.combo_intereses)
        
        # Botón modificar
        self.btn_modificar_interes = QPushButton('Modificar')
        self.btn_modificar_interes.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.color2};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color3};
            }}
        ''')
        self.btn_modificar_interes.clicked.connect(self.modificar_interes)
        gestion_layout.addWidget(self.btn_modificar_interes)
        
        # Botón eliminar
        self.btn_eliminar_interes = QPushButton('Eliminar')
        self.btn_eliminar_interes.setStyleSheet(f'''
            QPushButton {{
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #b71c1c;
            }}
        ''')
        self.btn_eliminar_interes.clicked.connect(self.eliminar_interes)
        gestion_layout.addWidget(self.btn_eliminar_interes)
        
        layout_intereses.addLayout(gestion_layout)
        
        # Lista de intereses actuales
        label_lista = QLabel('Intereses actuales:')
        label_lista.setStyleSheet(f'color: {self.color1}; background: none;')
        layout_intereses.addWidget(label_lista)
        
        self.lista_intereses = QListWidget()
        self.lista_intereses.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        self.lista_intereses.setMaximumHeight(120)
        layout_intereses.addWidget(self.lista_intereses)
        
        layout.addWidget(grupo_intereses)

        layout.addStretch(1)

        # Botones Guardar/Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

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
            self.intereses = []
            self.actualizar_lista_intereses()
            self.input_nombre.setEnabled(False)
            self.input_nuevo_interes.setEnabled(False)
            self.btn_agregar_interes.setEnabled(False)
            self.combo_intereses.setEnabled(False)
            self.btn_modificar_interes.setEnabled(False)
            self.btn_eliminar_interes.setEnabled(False)
            return
        id_str = self.combo_id.currentText()
        usuario = self.id_map.get(id_str)
        if usuario:
            self.input_nombre.setText(usuario.get('nombre', ''))
            self.intereses = usuario.get('intereses', [])
            self.actualizar_lista_intereses()
            self.input_nombre.setEnabled(True)
            self.input_nuevo_interes.setEnabled(True)
            self.btn_agregar_interes.setEnabled(True)
            self.combo_intereses.setEnabled(True)
            self.btn_modificar_interes.setEnabled(True)
            self.btn_eliminar_interes.setEnabled(True)
        else:
            self.input_nombre.setText("")
            self.intereses = []
            self.actualizar_lista_intereses()
            self.input_nombre.setEnabled(False)
            self.input_nuevo_interes.setEnabled(False)
            self.btn_agregar_interes.setEnabled(False)
            self.combo_intereses.setEnabled(False)
            self.btn_modificar_interes.setEnabled(False)
            self.btn_eliminar_interes.setEnabled(False)

    def actualizar_lista_intereses(self):
        self.lista_intereses.clear()
        self.combo_intereses.clear()
        for interes in self.intereses:
            self.lista_intereses.addItem(interes)
            self.combo_intereses.addItem(interes)

    def agregar_interes(self):
        interes = self.input_nuevo_interes.text().strip()
        if interes and interes not in self.intereses:
            self.intereses.append(interes)
            self.actualizar_lista_intereses()
            self.input_nuevo_interes.clear()
        elif interes in self.intereses:
            QMessageBox.warning(self, 'Error', 'Este interés ya está en la lista')

    def modificar_interes(self):
        if self.combo_intereses.currentText():
            interes_actual = self.combo_intereses.currentText()
            nuevo_interes, ok = QInputDialog.getText(
                self, 'Modificar Interés', 
                f'Modificar interés "{interes_actual}":', 
                text=interes_actual
            )
            if ok and nuevo_interes.strip():
                nuevo_interes = nuevo_interes.strip()
                if nuevo_interes not in self.intereses or nuevo_interes == interes_actual:
                    idx = self.intereses.index(interes_actual)
                    self.intereses[idx] = nuevo_interes
                    self.actualizar_lista_intereses()
                else:
                    QMessageBox.warning(self, 'Error', 'Este interés ya existe')

    def eliminar_interes(self):
        if self.combo_intereses.currentText():
            interes = self.combo_intereses.currentText()
            reply = QMessageBox.question(
                self, 'Confirmar eliminación', 
                f'¿Estás seguro de que quieres eliminar el interés "{interes}"?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.intereses.remove(interes)
                self.actualizar_lista_intereses()

    def get_intereses(self):
        return self.intereses

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = EditUserGui()
    if window.exec_() == QDialog.Accepted:
        print('Guardado:', window.combo_id.currentText(), window.input_nombre.text(), window.get_intereses())
    else:
        print('Cancelado')
