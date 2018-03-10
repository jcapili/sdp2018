# http://developer.choosemuse.com/research-tools-example/grabbing-data-from-museio-a-few-simple-examples-of-muse-osc-servers#python
#1. Gamma State: (30 — 100Hz) This is the state of hyperactivity and active learning. Gamma state is the most opportune time to retain information. This is why educators often have audiences jumping up and down or dancing around — to increase the likelihood of permanent assimilation of information. If over stimulated, it can lead to anxiety.
#
#2. Beta State: (13 — 30Hz) Where we function for most of the day, Beta State is associated with the alert mind state of the prefrontal cortex. This is a state of the “working” or "thinking mind": analytical, planning, assessing and categorizing.
#
#3. Alpha State: (9 — 13Hz) Brain waves start to slow down out of thinking mind. We feel more calm, peaceful and grounded. We often find ourselves in an “alpha state” after a yoga class, a walk in the woods, a pleasurable sexual encounter or during any activity that helps relax the body and mind. We are lucid, reflective, have a slightly diffused awareness. The hemispheres of the brain are more balanced (neural integration).
#
#4. Theta State: (4 — 8Hz) We're able to begin meditation. This is the point where the verbal/thinking mind transitions to the meditative/visual mind. We begin to move from the planning mind to a deeper state of awareness (often felt as drowsy), with stronger intuition, more capacity for wholeness and complicated problem solving. The Theta state is associated with visualization.
#
#5. Delta State: (1—3 Hz) Tibetan monks who have been meditating for decades can reach this in an alert, wakened phase, but most of us reach this final state during deep, dreamless sleep.


import argparse
import math
import pyaudio
import numpy as np
import sys

from tkinter import *
from tkinter.ttk import *
import os
import threading
import multiprocessing
import time

from pythonosc import dispatcher
from pythonosc import osc_server

#pydub sound generation

from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

#---Sound generation globals---
p = pyaudio.PyAudio()
volume = 0.5
fs = 44100
duration =2
samples = 0

#---Muse globals---
alpha_relative = 0
server = None

#---General functionality globals---
isHandled = False
isServing = True

#def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
#    print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)

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

#def absolutes(unused_addr, args, ch1, ch2, ch3, ch4):
#    print( alpha_relative )

#   This function generates the binaural beats with a 5 hertz difference based on the current
#   alpha_relative value

"""
#def binaural_beats():
#    global alpha_relative
#    fL = alpha_relative * 1500
#    print("in binaural_beats, ", alpha_relative, " ", fL )
#    fR = fL+5
#    sampleL = (np.sin(2*np.pi*np.arange(fs*duration)*fL/fs)).astype(np.float32)
#    sampleR = (np.sin(2*np.pi*np.arange(fs*duration)*fR/fs)).astype(np.float32)
    
#    global samples
#    samples = np.zeros(fs*duration*2).astype(np.float32)
#    samples[::2] = sampleL
#    samples[1::2] = sampleR

#   This function actually opens a stream and plays the binaural beats calculated in binaural_beats
def play(samples, volume):
    stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=2,
                    rate = fs,
                    output = True)
        
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    global isHandled
    isHandled = False"""
#    p.terminate()

#trying to generate Binaural beat via pydub instead of pyaudio
def binaural_beat_with_pydub():
    if alpha_relative !=0: 
        print("non 0 alpha_relative")
        tone1 = Sine(200).to_audio_segment(duration=10000)
        tone2 = Sine(210).to_audio_segment(duration=10000)

        left1 = tone1
        right1 = tone2

        tone3 = Sine(200).to_audio_segment(duration=3000)
        tone4 = Sine(204).to_audio_segment(duration=3000)

        left2 = tone3
        right2 = tone4

        alpha = AudioSegment.from_mono_audiosegments(left1, right1)
        theta = AudioSegment.from_mono_audiosegments(left2, right2)

        #descend = alpha.append(stereo2, crossfade=1000)
        alpha_to_theta = alpha.append(theta, crossfade=1000)
        play(alpha_to_theta)

    else: 
        print("alpha_relative is 0")
        run_server()
        isHandled = False

#   This function starts the server within the while loop
def begin_server():
    global isServing
    isServing = True

#   This function ends the server within the while loop
def end_server():
    global isServing
    isServing = False

#   This function recursively calls itself so that we don't need to use .serve_forever()
def run_server():
    # isServing allows us to start/stop the stream of data without having to rerun the program
    # isHandled makes sure handle_request, binaural_beats, and play() all run IN THAT ORDER
    if( isServing ):
        print("is serving")
        server.handle_request()
        if( isHandled ):
            print("is handling")
            #binaural_beats()
            #play(samples, volume)
            binaural_beat_with_pydub()
            isHandled = False


    # 1 is in milliseconds
    window.after(100, run_server) #KILLLING THE WHILE LOOP HOPEFULLY

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
    
    # use lambdas so the command functions don't run on button initialization
    button1 = Button(top, text="Start EEG data", command=lambda : begin_server())
    button2 = Button(bottom, text="Stop EEG data", command=lambda : end_server())
    
    button1.pack()
    button2.pack()

    # start the server
    run_server()
    
    # start the GUI
    window.mainloop()
