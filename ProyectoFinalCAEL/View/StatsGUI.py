from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QSizePolicy, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controlers.Stats import (
    total_usuarios, total_nodos, total_conexiones, usuario_mas_influyente, numero_comunidades, grado_promedio
)

class StatsGUI(QDialog):
    color1 = '#000000'  # Texto principal, bordes
    color2 = '#15284c'  # Fondo botones, encabezados tabla
    color3 = '#435ba0'  # Hover botones, badge
    color4 = '#7f95ff'  # Fondo secciones, separadores
    color5 = '#c9d4ff'  # Fondo general

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Estadísticas')
        self.setMinimumSize(480, 480)
        self.setMaximumSize(600, 600)
        self.setStyleSheet(f'background-color: {self.color5};')
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Título
        titulo = QLabel('Estadísticas')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont('Arial', 28, QFont.Bold))
        titulo.setStyleSheet(f'color: {self.color1}; margin-top: 24px; margin-bottom: 18px; letter-spacing: 1px;')
        main_layout.addWidget(titulo)

        # Cuadro central
        central_widget = QWidget()
        central_widget.setStyleSheet(f'''
            background: {self.color4};
            border-radius: 18px;
            border: 1.5px solid {self.color2};
        ''')
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(32, 28, 32, 28)
        central_layout.setSpacing(0)

        # Estadísticas
        stats = [
            ("Total de Usuarios:", str(total_usuarios())),
            ("Total de Nodos:", str(total_nodos())),
            ("Total de Conexiones:", str(total_conexiones())),
            ("Usuario más influyente:", usuario_mas_influyente() or '-'),
            ("Número de comunidades:", str(numero_comunidades())),
            ("Grado Promedio:", str(grado_promedio())),
        ]
        for i, (label, value) in enumerate(stats):
            row = QHBoxLayout()
            row.setSpacing(18)
            lbl = QLabel(label)
            lbl.setFont(QFont('Arial', 15, QFont.Medium))
            lbl.setStyleSheet(f'color: {self.color1}; background: none;')
            if label.startswith("Usuario más influyente"):
                val = QLabel(value)
                val.setFont(QFont('Arial', 15, QFont.Bold))
                val.setStyleSheet(f'background: {self.color3}; color: white; border-radius: 10px; padding: 2px 14px; letter-spacing: 1px;')
            else:
                val = QLabel(value)
                val.setFont(QFont('Arial', 15, QFont.Bold))
                val.setStyleSheet(f'color: {self.color1}; background: none; letter-spacing: 1px;')
            row.addWidget(lbl)
            row.addStretch(1)
            row.addWidget(val)
            central_layout.addLayout(row)
            # Separador sutil entre filas, menos en la última
            if i < len(stats) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setFrameShadow(QFrame.Plain)
                sep.setStyleSheet(f'color: {self.color2}; background: {self.color2}; min-height: 1px; max-height: 1px; margin-top: 10px; margin-bottom: 10px; border-radius: 1px;')
                central_layout.addWidget(sep)

        main_layout.addStretch(1)
        main_layout.addWidget(central_widget, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addStretch(1)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = StatsGUI()
    window.exec_()
