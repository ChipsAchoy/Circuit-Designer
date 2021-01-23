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
    
    f = open(filename+".txt", "w")
    print("open file")
    out = "Nodes:"
    list_nodes = graph.getNodes()
    for node in list_nodes:
        out += "/"
        out += str(node.x)+","+str(node.y)+","+node.id+":"
    out += "\nArcs:"        
    for i in range(len(graph.adMatrix)):
        current_i = list_nodes[i].id
        for j in range(len(graph.adMatrix[i])):
            current_j = list_nodes[j].id
            for arc in graph.adMatrix[i][j]:
                if arc != None:
                    out += "/"
                    out += current_i+","+current_j+","+arc.component+","+arc.name+","+str(arc.value)+","+str(arc.d1[0])+","+str(arc.d1[1])+","+str(arc.d2[0])+","+str(arc.d2[1])+":"
    f.write(out)
    f.close()
