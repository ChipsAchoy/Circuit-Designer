def searchNameRes(dictionary,
                  list):  # Busca el nombre de las resistencias tomando un diccionario con estas y una lista ordenada de las resistencias
    result = {}
    for i in list:
        for j in dictionary:
            if i == dictionary.get(j):
                temp = {j: i}
                result.update(temp)
    return result


def calcularCuadricula(num):
    return calcularCuadricula_aux(num, num)


def calcularCuadricula_aux(temp1, temp2):
    if temp1 % 50 == 0:
        return temp1
    elif temp2 % 50 == 0:
        return temp2
    else:
        return calcularCuadricula_aux(temp1 - 1, temp2 + 1)

#Llevar una lista de cables tambien
def generateSave(graph, filename):
    
    f = open("saves/"+filename+".txt", "w")
    print("open file")
    out = "Nodes:"
    list_nodes = graph.getNodes()
    for node in list_nodes:
        out += "["
        out += str(node.x)+","+str(node.y)+","+node.id+"]"
    out += "\nArcs:"        
    for i in range(len(graph.adMatrix)):
        current_i = list_nodes[i].id
        for j in range(len(graph.adMatrix[i])):
            current_j = list_nodes[j].id
            for arc in graph.adMatrix[i][j]:
                if arc != None:
                    out += "["
                    out += current_i+","+current_j+","+arc.component+","+arc.name+","+str(arc.value)+","+str(arc.d1[0])+","+str(arc.d1[1])+","+str(arc.d2[0])+","+str(arc.d2[1])+"]"
    f.write(out)
    f.close()


def loadSave(graph, filename, master):

    f = open(filename, "r")
    save = f.read()
    line = 0
    list_nodes = []
    list_arcs = []
    list_n = []
    list_a = []
    word = ""
    read_node = False
    read_arc = False
    for w in save:
        if w == ":":
            line += 1
            word = ""
        elif w == "[" and line == 1:
            read_node = True
        elif w == "[" and line == 2:
            print("change to nodes")
            read_arc = True
            read_node = False
            
        elif w == "," and read_node:
            list_n += [word]
            word = ""
        elif w == "," and read_arc:
            list_a += [word]
            word = ""
            
        elif w == "]" and read_node:
            list_n += [word]
            list_nodes += [list_n]
            list_n = []
            word = ""
        elif w == "]" and read_arc:
            list_a += [word]
            list_arcs += [list_a]
            list_a = []
            word = ""
            
        elif w !=  "," and (read_node or read_arc):
            word += w

    print("nodes", list_nodes)
    print("arcs", list_arcs)
    for node in list_nodes:
        graph.addNode(master, int(node[0]), int(node[1]), node[2])

    for arc in list_arcs:
        graph.addArc(master, arc[0], arc[1], arc[2], arc[3], int(arc[4]), [int(arc[5]), int(arc[6])], [int(arc[7]), int(arc[8])])
        
