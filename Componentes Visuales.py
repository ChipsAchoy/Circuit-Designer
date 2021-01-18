import tkinter
from tkinter import *


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


#Caracteristicas de la ventana
ventana = Tk()
ventana.title("Circuit Designer")
ventana.geometry("1000x600")
ventana.resizable(False, False)
ventana.configure(background="grey")


#TituloR hace referencia a la Resistencia
tituloR = tkinter.Label(ventana, text="Agregar resistencia", bg="grey", font="Times 18 bold")
tituloR.place(x=700, y=100)
botonR = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command = hola)
botonR.place(x=700,y=140)

#TituloFP hace referencia a la Fuente de poder
tituloFP = tkinter.Label(ventana, text="Agregar una fuente de poder", bg="grey", font="Times 18 bold")
tituloFP.place(x=700, y=200)
botonFP = tkinter.Button(ventana, text="AGREGAR", padx=10, pady=5, command = hola)
botonFP.place(x=700,y=240)

label = Label(ventana, bg="red",width=10,height=5)
label.place(x=0,y=0)

label2 = Label(ventana, bg="blue",width=10,height=5)
label2.place(x=100,y=100)

label.bind("<Button-1>", drag_start)
label.bind("<B1-Motion>", drag_motion)

label2.bind("<Button-1>", drag_start)
label2.bind("<B1-Motion>", drag_motion)

class Ventana_Principal:

    def __init__(self, master):
        self.canvas = Canvas(master, width = 700, height = 600, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x=0, y=0)
        self.matriz = []
        for i in range(10):  # El numero adentro es la cantiad de filas
            self.matriz.append([0] * 12)  # El numero despues del * es la cantidad de columnas
        self.size = 50
        self.paint(0,0)

        self.canvas.bind("<Button-1>", self.key_pressed)

    def paint(self, i, j):
        if i == len(self.matriz):
            return 0
        elif j == len(self.matriz[0]):
            return self.paint(i + 1, 0)
        else:
            self.canvas.create_rectangle(50*(j+1), 50*(i+1), 50*(j+1) + self.size, 50*(i+1) + self.size, fill = "white")
            return self.paint(i, j + 1)

    def key_pressed(self, event):
        i = (event.x//self.size) -1
        j = (event.y//self.size) -1
        print("hizo click en", "i: "+ str(i),"j: "+ str(j))

Ventana_Principal(ventana)
ventana.mainloop()
