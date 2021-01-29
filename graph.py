'''
    Tercer Proyecto Estructuras de Datos I
'''


import tkinter
from tools import *
import random

'''
Clase Node: Nodo utilizado en el grafo
    Atributos: id(String), volt(float), current(float)

    Metodos:
    __init__(ident):
        E: Un string que identifia al nodo
        S: -
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
        self.x = x
        self.y = y
        self.x_pos = x*50-5
        self.y_pos = y*50-5
        self.radius = 10
        self.master.create_oval(self.x_pos, self.y_pos, self.x_pos+self.radius, self.y_pos+self.radius, fill="blue")
        tituloNodo = tkinter.Label(self.master, text="Node_" + str(self.position[0]) + "_" + str(self.position[1]), bg="white", fg="black", font="Bahnschrift 8 bold")
        tituloNodo.place(x=x * 50 - 40, y=y * 50 - 30)

    def getId(self):
        return self.id


'''
Clase Arc: Arcos utilizados en el grafo, pueden representar tanto una resistencia como una fuente
    Atributos: value(float), component(String), name(String), ohms(float), volts(float)

    Metodos:
    __init__(component, name, value, d1, d2, direction):
        E: Dos string, un valor numerico (preferiblemente float), dos listas de enteros y una lista de string
        S: -
        R: -
    getValue():
        E: -
        S: El valor asociado al arco (varia con el componente)
        R: -
    getCurrent():
        E: -
        S: El valor de corriente
        R: -
    getVolt():
        E: -
        S: El valor del voltaje
        R: -
    getName():
        E: -
        S: El nombre del arco
        R: -
'''

class Arc:
    
    def __init__(self, master, component, name, value, d1, d2, direction):
        self.master = master
        self.d1 = d1
        self.d2 = d2
        self.direction = direction
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
Clase Graph: Implementacion del grafo por medio de una matriz de adyacencia y una lista que contiene la referencia a los nodos
    Atributos: adMatrix(matriz tridimensional), nodes(lista), nodesCount(entero)

    Metodos:
    __init__()
    checkNode(ident):
        E: Identificador de un nodo (String)
        S: Boolean que indica si el nodo esta en el grafo
        R: -
    getById(ident):
        E: Identificador de un nodo (String) 
        S: La referencia al objeto Node
        R: -
    addNode(master, x, y, ident):
        E: canvas donde se dibuja el nodo, posicion en x y en y en escala de la cuadricula, Identificador del nuevo nodo
        S: -
        R: -
    addArc(master, id1, id2, component, name, value, d1, d2):
        E: canvas donde se dibuja el arco, Las dos entradas iniciales son los identificadores de los nodos en el camino id1->id2. Luego se agrega el tipo de componente, nombre, valor asociado y las dos posiciones inicial y final
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
    dijkstra(find, master):
        E: la variable find indica si es el mas largo o mas corto, master es el canvas que se toma de referencia
        S: El camino mas corto o largo entre los nodos segun lo deseado 
        R: -
    
    drawLine(self,master,x1,y1,x2,y2,type,cant, name, value, dij=False, col=False)
        E: las coordenadas de los dos puntos, el tipo de elemento, la cantidad, nombre, valor, un condicional para cuando se usa dijkstra
        y otro condicional para un selector de color.
        S: Dibuja dos líneas entre los dos puntos con la figura de una resitencia/fuente de poder. 
        R: ---
'''

