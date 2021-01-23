import os
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from graph import *
from ordering_algorithms import *

from tools import calcularCuadricula

global listaCable
global listaNodos
global listaResistencias
global listaFDP


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


def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y


def drag_motion(event):
    # 1.Top left corner-2.Place where we click in the label-3.Where we drag the label
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)


# def nuevoNodo():
#    global placeNodo
#   placeNodo = True


# Esta funcion pregunta por el nombre de la resistencia y el voltaje luego los almacena en una lista
"""
def nuevaResistencia():
    nuevoNombre = simpledialog.askstring("Nueva Resistencia", "Ingrese el nombre de la nueva resistencia")
    nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
    if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
        messagebox.showerror("Error", "El nombre o el voltaje no se ingreso")
    elif nuevoNombre in listaResistencias:
        messagebox.showerror("Error", "Este nombre ya existe por favor ingrese otro")
    else:
        listaResistencias.append((nuevoNombre, nuevoVoltaje))
        print(listaResistencias)


# Esta funcion pregunta por el nombre de la Fuente de poder y el voltaje luego los almacena en una lista
def nuevaFDP():
    nuevoNombre = simpledialog.askstring("Nueva Fuente de poder", "Ingrese el nombre de la nueva fuente de poder")
    nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
    if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
        messagebox.showerror("Error", "El nombre o el voltaje no se ingreso")
    elif nuevoNombre in listaFDP:
        messagebox.showerror("Error", "Este nombre ya existe por favor ingrese otro")
    else:
        listaFDP.append((nuevoNombre, nuevoVoltaje))
        print(listaFDP)
"""

class Ventana_Principal:

    def __init__(self, master, graph, images):
        self.images = images
        self.master = master
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

        # self.canvas.bind("<Button-1>", self.key_pressed)

        # TituloC hace referencia al Cable
        tituloR = tkinter.Label(ventana, text="Cable", bg="#525252", fg="white", font="Bahnschrift 20 bold")
        tituloR.place(x=910, y=25)

        botonR = tkinter.Button(ventana, text="Agregar", padx=10, pady=5, command=self.genCable, bg="#2F2F2F", fg="#D1E10C",
                                font="Bahnschrift 14 bold")
        botonR.place(x=910, y=75)

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

    #    botonFP = tkinter.Button(ventana, text="Agregar", padx=10, pady=5, command=nuevaFDP, bg="#2F2F2F", fg="#D1E10C",
      #                           font="Bahnschrift 14 bold")
       # botonFP.place(x=910, y=375)

        self.botonPlay = tkinter.Button(ventana, padx=10, pady=5, command=self.startSimulation, bg="#2F2F2F",
                                        image=images[0])
        self.botonPlay.place(x=70, y=630)

        self.botonSelec = tkinter.Button(ventana, padx=10, pady=5, command=self.changeMode, bg="#2F2F2F",
                                         image=images[2])
        self.botonSelec.place(x=370, y=630)

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

        label = Label(ventana, bg="red", width=10, height=5)
        label.place(x=1110, y=25)

        label2 = Label(ventana, bg="blue", width=10, height=5)
        label2.place(x=1110, y=125)

        label3 = Label(ventana, image=images[4], width=43, height=43)
        label3.place(x=700, y=630)


        label4 = Label(ventana, image=images[5], width=43, height=43)
        label4.place(x=800, y=630)

        label.bind("<Button-1>", drag_start)
        label.bind("<B1-Motion>", drag_motion)

        label2.bind("<Button-1>", drag_start)
        label2.bind("<B1-Motion>", drag_motion)

        label3.bind("<Button-1>", drag_start)
        label3.bind("<B1-Motion>", drag_motion)

        label4.bind("<Button-1>", drag_start)
        label4.bind("<B1-Motion>", drag_motion)

    def changeMode(self):
        self.dijAs = not self.dijAs
        print(self.dijAs)
        if not self.dijAs:
            self.botonSelec.configure(image=self.images[2])
        else:
            self.botonSelec.configure(image=self.images[3])

    def startSimulation(self):
        global simulation
        print("------------------------------------------------------------------------")
        graph.printGraph()
        simulation = not simulation
        if not simulation:
            self.botonPlay.configure(image=self.images[0])
        else:
            self.botonPlay.configure(image=self.images[1])

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
            graph.addNode(self.canvas, self.position[0], self.position[1],
                          "Node_" + str(self.position[0]) + "_" + str(self.position[1]))
            tituloNodo = tkinter.Label(ventana, text="Node_" + str(self.position[0]) + "_" + str(self.position[1]),
                                       bg="white", fg="black", font="Bahnschrift 8 bold")
            tituloNodo.place(x=self.position[0] * 50 - 40, y=self.position[1] * 50 - 30)
            graph.printGraph()
        else:
            messagebox.showerror("Error", "Ya hay un nodo en esa posición")

    def genCable(self):
        self.line("Cable")

    def line(self,type,name="",value=0):
        print("SOPUTAMASRE")
        self.dibujando = True
        self.compType = type
        self.compName = name
        self.compValue = value
        print("Agregando: "+self.compType)
        self.canvas.bind("<Button-1>", self.line_aux)

    def line_aux(self, evento):
        if self.dibujando:
            if graph.checkNode(self.genID("Node",evento.x,evento.y)):
                if self.dibujado_linea:
                    self.dibujado_linea = False
                    self.x1 = calcularCuadricula(evento.x)
                    self.y1 = calcularCuadricula(evento.y)
                else:
                    self.x2 = calcularCuadricula(evento.x)
                    self.y2 = calcularCuadricula(evento.y)
                    self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=5, fill = self.genColor(self.compType))
                    print("Se relaciona: " + self.genID("Node",self.x1,self.y1) + " con " + self.genID("Node",self.x2,self.y2))
                    self.dibujado_linea = True
                    self.dibujando = False
                    self.addLine(self.x1,self.y1,self.x2,self.y2,self.compType)
            else:
                self.dibujando = False
                self.dibujado_linea = True
                print("No hay nodo en "+self.genID("Node",evento.x,evento.y))

    def addLine(self, x1, y1, x2, y2,type):
        if type == "resistor" or type == "source":
            graph.addArc(self.genID("Node",x1,y1),self.genID("Node",x2,y2),self.compType,self.compName
                         , self.compValue)
        else:
            graph.addArc(self.genID("Node",x1,y1),self.genID("Node",x2,y2),"Cable",
                         "Cable_"+str(x1)+"_"+str(y1)+"-"+str(x2)+"_"+str(y2))

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
ventana.geometry("1200x700")
ventana.resizable(False, False)
ventana.configure(background="#525252")
graph = Graph()
pause_i = load_img("play.png")
play_i = load_img("paused.png")
select_r = load_img("selec_r.png")
select_l = load_img("selec_l.png")
initial = load_img("init.png")
final = load_img("final.png")
vent = Ventana_Principal(ventana, graph, [play_i, pause_i, select_l, select_r, initial, final])
ventana.mainloop()
