import os
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog 
from graph import *

from ordering_algorithms import insertion_Sort, shell_Sort
from tools import *

global listaCable
global listaNodos
global listaResistencias
global listaFDP

'''
load_img(name): Encuentra una imagen segun la ruta dentro de la carpeta imgs
    E: string del nombre del archivo
    S: el objeto PhotoImage relacionado dicha direccion
    R: La ruta debe de existir
'''

def load_img(name):
    if isinstance(name, str):
        path = os.path.join("imgs", name)
        img = PhotoImage(file=path)
        return img
    else:
        print("Error")


# placeNodo = False
listaCable = []
listaNodos = []
listaResistencias = []
listaFDP = []
simulation = False

'''
clase VentanaMenu: Interfaz del menu principal
    
    Atributos: 
        master (Tk), graph(Graph), images(PhotoImage list)  
    Metodos:
        __init__(master, graph, images):
            E: un TK, un objeto Graph y una lista de imagenes
            S: -
            R: -
        menu_principal(): Abre la ventana del menu y crea objetos en ella
            E: -
            S: -
            R: -
        open_ventana_nueva(): Abre la Ventana Principal
            E: -
            S: -
            R: -
'''

class Ventana_Menu:

    # Caracteristicas principales de todas las ventanas
    def __init__(self, master, graph, images):
        self.ventana = master
        self.graph = graph
        self.images = images
        self.menu_principal()
        
    def menu_principal(self):
        img = load_img("logo.png")
        self.filename = None
        self.logo = tkinter.Label(self.ventana, image=img, bg="#525252")
        self.logo.place(x=450, y=150)
        self.canvas1 = Canvas(self.ventana, width=400, height=700, highlightthickness=0, relief="ridge", bg="black")
        self.canvas1.place(x=0, y=0)
        
        self.canvas2 = Canvas(self.ventana, width=400, height=700, highlightthickness=0, relief="ridge", bg="black")
        self.canvas2.place(x=1000, y=0)
        
        self.boton1 = tkinter.Button(self.ventana, text="Nuevo circuito", bg="#525252", fg="#82E0FE", font="Bahnschrift 20 bold", command=self.open_ventana_nueva)
        self.boton1.place(x=450, y=500)
        self.boton2 = tkinter.Button(self.ventana, text="Importar circuito", bg="#525252", fg="#82E0FE", font="Bahnschrift 20 bold", command=self.import_file)
        self.boton2.place(x=700, y=500)
        self.ventana.mainloop()

    def open_ventana_nueva(self):
        self.logo.destroy()
        self.boton1.destroy()
        self.boton2.destroy()
        self.canvas1.destroy()
        self.canvas2.destroy()
        vent = Ventana_Principal(self.ventana, self.graph, self.images, self.filename)
        
        
    def import_file(self):

        self.filename = filedialog.askopenfilename(initialdir = "C:/Users/INTEL/Documents/GitHub/Circuit-Designer/saves/", title = "Select a File",
                                                  filetypes = (("Text files",
                                                                "*.txt*"),
                                                               ("all files",
                                                                "*.*")))
        print(self.filename)
        self.open_ventana_nueva()

        
'''
clase Ventana_Principal
    Atribuitos: 
        master (Tk), graph(Graph), images(PhotoImage list), canvas (Canvas), position(int list), const(int), size(int), dibujando_linea(boolean),
        dibujando(boolean), placeNodo(boolean), dijAs(boolean), compName(str), compValue(int)
    Metodos:
        __init__(master, graph, images, filename): Clase constructora
            E: un Tk, un objeto Graph, una lista de objetos PhotoImage, un nombre de archivo
            S: -
            R: -
        clearSelec(): Deselecciona ambos botones de Dijsktra
        setInicio(): Selecciona un nodo inicial para realizar dijkstra
        setFinal(): Selecciona un nodo final para realizar dijkstra
        clickedInicio(event): Evento al clickear el boton de inicio
            E: posicion del mouse en ese momento
            S: -
            R: -
        clickedFinal(event): Evento al clickear el boton de final
            E: posicion del mouse en ese momento
            S: -
            R: -
        clear(): Limpia el canvas de resistencias y nodos y resetea el grafo
        motion(event): Evento al mover el mouse durante la simulacion
            E: posicion del mouse en ese momento
            S: -
            R: -
        save(): Realiza el guardado de una pantalla especifica
        changeMode(): Cambia el modo de busqueda en dijkstra
        getLists(): Realiza los llamados para ordenar las listas
            E: -
            S: Retorna las listas ordenadas de forma ascendente y descendente en una lista
            R: -
        startSimulation(): Inicia la simulacion con las condiciones actuales
        paint() & paint_aux(i, j): Coloca la cuadricula en la pantalla
            paint():
                E: -
                S: La salida de paint_aux
                R: -
            paint_aux(i,j):
                E: Las dos coordenadas inciales
                S: -
                R: -
        adjustPosition(x, y): Aproxima una posicion a una posicion de la cuadricula
            E: posiciones x y y
            S: La posicion aproxima a la escala de la cuadricula
            R: -
        key_pressed(event): Evento que se activa al clickear el canvas para poner un nodo
            E: posicion del mouse en ese momento
            S: -
            R: -
        drawNode(): Dibuja un nodo en pantalla
        nuevaResistencia(): Coloca una nueva resistencia
        nuevaFPD(): Coloca una nueva fuente de poder
                
'''

