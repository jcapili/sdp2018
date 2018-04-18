from tkinter import *
from tkinter.ttk import *
import os
import threading

import sound_generation as sg

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

#---General functionality globals---
chosen_song = None
xList = []
yList = []
yMA = [] # Moving Average of y
graphAlpha = True

#---GUI globals---
window = Tk()

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

"""
This function manually switches tones for demonstration purposes.
"""
def test():
    sg.switchTones = True

"""
This function updates the graph display while a user is in session.
"""
def animate(i):
    global xList, yList, yMA
    if sg.isPlaying is True:
        a.clear()
        if len(xList) != len(yMA):
            print(len(xList))
#            print(yList)
            print(len(yMA))
            print( "Size of xList is not the same size as yMA" )
        else:
            a.plot(xList, yMA)
#        a.plot(xList[len(xList)-len(yMA):], yMA)

"""
Sets the value of yMA. Used by server.py because importing yMA doesn't work for some reason
"""
def setYMA(setter):
    global yMA
    yMA = list(setter)

"""
This class is the container class for the GUI pages. It holds the SongChoice and the SessionData pages.
"""
class sdpApp():

    def __init__(self, top):
        Tk.wm_title(window, "app")

        
        container = Frame(window)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, SongChoice, SessionData):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

"""
This class contains all the GUI elements and methods associated with the first page of the GUI.
    """
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        global chosen_song
        Label(self, text="Binaural Beats with Muse").pack()
        
        #---Setting up the radio buttons---
        v = IntVar()
        v.set(0)  # initializing the choice
        choices = ["No music", "Just music", "Just alpha binaural beats", "Just theta binaural beats", "Music with alpha binaural beats", "Music with theta binaural beats"]
        choice = "No music"
        
        #---Setting up the buttons---
        
        def next():
            global graphAlpha
            if v.get() is 1: # Just music
                sg.playMusic = True
                sg.playBinBeats = False
            elif v.get() is 2: # Just alpha binaural beats
                graphAlpha = True
                sg.playMusic = False
                sg.playBinBeats = True
                sg.isAlpha = True
            elif v.get() is 3: # Just theta binaural beats
                graphAlpha = False
                sg.playMusic = False
                sg.playBinBeats = True
                sg.isAlpha = False
            elif v.get() is 4: # Music with alpha binaural beats
                graphAlpha = True
                sg.playMusic = True
                sg.playBinBeats = True
                sg.isAlpha = True
            elif v.get() is 5: # Music with theta binaural beats
                graphAlpha = False
                sg.playMusic = True
                sg.playBinBeats = True
                sg.isAlpha = False
            
            controller.show_frame(SongChoice)
        
        def start():
            global xList, yList
            xList = []
            yList = []
            sg.playMusic = False
            sg.playBinBeats = False
            sg.start_session("nothing")
            controller.show_frame(SessionData)
        
        next_btn = Button(self, text="Next", command = next)
        session_btn = Button( self, text="Start Session", command = start)
        
        def set_choice():
            if v.get() is 0:
                if next_btn.winfo_ismapped() is 1:
                    next_btn.pack_forget()
                if session_btn.winfo_ismapped() is 0:
                    session_btn.pack()
            else:
                if next_btn.winfo_ismapped() is 0:
                    next_btn.pack()
                if session_btn.winfo_ismapped() is 1:
                    session_btn.pack_forget()
        
        Label(self,
              text="""Choose the type of session:""",
              justify = LEFT).pack()
            
        for val, choices in enumerate(choices):
              Radiobutton(self,
                          text=choices,
                          variable=v,
                          command=set_choice,
                          value = val).pack(anchor=CENTER)

        session_btn.pack()

"""
This class contains all the GUI elements and methods associated with the song choice page of the GUI.
"""
class SongChoice(Frame):
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
              text="""Choose the key you'd like to listen to:""",
              justify = LEFT).pack()
            
        for val, guiSongs in enumerate(guiSongs):
              Radiobutton(self,
                          text=guiSongs,
                          variable=v,
                          command=set_choice,
                          value = val).pack(anchor=CENTER)

        #---Setting up the buttons---
        
        def start():
            sg.start_session(chosen_song)
            controller.show_frame(SessionData)
                
        def back():
            controller.show_frame(StartPage)
        
        Button(self, text="Start Session", command = start).pack()
        Button(self, text="Back", command = back).pack()

"""
This class contains all the GUI elements associated with the session data page of the GUI.
"""
class SessionData(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Average alpha/theta relative value")
        label.pack(pady=10,padx=10)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        def start():
            stop_btn.pack(side=BOTTOM)
            switch_btn.pack(side=BOTTOM)
            back_btn.pack_forget()
            controller.show_frame(StartPage)

        def stop():
            sg.stop_session()
            stop_btn.pack_forget()
            switch_btn.pack_forget()
            back_btn.pack(side=BOTTOM)
        
        def hide():
            canvas.get_tk_widget().pack_forget()
            canvas._tkcanvas.pack_forget()
            show_btn.pack(side=BOTTOM)
            hide_btn.pack_forget()
        
        def show():
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
            hide_btn.pack(side=BOTTOM)
            show_btn.pack_forget()

        stop_btn = Button(self, text="Stop Session", command= stop)
        switch_btn = Button(self, text="Switch Tones", command=test)
        back_btn = Button(self, text="Back to Home Page", command=start )
        hide_btn = Button(self, text="Hide Graph", command=hide)
        show_btn = Button(self, text="Show Graph", command=show)
        hide_btn.pack(side=BOTTOM)
        stop_btn.pack(side=BOTTOM)
        switch_btn.pack(side=BOTTOM)


"""
This method starts the GUI. Used by the server.py file.
"""
def start_gui():
    #---Starting the GUI---
    app = sdpApp(window)
    ani = animation.FuncAnimation(f, animate, interval=100)
    window.mainloop()
