from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QGroupBox, QSizePolicy, QSpacerItem, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controlers.Comunidades import obtener_datos_comunidades
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class ComunityGUI(QDialog):
    color1 = '#000000'
    color2 = '#15284c'  # Fondo botones, encabezados
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones (izquierda)
    color5 = '#c9d4ff'  # Fondo general (derecha)
    color6 = '#ffffff'  # Fondo tarjetas

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Comunidades')
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(f'background-color: {self.color6};')
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        main_vlayout = QVBoxLayout(self)
        main_vlayout.setContentsMargins(0, 0, 0, 0)
        main_vlayout.setSpacing(0)
        # Barra superior con botón atrás
        self.btn_atras = QPushButton('Atrás')
        self.btn_atras.setStyleSheet(f'QPushButton {{ background: {self.color2}; color: #fff; border-radius: 10px; padding: 8px 24px; font-weight: bold; font-size: 16px; }} QPushButton:hover {{ background: {self.color3}; }}')
        self.btn_atras.setFixedWidth(100)
        self.btn_atras.setFixedHeight(36)
        self.btn_atras.clicked.connect(self.cerrar_ventana)
        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        top_bar.addWidget(self.btn_atras)
        top_bar.setContentsMargins(0, 10, 20, 0)
        main_vlayout.addLayout(top_bar)
        # Layout horizontal principal
        main_layout = QHBoxLayout()
        # --- Panel izquierdo: Comunidades ---
        left_widget = QWidget()
        left_widget.setStyleSheet(f'background: {self.color5};')
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(20, 20, 10, 20)
        left_layout.setSpacing(20)
        label_titulo = QLabel('<b>Comunidades</b>')
        label_titulo.setFont(QFont('Arial', 22, QFont.Bold))
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(label_titulo)
        # Scroll para comunidades
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.comunidades_layout = QVBoxLayout(scroll_content)
        self.comunidades_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)
        main_layout.addWidget(left_widget, 3)
        # --- Panel derecho: Grafo ---
        right_widget = QWidget()
        right_widget.setStyleSheet(f'background: {self.color5};')
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 20, 20, 20)
        right_layout.setSpacing(10)
        self.label_grafico = QLabel('Gráfico')
        self.label_grafico.setFont(QFont('Arial', 16))
        self.label_grafico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.label_grafico)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas, 10)
        main_layout.addWidget(right_widget, 7)
        main_vlayout.addLayout(main_layout)
        # Cargar datos y poblar comunidades
        self.cargar_comunidades()

    def cargar_comunidades(self):
        comunidades, info_extra, usuarios_dict = obtener_datos_comunidades()
        self.comunidades = comunidades
        self.usuarios_dict = usuarios_dict
        self.info_extra = info_extra
        self.comunidades_layout.setSpacing(15)
        self.com_orden_map = {}  # Mapeo de id interno a número de orden
        # Limpiar layout
        while self.comunidades_layout.count():
            item = self.comunidades_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        # Crear tarjetas para cada comunidad
        for idx, (com_id, miembros) in enumerate(comunidades.items(), 1):
            self.com_orden_map[com_id] = idx
            box = QGroupBox()
            box.setStyleSheet(f'QGroupBox {{ background: {self.color6}; border: 2px solid #000; border-radius: 8px; }}')
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(10, 10, 10, 10)
            label = QLabel(f'Comunidad {idx} [{len(miembros)}]')
            label.setFont(QFont('Arial', 14, QFont.Bold))
            label.setStyleSheet(f"background-color: {self.color6}")
            box_layout.addWidget(label)
            label_conex = QLabel(f'Conexiones totales: {self.info_extra["conexiones_por_comunidad"].get(com_id, 0)}')
            label_conex.setFont(QFont('Arial', 11))
            label_conex.setStyleSheet(f"background-color: {self.color6}")
            box_layout.addWidget(label_conex)
            # Usuarios
            nombres = [self.usuarios_dict[uid]['nombre'] for uid in miembros if uid in self.usuarios_dict]
            nombres_str = ', '.join(nombres[:5])
            if len(nombres) > 5:
                nombres_str += ', ...'
            label_usuarios = QLabel(f'Usuarios conectados: {nombres_str}')
            label_usuarios.setFont(QFont('Arial', 11))
            label_usuarios.setStyleSheet(f"background-color: {self.color6}")
            box_layout.addWidget(label_usuarios)
            # Botón visualizar
            btn_viz = QPushButton('Vizualizar')
            btn_viz.setStyleSheet('background: #c97c7c; color: #fff; border-radius: 16px; padding: 6px 20px; font-weight: bold;')
            btn_viz.setFixedWidth(120)
            btn_viz.clicked.connect(lambda _, cid=com_id: self.mostrar_grafo_comunidad(cid))
            box_layout.addWidget(btn_viz, alignment=Qt.AlignmentFlag.AlignRight)
            self.comunidades_layout.addWidget(box)

    def mostrar_grafo_comunidad(self, com_id):
        miembros = self.comunidades[com_id]
        G = nx.Graph()
        # Añadir nodos
        for uid in miembros:
            G.add_node(uid, label=self.usuarios_dict[uid]['nombre'])
        # Añadir aristas solo entre miembros usando la base de datos de conexiones
        from controlers.Database import obtener_todas_conexiones
        conexiones = obtener_todas_conexiones()
        for conexion in conexiones:
            id1 = str(conexion['id1'])
            id2 = str(conexion['id2'])
            if id1 in miembros and id2 in miembros:
                G.add_edge(id1, id2)
        self.ax.clear()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=self.ax, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_color=self.color4, edge_color=self.color2, font_size=10, font_color=self.color1)
        # Mostrar el número de orden visual en el título
        num_orden = self.com_orden_map.get(com_id, com_id)
        self.ax.set_title(f'Comunidad {num_orden}')
        self.canvas.draw()
        self.label_grafico.setText(f'Comunidad: {num_orden}')

    def cerrar_ventana(self):
        self.close()
