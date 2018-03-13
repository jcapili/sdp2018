import argparse
import math
import numpy as np
import sys

from tkinter import *
from tkinter.ttk import *
import os
import threading
import time

from pythonosc import dispatcher
from pythonosc import osc_server

import sound_generation

#---Muse globals---
alpha_relative = 2
server = None

#---General functionality globals---
isHandled = False
isServing = True
timer = 0

#   This function is responsible for actually getting and printing out
#   the relative alpha values. The following values are the relative values
#   for the other brain waves:
#
#       delta_relative    1-4Hz
#       theta_relative    4-8Hz
#       alpha_relative    7.5-13Hz
#       beta_relative    13-30Hz
#       gamma_relative    30-44Hz
def get_alpha_relative(unused_addr, args, ch1, ch2, ch3, ch4 ):
    print("Alpha relative: ", ch1, ch2, ch3, ch4 )
    total = 0;
    numOfNotNan = 0;
    
    if( math.isnan(ch1) == False ):
        total += ch1
        numOfNotNan += 1
    
    if( math.isnan(ch2) == False ):
        total += ch2
        numOfNotNan += 1
    
    if( math.isnan(ch3) == False ):
        total += ch3
        numOfNotNan += 1
    
    if( math.isnan(ch4) == False ):
        total += ch4
        numOfNotNan += 1
    
    if( numOfNotNan == 0 ):
        print( "waiting for numbers...:" )
    else:
        global alpha_relative
        alpha_relative = total / numOfNotNan
        print("Average of alpha relative: ", alpha_relative )
    
    global isHandled
    isHandled = True

#   This function recursively calls itself so that we don't need to use .serve_forever()
def run_server():
    # isHandled makes sure handle_request, binaural_beats, and play() all run IN THAT ORDER
    if( isServing ):
        print("is serving")
        server.handle_request()

        if( isHandled ):
            print("is handling")
            global alpha_relative
            print(alpha_relative)

    # 1 is in milliseconds
    window.after(1, run_server)

def test1():
    sound_generation.switchTones = True
    print( sound_generation.switchTones )

def test2():
    sound_generation.switchTones = False
    print( sound_generation.switchTones )

if __name__ == "__main__":
    # This section sets up a connection
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=5000,
                        help="The port to listen on")
    args = parser.parse_args()
    
    
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    #    dispatcher.map("/muse/eeg", eeg_handler, "EEG")
    dispatcher.map("/muse/elements/alpha_relative", get_alpha_relative, "alpha_relative" )
    #    dispatcher.map("/muse/elements/alpha_absolute", absolutes, "alpha_absolute" )
    
    server = osc_server.ThreadingOSCUDPServer(
          (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

  
    #---Setting up the UI---
    window = Tk() # Create Tk window
    Label(window, text="Hello World").pack() # Add text to the window via a label
    
    top = Frame(window)
    top.pack()
    bottom = Frame(window)
    bottom.pack(side=BOTTOM)
    
    Button(top, text="Start Session", command= sound_generation.start_all_sounds).pack()
    Button(bottom, text="Stop Session", command=sound_generation.stop_all_sounds).pack()
    Button(bottom, text="Switch Tones", command=test1).pack()
    Button(bottom, text="Keep the current tone", command=test2).pack()

    
    

    
    # start the thread
    threading.Thread(name="server", target=run_server, daemon=True).start()

    # start the GUI
    window.mainloop()

