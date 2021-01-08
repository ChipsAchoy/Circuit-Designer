'''
    Tercer Proyecto Estructuras de Datos I
'''



class Node:
    def __init__(self, ident, component):
        self.id = ident
        self.comp = component

    def getId(self):
        return self.id

class Graph:

    def __init__(self):
        self.adMatrix = []
        self.nodes = [] #Nodos 
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
        
    def addNode(self, ident, component):
        self.nodesCount += 1
        self.nodes += [Node(ident, component)]
        if self.nodesCount == 1:
            self.adMatrix += [[0]]
        else:
            tmp = []
            for i in range(self.nodesCount):
                tmp_aij = []
                for j in range(self.nodesCount):
                    tmp_aij += [0]
                tmp += [tmp_aij]
                
            trans = self.adMatrix
            for i in range(self.nodesCount - 1):
                for j in range(self.nodesCount - 1):
                    tmp[i][j] = trans[i][j]
            self.adMatrix = tmp
            
    def addArc(self, id1, id2, value):
        if self.checkNode(id1) and self.checkNode(id2):
            index1 = self.nodes.index(self.getById(id1))
            index2 = self.nodes.index(self.getById(id2))
            
            self.adMatrix[index1][index2] = value

    def getNodes(self):
        return self.nodes
    
    def printGraph(self):
        print(self.adMatrix)


def main():
    graph = Graph()
    graph.addNode("1", "resistor")
    graph.printGraph()
    graph.addNode("2", "resistor")
    graph.printGraph()
    graph.addArc("1", "2", 5)
    graph.printGraph()
    graph.addArc("2", "1", 8)
    graph.printGraph()
    graph.addNode("3", "source")
    graph.addArc("3", "3", 14)
    graph.printGraph()


main()