class Ventana_Principal:

    def __init__(self, master, graph, images, filename):
        self.master = master
        self.images = images
        self.graph = graph
        self.canvas = Canvas(self.master, width=901, height=601, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.position = [0, 0]
        self.const = 50
        self.size = 50
        
        self.paint()
        self.canvas.bind("<Button-1>", self.key_pressed)
        
        self.compType = None

        self.dibujado_linea = True
        self.dibujando = True
        self.placeNodo = False
        self.dijAs = False

        self.compName = ""
        self.compValue = 0

        #self.genID = lambda type, x, y: type+"_"+str(x)+"_"+str(y)
        self.genID = lambda type, x, y: type+"_"+str(calcularCuadricula(x)//self.size)+\
                                               "_"+str(calcularCuadricula(y)//self.size)

        self.genColor = lambda type: "black" if type == "Cable" else "red" if type == "resistor" else "yellow"
        self.biggestLine = lambda x1, y1, x2, y2: True if abs(x2 - x1) >= abs(y2 - y1) else False
        self.calcDis = lambda x1, x2: (abs(x1 - x2) // 2) + (((abs(x1 - x2) // 2) * 0.1) * 4)
        # self.canvas.bind("<Button-1>", self.key_pressed)

        # TituloC hace referencia al Cable
        logoSmall = tkinter.Label(ventana, image=images[6], width=79, height=101, bg="#525252")
        logoSmall.place(x=910, y=25)


        # TituloN hace referencia al Nodo
        tituloR = tkinter.Label(ventana, text="Nodo", bg="#525252", fg="white", font="Bahnschrift 20 bold")
        tituloR.place(x=910, y=125)
        botonR = tkinter.Button(ventana, text="Agregar", padx=10, pady=5, command=self.nuevo_Nodo, bg="#2F2F2F",
                                fg="#D1E10C", font="Bahnschrift 14 bold")
        botonR.place(x=910, y=175)

        # TituloR hace referencia a la Resistencia
        tituloR = tkinter.Label(ventana, text="Resistencia", bg="#525252", fg="white", font="Bahnschrift 20 bold")
        tituloR.place(x=910, y=225)
        botonR = tkinter.Button(ventana, text="Agregar", padx=10, pady=5, command=self.nuevaResistencia, bg="#2F2F2F",
                                fg="#D1E10C", font="Bahnschrift 14 bold")
        botonR.place(x=910, y=275)

        # TituloFP hace referencia a la Fuente de poder
        tituloFP = tkinter.Label(ventana, text="Fuente de poder", bg="#525252", fg="white", font="Bahnschrift 20 bold")
        tituloFP.place(x=910, y=325)
        botonFP = tkinter.Button(ventana, text="Agregar", padx=10, pady=5, command=self.nuevaFDP, bg="#2F2F2F", fg="#D1E10C",
                                 font="Bahnschrift 14 bold")
        botonFP.place(x=910, y=375)

        botonSave = tkinter.Button(ventana, text="Exportar", padx=10, pady=5, command=self.save, bg="#2F2F2F", fg="#82E0FE",
                                 font="Bahnschrift 14 bold")
        botonSave.place(x=910, y=525)

        botonClear = tkinter.Button(ventana, text="Limpiar", padx=10, pady=5, command=self.clear, bg="#2F2F2F",fg="#FF5757",
                                   font="Bahnschrift 14 bold")
        botonClear.place(x=910, y=450)

        self.botonPlay = tkinter.Button(ventana, padx=10, pady=5, command=self.startSimulation, bg="#2F2F2F",
                                        image=images[0])
        self.botonPlay.place(x=70, y=630)

        self.botonSelec = tkinter.Button(ventana, padx=10, pady=5, command=self.changeMode, bg="#2F2F2F",
                                         image=images[2])
        self.botonSelec.place(x=370, y=630)

        self.tituloAsc = tkinter.Label(ventana, text="", bg="#525252", fg="#82E0FE", font="Bahnschrift 14 bold")
        self.tituloAsc.place(x=1170, y=25)
        
        self.ascend = tkinter.Label(ventana, text="", bg="#525252", fg="white", font="Bahnschrift 12 bold")
        self.ascend.place(x=1170, y=75)

        self.tituloDesc = tkinter.Label(ventana, text="", bg="#525252", fg="#82E0FE", font="Bahnschrift 14 bold")
        self.tituloDesc.place(x=1170, y=325)
        
        self.descend = tkinter.Label(ventana, text="", bg="#525252", fg="white", font="Bahnschrift 12 bold")
        self.descend.place(x=1170, y=375)

        tituloPlay = tkinter.Label(ventana, text="Simular", bg="#525252", fg="white", font="Bahnschrift 16 bold")
        tituloPlay.place(x=60, y=600)

        tituloDij = tkinter.Label(ventana, text="Modo de búsqueda", bg="#525252", fg="white",
                                  font="Bahnschrift 16 bold")
        tituloDij.place(x=300, y=600)

        titulom = tkinter.Label(ventana, text="Menor", bg="#525252", fg="white", font="Bahnschrift 16 bold")
        titulom.place(x=290, y=640)

        tituloM = tkinter.Label(ventana, text="Mayor", bg="#525252", fg="white", font="Bahnschrift 16 bold")
        tituloM.place(x=430, y=640)

        tituloT = tkinter.Label(ventana, text="Terminales", bg="#525252", fg="white", font="Bahnschrift 16 bold")
        tituloT.place(x=720, y=600)

        botIni = Button(ventana, image=images[4], width=43, height=43, command=self.setInicio)
        botIni.place(x=700, y=630)

        botFin  = Button(ventana, image=images[5], width=43, height=43, command=self.setFinal)
        botFin.place(x=800, y=630)

        botonClearSelec = tkinter.Button(ventana, text="Quitar selección", padx=10, pady=5, command=self.clearSelec, bg="#2F2F2F",
                                 fg="#FF5757",
                                 font="Bahnschrift 14 bold")
        botonClearSelec.place(x=900, y=630)


        self.labelInicio = Label(ventana, image=images[4], width=43, height=43)
        self.labelFinal = Label(ventana, image=images[5], width=43, height=43)

        self.setting_final = False
        self.setting_inicio = False

        self.labelPopup = Label(self.canvas, text="", bg="#69CEFD", fg="white", font="Bahnschrift 12 bold")

        self.canvas.bind('<Motion>', self.motion)

        if filename != None:
            loadSave(self.graph, filename, self.canvas)

    def clearSelec(self):
        self.setting_inicio = False
        self.setting_final = False
        graph.inicio = None
        graph.final = None
        self.labelInicio.place(x=1200, y=1200)
        self.labelFinal.place(x=1200, y=1200)

    def setInicio(self):
        self.setting_inicio = True
        self.setting_final = False
        self.canvas.bind("<Button-1>", self.clickedInicio)

    def setFinal(self):
        self.setting_final = True
        self.setting_inicio = False
        self.canvas.bind("<Button-1>", self.clickedFinal)

    def clickedInicio(self, event):
        position = self.adjustPosition(event.x, event.y)
        if self.setting_inicio:
            if graph.checkNode("Node_"+str(position[0])+"_"+str(position[1])):
                graph.inicio = "Node_"+str(position[0])+"_"+str(position[1])
                self.labelInicio.place(x=position[0] * 50 - 50, y=position[1] * 50 - 50)
                print(graph.inicio)


    def clickedFinal(self, event):
        position = self.adjustPosition(event.x, event.y)
        if self.setting_final:
            if graph.checkNode("Node_" + str(position[0]) + "_" + str(position[1])):
                graph.final = "Node_" + str(position[0]) + "_" + str(position[1])
                self.labelFinal.place(x=position[0] * 50 - 50, y=position[1] * 50 - 50)
                print(graph.final)

    def clear(self):
        global graph
        new_graph = Graph()
        graph = new_graph
        self.graph = new_graph
        self.canvas.destroy()
        self.canvas = Canvas(self.master, width=901, height=601, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.bind('<Motion>', self.motion)
        self.paint()
        self.canvas.bind("<Button-1>", self.key_pressed)

    def motion(self, event):
        global simulation
        xn, yn = event.x, event.y
        #print('{}, {}'.format(xn, yn))
        flag = False
        if simulation:
            for i in graph.adMatrix:
                for j in i:
                    for n in j:
                        if n != None:
                            x_pos = [n.d1[0], n.d2[0]]
                            y_pos = [n.d1[1], n.d2[1]]
                            dif_x = max(x_pos) - min(x_pos)
                            dif_y = max(y_pos) - min(y_pos)
                            if n.direction[0] == "horizontal":
                                if xn > min(x_pos)-5 and xn < max(x_pos)+5 and yn > max(y_pos)-5 and yn < max(y_pos)+5:
                                    flag = True
                                    print("Component: "+n.component+"\nVoltage: "+str(n.volts)+"\nCurrent: "+str(n.current)+"\nResistance: "+str(n.ohms))
                                    self.labelPopup.configure(text="Component: "+n.component+"\nVoltage: "+str(n.volts)+"V\nCurrent: "+str(n.current)+"mA\nResistance: "+str(n.ohms))
                                    self.labelPopup.place(x=xn, y=yn)
                                elif not flag:
                                    self.labelPopup.configure(text="")
                                    self.labelPopup.place(x=1200, y=1200)

                            elif n.direction[1] == "vertical":
                                if xn > min(x_pos)-5 and xn < min(x_pos)+5 and yn > min(y_pos)-5 and yn < max(y_pos)+5:
                                    flag = True
                                    print("Component: "+n.component+"\nVoltage: "+str(n.volts)+"\nCurrent: "+str(n.current)+"\nResistance: "+str(n.ohms))
                                    self.labelPopup.configure(text="Component: "+n.component+"\nVoltage: "+str(n.volts)+"V\nCurrent: "+str(n.current)+"mA\nResistance: "+str(n.ohms))
                                    self.labelPopup.place(x=xn, y=yn)
                                elif not flag:
                                    self.labelPopup.configure(text="")
                                    self.labelPopup.place(x=1200, y=1200)

                            else:
                                if dif_x >= dif_y:
                                    if (xn > min(x_pos)-5 and xn < max(x_pos)+5 and yn > n.d1[1]-5 and yn < n.d1[1]+5):
                                        flag = True
                                        print("Component: " + n.component + "\nVoltage: " + str(
                                            n.volts) + "\nCurrent: " + str(n.current) + "\nResistance: " + str(n.ohms))
                                        self.labelPopup.configure(
                                            text="Component: " + n.component + "\nVoltage: " + str(
                                                n.volts) + "V\nCurrent: " + str(n.current) + "mA\nResistance: " + str(
                                                n.ohms))
                                        self.labelPopup.place(x=xn, y=yn)
                                    elif not flag:
                                        self.labelPopup.configure(text="")
                                        self.labelPopup.place(x=1200, y=1200)
                                elif dif_x < dif_y:
                                    if (xn > n.d1[0]-5 and xn < n.d1[0]+5 and yn > min(y_pos)-5 and yn < max(y_pos)+5):
                                        flag = True
                                        print("Component: " + n.component + "\nVoltage: " + str(
                                            n.volts) + "\nCurrent: " + str(n.current) + "\nResistance: " + str(n.ohms))
                                        self.labelPopup.configure(
                                            text="Component: " + n.component + "\nVoltage: " + str(
                                                n.volts) + "V\nCurrent: " + str(n.current) + "mA\nResistance: " + str(
                                                n.ohms))
                                        self.labelPopup.place(x=xn, y=yn)
                                    elif not flag:
                                        self.labelPopup.configure(text="")
                                        self.labelPopup.place(x=1200, y=1200)

    def save(self):
        filename = simpledialog.askstring("Nombre del archivo", "Ingrese el nombre del archivo de guardado")
        generateSave(graph, filename)
        messagebox.showinfo("Información", "Se ha guardado el circuito")
    
    def changeMode(self):
        self.dijAs = not self.dijAs
        print(self.dijAs)
        if not self.dijAs:
            self.botonSelec.configure(image=self.images[2])
        else:
            self.botonSelec.configure(image=self.images[3])

    def getLists(self):
        resist_list = []
        for i in graph.adMatrix:
            for j in i:
                for x in j:
                    if x!= None and x.component == "resistor":
                        resist_list += [x.name]
        asc_str = ""
        des_str = ""
        for n in shell_Sort(resist_list):
            asc_str += n+"\n"
        for m in insertion_Sort(resist_list):
            des_str += m+"\n"
        return [asc_str, des_str]
        
    def startSimulation(self):
        global simulation
        print("------------------------------------------------------------------------")
        graph.printGraph()
        simulation = not simulation
        if not simulation:
            self.botonPlay.configure(image=self.images[0])
            self.ascend.configure(text="")
            self.descend.configure(text="")
            self.tituloAsc.configure(text="")
            self.tituloDesc.configure(text="")
            for i in graph.adMatrix:
                for j in i:
                    current_len = 1
                    init_pos = [0,0]
                    init_got = False
                    for x in j:
                        if x != None:
                            if not init_got:
                                init_pos = [x.d1[0], x.d1[1]]
                                init_got = True
                            graph.drawLine(self.canvas, init_pos[0], init_pos[1], x.d2[0], x.d2[1], x.component, current_len-1, x.name, x.value, True, False)
                            current_len += 1
        else:
            str_list = self.getLists()
            self.botonPlay.configure(image=self.images[1])
            self.ascend.configure(text=str_list[0])
            self.descend.configure(text=str_list[1])
            self.tituloAsc.configure(text="Orden ascendente")
            self.tituloDesc.configure(text="Orden descendente")

            if graph.inicio != None and graph.final != None:
                graph.dijkstra(self.dijAs, self.canvas)

            

    def paint(self):
        return self.paint_aux(0, 0)

    def paint_aux(self, i, j):
        for i in range(20):
            self.canvas.create_line(i * 50, 0, i * 50, 600, fill="black")
        for j in range(20):
            self.canvas.create_line(0, j * 50, 900, j * 50, fill="black")

    def adjustPosition(self, x, y):
        print("xy", x, y)

        up_limit = [0, 0]
        if x // 50 != 0 and y // 50 != 0:
            up_limit = [((x // 50) - 1) * 50, ((y // 50) - 1) * 50]
        limit = [(x // 50) * 50, (y // 50) * 50]
        down_limit = [((x // 50) + 1) * 50, ((y // 50) + 1) * 50]
        print("limits", up_limit, limit, down_limit)

        diffs_x = [abs(x - up_limit[0]), abs(x - limit[0]), abs(x - down_limit[0])]
        diffs_y = [abs(y - up_limit[1]), abs(y - limit[1]), abs(y - down_limit[1])]

        out = [min(diffs_x), min(diffs_y)]

        for i in range(3):
            if out[0] == diffs_x[i]:
                if i == 0:
                    out[0] = up_limit[0]
                elif i == 1:
                    out[0] = limit[0]
                elif i == 2:
                    out[0] = down_limit[0]

            if out[1] == diffs_y[i]:
                if i == 0:
                    out[1] = up_limit[1]
                elif i == 1:
                    out[1] = limit[1]
                elif i == 2:
                    out[1] = down_limit[1]

        out = [int(out[0] / 50), int(out[1] / 50)]
        print("out", out)
        return out

    def nuevo_Nodo(self):
        #   global placeNodo
        self.placeNodo = True
        self.canvas.bind("<Button-1>", self.key_pressed)


    def key_pressed(self, event):
        global placeNodo
        print("hizo click en", event.x, event.y)
        if event.x <= 900 and event.y <= 600 and self.placeNodo:
            self.position = self.adjustPosition(event.x, event.y)
            print("placing at", self.position)
            if self.position != None:
                self.drawNode()
        self.placeNodo = False

    def drawNode(self):
        if not graph.checkNode("Node_" + str(self.position[0]) + "_" + str(self.position[1])):
            graph.addNode(self.canvas, self.position[0], self.position[1],"Node_" + str(self.position[0]) + "_" + str(self.position[1]))
            tituloNodo = tkinter.Label(ventana, text="Node_" + str(self.position[0]) + "_" + str(self.position[1]), bg="white", fg="black", font="Bahnschrift 8 bold")
            tituloNodo.place(x=self.position[0] * 50 - 40, y=self.position[1] * 50 - 30)
            graph.printGraph()
            #loadSave(graph, "prueba")
        else:
            messagebox.showerror("Error", "Ya hay un nodo en esa posición")
        

    def genCable(self):
        self.line("Cable")

    def line(self,type,name="",value=0):
        self.dibujando = True
        self.compType = type
        self.compName = name
        self.compValue = value
        print("Agregando: "+self.compType)
        self.canvas.bind("<Button-1>", self.line_aux)

    def line_aux(self, evento):
   #     direction = [None, None]
        if self.dibujando:
            if graph.checkNode(self.genID("Node",evento.x,evento.y)):
                if self.dibujado_linea:
                    self.dibujado_linea = False
                    self.x1 = calcularCuadricula(evento.x)
                    self.y1 = calcularCuadricula(evento.y)
                    print(self.x1,self.y1)
                else:
                    self.x2 = calcularCuadricula(evento.x)
                    self.y2 = calcularCuadricula(evento.y)
                    print(self.x2,self.y2)
                  #  self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=5, fill = self.genColor(self.compType))
                    print("Se relaciona: " + self.genID("Node",self.x1,self.y1) + " con " + self.genID("Node",self.x2,self.y2))

                    self.dibujado_linea = True
                    self.dibujando = False
                    print(self.calcDis(self.x1, self.x2))
                    print(self.calcDis(self.y1, self.y2))
                    self.addLine(self.x1,self.y1,self.x2,self.y2,self.compType)#, direction)
            else:
                self.dibujando = False
                self.dibujado_linea = True
                print("No hay nodo en "+self.genID("Node",evento.x,evento.y))

    def addLine(self, x1, y1, x2, y2,type):#, direction):
        if type == "resistor" or type == "source":
            graph.addArc(self.canvas, self.genID("Node",x1,y1),self.genID("Node",x2,y2),self.compType,self.compName
                         , self.compValue, [x1, y1], [x2, y2])#, direction)
     #   else:
    #        graph.addArc(self.master, self.genID("Node",x1,y1),self.genID("Node",x2,y2),"Cable",
   #                      "Cable_"+str(x1)+"_"+str(y1)+"-"+str(x2)+"_"+str(y2), [x1, y1], [x2, y2])

        graph.printGraph()

    # Esta funcion pregunta por el nombre de la resistencia y el voltaje luego los almacena en una lista
    def nuevaResistencia(self):
        nuevoNombre = simpledialog.askstring("Nueva Resistencia", "Ingrese el nombre de la nueva resistencia")
        nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
        if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
            messagebox.showerror("Error", "El nombre o el voltaje no se ingreso")
        elif nuevoNombre in listaResistencias:
            messagebox.showerror("Error", "Este nombre ya existe por favor ingrese otro")
        else:
            listaResistencias.append((nuevoNombre, nuevoVoltaje))
            print(listaResistencias)
            self.line("resistor",nuevoNombre,nuevoVoltaje)

    # Esta funcion pregunta por el nombre de la Fuente de poder y el voltaje luego los almacena en una lista
    def nuevaFDP(self):
        print("Agredando source")
        nuevoNombre = simpledialog.askstring("Nueva Fuente de poder", "Ingrese el nombre de la nueva fuente de poder")
        nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
        if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
            messagebox.showerror("Error", "El nombre o el voltaje no se ingreso")
        elif nuevoNombre in listaFDP:
            messagebox.showerror("Error", "Este nombre ya existe por favor ingrese otro")
        else:
            listaFDP.append((nuevoNombre, nuevoVoltaje))
            self.line("source",nuevoNombre,nuevoVoltaje)



# Caracteristicas de la ventana
ventana = Tk()
ventana.title("Circuit Designer")
ventana.geometry("1400x700")
ventana.resizable(False, False)
ventana.configure(background="#525252")
graph = Graph()
pause_i = load_img("play.png")
play_i = load_img("paused.png")
select_r = load_img("selec_r.png")
select_l = load_img("selec_l.png")
initial = load_img("init.png")
final = load_img("final.png")
logoSmall = load_img("logo_chikito_uwu.png")
vent = Ventana_Menu(ventana, graph, [play_i, pause_i, select_l, select_r, initial, final, logoSmall])
ventana.mainloop()
