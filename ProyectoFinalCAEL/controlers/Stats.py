from controlers.Database import obtener_todos_usuarios, obtener_todas_conexiones
import networkx as nx

def total_usuarios():
    return len(obtener_todos_usuarios())

def total_nodos():
    return len(obtener_todos_usuarios())

def total_conexiones():
    return len(obtener_todas_conexiones())

def usuario_mas_influyente():
    usuarios = obtener_todos_usuarios()
    conexiones = obtener_todas_conexiones()
    G = nx.Graph()
    for u in usuarios:
        G.add_node(str(u['id']), nombre=u['nombre'])
    for c in conexiones:
        G.add_edge(str(c['id1']), str(c['id2']))
    if G.number_of_nodes() == 0:
        return None
    grados = dict(G.degree())
    if not grados:
        return None
    max_id = max(grados, key=lambda k: grados[k])
    nombre = G.nodes[max_id].get('nombre', str(max_id))
    return nombre

def numero_comunidades():
    usuarios = obtener_todos_usuarios()
    conexiones = obtener_todas_conexiones()
    G = nx.Graph()
    for u in usuarios:
        G.add_node(str(u['id']))
    for c in conexiones:
        G.add_edge(str(c['id1']), str(c['id2']))
    comunidades = list(nx.connected_components(G))
    return len(comunidades)

def grado_promedio():
    usuarios = obtener_todos_usuarios()
    conexiones = obtener_todas_conexiones()
    G = nx.Graph()
    for u in usuarios:
        G.add_node(str(u['id']))
    for c in conexiones:
        G.add_edge(str(c['id1']), str(c['id2']))
    if G.number_of_nodes() == 0:
        return 0
    grados_view = G.degree()
    if not hasattr(grados_view, '__iter__'):
        return 0
    grados = dict(grados_view)
    return round(sum(int(v) for v in grados.values()) / G.number_of_nodes(), 2) 