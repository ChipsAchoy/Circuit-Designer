'''
    Tercer Proyecto Estructuras de Datos I
'''


class Node:

    def __init__(self, ident):
        self.id = ident
        self.volt = 0
        self.current = 0

    def setVolt(self, volt):
        self.volt = volt

    def setCurrent(self, cur):
        self.current = cur

    def getVolt(self):
        return self.volt

    def getCurrent(self):
        return self.current

    def getId(self):
        return self.id


class Arc:

    def __init__(self, component, value=0):
        self.value = value
        self.component = component
        '''
        self.ohms = 0
        self.volts = 0
        if component == "resistor":
            self.ohms = value
        elif component == "source":
            self.volts = value
        '''
    def getValue(self):
        return self.value


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

    def addNode(self, ident):
        self.nodesCount += 1
        self.nodes += [Node(ident)]
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

    def addArc(self, id1, id2, component, value=0):
        arc = Arc(component, value)
        if self.checkNode(id1) and self.checkNode(id2):
            index1 = self.nodes.index(self.getById(id1))
            index2 = self.nodes.index(self.getById(id2))
            if self.adMatrix[index1][index2] != [None]:
                self.adMatrix[index1][index2] += [arc]
            else:
                self.adMatrix[index1][index2] = [arc]
                
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

    def getDictRes(self): #Retorna un diccionario con los nombres de resistencias y sus nombres
        result = {}
        for i in self.adMatrix:
            for j in i:
                if j != None:
                    temp = {j.component: j.value}
                    result.update(temp)
        return result

    def getRes(self): #Retorna una lista con las resistencias desordenadas
        result = []
        for i in self.adMatrix:
            for j in i:
                if j != None:
                    result+=[j.value]
        return result

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
                if find:
                    mat_ij += [max(j)]
                else:
                    mat_ij += [min(j)]

        print(mat)
        queue = [id1]
        visted = []
        output = []
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
                for i in self.adMatrix:
                    if i[current_i] != None:
                        values += [i[current_i].getValue()]
                        preds += [self.adMatrix.index(i)]
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

            for j in range(len(self.adMatrix[current_i])):
                if self.adMatrix[current_i][j] != None and not self.nodes[j].getId() in queue:
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
        print(output)


def radixSort(listIn):
    n = 0
    biggest = 0
    for elem in listIn:
        if elem > biggest:
            biggest = elem
        n += 1
    biggest = len(str(biggest))
    print(biggest)
    print(listIn)

    for x in range(biggest):
        print("###########################")
        listOut = []
        for i in range(len(listIn)):
            listOut += [0]
        digit = 10 ** x
        integers = []
        for i in range(10):
            integers += [0]
        for elem in listIn:
            dig = (elem // digit) % 10
            # print(dig)
            integers[dig] += 1
        for i in range(len(integers)):
            if i != 0:
                integers[i] += integers[i - 1]
        # print(integers)
        print(listIn)
        for i in range(len(listIn)):
            n = len(listIn) - (i + 1)
            dig = (listIn[n] // digit) % 10
            integers[dig] -= 1
            num = listIn[n]
            listOut[integers[dig]] = num
        print(listOut)
        listIn = listOut
    return listOut


def insertionSort(listOrd):
    position = 1
    while position < len(listOrd):
        ordered = False
        i = position
        while not ordered:
            if listOrd[i] > listOrd[i - 1] and i != 0:
                tmp = listOrd[i]
                listOrd[i] = listOrd[i - 1]
                listOrd[i - 1] = tmp
                i -= 1
            else:
                ordered = True
        position += 1

    return listOrd

def searchNameRes(dictionary, list): #Busca el nombre de las resistencias tomando un diccionario con estas y una lista ordenada de las resistencias
    result = {}
    for i in list:
        for j in dictionary:
            if i == dictionary.get(j):
                temp = {j:i}
                result.update(temp)
    return result

def main():
    
    """
    print(radixSort([170, 45, 75, 90, 802, 24, 2, 66]))
    print(insertionSort([170, 45, 75, 90, 802, 24, 2, 66]))
    """

    graph = Graph()
    graph.addNode("A")
    graph.addNode("B")
    graph.addNode("C")
    graph.addNode("D")
    graph.addNode("E")
    graph.addArc("A", "B", "R1", 10)
    graph.addArc("A", "B", "R8", 40)
    graph.addArc("B", "C", "R2", 20)
    graph.addArc("B", "D", "R3", 40)
    graph.addArc("C", "D", "R4", 10)
    graph.addArc("A", "C", "R5", 40)
    graph.addArc("C", "E", "R6", 40)
    graph.addArc("D", "A", "R7", 20)
    graph.printGraph()
    graph.dijkstra("A", "B", False)
    # graph.dijkstra("D", "E", False)
    #slist = insertionSort(graph.getRes())
    #searchNameRes(graph.getDictRes(),slist)

main()
