'''
    Tercer Proyecto Estructuras de Datos I
'''
from ordering_algorithms import *
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tools import generateSave
import random, time

'''
Clase Node: Nodo utilizado en el grafo
    Atributos: id(String), volt(float), current(float)

    Metodos:
    __init__(ident):
        E: Un string que identifia al nodo
        S: -
        R: -
    setVolt(volt):
        E: Obtiene un valor flotante para asociarlo al voltaje
        S: -
        R: -
    setCurrent(cur):
        E: Obtiene un valor flotante para asociarlo al current
        S: -
        R: -
    getVolt():
        E: -
        S: Retorna el voltaje asociado al nodo
        R: -
    getCurrent():
        E: -
        S: Retorna la corriente asociada al nodo
        R: -
    getId():
        E: -
        S: Retorna el identificar del nodo
        R: -
'''


class Node:

    def __init__(self, master, x, y, ident):
        self.master = master
        self.id = ident
        self.position = [x,y]
        self.master = master
        self.x = x*50-5
        self.y = y*50-5
        self.radius = 10
        self.master.create_oval(self.x, self.y, self.x+self.radius, self.y+self.radius, fill="blue")

    def getId(self):
        return self.id


'''
Clase Arc: Arcos utilizados en el grafo, pueden representar tanto una resistencia como una fuente
    Atributos: value(float), component(String), name(String), ohms(float), volts(float)

    Metodos:
    __init__(component, name, value):
        E: Dos string y un valor numerico (preferiblemente float)
        S: -
        R: -
    getValue():
        E: -
        S: El valor asociado al arco (varia con el componente)
        R: -
    getName():
        E: -
        S: El nombre del arco
        R: -
'''

class Arc:
    
    def __init__(self, master, component, name, value, d1, d2):
        self.master = master
        self.d1 = d1
        self.d2 = d2
        self.value = value
        self.component = component
        self.name = name
        self.ohms = 0
        self.volts = 0
        self.current = 0
        if component == "resistor":
            self.ohms = value
            self.volts = round(random.uniform(0, 10), 2)
        elif component == "source":
            self.ohms = 0
            self.volts = value
        self.current = round(random.uniform(0, 1000), 2)

    def getCurrent(self):
        return self.current

    def getValue(self):
        return self.volts

    def getName(self):
        return self.name

    def getComponet(self):
        return self.component

'''
Clase Grafo: Implementacion del grafo por medio de una matriz de adyacencia y una lista que contiene la referencia a los nodos
    Atributos: adMatrix(matriz tridimensional), nodes(lista), nodesCount(entero)

    Metodos:
    checkNode(ident):
        E: Identificador de un nodo (String)
        S: Boolean que indica si el nodo esta en el grafo
        R: -
    getById(ident):
        E: Identificador de un nodo (String) 
        S: La referencia al objeto Node
        R: -
    addNode(ident):
        E: Identificador del nuevo nodo
        S: -
        R: -
    addArc(id1, id2, component, name, value):
        E: Las dos entradas iniciales son los identificadores de los nodos en el camino id1->id2. Luego se agrega el tipo de componente, nombre y valor asociado
        S: -
        R: -
    deleteNode(ident):
        E: Identificador del nodo a eliminar con todos sus arcos asociados
        S: -
        R: El nodo debe estar en el grafo
    getNodes():
        E: -
        S: La lista de nodos del grafo
        R: -
    selectedElements(elems, func): #Funcion auxiliar de dijkstra
        E: Una lista de elementos y una funcion para evaluar dichos elementos
        S: Retorna el elemento menor o mayor segun sea necesario
        R: -
    dijkstra(id1, id2, find):
        E: Los identificadores de los nodos entre los que se busca el camino especifico, mientras que la variable find indica si es el mas largo o mas corto
        S: El camino mas corto o largo entre los nodos segun lo deseado 
        R: -
    
'''

