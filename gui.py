from tkinter import *
from tkinter.ttk import *
import os
import threading

import sound_generation
chosen_song = None

def test():
    sound_generation.switchTones = True

def start_gui():
    global chosen_song
    window = Tk() # Create Tk window
    Label(window, text="Binaural Beats with Muse").pack()
    
    top = Frame(window)
    top.pack()
    bottom = Frame(window)
    bottom.pack(side=BOTTOM)

    #---Setting up the radio buttons---
    v = IntVar()
    v.set(0)  # initializing the choice
    guiSongs = ["A", "Ab", "B", "Bb", "C", "D", "Db", "E", "Eb", "F", "G", "Gb"]
    chosen_song = "A"

    def set_choice():
        global chosen_song
        # Need to redefine guiSongs for some reason, not a mistake
        guiSongs = ["A", "Ab", "B", "Bb", "C", "D", "Db", "E", "Eb", "F", "G", "Gb"]
        print(guiSongs)
        chosen_song = guiSongs[v.get()]
        print(chosen_song)

    Label(window,
         text="""Choose the key of the song you'd like to listen to:""",
         justify = LEFT).pack()

    for val, guiSongs in enumerate(guiSongs):
         Radiobutton(window,
                     text=guiSongs,
                     variable=v,
                     command=set_choice,
                     value = val).pack(anchor=CENTER)

    #---Setting up the buttons---
    # Use lambda so function can take arguments without acutally running
    Button(text="Start Session", command = lambda:sound_generation.start_session(chosen_song)).pack()
    Button(bottom, text="Stop Session", command= sound_generation.stop_session).pack()
    Button(bottom, text="Switch Tones", command=test).pack()

    #---Starting the GUI---
    window.mainloop()
