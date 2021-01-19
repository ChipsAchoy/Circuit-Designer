import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from circuit_designer import *
from ordering_algorithms import *


global listaCable
global listaNodos
global listaResistencias
global listaFDP
listaCable = []
listaNodos = []
listaResistencias = []
listaFDP = []


class Cuadricula:

    def __init__(self, master, graph):
        self.master = master
        self.graph = graph
        self.canvas = Canvas(self.master, width = 901, height = 601, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x=0, y=0)
        self.position = [0,0]
        self.const = 50
        self.paint()
        self.canvas.bind("<Button-1>", self.key_pressed)

    def paint(self):
        return self.paint_aux(0,0)

    def paint_aux(self, i, j):
        for i in range(20):
            self.canvas.create_line(i*50, 0, i*50, 600, fill = "black")
        for j in range(20):
            self.canvas.create_line(0, j*50, 900, j*50, fill = "black")

    def adjustPosition(self, x, y):
        print("xy",x, y)
        
        up_limit = [0, 0]
        if x//50 != 0 and y//50 != 0:
            up_limit = [((x//50)-1)*50, ((y//50)-1)*50]
        limit = [(x//50)*50, (y//50)*50]
        down_limit = [((x//50)+1)*50, ((y//50)+1)*50]
        print("limits", up_limit, limit, down_limit)
        
        diffs_x = [abs(x-up_limit[0]), abs(x-limit[0]), abs(x-down_limit[0])]
        diffs_y = [abs(y-up_limit[1]), abs(y-limit[1]), abs(y-down_limit[1])]
        
        out = [radixSort(diffs_x)[0], radixSort(diffs_y)[0]]

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
            
        out = [out[0]/50, out[1]/50]
        print("out",out)
        return out
    
    def key_pressed(self, event):
        print("hizo click en", event.x, event.y)
        if event.x <= 900 and event.y <= 600:
            self.position = self.adjustPosition(event.x, event.y)
            print(self.position)
            if self.position != None:
                self.drawNode()
            
    def drawNode(self):
        if not graph.checkNode("Node_"+str(self.position[0])+"_"+str(self.position[1])):
            graph.addNode(self.canvas, self.position[0], self.position[1], "Node_"+str(self.position[0])+"_"+str(self.position[1]))
            graph.printGraph()
        else:
            print("Ya el nodo esta")

def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def drag_motion(event):
    #1.Top left corner-2.Place where we click in the label-3.Where we drag the label
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x,y=y)

def hola():
    print("Se clickeo el boton")


#Esta funcion pregunta por el nombre de la resistencia y el voltaje luego los almacena en una lista
def nuevaResistencia():
    nuevoNombre = simpledialog.askstring("Nueva Resistencia", "Ingrese el nombre de la nueva resistencia")
    nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
    if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
        messagebox.showerror("HUBO UN ERROR", "El nombre o el voltaje no se ingreso")
    elif nuevoNombre in listaResistencias:
        messagebox.showerror("HUBO UN ERROR", "Este nombre ya existe por favor ingrese otro")
    else:
        listaResistencias.append((nuevoNombre,nuevoVoltaje))
        print(listaResistencias)

#Esta funcion pregunta por el nombre de la Fuente de poder y el voltaje luego los almacena en una lista
def nuevaFDP():
    nuevoNombre = simpledialog.askstring("Nueva Fuente de poder", "Ingrese el nombre de la nueva fuente de poder")
    nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
    if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
        messagebox.showerror("HUBO UN ERROR", "El nombre o el voltaje no se ingreso")
    elif nuevoNombre in listaFDP:
        messagebox.showerror("HUBO UN ERROR", "Este nombre ya existe por favor ingrese otro")
    else:
        listaFDP.append((nuevoNombre,nuevoVoltaje))
        print(listaFDP)


#Caracteristicas de la ventana
ventana = Tk()
ventana.title("Circuit Designer")
ventana.geometry("1200x700")
ventana.resizable(False, False)
ventana.configure(background="grey")

#TituloC hace referencia al Cable
tituloR = tkinter.Label(ventana, text="Cable", bg="grey", font="Times 20 bold")
tituloR.place(x=910, y=25)
botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command = hola)
botonR.place(x=910,y=75)

#TituloN hace referencia al Nodo
tituloR = tkinter.Label(ventana, text="Nodo", bg="grey", font="Times 20 bold")
tituloR.place(x=910, y=125)
botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command = hola)
botonR.place(x=910,y=175)

#TituloR hace referencia a la Resistencia
tituloR = tkinter.Label(ventana, text="Resistencia", bg="grey", font="Times 20 bold")
tituloR.place(x=910, y=225)
botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command = nuevaResistencia)
botonR.place(x=910,y=275)

#TituloFP hace referencia a la Fuente de poder
tituloFP = tkinter.Label(ventana, text="Fuente de poder", bg="grey", font="Times 20 bold")
tituloFP.place(x=910, y=325)
botonFP = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command = nuevaFDP)
botonFP.place(x=910,y=375)


label = Label(ventana, bg="red",width=10,height=5)
label.place(x=1110,y=25)

label2 = Label(ventana, bg="blue",width=10,height=5)
label2.place(x=1110,y=125)

label.bind("<Button-1>", drag_start)
label.bind("<B1-Motion>", drag_motion)

label2.bind("<Button-1>", drag_start)
label2.bind("<B1-Motion>", drag_motion)

graph = Graph()

cuadr = Cuadricula(ventana, graph)
ventana.mainloop()
