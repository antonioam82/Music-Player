from tkinter import *
import tkinter.scrolledtext as sct
from tkinter import filedialog, messagebox
import playsound
import os

class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.geometry("803x301")

        self.filename = StringVar()
        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())

        entryDir = Entry(self.root,textvariable=self.currentDir,width=133)
        entryDir.place(x=0,y=0)
        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","34"),width=13,height=2)
        self.timer.place(x=9,y=28)
        self.entryFile = Entry(self.root,textvariable=self.filename,width=29,font=("arial",20))
        self.entryFile.place(x=355,y=28)
        Button(self.root,text="SEARCH",width=61,bg="light gray").place(x=356,y=65)

        self.root.mainloop()

if __name__=="__main__":
    Player()

