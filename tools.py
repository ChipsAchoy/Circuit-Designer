

'''
    biggestLine = lambda x1, y1, x2, y2
        E: cuatro coordenadas
        S: un true si las "x" son mayores a las "y", caso contrario, envía un false
        R: ----
'''
biggestLine = lambda x1, y1, x2, y2: True if abs(x2 - x1) >= abs(y2 - y1) else False

'''
    calcDis = lambda x1, x2
        E: dos coordenadas
        S: la distancia entre estas a usar para crear las imágenes de resistencia o fuente de poder.
        R: ----
'''
calcDis = lambda x1, x2: (abs(x1 - x2) // 2) + (((abs(x1 - x2) // 2) * 0.1) * 4)

'''
searchNameRes(dictionary,list)
    E: un diccionaro y una lista
    S: retorna un diccionario ordenado a partir de un diccionario desordenado y una lista ordenada
    R: la lista debe tener los elementos que están en el diccionario        
'''
def searchNameRes(dictionary,
                  list):  # Busca el nombre de las resistencias tomando un diccionario con estas y una lista ordenada de las resistencias
    result = {}
    for i in list:
        for j in dictionary:
            if i == dictionary.get(j):
                temp = {j: i}
                result.update(temp)
    return result

#Función principal de calcularCuadrícula, esta llama a calcularCuadrícula_aux()
def calcularCuadricula(num):
    return calcularCuadricula_aux(num, num)


'''
calcularCuadricula_aux(temp1, temp2)
    E: Dos coordenadas
    S: la cuadrícula más cercana, tomando en cuenta 50 pixeles, al que se logre acercar primero, se enviará
    R: ------

'''
def calcularCuadricula_aux(temp1, temp2):
    if temp1 % 50 == 0:
        return temp1
    elif temp2 % 50 == 0:
        return temp2
    else:
        return calcularCuadricula_aux(temp1 - 1, temp2 + 1)


'''
createResImage(master, x1, y1, x2, y2, horizontal, type)
    E: el master del canvas, posiciones de los puntos, un condicional para saber cuando es horizontal o vertical
    y el tipo de elemento a dibujar.
    S: el dibujo de una resistencia o la fuente de poder acorde al tamaño de los cables.
    R: ----
'''

def createResImage(master, x1, y1, x2, y2, horizontal, type):
    line_size = 3
    if type == "resistor":
        if horizontal:
            sizeConst = abs(x1 - x2)
            master.create_line(x1, y1, x1 + (sizeConst / 6), y2 + (sizeConst / 3), width=line_size, fill="red")
            master.create_line(x1 + (sizeConst / 6), y1 + (sizeConst / 3), x1 + ((sizeConst / 6) * 2),
                               y2 - (sizeConst / 3), width=line_size, fill="red")
            master.create_line(x1 + ((sizeConst / 6) * 2), y1 - (sizeConst / 3), x1 + ((sizeConst / 6) * 3),
                               y2 + (sizeConst / 3), width=line_size, fill="red")
            master.create_line(x1 + ((sizeConst / 6) * 3), y1 + (sizeConst / 3), x1 + ((sizeConst / 6) * 4),
                               y2 - (sizeConst / 3), width=line_size, fill="red")
            master.create_line(x1 + ((sizeConst / 6) * 4), y1 - (sizeConst / 3), x1 + ((sizeConst / 6) * 5),
                               y2 + (sizeConst / 3), width=line_size, fill="red")
            master.create_line(x1 + ((sizeConst / 6) * 5), y1 + (sizeConst / 3), x1 + ((sizeConst / 6) * 6), y2,
                               width=line_size, fill="red")
        else:
            sizeConst = abs(y1 - y2)
            master.create_line(x1, y1, x1 + (sizeConst / 3), y1 + (sizeConst / 6), width=line_size, fill="red")
            master.create_line(x1 + (sizeConst / 3), y1 + (sizeConst / 6), x1 - (sizeConst / 3),
                               y1 + ((sizeConst / 6) * 2), width=line_size, fill="red")
            master.create_line(x1 - (sizeConst / 3), y1 + ((sizeConst / 6) * 2), x1 + (sizeConst / 3),
                               y1 + ((sizeConst / 6) * 3), width=line_size, fill="red")
            master.create_line(x1 + (sizeConst / 3), y1 + ((sizeConst / 6) * 3), x1 - (sizeConst / 3),
                               y1 + ((sizeConst / 6) * 4), width=line_size, fill="red")
            master.create_line(x1 - (sizeConst / 3), y1 + ((sizeConst / 6) * 4), x1 + (sizeConst / 3),
                               y1 + ((sizeConst / 6) * 5), width=line_size, fill="red")
            master.create_line(x1 + (sizeConst / 3), y1 + ((sizeConst / 6) * 5), x1, y1 + sizeConst, width=line_size,
                               fill="red")
    else:
        sizeConst = 25
        if horizontal:
            master.create_oval(x1, y1 - sizeConst, x2, y2 + sizeConst, fill="yellow")
        else:
            master.create_oval(x1 - sizeConst, y1, x2 + sizeConst, y2, fill="yellow")


# Llevar una lista de cables tambien
def generateSave(graph, filename):
    f = open("saves/" + filename + ".txt", "w")
    print("open file")
    out = "Nodes:"
    list_nodes = graph.getNodes()
    for node in list_nodes:
        out += "["
        out += str(node.x) + "," + str(node.y) + "," + node.id + "]"
    out += "\nArcs:"
    for i in range(len(graph.adMatrix)):
        current_i = list_nodes[i].id
        for j in range(len(graph.adMatrix[i])):
            current_j = list_nodes[j].id
            base_arc = [0,0]
            checked = False
            for arc in graph.adMatrix[i][j]:
                if arc != None:
                    if not checked:
                        base_arc = [arc.d1[0], arc.d1[1]]
                        checked = True
                    out += "["
                    out += current_i + "," + current_j + "," + arc.component + "," + arc.name + "," + str(
                        arc.value) + "," + str(base_arc[0]) + "," + str(base_arc[1]) + "," + str(arc.d2[0]) + "," + str(
                        arc.d2[1]) + "," + str(arc.direction[0]) + "," + str(arc.direction[1]) + "]"
    f.write(out)
    f.close()

'''
loadSave(graph, filename, master)
    E: Un grafo, el nombre del archivo y el master del canvas
    S: Carga y dibuja el archivo
    R: el archivo debe tener elementos a carcar
'''
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

        elif w != "," and (read_node or read_arc):
            word += w

    print("nodes", list_nodes)
    print("arcs", list_arcs)
    for node in list_nodes:
        graph.addNode(master, int(node[0]), int(node[1]), node[2])

    for arc in list_arcs:
        graph.addArc(master, arc[0], arc[1], arc[2], arc[3], int(arc[4]), [int(arc[5]), int(arc[6])],
                     [int(arc[7]), int(arc[8])])

