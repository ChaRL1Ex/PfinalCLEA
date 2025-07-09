from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
from controlers.Database import obtener_todos_usuarios, obtener_todas_conexiones
import math

class ViewRedGUI(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Visualizar Red')
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(f'background-color: {self.color5};')
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header
        header = QLabel('Red')
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont('Arial', 24, QFont.Bold))
        header.setStyleSheet(f'color: {self.color1}; background: {self.color5};')
        layout.addWidget(header)

        # Canvas para la red
        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, stretch=1)
        self.dibujar_red()
        main_layout.addLayout(layout)
        main_vlayout.addLayout(main_layout)

    def dibujar_red(self):
        self.ax.clear()
        G = nx.Graph()
        usuarios = obtener_todos_usuarios()
        conexiones = obtener_todas_conexiones()
        
        # Calcular conexiones por usuario
        conexiones_por_usuario = {}
        for c in conexiones:
            id1 = str(c.get('id1'))
            id2 = str(c.get('id2'))
            conexiones_por_usuario[id1] = conexiones_por_usuario.get(id1, 0) + 1
            conexiones_por_usuario[id2] = conexiones_por_usuario.get(id2, 0) + 1
        
        # Añadir nodos
        for u in usuarios:
            id_usuario = str(u['id'])
            conexiones_usuario = conexiones_por_usuario.get(id_usuario, 0)
            G.add_node(id_usuario, label=u['nombre'], conexiones=conexiones_usuario)
        
        # Añadir aristas
        for c in conexiones:
            G.add_edge(str(c['id1']), str(c['id2']))
        
        pos = nx.spring_layout(G, seed=42)
        
        # Detectar nodos aislados
        aislados = [n for n in G.nodes if G.degree[n] == 0]
        conectados = [n for n in G.nodes if G.degree[n] > 0]
        
        # Normalizar posiciones de conectados para centrar
        for k in conectados:
            x, y = pos[k]
            x = 0.22 + 0.56 * x
            y = 0.22 + 0.56 * y
            pos[k] = (x, y)
        
        # Distribuir nodos aislados en círculo
        n_aislados = len(aislados)
        radio = 0.38
        centro = (0.5, 0.5)
        for i, k in enumerate(aislados):
            ang = 2 * math.pi * i / max(n_aislados, 1)
            x = centro[0] + radio * math.cos(ang)
            y = centro[1] + radio * math.sin(ang)
            pos[k] = (x, y)
        
        # Separar nodos por tipo
        nodos_normales = []
        nodos_influyentes = []
        nodos_influencers = []
        
        for n in G.nodes:
            conexiones_nodo = G.nodes[n].get('conexiones', 0)
            if conexiones_nodo >= 15:  # Influencer
                nodos_influencers.append(n)
            elif conexiones_nodo >= 4:  # Usuario influyente
                nodos_influyentes.append(n)
            else:  # Usuario normal
                nodos_normales.append(n)
        
        # Dibujar nodos con diferentes tamaños
        if nodos_normales:
            nx.draw_networkx_nodes(G, pos, nodelist=nodos_normales, ax=self.ax, 
                                 node_color='#7f95ff', node_size=700)
        
        if nodos_influyentes:
            nx.draw_networkx_nodes(G, pos, nodelist=nodos_influyentes, ax=self.ax, 
                                 node_color='#7f95ff', node_size=1000)
        
        if nodos_influencers:
            nx.draw_networkx_nodes(G, pos, nodelist=nodos_influencers, ax=self.ax, 
                                 node_color='#ff6b6b', node_size=1200)
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='#435ba0')
        
        # Dibujar etiquetas con diferentes colores
        labels = {n: G.nodes[n].get('label', str(n)) for n in G.nodes}
        
        # Etiquetas normales
        if nodos_normales:
            labels_normales = {n: labels[n] for n in nodos_normales}
            nx.draw_networkx_labels(
                G, pos, labels_normales, font_color='black', font_size=10, ax=self.ax,
                bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2', alpha=0.7)
            )
        
        # Etiquetas influyentes
        if nodos_influyentes:
            labels_influyentes = {n: labels[n] for n in nodos_influyentes}
            nx.draw_networkx_labels(
                G, pos, labels_influyentes, font_color='black', font_size=10, ax=self.ax,
                bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2', alpha=0.7)
            )
        
        # Etiquetas influencers (dorado)
        if nodos_influencers:
            labels_influencers = {n: labels[n] for n in nodos_influencers}
            nx.draw_networkx_labels(
                G, pos, labels_influencers, font_color='#FFD700', font_size=12, font_weight='bold', ax=self.ax,
                bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2', alpha=0.7)
            )
        
        self.ax.set_axis_off()
        self.ax.margins(0.15)
        # Ajuste automático de límites para evitar desbordes
        all_x = [pos[n][0] for n in G.nodes]
        all_y = [pos[n][1] for n in G.nodes]
        if all_x and all_y:
            min_x, max_x = min(all_x), max(all_x)
            min_y, max_y = min(all_y), max(all_y)
            padding_x = (max_x - min_x) * 0.15 if max_x > min_x else 0.1
            padding_y = (max_y - min_y) * 0.15 if max_y > min_y else 0.1
            self.ax.set_xlim(min_x - padding_x, max_x + padding_x)
            self.ax.set_ylim(min_y - padding_y, max_y + padding_y)
        self.figure.tight_layout(pad=2.0)
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        self.canvas.draw()

    def cerrar_ventana(self):
        self.close()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ViewRedGUI()
    window.exec_()
