from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import os
import threading
import csv

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
        
        for F in ( SongChoice, SessionData):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(SongChoice)
    
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

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
            global xList, yList
            xList = []
            yList = []
            sg.start_session(chosen_song)
            controller.show_frame(SessionData)
                
        def back():
            controller.show_frame(StartPage)
        
        Button(self, text="Start Session", command = start).pack()
#        Button(self, text="Back", command = back).pack()

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
            controller.show_frame(SongChoice)

        def stop():
            sg.stop_session()
            stop_btn.pack_forget()
            switch_btn.pack_forget()
            back_btn.pack(side=BOTTOM)
            csv_btn.pack(side=BOTTOM)
        
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
        
        def generate():
            with open('session1.csv', 'w' ) as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                for i in yList:
                    temp = []
                    temp.append(i)
                    writer.writerow(temp)
            messagebox.showinfo("Alert","CSV file generated successfully")

        stop_btn = Button(self, text="Stop Session", command= stop)
        switch_btn = Button(self, text="Switch Tones", command=test)
        back_btn = Button(self, text="Back to Home Page", command=start )
        hide_btn = Button(self, text="Hide Graph", command=hide)
        show_btn = Button(self, text="Show Graph", command=show)
        csv_btn = Button(self, text="Generate CSV File", command=generate)
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
