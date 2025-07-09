from Models.Grafos import Grafo, detectar_comunidades_label_propagation
from controlers.Database import obtener_todos_usuarios, obtener_todas_conexiones


def obtener_datos_comunidades():
    """
    Construye el grafo a partir de la base de datos y detecta comunidades.
    Retorna:
        comunidades: {id_comunidad: [ids de usuarios]}
        info_extra: dict con datos estadísticos
        usuarios_dict: {id_usuario: datos_usuario}
    """
    usuarios = obtener_todos_usuarios()
    conexiones = obtener_todas_conexiones()
    grafo = Grafo()
    usuarios_dict = {}
    # Agregar nodos
    for usuario in usuarios:
        grafo.agregar_nodo(str(usuario['id']))
        usuarios_dict[str(usuario['id'])] = usuario
    # Agregar aristas
    for conexion in conexiones:
        grafo.agregar_arista(str(conexion['id1']), str(conexion['id2']))
    comunidades, info_extra = detectar_comunidades_label_propagation(grafo)
    return comunidades, info_extra, usuarios_dict 