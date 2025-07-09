from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QApplication, QWidget, QGroupBox, QSizePolicy, QMessageBox, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controlers.Database import obtener_todos_usuarios, obtener_usuario
from controlers.Conexiones import crear_conexion
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class SetConexionGUI(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones
    color4 = '#7f95ff'  # Fondo secciones
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Establecer Conexion')
        self.setMinimumSize(1200, 800)  # Aumentar tamaño de ventana
        self.setStyleSheet(f'background-color: {self.color5};')
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        # Layout principal vertical para toda la ventana
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
        # Layout horizontal principal (formulario y contenido)
        main_layout = QHBoxLayout()
        # --- Lado izquierdo: Formulario ---
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(30, 30, 30, 30)

        # Agrupa el formulario en un QGroupBox con borde negro
        form_group = QGroupBox()
        form_group.setStyleSheet('QGroupBox { border: 2px solid #000; border-radius: 4px; margin-top: 0.5em; background: none; }')
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)

        # Título
        titulo = QLabel('Establecer Conexion')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont('Arial', 20, QFont.Bold))
        titulo.setStyleSheet(f'color: {self.color1}; background: none;')
        form_layout.addWidget(titulo)

        # Usuario 1
        form_layout.addWidget(QLabel('Usuario 1:'))
        id1_layout = QHBoxLayout()
        label_id1 = QLabel('ID:')
        label_id1.setStyleSheet(f'color: {self.color1}; background: none;')
        id1_layout.addWidget(label_id1)
        self.combo_id1 = QComboBox()
        self.combo_id1.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        id1_layout.addWidget(self.combo_id1)
        self.btn_vaciar_id1 = QPushButton('Vaciar')
        self.btn_vaciar_id1.setFixedWidth(60)
        self.btn_vaciar_id1.setStyleSheet(f'QPushButton {{ background: {self.color3}; color: #fff; border-radius: 8px; padding: 4px 8px; font-size: 12px; }} QPushButton:hover {{ background: {self.color2}; }}')
        self.btn_vaciar_id1.clicked.connect(lambda: self.combo_id1.setCurrentIndex(-1))
        id1_layout.addWidget(self.btn_vaciar_id1)
        form_layout.addLayout(id1_layout)
        self.combo_id1.currentIndexChanged.connect(self.on_id1_selected)

        label_nombre1 = QLabel('Nombre:')
        label_nombre1.setStyleSheet(f'color: {self.color1}; background: none;')
        form_layout.addWidget(label_nombre1)
        self.input_nombre1 = QLineEdit()
        self.input_nombre1.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_nombre1.setEnabled(False)
        form_layout.addWidget(self.input_nombre1)

        label_intereses1 = QLabel('Intereses')
        label_intereses1.setStyleSheet(f'color: {self.color1}; background: none;')
        form_layout.addWidget(label_intereses1)
        self.input_intereses1 = QLineEdit()
        self.input_intereses1.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_intereses1.setEnabled(False)
        form_layout.addWidget(self.input_intereses1)

        # Espacio
        form_layout.addSpacing(20)

        # Usuario 2
        form_layout.addWidget(QLabel('Usuario 2:'))
        id2_layout = QHBoxLayout()
        label_id2 = QLabel('ID:')
        label_id2.setStyleSheet(f'color: {self.color1}; background: none;')
        id2_layout.addWidget(label_id2)
        self.combo_id2 = QComboBox()
        self.combo_id2.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        id2_layout.addWidget(self.combo_id2)
        self.btn_vaciar_id2 = QPushButton('Vaciar')
        self.btn_vaciar_id2.setFixedWidth(60)
        self.btn_vaciar_id2.setStyleSheet(f'QPushButton {{ background: {self.color3}; color: #fff; border-radius: 8px; padding: 4px 8px; font-size: 12px; }} QPushButton:hover {{ background: {self.color2}; }}')
        self.btn_vaciar_id2.clicked.connect(lambda: self.combo_id2.setCurrentIndex(-1))
        id2_layout.addWidget(self.btn_vaciar_id2)
        form_layout.addLayout(id2_layout)
        self.combo_id2.currentIndexChanged.connect(self.on_id2_selected)

        label_nombre2 = QLabel('Nombre:')
        label_nombre2.setStyleSheet(f'color: {self.color1}; background: none;')
        form_layout.addWidget(label_nombre2)
        self.input_nombre2 = QLineEdit()
        self.input_nombre2.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_nombre2.setEnabled(False)
        form_layout.addWidget(self.input_nombre2)

        label_intereses2 = QLabel('Intereses')
        label_intereses2.setStyleSheet(f'color: {self.color1}; background: none;')
        form_layout.addWidget(label_intereses2)
        self.input_intereses2 = QLineEdit()
        self.input_intereses2.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_intereses2.setEnabled(False)
        form_layout.addWidget(self.input_intereses2)

        # Campo Peso y botón establecer conexión
        label_peso = QLabel('Peso:')
        label_peso.setStyleSheet(f'color: {self.color1}; background: none;')
        form_layout.addWidget(label_peso)
        self.input_peso = QLineEdit()
        self.input_peso.setText('1')
        self.input_peso.setStyleSheet(f'background: {self.color4}; border: 1px solid {self.color2}; padding: 6px; color: {self.color1};')
        self.input_peso.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addWidget(self.input_peso)
        self.btn_establecer = QPushButton('Establecer conexion')
        self.btn_establecer.setStyleSheet('background: #c97c7c; color: #111; border-radius: 16px; padding: 8px 20px; font-weight: bold;')
        self.btn_establecer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_establecer.clicked.connect(self.establecer_conexion)
        form_layout.addWidget(self.btn_establecer, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Espacio flexible
        form_layout.addStretch(1)

        # QGroupBox solo para el formulario de los dos usuarios
        form_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(form_group)
        left_layout.addStretch(1)
        main_layout.addLayout(left_layout, 2)
        # --- Lado derecho: Gráfico arriba, sugerencias abajo ---
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(10, 20, 20, 20)
        # Gráfico
        self.graph_widget = QWidget()
        self.graph_widget.setMinimumSize(500, 350)
        self.graph_widget.setStyleSheet('background: #d3d3d3;')
        self.graph_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graph_layout = QVBoxLayout(self.graph_widget)
        graph_layout.addWidget(self.canvas)
        right_layout.addWidget(self.graph_widget, 5)  # Proporción mayor para el gráfico
        # Sugerencias
        self.recom_widget = QWidget()
        self.recom_widget.setMinimumSize(500, 300)
        self.recom_widget.setStyleSheet('background: #f5f5ff; border: 1px solid #888;')
        self.recom_layout = QVBoxLayout(self.recom_widget)
        self.recom_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.addWidget(self.recom_widget, 3)  # Proporción menor para recomendaciones
        self.recom_widget.hide()
        main_layout.addLayout(right_layout, 4)
        main_vlayout.addLayout(main_layout)
        self.cargar_ids()
        self.redibujar_grafo()

    def cargar_ids(self):
        self.combo_id1.blockSignals(True)
        self.combo_id2.blockSignals(True)
        self.combo_id1.clear()
        self.combo_id2.clear()
        usuarios = obtener_todos_usuarios()
        self.id_map = {}
        for usuario in usuarios:
            id_str = str(usuario.get('id', ''))
            self.combo_id1.addItem(id_str)
            self.combo_id2.addItem(id_str)
            self.id_map[id_str] = usuario
        self.combo_id1.setCurrentIndex(-1)
        self.combo_id2.setCurrentIndex(-1)
        self.combo_id1.blockSignals(False)
        self.combo_id2.blockSignals(False)

    def on_id1_selected(self, idx):
        id1 = self.combo_id1.currentText()
        usuario = self.id_map.get(id1)
        if usuario:
            self.input_nombre1.setText(usuario.get('nombre', ''))
            self.input_intereses1.setText(','.join(usuario.get('intereses', [])))
        else:
            self.input_nombre1.setText("")
            self.input_intereses1.setText("")
        self.actualizar_combo2()
        self.redibujar_grafo()
        # Mostrar recomendaciones si el otro campo está vacío
        if id1 and (self.combo_id2.currentIndex() == -1 or not self.combo_id2.currentText()):
            self.mostrar_recomendaciones(id1, 'id1')
        else:
            self.recom_widget.hide()

    def on_id2_selected(self, idx):
        id2 = self.combo_id2.currentText()
        usuario = self.id_map.get(id2)
        if usuario:
            self.input_nombre2.setText(usuario.get('nombre', ''))
            self.input_intereses2.setText(','.join(usuario.get('intereses', [])))
        else:
            self.input_nombre2.setText("")
            self.input_intereses2.setText("")
        self.actualizar_combo1()
        self.redibujar_grafo()
        # Mostrar recomendaciones si el otro campo está vacío
        if id2 and (self.combo_id1.currentIndex() == -1 or not self.combo_id1.currentText()):
            self.mostrar_recomendaciones(id2, 'id2')
        else:
            self.recom_widget.hide()

    def actualizar_combo2(self):
        id1 = self.combo_id1.currentText()
        current_id2 = self.combo_id2.currentText()
        self.combo_id2.blockSignals(True)
        self.combo_id2.clear()
        for id_str in self.id_map:
            if id_str != id1:
                self.combo_id2.addItem(id_str)
        # Restaura selección si es válida
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

    def redibujar_grafo(self):
        self.figure.clear()
        G = nx.Graph()
        id1 = self.combo_id1.currentText()
        id2 = self.combo_id2.currentText()
        if id1 and id2 and id1 != id2:
            G.add_node(id1)
            G.add_node(id2)
            G.add_edge(id1, id2)
        elif id1:
            G.add_node(id1)
        elif id2:
            G.add_node(id2)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=self.figure.add_subplot(111), with_labels=True, node_color='black', font_color='white', node_size=1200)
        self.canvas.draw()

    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def mostrar_recomendaciones(self, id_seleccionado, campo):
        from PyQt5.QtWidgets import QSizePolicy, QSpacerItem
        from controlers.Database import obtener_todos_usuarios, obtener_todas_conexiones
        print(f"[DEBUG] id_seleccionado: {id_seleccionado}")
        self.limpiar_layout(self.recom_layout)
        self.recom_layout.setSpacing(18)
        self.recom_layout.setContentsMargins(8, 8, 8, 8)
        titulo = QLabel('Recomendaciones de conexión:')
        titulo.setStyleSheet(f'color: {self.color1}; font-weight: bold; background: none; font-size: 20px;')
        titulo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.recom_layout.addWidget(titulo)
        usuarios = obtener_todos_usuarios()
        print(f"[DEBUG] usuarios: {usuarios}")
        conexiones = obtener_todas_conexiones()
        conectados = set()
        for c in conexiones:
            if str(c['id1']) == id_seleccionado:
                conectados.add(str(c['id2']))
            elif str(c['id2']) == id_seleccionado:
                conectados.add(str(c['id1']))
        usuario_sel = next((u for u in usuarios if str(u['id']) == id_seleccionado), None)
        print(f"[DEBUG] usuario_sel: {usuario_sel}")
        if not usuario_sel:
            self.recom_widget.hide()
            return
        intereses_sel = set(usuario_sel.get('intereses', []))
        recomendaciones = []
        for u in usuarios:
            if str(u['id']) == str(id_seleccionado) or str(u['id']) in conectados:
                continue
            intereses_u = set(u.get('intereses', []))
            interseccion = intereses_sel & intereses_u
            if len(interseccion) >= 1:
                recomendaciones.append((u, interseccion))
        recomendaciones = sorted(recomendaciones, key=lambda x: -len(x[1]))[:3]
        print(f"[DEBUG] recomendaciones: {recomendaciones}")
        if not recomendaciones:
            sin_label = QLabel('No hay recomendaciones.')
            sin_label.setStyleSheet(f'color: {self.color2}; background: none; font-size: 16px;')
            sin_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.recom_layout.addWidget(sin_label)
        for u, interseccion in recomendaciones:
            box = QGroupBox()
            box.setStyleSheet(f'''QGroupBox {{ background: {self.color5}; border: 2px solid {self.color2}; border-radius: 16px; margin-top: 10px; padding: 10px;}}''')
            box.setMinimumHeight(120)
            box.setMaximumHeight(180)
            box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            box_layout = QVBoxLayout()
            box_layout.setSpacing(14)
            box_layout.setContentsMargins(12, 12, 12, 12)
            box_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            nombre = QLabel(f"{u.get('nombre','')} (ID: {u.get('id')})")
            nombre.setStyleSheet(f'color: {self.color1}; font-weight: bold; font-size: 18px; background: none;')
            nombre.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            intereses = QLabel(f"Intereses en común: {', '.join(interseccion) if interseccion else 'Sin intereses en común'}")
            intereses.setWordWrap(True)
            intereses.setStyleSheet(f'color: {self.color2}; background: none; font-size: 16px;')
            intereses.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            if len(interseccion) >= 3:
                intereses.setStyleSheet(f'color: #fff; background: {self.color3}; font-weight: bold; border-radius: 8px; padding: 8px 16px; font-size: 16px;')
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.addStretch(1)
            btn = QPushButton('Conectar')
            btn.setStyleSheet(f'QPushButton {{ background: {self.color2}; color: #fff; border-radius: 12px; padding: 10px 32px; font-weight: bold; font-size: 16px; }} QPushButton:hover {{ background: {self.color3}; }}')
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, uid=u['id']: self.conectar_recomendado(id_seleccionado, uid, campo))
            btn_layout.addWidget(btn)
            box_layout.addWidget(nombre)
            box_layout.addWidget(intereses)
            box_layout.addLayout(btn_layout)
            box.setLayout(box_layout)
            self.recom_layout.addWidget(box)
        self.recom_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.recom_widget.show()
        self.recom_widget.updateGeometry()
        self.recom_widget.adjustSize()

    def establecer_conexion(self):
        id1 = self.combo_id1.currentText()
        id2 = self.combo_id2.currentText()
        peso = self.input_peso.text()
        res = crear_conexion(id1, id2, peso)
        if res['ok']:
            QMessageBox.information(self, 'Éxito', 'Conexión creada correctamente')
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', res['error'])

    def conectar_recomendado(self, id_seleccionado, id_recomendado, campo):
        # campo: 'id1' o 'id2'
        if campo == 'id1':
            self.combo_id2.setCurrentText(str(id_recomendado))
        else:
            self.combo_id1.setCurrentText(str(id_recomendado))
        self.input_peso.setText('1')
        self.recom_widget.hide()

    def cerrar_ventana(self):
        self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = SetConexionGUI()
    window.show()
    sys.exit(app.exec_())
