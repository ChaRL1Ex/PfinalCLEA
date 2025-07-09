from controlers.Database import agregar_conexion

def crear_conexion(id1, id2, peso):
    # Validación básica
    if not id1 or not id2 or id1 == id2:
        return {'ok': False, 'error': 'IDs inválidos o iguales'}
    try:
        peso = float(peso)
    except ValueError:
        return {'ok': False, 'error': 'El peso debe ser un número'}
    # Forzar tipo correcto para TinyDB
    if str(id1).isdigit():
        id1 = int(id1)
    if str(id2).isdigit():
        id2 = int(id2)
    conexion = {'id1': id1, 'id2': id2, 'peso': peso}
    return agregar_conexion(conexion)

def calcular_distancia_y_ruta(id1, id2):
    """
    Calcula la distancia mínima (en número de conexiones) y la ruta entre dos usuarios.
    Retorna (distancia, ruta) o (None, []) si no hay conexión.
    """
    from controlers.Database import obtener_todas_conexiones
    id1 = str(id1)
    id2 = str(id2)
    conexiones = obtener_todas_conexiones()
    # Construir grafo como diccionario de adyacencia
    grafo = {}
    for c in conexiones:
        a, b = str(c['id1']), str(c['id2'])
        grafo.setdefault(a, set()).add(b)
        grafo.setdefault(b, set()).add(a)
    # BFS
    from collections import deque
    visitados = set()
    cola = deque([(id1, [id1])])
    while cola:
        actual, ruta = cola.popleft()
        if actual == id2:
            return len(ruta)-1, ruta
        visitados.add(actual)
        for vecino in grafo.get(actual, []):
            if vecino not in visitados and vecino not in [n for n in ruta]:
                cola.append((vecino, ruta + [vecino]))
    return None, []
