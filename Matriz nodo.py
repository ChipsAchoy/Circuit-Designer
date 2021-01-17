import tkinter, os
from tkinter import *


def load_img(name):
    if isinstance(name, str):
        path = os.path.join("imgs", name)
        img = PhotoImage(file=path)
        return img
    else:
        print("Error")



class Node:

    def __init__(self, master, x, y, name):
        self.master = master
        self.x = x*50-5
        self.y = y*50-5
        self.radius = 10
        self.name = name
        self.master.create_oval(self.x, self.y, self.x+self.radius, self.y+self.radius, fill="black")
        
class Cuadricula:

    def __init__(self, master, graph):
        self.master = master
        self.graph = graph
        self.canvas = Canvas(self.master, width = 905, height = 605, highlightthickness = 0, relief = "ridge")
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
        border_x = (x//50)
        border_y = (y//50)
        mod_x = x%50
        mod_y = x%50
        return [border_x, border_y]
        
    def key_pressed(self, event):
        print("hizo click en", event.x, event.y)
        if event.x <= 905 and event.y <= 600:
            self.position = self.adjustPosition(event.x, event.y)
            print(self.position)
            if self.position != None:
                self.drawNode()
            
    def drawNode(self):
        node = Node(self.canvas, self.position[0], self.position[1], "Node_"+str(self.position[0])+"_"+str(self.position[1]))


window = Tk()
window.title("Circuit Designer")
window.geometry('1100x700')
window.resizable(False, False)
cuadr = Cuadricula(window, None)
window.minsize(1000, 700)
window.mainloop()
