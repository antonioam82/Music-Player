from tkinter import *
import tkinter.scrolledtext as sct
from tkinter import filedialog, messagebox
import playsound

class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.geometry("800x290")

        self.root.mainloop()

if __name__=="__main__":
    Player()