class Graph:

    def __init__(self):
        self.adMatrix = []
        self.nodes = []  # Nodos
        self.nodesCount = 0
        self.inicio = None
        self.final = None

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
        print("se ha creado un nodo")
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

        if self.checkNode(id1) and self.checkNode(id2):
            index1 = self.nodes.index(self.getById(id1))
            index2 = self.nodes.index(self.getById(id2))
            if self.adMatrix[index1][index2] != [None]:
                print("más")
                arc = self.drawLine(master, d1[0], d1[1], d2[0], d2[1],
                                          component,len(self.adMatrix[index1][index2]),name,value)
                self.adMatrix[index1][index2] += [arc]
                print(len(self.adMatrix[index1][index2]))
            else:
                print("solito")
                arc = self.drawLine(master, d1[0], d1[1], d2[0], d2[1],
                                          component,0,name,value)
                self.adMatrix[index1][index2] = [arc]

            print("Se ha creado arco entre "+id1+" y "+id2+" en"+str(d1)+"-"+str(d2))
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
        #for i in range(9):
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

    def dijkstra(self, find, master):
        id1 = self.inicio
        id2 = self.final
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
            self.drawLine(master, self.getFirstIn(i)[0], self.getFirstIn(i)[1], i.d2[0], i.d2[1], i.component, self.getPositionIn(i), i.name, i.value, True, True)
            #d1[0], d1[1], d2[0], d2[1],
            #component, len(self.adMatrix[index1][index2]), name, value
        print(output)

    def getPositionIn(self, elem):
        for i in self.adMatrix:
            for j in i:
                for x in range(len(j)):
                    if j[x] == elem:
                        return x

    def getFirstIn(self, elem):
        for i in self.adMatrix:
            for j in i:
                for x in range(len(j)):
                    if j[x] == elem:
                        return [j[0].d1[0], j[0].d1[1]]


    def drawLine(self,master,x1,y1,x2,y2,type,cant, name, value, dij=False, col=False):
        direction = [None, None]
        multiplier = 30
        label_position = [0,0]
        color = None
        if col:
            color = "#474CFF"
        else:
            color = "#000000"
        if biggestLine(x1, y1, x2, y2):  # Dibuja en x
            if y1 - y2 == 0:
                label_position = [max([x1, x2]) -abs(x1-x2)//2, y1+20*cant]
                print("Recta")
                direction[0] = "horizontal"
                master.create_line(x1,y1,x1,y1 + cant * multiplier,width=5, fill = color)
                master.create_line(x2,y2,x2,y2+ cant * multiplier,width=5, fill = color)
                y1 = y1 + cant * multiplier
                if x1 - x2 > 0:
                    master.create_line(x1, y1, x2 + calcDis(x1, x2), y1,
                                            width=5, fill = color)
                    master.create_line(x1 - calcDis(x1, x2), y1, x2, y1,
                                            width=5, fill = color)
                    createResImage(master, x1 - calcDis(x1, x2), y1,
                                   x2 + calcDis(x1, x2), y1, True, type)
                else:
                    master.create_line(x1, y1, x2 - calcDis(x1, x2), y1,
                                            width=5, fill = color)
                    master.create_line(x1 + calcDis(x1, x2), y1, x2, y1,
                                            width=5, fill = color)
                    createResImage(master, x2 - calcDis(x1, x2), y1,
                                   x1 + calcDis(x1, x2), y1, True, type)

            elif (y1 - y2 < 0 and x1 - x2 < 0) or (
                    y1 - y2 > 0 and x1 - x2 < 0):
                print("Abajo")
                direction[1] = "abajo"
                y1 = y1 + cant * multiplier
                master.create_line(x1, y1, x1, y1 - cant * multiplier, width=5, fill = color)

                master.create_line(x1, y1, x2 - calcDis(x1, x2), y1, width=5, fill = color)
                master.create_line(x1 + calcDis(x1, x2), y1, x2, y1, width=5, fill = color)
                createResImage(master, x2 - calcDis(x1, x2), y1,
                               x1 + calcDis(x1, x2), y1, True, type)
                master.create_line(x2, y2, x2, y1, width=5, fill = color)
                label_position = [max([x1, x2]) - abs(x1-x2)//2, y1+20*cant]

            else:
                print("Arriba")
                direction[1] = "arriba"
                y1 = y1 - cant * multiplier
                master.create_line(x1, y1, x1, y1 + cant * multiplier, width=5, fill = color)
                master.create_line(x1, y1, x2 + calcDis(x1, x2), y1, width=5, fill = color)
                master.create_line(x1 - calcDis(x1, x2), y1, x2, y1, width=5, fill = color)
                createResImage(master, x1 - calcDis(x1, x2), y1,
                               x2 + calcDis(x1, x2), y1, True, type)
                master.create_line(x2, y2, x2, y1, width=5, fill = color)
                label_position = [max([x1, x2]) - abs(x1-x2)//2, y1+20*cant]

        else:  # Dibuja en y
            if x1 - x2 == 0:  # Linea recta
                label_position = [x1+20*cant, max([y1, y2]) - abs(y1 - y2) // 2]
                direction[1] = "vertical"
                x1 = x1 - cant * multiplier
                master.create_line(x1, y1, x1+cant * multiplier, y1, width=5, fill = color)
                master.create_line(x1, y1, x2+cant * multiplier, y1, width=5, fill = color)
                if y1 - y2 > 0:
                    master.create_line(x1, y1, x1, y2 + calcDis(y1, y2),
                                            width=5, fill = color)
                    master.create_line(x1, y1 - calcDis(y1, y2), x1, y2,
                                            width=5, fill = color)
                    createResImage(master, x1, y1 - calcDis(y1, y2), x1,
                                   y2 + calcDis(y1, y2), False, type)
                else:
                    master.create_line(x1, y1, x1, y2 - calcDis(y1, y2),
                                            width=5, fill = color)
                    master.create_line(x1, y1 + calcDis(y1, y2), x1, y2,
                                            width=5, fill = color)
                    createResImage(master, x1, y2 - calcDis(y1, y2), x1,
                                   y1 + calcDis(y1, y2), False, type)

            elif (x1 - x2 < 0 and y1 - y2 < 0) or (x1 - x2 > 0 and y1 - y2 < 0):
                label_position = [x1 + 20*cant, max([y1, y2]) - abs(y1 - y2) // 2]
                print("Izquierda")
                direction[0] = "izquierda"
                x1 = x1 + cant * multiplier
                master.create_line(x1, y1, x1 - cant * multiplier, y1, width=5, fill = color)
                master.create_line(x1, y1, x1, y2 - calcDis(y1, y2), width=5, fill = color)
                master.create_line(x1, y1 + calcDis(y1, y2), x1, y2, width=5, fill = color)
                createResImage(master, x1, y2 - calcDis(y1, y2), x1,
                               y1 + calcDis(y1, y2), False, type)
                master.create_line(x2, y2, x1, y2, width=5, fill = color)
            else:
                print("Derecha")
                label_position = [x1 + 20*cant, max([y1, y2]) - abs(y1 - y2) // 2]
                direction[0] = "derecha"
                x1 = x1 - cant * multiplier
                master.create_line(x1, y1, x1 + cant * multiplier, y1, width=5, fill = color)

                master.create_line(x1, y1, x1, y2 + calcDis(y1, y2),
                                        width=5, fill = color)
                master.create_line(x1, y1 - calcDis(y1, y2), x1, y2,
                                        width=5, fill = color)
                createResImage(master, x1, y1 - calcDis(y1, y2), x1,
                               y2 + calcDis(y1, y2), False, type)
                master.create_line(x2, y2, x1, y2, width=5, fill = color)

        print([x1, y1,], [x2,y2])
        if not dij:
            arc = Arc(master, type, name, value, [x1,y1], [x2,y2], direction)
            tituloArc = tkinter.Label(master, text=arc.name,
                                       bg="white", fg="black", font="Bahnschrift 10 bold")
            tituloArc.place(x=label_position[0], y=label_position[1])
            return arc