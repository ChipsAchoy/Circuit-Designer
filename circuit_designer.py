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
        
    def addNode(self, ident):
        self.nodesCount += 1
        self.nodes += [Node(ident)]
        if self.nodesCount == 1:
            self.adMatrix += [[None]]
        else:
            tmp = []
            for i in range(self.nodesCount):
                tmp_aij = []
                for j in range(self.nodesCount):
                    tmp_aij += [None]
                tmp += [tmp_aij]
                
            trans = self.adMatrix
            for i in range(self.nodesCount - 1):
                for j in range(self.nodesCount - 1):
                    tmp[i][j] = trans[i][j]
            self.adMatrix = tmp
            
    def addArc(self, id1, id2, component,value=0):
        arc = Arc(component, value)
        if self.checkNode(id1) and self.checkNode(id2):
            index1 = self.nodes.index(self.getById(id1))
            index2 = self.nodes.index(self.getById(id2))
            self.adMatrix[index1][index2] = arc

    def deleteNode(self, ident): #Elimina los arcos asociados a ese nodo tanto de ida como de vuleta
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
                if j != None:
                    print(j.component+":"+str(j.value)+" ", end="")
                else:
                    print("None ", end="")
            print("]")


        

'''
def main():
    graph = Graph()
    graph.addNode("1")
    graph.printGraph()
    graph.addNode("2")
    graph.printGraph()
    graph.addArc("1", "2", 5)
    graph.printGraph()
    graph.addArc("2", "1", 8)
    graph.printGraph()
    graph.addNode("3")
    graph.addArc("3", "3", 14)
    graph.printGraph()


main()
'''
