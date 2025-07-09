from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QSpacerItem, QSizePolicy, QFrame, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from View.DistanceCalcGUI import DistanceCalcGUI
from View.StatsGUI import StatsGUI

class GuiMain(QDialog):
    # Paleta de colores a nivel de clase
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menú Principal')
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(f'background-color: {self.color5};')
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        main_vlayout = QVBoxLayout(self)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)
        # Botón salir en la esquina superior derecha
        self.btn_salir = QPushButton('Salir')
        self.btn_salir.setStyleSheet('QPushButton { background: #15284c; color: #fff; border-radius: 10px; padding: 8px 24px; font-weight: bold; font-size: 16px; } QPushButton:hover { background: #435ba0; }')
        self.btn_salir.setFixedWidth(100)
        self.btn_salir.setFixedHeight(36)
        self.btn_salir.clicked.connect(self.cerrar_ventana)
        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        top_bar.addWidget(self.btn_salir)
        top_bar.setContentsMargins(0, 10, 20, 0)
        main_vlayout.addLayout(top_bar)
        # Layout principal original
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # Sección Usuarios
        usuarios_box = QGroupBox()
        usuarios_box.setStyleSheet(f'QGroupBox {{ background: {self.color4}; border: none; }}')
        usuarios_layout = QVBoxLayout(usuarios_box)
        usuarios_layout.setContentsMargins(5, 5, 5, 5)
        usuarios_layout.setSpacing(10)
        label_usuarios = QLabel('<b>Usuarios</b>')
        label_usuarios.setStyleSheet(f'QLabel {{ color: {self.color1}; font-size: 16px; background-color: {self.color4}; border: none; }}')
        usuarios_layout.addWidget(label_usuarios)
        btns_usuarios_layout = QHBoxLayout()
        btns_usuarios_layout.setSpacing(30)
        btns_usuarios_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_agregar = QPushButton('Agregar Usuario')
        self.btn_editar = QPushButton('Editar Usuario')
        self.btn_eliminar = QPushButton('Eliminar Usuario')
        for btn in [self.btn_agregar, self.btn_editar, self.btn_eliminar]:
            btn.setStyleSheet(self.button_style(self.color2, self.color5, self.color3))
            btn.setFont(QFont('Arial', 11))
            btn.setFixedWidth(170)
            btns_usuarios_layout.addWidget(btn)
        btns_usuarios_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        usuarios_layout.addLayout(btns_usuarios_layout)
        main_layout.addWidget(usuarios_box)

        # Línea divisoria
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setFrameShadow(QFrame.Sunken)
        linea.setStyleSheet(f'color: {self.color1}; background: {self.color1}; max-height: 2px;')
        main_layout.addWidget(linea)

        # Sección Conexiones
        conexiones_box = QGroupBox()
        conexiones_box.setStyleSheet(f'QGroupBox {{ background: {self.color4}; border: none; }}')
        conexiones_layout = QVBoxLayout(conexiones_box)
        conexiones_layout.setContentsMargins(5, 5, 5, 5)
        conexiones_layout.setSpacing(10)
        label_conexiones = QLabel('<b>Conexiones</b>')
        label_conexiones.setStyleSheet(f'QLabel {{ color: {self.color1}; font-size: 16px; background-color: {self.color4}; border: none; }}')
        conexiones_layout.addWidget(label_conexiones)
        btns_conexiones_layout = QHBoxLayout()
        btns_conexiones_layout.setSpacing(30)
        btns_conexiones_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_establecer = QPushButton('Establecer conexion')
        self.btn_eliminar_con = QPushButton('Eliminar conexion')
        self.btn_calcular_distancia = QPushButton('Calcular distancia')
        for btn in [self.btn_establecer, self.btn_eliminar_con, self.btn_calcular_distancia]:
            btn.setStyleSheet(self.button_style(self.color2, self.color5, self.color3))
            btn.setFont(QFont('Arial', 11))
            btn.setFixedWidth(200)
            btns_conexiones_layout.addWidget(btn)
        btns_conexiones_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        conexiones_layout.addLayout(btns_conexiones_layout)
        main_layout.addWidget(conexiones_box)

        # Tabla central
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Intereses", "Conexiones"])
        self.table.setStyleSheet(f'QTableWidget {{ background: {self.color5}; color: {self.color1}; gridline-color: {self.color1}; }}')
        header = self.table.horizontalHeader()
        if header is not None:
            header.setStyleSheet(f'QHeaderView::section {{ background: {self.color2}; color: {self.color5}; }}')
            header.setSectionResizeMode(QHeaderView.Stretch)
        vheader = self.table.verticalHeader()
        if vheader is not None:
            vheader.setVisible(False)
        # Hacer que la tabla se expanda hasta el footer
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.table, stretch=1)

        # Espacio en blanco
        # main_layout.addSpacerItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón inferior
        bottom_box = QGroupBox()
        bottom_box.setStyleSheet(f'QGroupBox {{ background: {self.color4}; border: none; }}')
        bottom_layout = QHBoxLayout(bottom_box)
        bottom_layout.setContentsMargins(10, 10, 10, 10)
        # Centrado de botones
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_visualizar = QPushButton('Vizualizar red')
        self.btn_visualizar.setStyleSheet(self.button_style(self.color2, self.color5, self.color3))
        self.btn_visualizar.setFont(QFont('Arial', 12))
        self.btn_visualizar.setFixedWidth(200)
        bottom_layout.addWidget(self.btn_visualizar)
        bottom_layout.addSpacing(40)
        btn_estadisticas = QPushButton('Estadísticas')
        btn_estadisticas.setStyleSheet(self.button_style(self.color2, self.color5, self.color3))
        btn_estadisticas.setFont(QFont('Arial', 12))
        btn_estadisticas.setFixedWidth(200)
        btn_estadisticas.clicked.connect(self.mostrar_estadisticas)
        bottom_layout.addWidget(btn_estadisticas)
        bottom_layout.addSpacing(40)
        # Botón de comunidades
        self.btn_comunidades = QPushButton('Comunidades')
        self.btn_comunidades.setStyleSheet(self.button_style(self.color2, self.color5, self.color3))
        self.btn_comunidades.setFont(QFont('Arial', 12))
        self.btn_comunidades.setFixedWidth(200)
        bottom_layout.addWidget(self.btn_comunidades)
        bottom_layout.addSpacing(40)
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addWidget(bottom_box)
        main_vlayout.addLayout(main_layout)

    def button_style(self, bg_color, text_color, hover_color):
        return (
            f'QPushButton {{'
            f'background-color: {bg_color};'
            f'color: {text_color};'
            'border-radius: 8px;'
            'padding: 8px 20px;'
            'font-weight: bold;'
            '}'
            f'QPushButton:hover {{'
            f'background-color: {hover_color};'
            '}'
        )

    def mostrar_estadisticas(self):
        ventana = StatsGUI()
        ventana.exec_()

    def cerrar_ventana(self):
        self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = GuiMain()
    window.show()
    sys.exit(app.exec_())
