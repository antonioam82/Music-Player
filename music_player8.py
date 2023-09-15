#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog, messagebox
import random
from pygame import mixer, display
import threading
import json
import os

if not "music_favs.json" in os.listdir():
    d = {}
    with open("music_favs.json", "w") as f:
        json.dump(d, f)
        print("created music_favs.json")

class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.configure(bg="gray78")
        self.root.geometry("928x306")
        self.root.resizable(height=FALSE, width=FALSE)
        self.CHUNK = 1024

        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())
        self.filename = StringVar()
        self.playing = False
        self.file_path = ""
        mixer.init()
        display.init()
        self.paused = False
        self.stopped = False
        self.random_mode = False
        self.running = False
        self.c = 0
        self.text_x = 0
        self.text_direction = 1

        with open("music_favs.json") as f:
            self.audio_list = json.load(f)

        entryDir = Entry(self.root, textvariable=self.currentDir, width=154)
        entryDir.place(x=0, y=0)
        self.timer = Label(self.root, text="0:00:00", bg="black", fg="green", font=("arial", "34"), width=13, height=2)
        self.timer.place(x=9, y=28)
        #self.entryFile = Entry(self.root, textvariable=self.filename, width=37, font=("arial", 20))
        #self.entryFile.place(x=358, y=28)
        Button(self.root, text="SEARCH", width=79, bg="blue", fg="white").place(x=356, y=75)
        Button(self.root, text="PLAY", width=10, bg="goldenrod1").place(x=356, y=108)
        self.btnPause = Button(self.root, text="PAUSE", width=10, bg="goldenrod1")
        self.btnPause.place(x=437, y=108)
        Button(self.root, text="STOP", width=10, bg="goldenrod1").place(x=518, y=108)
        Button(self.root, text="ADD TO PLAYLIST", width=44, bg="goldenrod1").place(x=601, y=108)
        self.items = Label(self.root, text=('{} ITEMS ON PLAYLIST'.format(len(self.audio_list))), font=("arial", 10),
                           width=39, height=2, bg="black", fg="red")
        self.items.place(x=601, y=147)
        Button(self.root, text="REMOVE PLAYLIST", width=44).place(x=601, y=220)
        Button(self.root, text="REMOVE FROM PLAYLIST", width=44).place(x=601, y=190)
        self.btnPlayall = Button(self.root, text="PLAY ALL", width=21, height=2)
        self.btnPlayall.place(x=601, y=254)
        self.btnRandom = Button(self.root, text="RANDOM (OFF)", width=21, height=2)
        self.btnRandom.place(x=762, y=254)
        self.canvas = Canvas(self.root)
        self.canvas.place(x=9, y=147)
        self.scrollbar = Scrollbar(self.canvas, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.fav_list = Listbox(self.canvas, width=94, height=9, bg="gray96")
        self.fav_list.pack()
        self.fav_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.fav_list.yview)

        # Crear una etiqueta para mostrar el texto que se moverá
        self.display_text = Label(self.root, text="", bg="white", fg="black", font=("arial", 25))
        self.display_text = Label(self.root, text="", bg="white", fg="black", width = 79, height = 2)
        self.display_text.place(x=358, y=28)

        # Crear un Canvas para la animación del texto dentro de entryFile
        self.canvas_text = Canvas(self.root, width=79, height=2, bg="white", highlightthickness=0)
        self.canvas_text.place(x=358, y=28)

        # Iniciar la función para mover el texto dentro de entryFile
        #self.move_text()

        #self.show_list()
        self.root.mainloop()



    '''def move_text(self):
        text = self.entryFile.get()

        # Mueva el texto dentro de entryFile
        self.canvas_text.delete("all")  # Borrar el texto actual en el Canvas
        self.canvas_text.create_text(self.text_x, 15, text=text, anchor="w", fill="black", font=("arial", 20))
        self.text_x += self.text_direction * 5

        # Obtenga el ancho del Canvas
        canvas_width = self.canvas_text.winfo_width()

        # Si el texto se mueve fuera del área visible del Canvas, cambie la dirección
        if self.text_x > canvas_width:
            self.text_direction = -1
        elif self.text_x < 0:
            self.text_direction = 1

        # Vuelva a llamar a esta función después de un cierto tiempo para crear una animación continua
        self.root.after(100, self.move_text)'''

    def __del__(self):
        mixer.music.stop()
        self.stopped = True
        self.running = False

if __name__ == "__main__":
    Player()

