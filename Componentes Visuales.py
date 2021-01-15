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

#####################################################
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

ventana.mainloop()

#function for create a metrix
def makeMatriz(rows,columns):
    matriz = []
    for i in range(rows):
        lista = []
        for j in range(columns):
            lista += [[]]
        matriz += [lista]
    return matriz

#Incio de la ventana Administrador
'''class Cliente():
    def __init__(self):
        self.Cliente = Toplevel()
        self.Cliente.resizable(False, False)
        self.Cliente.geometry("1000x600")
        self.canvas = Canvas(self.Cliente, width=1400, height=700, bg='white')
        self.canvas.place(x=0,y=0)

#Matriz y su tamaño
        self.matriz = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.size = 60

        self.PintarMatriz()
        self.canvas.bind("<Button-1>", self.MatrizPosicion)

    def SALIR(self):
        self.Cliente.quit()

#Dibuja la matriz en el canvas
    def PintarMatriz(self):
        for j in range(0, len((self.matriz[0]))):
            for i in range(0,len(self.matriz)):
                color = self.get_color(i, j)
                self.canvas.create_rectangle(60 * (j + 1), 60 * (i + 1), 60 * (j + 1) + self.size, 60 * (i + 1) + self.size, fill = color)
                #bloque = self.matriz[i][j]

    def get_color(self, i, j):
            return "red"

#Indica la posicion de fila y columna dentro de la matriz
    def MatrizPosicion(self, eventorigin):
        columna = eventorigin.x // self.size - 1
        fila = eventorigin.y // self.size - 1
        if 0 <= fila < len(self.matriz) and 0 <= columna < len(self.matriz[0]):
            if columna + self.bloqueActual[1] <= len(self.matriz[0]):
                for i in range(0,self.bloqueActual[1]):
                    self.matriz[fila][columna+i] = self.bloqueActual[0]
                self.PintarMatriz()
            print(self.matriz)
            #self.get_color(fila, columna)
            print("Fila: ", fila, "Columna: ", columna)

window = Tk()
window.title("Circuit Designer")
window.geometry("1000x600")
window.resizable(False,False)
#start = Principal_Menu(window)
window.mainloop()'''

class Ventana_Principal:

    def __init__(self, master):
        self.canvas = Canvas(master, width = 1000, height = 600, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x=0, y=0)
        self.matrix = [ [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],]
        self.size = 50
        self.ini = 50
        self.paint()

        self.canvas.bind("<Button-1>", self.key_pressed)

    def paint(self):
        return self.paint_aux(0,0)

    def paint_aux(self, i, j):
        if i == len(self.matrix):
            return 0
        elif j == len(self.matrix[0]):
            return self.paint_aux(i+1,0)
        else:
            torre = self.matrix[i][j]
            color = self.get_color(torre)
            self.canvas.create_rectangle(50*(j+1), 50*(i+1), 50*(j+1) + self.size, 50*(i+1) + self.size, fill = color)
            #print(color)
            return self.paint_aux(i,j+1)

    def get_color(self,torre):
        if torre == 0:
            return "white"
        elif torre == 1:
            return "orange"
        elif torre == 2:
            return "black"
        elif torre == 3:
            return "purple"
        else:
            return "red"

    def key_pressed(self, event):
        print("hizo click en", event.x//10, event.y//10)
        i = (event.x//self.size) -1
        j = (event.y//self.size) -1
        if i < len(self.matrix) and j < len(self.matrix[0]):
            if self.matrix[i][j] == 3:
                return self.shoot(i,j+1,0)
            else:
                self.matrix[i][j] = 3
                self.paint()
        else:
            return 0

window = Tk()
ventana_principal = Ventana_Principal(window)
window.minsize(1000, 600)
window.mainloop()
