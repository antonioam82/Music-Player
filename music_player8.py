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
        self.root.resizable(height=FALSE,width=FALSE)
        self.CHUNK = 1024
 
        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())
        self.filename = StringVar()
        self.file_path = ""
        mixer.init()
        display.init()
        
        self.playing = False
        self.paused = False
        self.stopped = False
        self.random_mode = False
        self.running = False
        
        self.c = 0
 
        with open("music_favs.json") as f:
            self.audio_list = json.load(f)
 
        entryDir = Entry(self.root,textvariable=self.currentDir,width=154)
        entryDir.place(x=0,y=0)
        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","34"),width=13,height=2)
        self.timer.place(x=9,y=28)
        self.entryFile = Entry(self.root,textvariable=self.filename,width=37,font=("arial",20))
        self.entryFile.place(x=358,y=28)
        Button(self.root,text="SEARCH",width=79,bg="blue",fg="white",command=self.open_file).place(x=356,y=75)
        Button(self.root,text="PLAY",width=10,bg="goldenrod1").place(x=356,y=108)
        self.btnPause = Button(self.root,text="PAUSE",width=10,bg="goldenrod1")
        self.btnPause.place(x=437,y=108)
        Button(self.root,text="STOP",width=10,bg="goldenrod1").place(x=518,y=108)
        Button(self.root,text="ADD TO PLAYLIST",width=44,bg="goldenrod1",command=self.add).place(x=601,y=108)#self.add
        self.items = Label(self.root,text=('{} ITEMS ON PLAYLIST'.format(len(self.audio_list))),font=("arial",10),width=39,height=2,bg="black",fg="red")
        self.items.place(x=601,y=147)
        Button(self.root,text="REMOVE PLAYLIST",width=44).place(x=601,y=220)#215
        Button(self.root,text="REMOVE FROM PLAYLIST",command=self.remove_from_list,width=44).place(x=601,y=190)#249
        self.btnPlayall = Button(self.root,text="PLAY ALL",width=21,height=2)
        self.btnPlayall.place(x=601,y=254)
        self.btnRandom = Button(self.root,text="RANDOM (OFF)",width=21,height=2)
        self.btnRandom.place(x=762,y=254)
        self.canvas = Canvas(self.root)
        self.canvas.place(x=9,y=147)
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.fav_list = Listbox(self.canvas,width=94,height=9,bg="gray96")
        self.fav_list.pack()
        self.fav_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.fav_list.yview)
 
        self.show_list()
 
        self.root.mainloop()

    def show_list(self):
        if len(self.audio_list) > 0:
            self.my_list = []
            c = 1
            for i in (self.audio_list):
                self.fav_list.insert(END,(str(c)+"- "+i))
                self.my_list.append(self.audio_list[i])
                c+=1

    def is_any_selected(self):
        self.num_selected = 0
        for i in range(0,self.fav_list.size()):
            if self.fav_list.selection_includes(i):
                self.num_selected += 1
                sel = True
                break
        else:
            sel = False
        return sel

    def get_key(self,val):
        for key, value in self.audio_list.items():
            if val == value:
                return key

    def remove_from_list(self):
        if self.fav_list.size() > 0:
            self.any_selected = self.is_any_selected()
            if self.any_selected:
                message = messagebox.askquestion("REMOVE ITEM",'Delete selected item from playlist?')
                if message == "yes":
                    
                    '''if self.running == False:
                        mixer.music.stop()
                    else:
                        self.running = False
                        self.btnPlayall.configure(state='normal')'''
 
                    self.file_path = self.my_list[self.fav_list.curselection()[ 0 ] ]
                    self.key = self.get_key(self.file_path)
                    del self.audio_list[self.key]
                    self.fav_list.delete(0,END)
                    with open("music_favs.json", "w") as f:
                        json.dump(self.audio_list, f)
                    self.show_list()
                    self.items.configure(text='{} ITEMS ON PLAYLIST'.format(len(self.audio_list)))
            else:
                messagebox.showwarning("NO ITEM SELECTED","Select the item you want to delete.")

    def add(self):
        self.any_selected = self.is_any_selected()
        #if self.entryFile.get() != "" and self.running == False and self.any_selected == False:
        if self.entryFile.get() != "" and self.any_selected == False:
            if not self.file_path in self.audio_list.values():
                self.fav_list.delete(0,END)
                self.audio_list[self.filename.get()]=self.file_path
                with open("music_favs.json", "w") as f:
                    json.dump(self.audio_list, f)
                self.show_list()
                self.items.configure(text='{} ITEMS ON PLAYLIST'.format(len(self.audio_list)))
            else:
                messagebox.showwarning("ALREADY SAVED","Selected item is already saved on playlist.")

    def open_file(self):
        try:
            fpath = filedialog.askopenfilename(initialdir = "/",title = "Select File",
                    filetypes = (("mp3 files","*.mp3"),("wav files","*.wav"),("ogg files",".ogg")))#,("all files","*.*")))
 
            if fpath:
                self.any_selected = self.is_any_selected()
                if self.any_selected:
                    self.fav_list.selection_clear(self.fav_list.curselection()[0])
                    self.stop()
                if self.playing == True:
                    self.stop()
                self.file_path = fpath
                self.filename.set(self.file_path.split("/")[-1])
                
        except Exception as e:
            messagebox.showwarning("UNEXPECECTED ERROR", str(e))

if __name__ == '__main__':
    Player()