class Graph:

    def __init__(self):
        self.adMatrix = []
        self.nodes = []  # Nodos
        self.nodesCount = 0

    def checkNode(self, ident):
        checked = False
        for i in self.nodes:
            if i.getId() == ident:
                checked = True
                break
        return checked

    def getById(self, ident):
        for i in self.nodes:
            if i.getId() == ident:
                return i

    def addNode(self, master, x, y, ident):
        self.nodesCount += 1
        self.nodes += [Node(master, x, y, ident)]
        if self.nodesCount == 1:
            self.adMatrix += [[[None]]]
        else:
            tmp = []
            for i in range(self.nodesCount):
                tmp_aij = []
                for j in range(self.nodesCount):
                    tmp_aij += [[None]]
                tmp += [tmp_aij]

            trans = self.adMatrix
            for i in range(self.nodesCount - 1):
                for j in range(self.nodesCount - 1):
                    tmp[i][j] = trans[i][j]
            self.adMatrix = tmp

    def addArc(self, master, id1, id2, component, name, value, d1, d2):
        arc = Arc(master, component, name, value, d1, d2)
        if self.checkNode(id1) and self.checkNode(id2):
            index1 = self.nodes.index(self.getById(id1))
            index2 = self.nodes.index(self.getById(id2))
            if self.adMatrix[index1][index2] != [None]:
                self.adMatrix[index1][index2] += [arc]
            else:
                self.adMatrix[index1][index2] = [arc]
                
            print("Se ha creado arco entre "+id1+" y "+id2)
        else:
            print("No se puede crear una relación")

    def deleteNode(self, ident):  # Elimina los arcos asociados a ese nodo tanto de ida como de vuleta
        if self.checkNode(ident):
            tmp = []
            self.nodesCount -= 1
            ind = self.nodes.index(self.getById(ident))
            self.nodes.pop(ind)
            self.adMatrix.pop(ind)
            for i in self.adMatrix:
                i.pop(ind)

    def getNodes(self):
        return self.nodes

    def printGraph(self):
        for i in self.adMatrix:
            print("[", end="")
            for j in i:
                print("[", end="")
                for x in j:
                    if x != None:
                        print(x.component + ":" + str(x.value) + " ", end="")
                    else:
                        print("None ", end="")
                print("]", end="")

            print("]")

    def getDictRes(self):  # Retorna un diccionario con los nombres de resistencias y sus nombres
        result = {}
        for i in self.adMatrix:
            for j in i:
                for x in j:
                    if x != None:
                        temp = {x.component: x.value}
                        result.update(temp)
        return result

    def getRes(self):  # Retorna una lista con las resistencias desordenadas
        result = []
        for i in self.adMatrix:
            for j in i:
                for x in j:
                    if x != None:
                        result += [x.value]
        return result

    def selectedElement(self, elems, func):
        selected = elems[0]
        for elem in elems:
            if func(elem.getValue(), selected.getValue()):
                selected = elem
        return selected

    def dijkstra(self, id1, id2, find):
        funct = None
        mat = []
        if find:
            funct = lambda a, b: a > b
        else:
            funct = lambda a, b: a < b

        for i in self.adMatrix:
            mat_ij = []
            for j in i:
                if j != [None]:
                    mat_ij += [self.selectedElement(j, funct)]
                else:
                    mat_ij += [None]
            mat += [mat_ij]
        for i in mat:
            print("[", end="")
            for j in i:
                if j != None:
                    print(j.getValue(), end=" ")
                else:
                    print("None", end=" ")
            print("]")

        queue = [id1]
        output = []
        arcs = []
        initial = self.getById(id1)
        final = self.getById(id2)
        finished = False
        chart = []

        for i in range(self.nodesCount):
            chart_i = [self.nodes[i].getId(), -1, ""]
            chart += [chart_i]

        for i in chart:
            print(i)

        while not finished:

            if queue == []:
                print("No hay camino hacia ese nodo")
                finished = True
                break
            current = queue[0]
            current_i = self.nodes.index(self.getById(current))
            queue = queue[1:]
            # print(current)
            if current == initial.getId():
                chart[current_i][1] = 0
            else:
                preds = []
                values = []
                pred = ""
                path = -1
                for i in mat:
                    if i[current_i] != None:
                        values += [i[current_i].getValue()]
                        preds += [mat.index(i)]
                # print(preds, values)

                tmp_path = 0
                for i in range(len(preds)):
                    if chart[preds[i]][1] != -1:
                        tmp_path = values[i] + chart[preds[i]][1]
                    if path == -1:
                        path = tmp_path
                        pred = chart[preds[i]][0]
                    else:
                        if funct(tmp_path, path):
                            path = tmp_path
                            pred = chart[preds[i]][0]

                chart[current_i][1] = path
                chart[current_i][2] = pred

                for i in chart:
                    print(i)

            for j in range(len(mat[current_i])):
                if mat[current_i][j] != None and not self.nodes[j].getId() in queue:
                    queue += [self.nodes[j].getId()]

            if current == final.getId():
                tmp = final.getId()
                tmp_i = current_i
                output += [final.getId()]
                while tmp != initial.getId():
                    # print(tmp)
                    output += [chart[tmp_i][2]]
                    tmp = chart[tmp_i][2]
                    tmp_i = self.nodes.index(self.getById(tmp))
                finished = True
                break
        twist_out = []
        for x in output:
            twist_out = [x] + twist_out
        output = twist_out

        for o in range(len(output)):
            if o + 1 < len(output):
                i = self.nodes.index(self.getById(output[o]))
                j = self.nodes.index(self.getById(output[o + 1]))
                arcs += [mat[i][j]]
            else:
                break
        for i in arcs:
            print(i.getName())
        print(output)
