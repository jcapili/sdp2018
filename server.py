import argparse
import math
import numpy as np
import sys

from tkinter import *
from tkinter.ttk import *
import os
import threading

from pythonosc import dispatcher
from pythonosc import osc_server

#<<<<<<< HEAD
#pydub sound generation

from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play


#---Sound effect---
sound1 = AudioSegment.from_file("/Users/Maile/Desktop/GitHub/sdp2018/sounds/birds.m4a")

#---Sound generation globals---
#p = pyaudio.PyAudio()
volume = 0.5
fs = 44100
duration =2
samples = 0

import sound_generation
#<<<<<<< HEAD
from gui import start_gui
#>>>>>>> master
#=======
from gui import start_gui, window
#>>>>>>> master

#---Muse globals---
alpha_relative = 0
server = None
old_average = 0
new_average = 0
counter = 0

#---General functionality globals---
isHandled = False
isServing = True

#---Numpy globals---
# empty list to append values to
alpha_values = []

#---Changeable variables---
average_size = 50
max_percent_change = 20

"""
This function is responsible for actually getting and printing out
the relative alpha values. The following values are the relative values
for the other brain waves:

       delta_relative    1-4Hz
       theta_relative    4-8Hz
       alpha_relative    7.5-13Hz
       beta_relative    13-30Hz
       gamma_relative    30-44Hz
"""
def get_alpha_relative(unused_addr, args, ch1, ch2, ch3, ch4 ):
#    print("Alpha relative: ", ch1, ch2, ch3, ch4 )
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
    global alpha_values
    alpha_values.append(alpha_relative)
    print(alpha_values)

"""
This function handles server requests and calls the function calculate_sounds every time a request is successfully handled. It recursively calls itself so that we don't need to use .serve_forever(), which eliminates the use for another thread
"""
def run_server():
    global isHandled
    # isHandled makes sure handle_request and calculate_sounds play in that order
    if( isServing ):
        server.handle_request()

        if( isHandled ):
            calculate_sounds()
                
    isHandled = False
    # 1 is in milliseconds
    window.after(1, run_server)

"""
This function takes the average of a certain number of previous alpha_relative values specified by average_size. Every time the global counter reaches the average_size, the program determines if the current binaural beat needs to be changed, based on max_percent_change.
"""
def calculate_sounds():
    global alpha_relative, counter, old_average, new_average
    
    if counter is average_size:
        new_average = new_average / counter
        if old_average > 0:
            percent_change = (new_average - old_average) / old_average * 100
#            print("percent_change: ", percent_change)
            # integrate machine learning here
            if percent_change > max_percent_change and sound_generation.isPlaying is True:
                print("switching tones")
                sound_generation.switchTones = True
                #switch tones to get user closest to alpha
        old_average = new_average
        new_average = 0
        counter = 0
    else:
        new_average = new_average + alpha_relative
        counter += 1

if __name__ == "__main__":
    #---Set up connection with Muse---
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

    #---Start the server thread, which should always be running---
    threading.Thread(name="server", target=run_server, daemon=True).start()

    #---Start the GUI---
    start_gui()

