from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QApplication,
    QHBoxLayout, QPushButton, QListWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AddUserGui(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self, id_disponible):
        super().__init__()
        self.setWindowTitle('Agregar Usuario')
        self.setMinimumSize(400, 600)
        self.setStyleSheet(f'background-color: {self.color5};')
        self.intereses = []
        self.init_ui(id_disponible)

    def init_ui(self, id_disponible):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        titulo = QLabel('Agregar Usuario')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont('Arial', 14))
        titulo.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(titulo)

        # Nombre
        label_nombre = QLabel('Nombre:')
        label_nombre.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_nombre)
        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        layout.addWidget(self.input_nombre)

        # Intereses
        label_intereses = QLabel('Intereses:')
        label_intereses.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_intereses)
        
        # Campo de entrada para nuevo interés
        input_layout = QHBoxLayout()
        self.input_interes = QLineEdit()
        self.input_interes.setPlaceholderText('Escribe un interés...')
        self.input_interes.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        input_layout.addWidget(self.input_interes)
        
        # Botón para agregar interés
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
        layout.addLayout(input_layout)
        
        # Lista de intereses
        label_lista = QLabel('Intereses agregados:')
        label_lista.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_lista)
        
        self.lista_intereses = QListWidget()
        self.lista_intereses.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        self.lista_intereses.setMaximumHeight(150)
        layout.addWidget(self.lista_intereses)

        # ID disponible
        label_id = QLabel(f'ID disponible:  {id_disponible}')
        label_id.setStyleSheet(f'color: {self.color1}; background: none;')
        layout.addWidget(label_id)
        layout.addStretch(1)

        # Botones Guardar/Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def agregar_interes(self):
        interes = self.input_interes.text().strip()
        if interes and interes not in self.intereses:
            self.intereses.append(interes)
            self.lista_intereses.addItem(interes)
            self.input_interes.clear()
        elif interes in self.intereses:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Error', 'Este interés ya está en la lista')

    def get_intereses(self):
        return self.intereses

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AddUserGui(1)
    if window.exec_() == QDialog.Accepted:
        print('Guardado:', window.input_nombre.text(), window.get_intereses())
    else:
        print('Cancelado')
