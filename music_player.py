from tkinter import *
import tkinter.scrolledtext as sct
from tkinter import filedialog, messagebox
import wave
import pyaudio
import threading
import os

class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music Player")
        self.root.geometry("803x301")
        self.CHUNK = 1024
        
        
        

        self.filename = StringVar()
        self.currentDir = StringVar()
        self.currentDir.set(os.getcwd())
        self.file_path = None
        self.playing = True

        entryDir = Entry(self.root,textvariable=self.currentDir,width=133)
        entryDir.place(x=0,y=0)
        self.timer = Label(self.root,text="0:00:00",bg="black",fg="green",font=("arial","34"),width=13,height=2)
        self.timer.place(x=9,y=28)
        self.entryFile = Entry(self.root,textvariable=self.filename,width=29,font=("arial",20))
        self.entryFile.place(x=355,y=28)
        Button(self.root,text="SEARCH",width=61,bg="light gray",command=self.open_file).place(x=356,y=75)
        Button(self.root,text="PLAY",width=15,bg="light gray",command=self.init_task).place(x=356,y=108)
        Button(self.root,text="STOP",width=15,bg="light gray",command=self.stop_music).place(x=474,y=108)

        self.root.mainloop()

    def init_task(self):
        t = threading.Thread(target=self.music)
        t.start()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(initialdir = "/",
                 title = "Select File",filetypes = (("wav files","*.wav"),
                 ("all files","*.*")))
        if self.file_path:
            self.filename.set(self.file_path.split("/")[-1])

    def stop_music(self):
        
        self.playing=False

    def music(self):
        if self.file_path:
            self.p = pyaudio.PyAudio()
            wf = wave.open(self.file_path, 'rb')
            self.stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
            data = wf.readframes(self.CHUNK)
            while data != '' and self.playing==True:
                self.stream.write(data)
                data = wf.readframes(self.CHUNK)
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.playing=True
            
if __name__=="__main__":
    Player()


