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

        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())

        entryDir = Entry(self.root,textvariable=self.currentDir,width=133)
        entryDir.place(x=0,y=0)
        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","33"),width=14,height=2)
        self.timer.place(x=9,y=28)

        self.root.mainloop()

if __name__=="__main__":
    Player()

