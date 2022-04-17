import numpy as np
from collections import deque
import pandas as pd
datos = pd.read_csv('calles_de_medellin_con_acoso.csv', sep = ';',)
datos.harassmentRisk = datos.harassmentRisk.fillna(datos.harassmentRisk.mean())
grafo= {}
origenes_unicos = datos.origin.unique()
# En este ciclo, se crea grafo como diccionario de diccionarios. 
# Inicialmente, las llaves son los origenes
# que estan en el dataframe 'datos'
# Y los valores son diccionarios vacios.
for i in range(len(origenes_unicos)):
    grafo[origenes_unicos[i]] = {}
 
# Se completa el grafo. En el diccionario de cada valor,
# las llaves son los destinos, y los valores son
# la distancia y el porcentaje de acoso para ese destino
# Se tiene en cuenta el valor de 'oneway' en el dataframe, 
# ya que si es Verdadero, la relacion origen-destino es simetrica, y se debe
# añadir en ambos sentidos al diccionario.
for i in datos.index:
    if datos["oneway"][i]==False:
        grafo[datos["origin"][i]][datos["destination"][i]]=(datos["length"][i],datos["harassmentRisk"][i])
    else:
        grafo[datos["origin"][i]][datos["destination"][i]]=(datos["length"][i],datos["harassmentRisk"][i])
        try:
            grafo[datos["destination"][i]][datos["origin"][i]]=(datos["length"][i],datos["harassmentRisk"][i])
        except KeyError: # Este error se da cuando, el valor de 'oneway' es verdadero, y el destino debe ser un origen en el diccionario.
                         # En ciertos casos, ese destino no se encontraba como origen en el dataframe, por lo que no se encontraba en 
                         # 'grafos' y tratar de acceder a este genera 'KeyError'. La solucion es simplemente
                         # añadirlo como una nueva llave y crear el otro diccionario en el valor.
            grafo[datos['destination'][i]]={datos["origin"][i]:(datos["length"][i],datos["harassmentRisk"][i])}
 
def obtenerMenor(dist,unvisited):
    menor = 400000
    llave = ''
    for vertice in unvisited:
	    if dist[vertice] <= menor:
             menor = dist[vertice]
             llave = vertice
	
    return llave	
def printPath(parent, j):
	#Base Case : If j is source
	if parent[j] == -1 :
		print(j,end=" ")
		return
	printPath(parent , parent[j])
	print (j,end="->")
 
def dijkstraDist(start,target,graph):
    dist = dict()
    parent=dict()
    unvisited = deque()
    for key in graph:
        parent[key]=-1
        dist[key] = 1e7
        unvisited.appendleft(key)
    dist[start] = 0
    while len(unvisited) != 0:
        actual = obtenerMenor(dist,unvisited)
        if actual == target: break
        unvisited.remove(actual)
        for adyacente in graph[actual]:
            alt = dist[actual] + graph[actual][adyacente][0]
            if alt < dist[adyacente]:
                    parent[adyacente] = actual
                    dist[adyacente] = alt		
    printPath(parent,target)
    print()
    print(dist[target])
 


def dijkstraAcoso(start,target,graph):
    acoso = dict()
    parent=dict()
    unvisited = deque()
    for key in graph:
        parent[key]=-1
        acoso[key] = 1e7
        unvisited.appendleft(key)
    acoso[start] = 0
    while len(unvisited) != 0:
        actual = obtenerMenor(acoso,unvisited)
        if actual == target: break
        unvisited.remove(actual)
        for adyacente in graph[actual]:
            alt = acoso[actual] + graph[actual][adyacente][1]
            if alt < acoso[adyacente]:
                    parent[adyacente] = actual
                    acoso[adyacente] = alt	
    printPath(parent,target)
    print()
    print(acoso[target])
