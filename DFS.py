from flask import Flask, render_template, request
from Arbol import Nodo
PythonDebugger = True

app = Flask(__name__)

def buscar_solucion_DFS_Rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        # Expandir los nodos sucesores (hijos)
        dato_nodo = nodo_inicial.get_datos()
        hijo_izquierdo = Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]])
        hijo_central = Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]])
        hijo_derecho = Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
        nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

        for nodo_hijo in nodo_inicial.get_hijos():
            if nodo_hijo.get_datos() not in visitados:
                # Llamada Recursiva
                sol = buscar_solucion_DFS_Rec(nodo_hijo, solucion, visitados)
                if sol is not None:
                    return sol

        return None

# En tu función de vista
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener datos del formulario
        estado_inicial = [int(x) for x in request.form['estado_inicial'].split(',')]
        solucion = [int(x) for x in request.form['solucion'].split(',')]
        
        # Realizar la búsqueda DFS
        visitados = []
        nodo_inicial = Nodo(estado_inicial)
        nodo_solucion = buscar_solucion_DFS_Rec(nodo_inicial, solucion, visitados)

        # Reconstruir el camino hacia la solución
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.insert(0, nodo.get_datos())
            nodo = nodo.get_padre()

        # Invertir el orden de la lista en Python
        resultado = list(reversed(resultado))

        return render_template('resultado.html', resultado=resultado)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
