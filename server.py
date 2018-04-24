import argparse
import math
import numpy as np
from numpy import convolve
import sys
import time

from tkinter import *
from tkinter.ttk import *
import os
import threading

from pythonosc import dispatcher
from pythonosc import osc_server

import sound_generation
from gui import start_gui, window

#---Muse globals---
alpha_relative = 0
theta_relative = 0
server = None
old_average = 0
new_average = 0
counter = 0
q1 = 1
q2 = 1
q3 = 1
q4 = 1

#---General functionality globals---
isHandled = False
isServing = True

#---Changeable variables---
average_size = 50
max_percent_change = 15

def get_weights(unused_addr, args, ch1, ch2, ch3, ch4 ):
    print("Signal quality per channel: ", ch1, ch2, ch3, ch4 )
    global q1, q2, q3, q4
    q1 = ch1
    q2 = ch2
    q3 = ch3
    q4 = ch4

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
    total = 0
    numOfNotNan = 0
    
    if math.isnan(ch1) == False and q1 == 1:
        total += ch1
        numOfNotNan += 1
    
    if math.isnan(ch2) == False and q2 == 1:
        total += ch2
        numOfNotNan += 1
    
    if math.isnan(ch3) == False and q3 == 1:
        total += ch3
        numOfNotNan += 1
    
    if math.isnan(ch4) == False and q4 == 1:
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

"""
    This function is responsible for actually getting and printing out
    the relative theta values. The following values are the relative values
    for the other brain waves:
    
    delta_relative    1-4Hz
    theta_relative    4-8Hz
    alpha_relative    7.5-13Hz
    beta_relative    13-30Hz
    gamma_relative    30-44Hz
    """
def get_theta_relative(unused_addr, args, ch1, ch2, ch3, ch4 ):
    total = 0
    numOfNotNan = 0
    
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
        global theta_relative
        theta_relative = total / numOfNotNan
        print("Average of theta relative: ", theta_relative )
    
    global isHandled
    isHandled = True

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
            if sound_generation.isPlaying is True:
                update_gui()

    isHandled = False
    # 1 is in milliseconds
#    time.sleep(1)
#    run_server()
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
"""
Calculates the moving average of yList to make a smoother graph. Taken from https://gordoncluster.wordpress.com/2014/02/13/python-numpy-how-to-generate-moving-averages-efficiently-part-2/
"""
def moving_average( values, window ):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

"""
Updates the gui according to a moving average.
"""
def update_gui():
    from gui import xList, yList, yMA, setYMA

    xList.append(len(xList))
    if( sound_generation.graphAlpha):
        yList.append(alpha_relative)
    else:
        yList.append(theta_relative)

    yMA = moving_average(yList,3).tolist()

    setYMA(yMA)

    for i in range(len(xList)-len(yMA)):
        xList.pop()

#    print(yMA)
#    print( xList )
#    print( yList )


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
    dispatcher.map("/muse/elements/horseshoe", get_weights, "horseshoe" )
    dispatcher.map("/muse/elements/alpha_relative", get_alpha_relative, "alpha_relative" )
    dispatcher.map("/muse/elements/theta_relative", get_theta_relative, "theta_relative" )

    #    dispatcher.map("/muse/elements/alpha_absolute", absolutes, "alpha_absolute" )

    server = osc_server.ThreadingOSCUDPServer(
          (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    #---Start the server thread, which should always be running---
    threading.Thread(name="server", target=run_server, daemon=True).start()

    #---Start the GUI---
    start_gui()

