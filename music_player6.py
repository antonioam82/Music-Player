#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog, messagebox
import random
import mutagen
from pygame import mixer#####################################
import threading
import json
import time
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
        self.CHUNK = 1024

        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())
        self.filename = StringVar()
        self.playing = False
        self.file_path = ""
        mixer.init()

        #with open("data.json") as f:
            #self.audio_list = json.load(f)

        entryDir = Entry(self.root,textvariable=self.currentDir,width=154)
        entryDir.place(x=0,y=0)
        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","34"),width=13,height=2)
        self.timer.place(x=9,y=28)
        self.entryFile = Entry(self.root,textvariable=self.filename,width=37,font=("arial",20))
        self.entryFile.place(x=358,y=28)
        Button(self.root,text="SEARCH",width=79,bg="blue",fg="white",command=self.open_file).place(x=356,y=75)
        Button(self.root,text="PLAY",width=10,bg="goldenrod1",command=self.init_task).place(x=356,y=108)
        self.btnPause = Button(self.root,text="PAUSE",width=10,bg="goldenrod1",command=self.pause)
        self.btnPause.place(x=437,y=108)
        Button(self.root,text="STOP",width=10,bg="goldenrod1",command=self.stop).place(x=518,y=108)
        Button(self.root,text="ADD TO PLAYLIST",width=44,bg="goldenrod1").place(x=601,y=108)#self.add
        self.items = Label(self.root,font=("arial",10),width=39,height=2,bg="black",fg="red")
        self.items.place(x=601,y=147)
        Button(self.root,text="REMOVE PLAYLIST",width=44).place(x=601,y=220)#215
        Button(self.root,text="REMOVE FROM PLAYLIST",width=44).place(x=601,y=190)#249
        self.btnPlayall = Button(self.root,text="PLAY ALL",width=21,height=2)
        self.btnPlayall.place(x=601,y=254)
        self.btnRandom = Button(self.root,text="RANDOM MODE: OFF",width=21,height=2)
        self.btnRandom.place(x=762,y=254)
        self.canvas = Canvas(self.root)
        self.canvas.place(x=9,y=147)
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.fav_list = Listbox(self.canvas,width=94,height=9,bg="gray96")
        self.fav_list.pack()
        self.fav_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.fav_list.yview)

        #self.show_list()

        self.root.mainloop()

    def open_file(self):
        fpath = filedialog.askopenfilename(initialdir = "/",title = "Select File",
                filetypes = (("mp3 files","*.mp3"),("ogg files",".ogg"),("all files","*.*")))
        
        if fpath:
            self.file_path = fpath
            self.filename.set(self.file_path.split("/")[-1])

    def update_timer(self):
        pos_time = mixer.music.get_pos()
        print(pos_time)
        self.root.after(500, self.update_timer)


    def play(self):
        if self.file_path != "":
            #audio = mutagen.File(self.file_path)
            #total_length = audio.info.length
            #print(total_length)
            print("PLAYING")
            mixer.music.load(self.file_path)
            mixer.music.play()
            self.update_timer()

    def stop(self):
        mixer.music.stop()
        #self.btnPause.configure(text="PAUSE")

    def pause(self):
        mixer.music.pause()
        self.btnPause.configure(text="RESTART",command=self.unpause)

    def unpause(self):
        mixer.music.unpause()
        self.btnPause.configure(text="PAUSE",command=self.pause)

    def init_task(self):
        t = threading.Thread(target=self.play)
        t.start()
            

if __name__=="__main__":
    Player()



