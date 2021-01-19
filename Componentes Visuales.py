import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

from tools import calcularCuadricula

global listaCable
global listaNodos
global listaResistencias
global listaFDP
listaCable = []
listaNodos = []
listaResistencias = []
listaFDP = []


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


def hola():
    print("Se clickeo el boton")


# Esta funcion pregunta por el nombre de la resistencia y el voltaje luego los almacena en una lista
def nuevaResistencia():
    nuevoNombre = simpledialog.askstring("Nueva Resistencia", "Ingrese el nombre de la nueva resistencia")
    nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
    if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
        messagebox.showerror("HUBO UN ERROR", "El nombre o el voltaje no se ingreso")
    elif nuevoNombre in listaResistencias:
        messagebox.showerror("HUBO UN ERROR", "Este nombre ya existe por favor ingrese otro")
    else:
        listaResistencias.append((nuevoNombre, nuevoVoltaje))
        print(listaResistencias)


# Esta funcion pregunta por el nombre de la Fuente de poder y el voltaje luego los almacena en una lista
def nuevaFDP():
    nuevoNombre = simpledialog.askstring("Nueva Fuente de poder", "Ingrese el nombre de la nueva fuente de poder")
    nuevoVoltaje = simpledialog.askinteger("Nuevo Voltaje", "Ingrese el valor del voltaje")
    if nuevoNombre == '' or nuevoVoltaje == '' or nuevoNombre == None or nuevoVoltaje == None:
        messagebox.showerror("HUBO UN ERROR", "El nombre o el voltaje no se ingreso")
    elif nuevoNombre in listaFDP:
        messagebox.showerror("HUBO UN ERROR", "Este nombre ya existe por favor ingrese otro")
    else:
        listaFDP.append((nuevoNombre, nuevoVoltaje))
        print(listaFDP)


# Caracteristicas de la ventana
ventana = Tk()
ventana.title("Circuit Designer")
ventana.geometry("1000x600")
ventana.resizable(False, False)
ventana.configure(background="grey")


class Ventana_Principal:

    def __init__(self, master):
        self.canvas = Canvas(master, width=700, height=600, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.matriz = []
        for i in range(10):  # El numero adentro es la cantiad de filas
            self.matriz.append([0] * 12)  # El numero despues del * es la cantidad de columnas

        self.size = 50
        self.paint(0, 0)
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.dibujado_linea = True
        self.dibujando = True


        self.canvas.create_line(100, 0, 100, 25, width=5)

        self.canvas.bind("<Button-1>", self.key_pressed)

        # TituloC hace referencia al Cable
        tituloR = tkinter.Label(ventana, text="Cable", bg="grey", font="Times 20 bold")
        tituloR.place(x=710, y=25)

        botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command=self.line)
        botonR.place(x=710, y=75)

        # TituloN hace referencia al Nodo
        tituloR = tkinter.Label(ventana, text="Nodo", bg="grey", font="Times 20 bold")
        tituloR.place(x=710, y=125)
        botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command=hola)
        botonR.place(x=710, y=175)

        # TituloR hace referencia a la Resistencia
        tituloR = tkinter.Label(ventana, text="Resistencia", bg="grey", font="Times 20 bold")
        tituloR.place(x=710, y=225)
        botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command=nuevaResistencia)
        botonR.place(x=710, y=275)

        # TituloFP hace referencia a la Fuente de poder
        tituloFP = tkinter.Label(ventana, text="Fuente de poder", bg="grey", font="Times 20 bold")
        tituloFP.place(x=710, y=325)
        botonFP = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command=nuevaFDP)
        botonFP.place(x=710, y=375)

        label = Label(ventana, bg="red", width=10, height=5)
        label.place(x=810, y=25)

        label2 = Label(ventana, bg="blue", width=10, height=5)
        label2.place(x=810, y=125)

        label.bind("<Button-1>", drag_start)
        label.bind("<B1-Motion>", drag_motion)

        label2.bind("<Button-1>", drag_start)
        label2.bind("<B1-Motion>", drag_motion)

    def paint(self, i, j):
        if i == len(self.matriz):
            return 0
        elif j == len(self.matriz[0]):
            return self.paint(i + 1, 0)
        else:
            self.canvas.create_rectangle(50 * (j + 1), 50 * (i + 1), 50 * (j + 1) + self.size, 50 * (i + 1) + self.size,
                                         fill="white")
            return self.paint(i, j + 1)

    def key_pressed(self, event):
        i = (event.x // self.size) - 1
        j = (event.y // self.size) - 1
        print("hizo click en", "i: " + str(i), "j: " + str(j))

    def line(self):
        self.dibujando = True
        self.canvas.bind("<Button-1>", self.line_aux)

    def line_aux(self, evento):
        if self.dibujando:
            if self.dibujado_linea:
                self.dibujado_linea = False
                self.x1 = calcularCuadricula(evento.x)
                self.y1 = calcularCuadricula(evento.y)
            else:
                self.x2 = calcularCuadricula(evento.x)
                self.y2 = calcularCuadricula(evento.y)
                self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=5)
                print("Se relaciona "+str(self.x1// self.size)+","+str(self.y1// self.size)+" con "+str(self.x2// self.size)+","+str(self.y2// self.size))
                self.dibujado_linea = True
                self.dibujando = False

    def line_exit(self):
        self.canvas.bind("<Button-1>", hola())

Ventana_Principal(ventana)
ventana.mainloop()
