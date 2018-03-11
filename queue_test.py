# python3 source code
from tkinter import *
from tkinter.ttk import *
import threading
import time
import queue

from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

root = Tk()
msg = StringVar()
Label(root, textvariable=msg).pack()
tone_length = 2000

# This is our own event queue, each element should be in this form:
# (function_to_be_called_from_gui_thread, function_arguments)
# In python, functions are objects and can be put in a queue.
my_event_queue = queue.Queue()


def play_tone_1():
    tone1 = Sine(200).to_audio_segment(duration=tone_length)
    tone2 = Sine(210).to_audio_segment(duration=tone_length)
    
    left1 = tone1
    right1 = tone2
    
    tone3 = Sine(200).to_audio_segment(duration=tone_length)
    tone4 = Sine(204).to_audio_segment(duration=tone_length)
    
    left2 = tone3
    right2 = tone4
    
    alpha = AudioSegment.from_mono_audiosegments(left1, right1)
    theta = AudioSegment.from_mono_audiosegments(left2, right2)
    
    #descend = alpha.append(stereo2, crossfade=1000)
    alpha_to_theta = alpha.append(theta, crossfade=1000)
    play(alpha_to_theta)

def play_tone_2():
    tone1 = Sine(400).to_audio_segment(duration=tone_length)
    tone2 = Sine(420).to_audio_segment(duration=tone_length)
    
    left1 = tone1
    right1 = tone2
    
    tone3 = Sine(400).to_audio_segment(duration=tone_length)
    tone4 = Sine(408).to_audio_segment(duration=tone_length)
    
    left2 = tone3
    right2 = tone4
    
    alpha = AudioSegment.from_mono_audiosegments(left1, right1)
    theta = AudioSegment.from_mono_audiosegments(left2, right2)
    
    #descend = alpha.append(stereo2, crossfade=1000)
    alpha_to_theta = alpha.append(theta, crossfade=1000)
    play(alpha_to_theta)



def test():
    print("it's working")

def test1():
    threading.Thread(target=play_tone_1, daemon=True).start()  # start worker in new thread

def test2():
    threading.Thread(target=play_tone_2, daemon=True).start()  # start worker in new thread


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


#my_event_handler()  # start handler, after root.mainloop(), this method will be called every 100ms. Or you can use root.after(100, my_event_handler)

Label(root, text="Hello World").pack() # Add text to the window via a label

top = Frame(root)
top.pack()
bottom = Frame(root)
bottom.pack(side=BOTTOM)

# use lambdas so the command functions don't run on button initialization
button1 = Button(top, text="Play tone 1", command=lambda : test1())
button2 = Button(bottom, text="Play tone 2", command=lambda : test2())

button1.pack()
button2.pack()

root.mainloop()
