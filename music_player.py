from tkinter import *
import tkinter.scrolledtext as sct
from tkinter import filedialog, messagebox
import playsound

class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.geometry("800x290")

        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","29"),width=10,height=2)
        self.timer.place(x=15,y=20)

        self.root.mainloop()

if __name__=="__main__":
    Player()

