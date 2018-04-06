from tkinter import *
from tkinter.ttk import *
import os
import threading

import sound_generation

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

chosen_song = None
xList = []
yList = []

window = Tk()

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def test():
    sound_generation.switchTones = True

def animate(i):
    if sound_generation.isPlaying is True:
#        print(xList,yList)
        a.clear()
        a.plot(xList, yList)

class sdpApp():

    def __init__(self, top):
        Tk.wm_title(window, "app")

        
        container = Frame(window)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, SessionData):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        global chosen_song
        Label(self, text="Binaural Beats with Muse").pack()

        #---Setting up the radio buttons---
        v = IntVar()
        v.set(0)  # initializing the choice
        guiSongs = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
        chosen_song = "Ab"
        
        def set_choice():
            global chosen_song
            # Need to redefine guiSongs for some reason, not a mistake
            guiSongs = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
            print(guiSongs)
            chosen_song = guiSongs[v.get()]
            print(chosen_song)
        
        Label(self,
              text="""Choose the key of the song you'd like to listen to:""",
              justify = LEFT).pack()
            
        for val, guiSongs in enumerate(guiSongs):
              Radiobutton(self,
                          text=guiSongs,
                          variable=v,
                          command=set_choice,
                          value = val).pack(anchor=CENTER)

        #---Setting up the buttons---
        
        def start():
            sound_generation.start_session(chosen_song)
            controller.show_frame(SessionData)
        
        Button(self, text="Start Session", command = start).pack()

class SessionData(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Average alpha relative value")
        label.pack(pady=10,padx=10)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        def stop():
            sound_generation.stop_session()
            stop_btn.pack_forget()
            switch_btn.pack_forget()
            Button(self, text="Back to Home Page", command=lambda:controller.show_frame(StartPage) ).pack()

        stop_btn = Button(self, text="Stop Session", command= stop)
        stop_btn.pack()
        switch_btn = Button(self, text="Switch Tones", command=test)
        switch_btn.pack()

def start_gui():
    #---Starting the GUI---
    app = sdpApp(window)
    ani = animation.FuncAnimation(f, animate, interval=100)
    window.mainloop()
