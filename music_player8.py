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
        #self.stopped = False
        self.random_mode = False
        self.playing_loop = False
        
        self.c = 0
        self.text_x = 0
        self.text_direction = 1
        self.sleeep = False
 
        with open("music_favs.json") as f:
            self.audio_list = json.load(f)
 
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
        Button(self.root,text="ADD TO PLAYLIST",width=44,bg="goldenrod1",command=self.add).place(x=601,y=108)#self.add
        self.items = Label(self.root,text=('{} ITEMS ON PLAYLIST'.format(len(self.audio_list))),font=("arial",10),width=39,height=2,bg="black",fg="red")
        self.items.place(x=601,y=147)
        Button(self.root,text="REMOVE PLAYLIST",width=44,command=self.remove_playlist).place(x=601,y=220)#215
        Button(self.root,text="REMOVE FROM PLAYLIST",command=self.remove_from_list,width=44).place(x=601,y=190)#249
        self.btnPlayall = Button(self.root,text="PLAY ALL",command=self.init_task2,width=21,height=2)
        self.btnPlayall.place(x=601,y=254)
        self.btnRandom = Button(self.root,text="RANDOM (OFF)",width=21,height=2,command=self.random_mod)
        self.btnRandom.place(x=762,y=254)
        self.canvas = Canvas(self.root)
        self.canvas.place(x=9,y=147)
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.fav_list = Listbox(self.canvas,width=94,height=9,bg="gray96")
        self.fav_list.pack()
        self.fav_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.fav_list.yview)

        self.canvas_text = Canvas(self.root, width=559, height=36, bg="white", highlightthickness=0)#width=559,
        self.canvas_text.place(x=358, y=28)

        self.move_text()
        
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

    def create_list(self,p,c):
        lista = []
        for i in range(len(p)):
            lista.append(i)
        random.shuffle(lista)
        if c == lista[0]:
            lista.append(lista.pop(lista.index(c)))
        return lista

    def random_mod(self):
        if self.random_mode == False:
            self.random_mode = True
            self.listado = self.create_list(self.my_list,self.c)
            self.playlist = self.my_list
            self.btnRandom.configure(text="RANDOM (ON)")
 
        else:
            self.random_mode = False
            self.c = 0
            self.playlist = self.my_list[::-1]
            self.btnRandom.configure(text="RANDOM (OFF)")

    def remove_playlist(self):
        if self.fav_list.size() > 0:
            message = messagebox.askquestion("REMOVE PLAYLIST",'Do you want to remove all the playlist?')
            if message == "yes":
                self.stop()######
                self.playing = False
                self.running = False
                self.btnPlayall.configure(state='normal')
                self.my_list = []
                self.fav_list.delete(0,END)
                self.audio_list = {}
                d = {}
                with open("music_favs.json", "w") as f:
                    json.dump(d, f)
                self.items.configure(text='0 ITEMS ON PLAYLIST')

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

    def play_loop(self):
        self.stop()
        self.playing_loop = True
        self.playing = True
        self.stopped = False
        self.paused = False
        self.btnPlayall.configure(state="disabled")
 
        self.c = 0
        if self.random_mode == False:
            self.playlist = self.my_list[::-1]
        else:
            self.listado = self.create_list(self.my_list,self.c)
            self.playlist = self.my_list
 
        while self.playing_loop:
            print("-->"+str(self.c))
            if len(self.playlist) > 0 and self.stopped == False:
                if mixer.music.get_busy() == 0 and self.paused == False:
                    if self.random_mode == False:
                        current = self.playlist.pop()
                    else:
                        current = self.playlist[self.listado[self.c]]
 
                    try:
                        mixer.music.load(current)
                        self.filename.set(self.get_key(current))
                        any_selected = self.is_any_selected()
                        if any_selected:
                            self.fav_list.selection_clear(self.fav_list.curselection()[0])
 
                        if self.random_mode == False:
                            self.fav_list.selection_set(self.c)
                            self.fav_list.see(self.c)
                            self.c+=1
                        else:
                            self.fav_list.selection_set(self.listado[self.c])
                            self.fav_list.see(self.listado[self.c])
                            if self.c < len(self.listado)-1:
                                self.c+=1
                            else:
                                self.listado = self.create_list(self.my_list,self.listado[self.c])
                                self.c = 0
                        self.playing = True
                        mixer.music.play()
                        self.update_timer()
                    except:
                        if self.random_mode == False:
                            self.c+=1
                        else:
                            if self.c < len(self.listado)-1:
                                self.c += 1
                            else:
                                self.listado = self.create_list(self.my_list,self.listado[self.c])
                                self.c = 0
            else:
                if self.c != 0:
                    self.c = 0
                    self.playlist = self.my_list[::-1]
        self.playing = False
        self.playing_loop = False


    def get_key(self,val):
        for key, value in self.audio_list.items():
            if val == value:
                return key

    def init_task2(self):
        if len(self.audio_list)>0 and self.playing_loop == False:
            self.btnPlayall.configure(state="disabled")
            t2 = threading.Thread(target=self.play_loop)
            t2.start()

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
                    
                    #if self.file_path == self.my_list[self.fav_list.curselection()[ 0 ] ]:######
                        #self.stop()#############################################################
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
                    #self.stop()
                if self.playing == True:
                    self.stop()
                self.file_path = fpath
                self.filename.set(self.file_path.split("/")[-1])
                
        except Exception as e:
            messagebox.showwarning("UNEXPECECTED ERROR", str(e))

    def update_timer(self):
        pos_time = mixer.music.get_pos()
        s = pos_time//1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        h, m, s = int(h), int(m), int(s)
        self.timer['text']=f"{h:01}:{m:02}:{s:02}"

        self.process = self.root.after(500, self.update_timer)
        if h == -1:
            self.timer['text']="0:00:00"
            self.root.after_cancel(self.process)
            self.btnPause.configure(text="PAUSE",command=self.pause)
            self.playing = False

    def play(self):
        self.playing = True
        self.btnPlayall.configure(state="normal")
        self.btnPause.configure(text="PAUSE",command=self.pause)
        try:
            mixer.music.load(self.file_path)
            mixer.music.play()
            self.update_timer()
        except:
            messagebox.showwarning("ERROR","Can't open the file '{}'.".format(self.entryFile.get()))
            self.playing = False

    def stop(self):
        self.playing_loop = False
        self.playing = False
        mixer.music.stop()
        self.stopped = True
        #self.running = False #
        self.btnPlayall.configure(state="normal")

    def pause(self):
        print(self.paused)
        print(self.playing)
        if self.playing == True:
            mixer.music.pause()
            self.paused = True
            self.btnPause.configure(text="CONTINUE",command=self.unpause)

    def unpause(self):
        mixer.music.unpause()
        #self.stopped = False
        self.paused = False
        self.btnPause.configure(text="PAUSE",command=self.pause)

    def init_task(self):
        self.stop()
        self.playing = True
        print(self.playing)
        self.any_selected = self.is_any_selected()
        if self.any_selected:
            self.file_path = self.my_list[self.fav_list.curselection() [ 0 ] ]
            self.key = self.get_key(self.file_path)
            self.filename.set(self.key)
        if self.file_path:
            if os.path.exists(self.file_path):
                self.timer['text']="0:00:00"
                t = threading.Thread(target=self.play)
                t.start()
            else:
                messagebox.showwarning("NO FILE",'''Path not found, file may have
been deleted or moved.''')

    def move_text(self):
        text = self.entryFile.get()
        canvas_width = self.canvas_text.winfo_width()
 
        text_bbox = self.canvas_text.bbox(self.canvas_text.create_text(0, 0, text=text, anchor="w", font=("arial", 20)))
        text_width = text_bbox[2] - text_bbox[0]
 
        if text_width > canvas_width:
            self.canvas_text.delete("all")
            self.canvas_text.create_text(self.text_x, 15, text=text, anchor="w", fill="black", font=("arial", 20))
            self.text_x -= 5
 
            if self.text_x <= - text_width:
                self.text_x = canvas_width
        else:
            self.canvas_text.delete("all")
            self.canvas_text.create_text(self.text_x, 15, text=text, anchor="w", fill="black", font=("arial", 20))
            self.text_x = 0
 
        self.root.after(100, self.move_text)

    def __del__(self):
        mixer.music.stop()
        self.stopped = True
        self.playing_loop = False

if __name__ == '__main__':
    Player()

