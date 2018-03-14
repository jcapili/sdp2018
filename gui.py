from tkinter import *
from tkinter.ttk import *
import os
import threading

import sound_generation
def test():
    sound_generation.switchTones = True

def start_gui():
    window = Tk() # Create Tk window
    Label(window, text="Binaural Beats with Muse").pack()
    
    top = Frame(window)
    top.pack()
    bottom = Frame(window)
    bottom.pack(side=BOTTOM)
    
    Button(top, text="Start Session", command = sound_generation.start_all_sounds).pack()
    Button(bottom, text="Stop Session", command= sound_generation.stop_all_sounds).pack()
    Button(bottom, text="Switch Tones", command=test).pack()
    
    window.mainloop()
