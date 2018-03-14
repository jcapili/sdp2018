# python3 source code
from tkinter import *
from tkinter.ttk import *
import threading
import time
import queue

import os
import threading


from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

from random import *

global binaural_beat

#window = Tk()

root = Tk()
Label(root, text="Hello World").pack() # Add text to the window via a label
    
top = Frame(root)
top.pack()
bottom = Frame(root)
bottom.pack(side=BOTTOM)
    
    # use lambdas so the command functions don't run on button initialization


msg = StringVar()
Label(root, textvariable=msg).pack()

# This is our own event queue, each element should be in this form:
# (function_to_be_called_from_gui_thread, function_arguments)
# In python, functions are objects and can be put in a queue.
my_event_queue = queue.Queue()

def main():
    button1 = Button(top, text="play music", command=lambda : play_binaural_beat())
    button2 = Button(bottom, text="create new beat", command=lambda : generate_binaural_beat())
    #button3 = Button(text="start thread", command = worker())
        
    button1.pack()
    button2.pack()
    #button3.pack()
    root.main()


def generate_binaural_beat():

    x = randint(90, 200)

    tone1 = Sine(x).to_audio_segment(duration=3000)
    tone2 = Sine(x+10).to_audio_segment(duration=3000)

    left1 = tone1
    right1 = tone2

    tone3 = Sine(x).to_audio_segment(duration=3000)
    tone4 = Sine(x+4).to_audio_segment(duration=3000)

    left2 = tone3
    right2 = tone4

    alpha = AudioSegment.from_mono_audiosegments(left1, right1)
    theta = AudioSegment.from_mono_audiosegments(left2, right2)
    global binaural_beat
    binaural_beat = alpha.append(theta, crossfade=1000)
    my_event_queue.put((msg.set, 'binaural beat generated'))
    #play(binaural_beat)

def play_binaural_beat():
    global binaural_beat
    my_event_queue.put((msg.set, 'playing'))
    play(binaural_beat)
    generate_binaural_beat()

def worker():
    """
    This is a time consuming worker, it takes 1 second for each task.
    If you put such a worker in the GUI thread, the GUI will be blocked.
    """
    task_counter = 0
    while True:
        #time.sleep(1)  # simulate a time consuming task
        # show how many tasks finished in the Label. We put this action in my_event_queue instead of handle
        # it from this worker thread which is not safe. This action will be handled by my_event_handler which is
        # called from GUI thread.
        my_event_queue.put((msg.set, '{} tasks finished.'.format(task_counter)))
        main()
        #worker()
        #generate_binaural_beat()
        task_counter += 1


def my_event_handler():
    """
    Query my_event_queue, and handle one event per time.
    """
    try:
        func, *args = my_event_queue.get(block=False)
    except queue.Empty:
        pass
    else:
        func(*args)

    # At last schedule handling for next time.
    # Every 100 ms, my_event_handler will be called
    root.after(100, my_event_handler)



threading.Thread(target=worker, daemon=True).start()  # start worker in new thread


my_event_handler()  # start handler. after root.mainloop(), this method will be called every 100ms. Or you can use root.after(100, my_event_handler)

root.mainloop()


"""
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
"""
    

  
    #---Setting up the UI---
"""
    Label(root, text="Hello World").pack() # Add text to the window via a label
    
    top = Frame(root)
    top.pack()
    bottom = Frame(root)
    bottom.pack(side=BOTTOM)
    
    # use lambdas so the command functions don't run on button initialization
    button1 = Button(top, text="Start EEG data", command=lambda : begin_server())
    button2 = Button(bottom, text="Stop EEG data", command=lambda : end_server())
    
    button1.pack()
    button2.pack()
    """
    # start the server
    #run_server()
    
    # start the GUI
    #window.mainloop()
