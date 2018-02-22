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

from pythonosc import dispatcher
from pythonosc import osc_server

p = pyaudio.PyAudio()

alpha_relative = 0
volume = 0.5
fs = 44100
duration =2

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)

#delta_relative    1-4Hz
#theta_relative    4-8Hz
#alpha_relative    7.5-13Hz
#beta_relative    13-30Hz
#gamma_relative    30-44Hz

def get_alpha_relative(unused_addr, args, ch1, ch2, ch3, ch4 ):
#        print("Alpha relative: ", ch1, ch2, ch3, ch4 )
    total = 0;
    numOfNotNan = 0;
    
    if( math.isnan(ch1) == False ):
#            print( "ch1 is a num ")
        total += ch1
        numOfNotNan += 1
    
    if( math.isnan(ch2) == False ):
#            print( "ch2 is a num ")
        total += ch2
        numOfNotNan += 1

    if( math.isnan(ch3) == False ):
#            print( "ch3 is a num ")
        total += ch3
        numOfNotNan += 1

    if( math.isnan(ch4) == False ):
#            print( "ch4 is a num ")
        total += ch4
        numOfNotNan += 1

    if( numOfNotNan == 0 ):
        print( "waiting for numbers...:" )
    else:
        global alpha_relative
        alpha_relative = total / numOfNotNan
        print("Average of alpha relative: ", alpha_relative )

def absolutes(unused_addr, args, ch1, ch2, ch3, ch4):
    print( alpha_relative )

def get_alpha():
    global alpha_relative
    return alpha_relative

def binaural_beats():
    fL = get_alpha() * 1500
    print("in binaural_beats, ", get_alpha(), " ", fL )
    fR = fL+5
    sampleL = (np.sin(2*np.pi*np.arange(fs*duration)*fL/fs)).astype(np.float32)
    sampleR = (np.sin(2*np.pi*np.arange(fs*duration)*fR/fs)).astype(np.float32)

    samples = np.zeros(fs*duration*2).astype(np.float32)
    samples[::2] = sampleL
    samples[1::2] = sampleR

    stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=2,
                    rate = fs,
                    output = True)
    print("here")
#    stream.write(volume*samples)
#
#    except KeyboardInterrupt:
#        stream.stop_stream()
#        stream.close()
#        p.terminate()

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
    dispatcher.map("/muse/elements/alpha_absolute", absolutes, "alpha_absolute" )


    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    
    while(1):
        server.handle_request();
#        print( "handled request" )
        binaural_beats();


