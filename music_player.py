from tkinter import *
from tkinter import filedialog, messagebox
import wave
import pyaudio
import threading
import json
import os

class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.configure(bg="gray78")
        self.root.geometry("803x324")
        self.CHUNK = 1024
        with open("data.json") as f:
            self.audio_list = json.load(f)
        
        self.filename = StringVar()
        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())
        self.file_path = None
        self.playing = False
        self.my_list = []

        entryDir = Entry(self.root,textvariable=self.currentDir,width=133)
        entryDir.place(x=0,y=0)
        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","34"),width=13,height=2)
        self.timer.place(x=9,y=28)
        self.entryFile = Entry(self.root,textvariable=self.filename,width=29,font=("arial",20))
        self.entryFile.place(x=355,y=28)
        Button(self.root,text="SEARCH",width=61,bg="blue",fg="white",command=self.open_file).place(x=356,y=75)
        Button(self.root,text="PLAY",width=15,bg="goldenrod1",command=self.init_task).place(x=356,y=108)
        Button(self.root,text="STOP",width=15,bg="goldenrod1",command=self.stop_music).place(x=474,y=108)
        Button(self.root,text="ADD TO PLAYLIST",width=27,bg="goldenrod1",command=self.add).place(x=594,y=108)
        Button(self.root,text="SELECT FROM PLAYLIST",width=55,command=self.list_selection).place(x=11,y=290)
        Button(self.root,text="REMOVE PLAYLIST",width=54,command=self.remove_playlist).place(x=405,y=290)
        self.canvas = Canvas(self.root)
        self.canvas.place(x=9,y=142)
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.fav_list = Listbox(self.canvas,width=127,height=9,bg="gray96")
        self.fav_list.pack()
        self.fav_list.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.fav_list.yview)

        self.show_list()
            
        self.root.mainloop()

    def init_task(self):
        self.clear_counter()###############################################
        if self.file_path and self.playing == False:
            t = threading.Thread(target=self.music)
            t.start()

    def remove_playlist(self):
        message = messagebox.askquestion("REMOVE PLAYLIST",'Do you want to remove all the playlist?')
        if message == "yes":
            self.my_list = []
            self.fav_list.delete(0,END)
            self.audio_list = {}
            d = {}
            with open("data.json", "w") as f:
                json.dump(d, f)    

    def add(self):
        if self.entryFile.get() != "":
            self.fav_list.delete(0,END)
            self.audio_list[self.filename.get()]=self.file_path
            with open("data.json", "w") as f:
                json.dump(self.audio_list, f)
            self.show_list()

    def list_selection(self):
        if len(self.audio_list) > 0:
            try:
                #print("SELECTION: ",self.fav_list.curselection()[0])
                #print("MY_LIST: ",self.my_list)
                self.file_path = self.my_list[self.fav_list.curselection()[0]]
                #print("PATH: ",self.file_path)
                key = self.get_key(self.file_path)
                self.filename.set(key)
            except:
                messagebox.showwarning("ERROR","No element selected.")

    def show_list(self):
        if len(self.audio_list) > 0:
            self.my_list = []
            c=1
            for i in (self.audio_list):
                self.fav_list.insert(END,(str(c)+"- "+i))
                self.my_list.append(self.audio_list[i])
                c+=1
            
    def open_file(self):
        if self.playing == False:
            fpath = filedialog.askopenfilename(initialdir = "/",
                 title = "Select File",filetypes = (("wav files","*.wav"),
                 ("all files","*.*")))
            if fpath:
                self.file_path = fpath
                self.filename.set(self.file_path.split("/")[-1])

    def stop_music(self):
        self.timer.after_cancel(self.process)###################################
        if self.playing == True:
            self.playing = False
        

    def clear_counter(self):
        self.sec_counter = 0
        self.min_counter = 0
        self.hour_counter = 0

    def counter_format(self,c):
        if c<10:
            c="0"+str(c)
        return c

    def timer_count(self):
        self.timer['text'] = str(self.hour_counter)+":"+str(self.counter_format(self.min_counter))+":"+str(self.counter_format(self.sec_counter))
        self.sec_counter+=1
        if self.sec_counter==60:
            self.sec_counter=0
            self.min_counter+=1
        if self.min_counter==60:
            self.min_counter=0
            self.hour_counter+=1
        self.process=self.timer.after(1000,self.timer_count)

    def music(self):
        self.playing = True
        self.p = pyaudio.PyAudio()
        wf = wave.open(self.file_path, 'rb')
        self.stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
        data = wf.readframes(self.CHUNK)
        self.timer_count()###############################3
        while data and self.playing == True:
            self.stream.write(data)
            data = wf.readframes(self.CHUNK)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.stop_music()#############

    def get_key(self,val):
        for key, value in self.audio_list.items():
            if val == value:
                return key
            
if __name__=="__main__":
    Player()


