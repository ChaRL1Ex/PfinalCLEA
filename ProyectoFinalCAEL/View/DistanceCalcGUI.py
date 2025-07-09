from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget, QWidget, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
from controlers.Database import obtener_todos_usuarios, obtener_todas_conexiones
from controlers.Conexiones import calcular_distancia_y_ruta

class DistanceCalcGUI(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general
    color6 = '#ffffff'  # Texto blanco

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calcular Distancia')
        self.setMinimumSize(1200, 800)
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        main_vlayout = QVBoxLayout(self)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)
        # Botón atrás en la esquina superior derecha
        self.btn_atras = QPushButton('Atrás')
        self.btn_atras.setStyleSheet('QPushButton { background: #15284c; color: #fff; border-radius: 10px; padding: 8px 24px; font-weight: bold; font-size: 16px; } QPushButton:hover { background: #435ba0; }')
        self.btn_atras.setFixedWidth(100)
        self.btn_atras.setFixedHeight(36)
        self.btn_atras.clicked.connect(self.cerrar_ventana)
        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        top_bar.addWidget(self.btn_atras)
        top_bar.setContentsMargins(0, 10, 20, 0)
        main_vlayout.addLayout(top_bar)
        # Layout horizontal principal (contenido original)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(10)

        # Título
        titulo = QLabel('Calcular distancia')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont('Arial', 28, QFont.Bold))
        titulo.setStyleSheet(f'color: {self.color1}; background: none;')
        main_layout.addWidget(titulo)

        # Layout principal horizontal
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)

        # Columna Usuario 1
        col1 = QVBoxLayout()
        h_layout.addLayout(col1, 2)
        col1.addSpacing(20)
        label_u1 = QLabel('Usuario 1:')
        label_u1.setFont(QFont('Arial', 14))
        label_u1.setStyleSheet(f'color: {self.color1}; background: none;')
        col1.addWidget(label_u1)
        col1.addSpacing(5)
        col1.addWidget(QLabel('id:'))
        self.combo_id1 = QComboBox()
        self.combo_id1.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1}; padding: 6px;')
        col1.addWidget(self.combo_id1)
        col1.addSpacing(10)
        col1.addWidget(QLabel('Nombre:'))
        self.input_nombre1 = QLineEdit()
        self.input_nombre1.setReadOnly(True)
        self.input_nombre1.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        col1.addWidget(self.input_nombre1)
        col1.addSpacing(10)
        label_intereses1 = QLabel('Intereses')
        label_intereses1.setStyleSheet(f'color: {self.color1}; background: none;')
        col1.addWidget(label_intereses1)
        self.lista_intereses1 = QListWidget()
        self.lista_intereses1.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        self.lista_intereses1.setMinimumHeight(120)
        col1.addWidget(self.lista_intereses1)
        col1.addStretch(1)

        # Columna central (grafo, botón, labels)
        centro = QVBoxLayout()
        h_layout.addLayout(centro, 4)
        centro.addSpacing(10)
        # Grafo
        self.graph_widget = QWidget()
        self.graph_widget.setMinimumSize(800, 600)
        self.graph_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        graph_layout = QVBoxLayout(self.graph_widget)
        graph_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.graph_widget, stretch=2)
        # Botón Calcular
        self.btn_calcular = QPushButton('Calcular')
        self.btn_calcular.setStyleSheet('background: #c97c7c; color: #111; border-radius: 16px; padding: 8px 20px; font-weight: bold;')
        self.btn_calcular.setFont(QFont('Arial', 13, QFont.Bold))
        self.btn_calcular.setFixedWidth(180)
        self.btn_calcular.clicked.connect(self.on_btn_calcular)
        centro.addWidget(self.btn_calcular, alignment=Qt.AlignmentFlag.AlignHCenter)
        # Label de distancia y ruta (inicialmente ocultos)
        self.label_distancia = QLabel()
        self.label_distancia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_distancia.setFont(QFont('Arial', 14, QFont.Bold))
        self.label_distancia.setStyleSheet(f'color: {self.color1}; background: none;')
        self.label_distancia.hide()
        centro.addWidget(self.label_distancia)
        self.label_ruta = QLabel()
        self.label_ruta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_ruta.setFont(QFont('Arial', 12))
        self.label_ruta.setStyleSheet(f'color: {self.color1}; background: none;')
        self.label_ruta.hide()
        centro.addWidget(self.label_ruta)
        centro.addStretch(1)

        # Columna Usuario 2
        col2 = QVBoxLayout()
        h_layout.addLayout(col2, 2)
        col2.addSpacing(20)
        label_u2 = QLabel('Usuario 2:')
        label_u2.setFont(QFont('Arial', 14))
        label_u2.setStyleSheet(f'color: {self.color1}; background: none;')
        col2.addWidget(label_u2)
        col2.addSpacing(5)
        col2.addWidget(QLabel('id:'))
        self.combo_id2 = QComboBox()
        self.combo_id2.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1}; padding: 6px;')
        col2.addWidget(self.combo_id2)
        col2.addSpacing(10)
        col2.addWidget(QLabel('Nombre:'))
        self.input_nombre2 = QLineEdit()
        self.input_nombre2.setReadOnly(True)
        self.input_nombre2.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        col2.addWidget(self.input_nombre2)
        col2.addSpacing(10)
        label_intereses2 = QLabel('Intereses')
        label_intereses2.setStyleSheet(f'color: {self.color1}; background: none;')
        col2.addWidget(label_intereses2)
        self.lista_intereses2 = QListWidget()
        self.lista_intereses2.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; color: {self.color1};')
        self.lista_intereses2.setMinimumHeight(120)
        col2.addWidget(self.lista_intereses2)
        col2.addStretch(1)

        # Cargar datos
        self.cargar_ids_con_conexiones()
        self.combo_id1.currentIndexChanged.connect(self.on_id1_selected)
        self.combo_id2.currentIndexChanged.connect(self.on_id2_selected)
        main_vlayout.addLayout(main_layout)

    def cargar_ids_con_conexiones(self):
        self.usuarios = obtener_todos_usuarios()
        self.conexiones = obtener_todas_conexiones()
        ids_con_conex = set()
        for c in self.conexiones:
            ids_con_conex.add(str(c.get('id1')))
            ids_con_conex.add(str(c.get('id2')))
        self.id_map = {str(u['id']): u for u in self.usuarios if str(u['id']) in ids_con_conex}
        self.combo_id1.blockSignals(True)
        self.combo_id2.blockSignals(True)
        self.combo_id1.clear()
        self.combo_id2.clear()
        for id_str in self.id_map:
            self.combo_id1.addItem(id_str)
            self.combo_id2.addItem(id_str)
        self.combo_id1.setCurrentIndex(-1)
        self.combo_id2.setCurrentIndex(-1)
        self.combo_id1.blockSignals(False)
        self.combo_id2.blockSignals(False)

    def on_btn_calcular(self):
        self.mostrar_distancia_y_grafo()

    def mostrar_distancia_y_grafo(self):
        id1 = self.combo_id1.currentText()
        id2 = self.combo_id2.currentText()
        nombre1 = self.input_nombre1.text() or 'Usuario 1'
        nombre2 = self.input_nombre2.text() or 'Usuario 2'
        if id1 and id2 and id1 != id2:
            distancia, ruta = calcular_distancia_y_ruta(id1, id2)
            if distancia is not None:
                self.label_distancia.setText(f'Distancia entre {nombre1} y {nombre2}: {distancia} conexiones')
                self.label_ruta.setText('Ruta: ' + ' → '.join(ruta))
                self.dibujar_grafo_ruta(ruta)
            else:
                self.label_distancia.setText(f'No hay conexión entre {nombre1} y {nombre2}')
                self.label_ruta.setText('Ruta: -')
                self.dibujar_grafo_ruta([])
        else:
            self.label_distancia.setText('Selecciona dos usuarios distintos.')
            self.label_ruta.setText('Ruta: -')
            self.dibujar_grafo_ruta([])
        self.label_distancia.show()
        self.label_ruta.show()

    def on_id1_selected(self, idx):
        id1 = self.combo_id1.currentText()
        usuario = self.id_map.get(id1)
        if usuario:
            self.input_nombre1.setText(usuario.get('nombre', ''))
            self.lista_intereses1.clear()
            for interes in usuario.get('intereses', []):
                self.lista_intereses1.addItem(interes)
        else:
            self.input_nombre1.setText("")
            self.lista_intereses1.clear()
        self.actualizar_combo2()
        self.label_distancia.hide()
        self.label_ruta.hide()
        self.dibujar_grafo_ruta([])

    def on_id2_selected(self, idx):
        id2 = self.combo_id2.currentText()
        usuario = self.id_map.get(id2)
        if usuario:
            self.input_nombre2.setText(usuario.get('nombre', ''))
            self.lista_intereses2.clear()
            for interes in usuario.get('intereses', []):
                self.lista_intereses2.addItem(interes)
        else:
            self.input_nombre2.setText("")
            self.lista_intereses2.clear()
        self.actualizar_combo1()
        self.label_distancia.hide()
        self.label_ruta.hide()
        self.dibujar_grafo_ruta([])

    def actualizar_combo2(self):
        id1 = self.combo_id1.currentText()
        current_id2 = self.combo_id2.currentText()
        self.combo_id2.blockSignals(True)
        self.combo_id2.clear()
        for id_str in self.id_map:
            if id_str != id1:
                self.combo_id2.addItem(id_str)
        idx = self.combo_id2.findText(current_id2)
        self.combo_id2.setCurrentIndex(idx if idx >= 0 else -1)
        self.combo_id2.blockSignals(False)

    def actualizar_combo1(self):
        id2 = self.combo_id2.currentText()
        current_id1 = self.combo_id1.currentText()
        self.combo_id1.blockSignals(True)
        self.combo_id1.clear()
        for id_str in self.id_map:
            if id_str != id2:
                self.combo_id1.addItem(id_str)
        idx = self.combo_id1.findText(current_id1)
        self.combo_id1.setCurrentIndex(idx if idx >= 0 else -1)
        self.combo_id1.blockSignals(False)

    def dibujar_grafo_ruta(self, ruta):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        G = nx.Graph()
        if len(ruta) >= 2:
            for i in range(len(ruta)-1):
                G.add_edge(ruta[i], ruta[i+1])
            for n in ruta:
                G.add_node(n)
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='black', font_color='white', node_size=900, edge_color=self.color2, width=2)
        elif len(ruta) == 1:
            G.add_node(ruta[0])
            pos = {ruta[0]: (0.5, 0.5)}
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='black', font_color='white', node_size=900)
        ax.set_axis_off()
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def cerrar_ventana(self):
        self.close()
