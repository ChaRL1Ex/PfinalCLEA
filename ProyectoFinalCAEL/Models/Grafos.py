class Grafo:
    def __init__(self):
        # Diccionario de adyacencia: {id: {vecino_id: peso, ...}}
        self.adyacencia = {}

    def agregar_nodo(self, id):
        if id not in self.adyacencia:
            self.adyacencia[id] = {}

    def agregar_arista(self, id1, id2, peso=1):
        self.agregar_nodo(id1)
        self.agregar_nodo(id2)
        self.adyacencia[id1][id2] = peso
        self.adyacencia[id2][id1] = peso  # Grafo no dirigido

    def obtener_vecinos(self, id):
        return self.adyacencia.get(id, {})

    def obtener_aristas(self):
        aristas = set()
        for id1 in self.adyacencia:
            for id2, peso in self.adyacencia[id1].items():
                if (id2, id1) not in aristas:
                    aristas.add((id1, id2, peso))
        return list(aristas)

    def existe_arista(self, id1, id2):
        return id2 in self.adyacencia.get(id1, {})

def detectar_comunidades_label_propagation(grafo):
    """
    Detecta comunidades en un grafo no dirigido usando Label Propagation.
    Retorna:
        comunidades_dict: {id_comunidad: [lista de ids de usuarios]}
        info_extra: {
            'total_comunidades': int,
            'tamanos': {id_comunidad: tamaño},
            'total_usuarios': int,
            'porcentaje_por_comunidad': {id_comunidad: float},
            'conexiones_por_comunidad': {id_comunidad: int}
        }
    """
    import random
    nodos = list(grafo.adyacencia.keys())
    if not nodos:
        return {}, {}
    # Inicializar etiquetas
    etiquetas = {nodo: nodo for nodo in nodos}
    cambiado = True
    while cambiado:
        cambiado = False
        nodos_aleatorios = nodos[:]
        random.shuffle(nodos_aleatorios)
        for nodo in nodos_aleatorios:
            vecinos = list(grafo.obtener_vecinos(nodo).keys())
            if not vecinos:
                continue
            # Contar etiquetas de vecinos
            etiquetas_vecinos = {}
            for v in vecinos:
                etiqueta = etiquetas[v]
                etiquetas_vecinos[etiqueta] = etiquetas_vecinos.get(etiqueta, 0) + 1
            # Elegir la etiqueta más frecuente (desempate aleatorio)
            max_freq = max(etiquetas_vecinos.values())
            etiquetas_max = [e for e, f in etiquetas_vecinos.items() if f == max_freq]
            nueva_etiqueta = random.choice(etiquetas_max)
            if etiquetas[nodo] != nueva_etiqueta:
                etiquetas[nodo] = nueva_etiqueta
                cambiado = True
    # Agrupar por etiquetas
    comunidades = {}
    for nodo, etiqueta in etiquetas.items():
        comunidades.setdefault(etiqueta, []).append(nodo)
    # Calcular datos extra
    total_usuarios = len(nodos)
    total_comunidades = len(comunidades)
    tamanos = {k: len(v) for k, v in comunidades.items()}
    porcentaje_por_comunidad = {k: len(v)/total_usuarios*100 for k, v in comunidades.items()}
    # Conexiones por comunidad
    conexiones_por_comunidad = {}
    for etiqueta, miembros in comunidades.items():
        conexiones = 0
        for nodo in miembros:
            for vecino in grafo.obtener_vecinos(nodo):
                if vecino in miembros:
                    conexiones += 1
        conexiones_por_comunidad[etiqueta] = conexiones // 2  # Cada arista contada dos veces
    info_extra = {
        'total_comunidades': total_comunidades,
        'tamanos': tamanos,
        'total_usuarios': total_usuarios,
        'porcentaje_por_comunidad': porcentaje_por_comunidad,
        'conexiones_por_comunidad': conexiones_por_comunidad
    }
    return comunidades, info_extra
