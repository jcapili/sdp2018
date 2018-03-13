from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

import threading
import time

#---Sound generation globals---
tone_length = 2000 # Changeable
fade_length = int(tone_length * 0.25) # Changeable

"""
Sleep time between sounds in seconds, used with the time library
"""
sleep_time = tone_length * 0.75 / 1000 # Changeable

"""
Used by server.py to switch tones if the difference in alpha waves is large enough
"""
switchTones = False

freq1 = 200
freq2 = 400

#---Threading globals---
"""
If this is True, the current binaural beat is the first tone. If this is False, the current binaural beat is the second tone
"""
firstIsPlaying = True

"""
Used to start/stop the threads from calling each other
"""
isPlaying = False

"""
This function plays the specified freq1 tone as a binaural beat, with specified tone_length and fade_length
"""
def play_tone_1():
    tone1 = Sine(freq1).to_audio_segment(duration=tone_length)
    tone2 = Sine(freq1+10).to_audio_segment(duration=tone_length)
    
    left = tone1
    right = tone2

    alpha = AudioSegment.from_mono_audiosegments(left, right).fade_in(duration=fade_length).fade_out(duration=fade_length)

    play(alpha)

"""
This function plays the specified freq2 tone as a binaural beat, with specified tone_length and fade_length.
"""
def play_tone_2():
    tone1 = Sine(freq2).to_audio_segment(duration=tone_length)
    tone2 = Sine(freq2+8).to_audio_segment(duration=tone_length)
    
    left = tone1
    right = tone2

    theta = AudioSegment.from_mono_audiosegments(left, right).fade_in(duration=fade_length).fade_out(duration=fade_length)

    play(theta)

"""
This function plays the given sound file, which in this case is birds chirping.
"""
def sound_effects():
    sound1 = AudioSegment.from_file("/Users/jasoncapili/Documents/GitHub/sounds/birds.m4a", format="m4a")
    play(sound1)

"""
This function uses a while loop within the thread from the function start_timer to keep track of how long a binaural beat has been playing. Once the beat has been playing for sleep_time, the function uses the state of various global variables to either keep playing the current tone or switch to the other tone. It then breaks out of the while loop and terminates the daemon thread it's in.
"""
def timer():
    global firstIsPlaying, sleep_time, switchTones
    start = time.time()
    while(1):
        # sleep_time - 1 accounts for sleep before starting timer
        if (time.time() - start) > (sleep_time - 1):
            if firstIsPlaying is True and switchTones is False:
                print("starting bin beat 1")
                binaural_thread_1()
            elif firstIsPlaying is True and switchTones is True:
                print("starting bin beat 2")
                binaural_thread_2()
                firstIsPlaying = False
                switchTones = False
            elif firstIsPlaying is False and switchTones is False:
                print("starting bin beat 2")
                binaural_thread_2()
            elif firstIsPlaying is False and switchTones is True:
                print("starting bin beat 1")
                binaural_thread_1()
                firstIsPlaying = True
                switchTones = False
            break

"""
This function starts the thread that contains the timer for each binaural beat.
"""
def start_timer():
    if( isPlaying ):
        threading.Thread(target=timer, daemon=True).start()

"""
This function starts the thread that contains play_tone_1.
"""
def binaural_thread_1():
    threading.Thread(target=play_tone_1, daemon=True).start()
    # Sleep to avoid seg fault
    time.sleep(1)
    start_timer()

"""
This function starts the thread that contains play_tone_2.
"""
def binaural_thread_2():
    threading.Thread(target=play_tone_2, daemon=True).start()
    # Sleep to avoid seg fault
    time.sleep(1)
    start_timer()

"""
This function starts the thread that contains sound_effects.
"""
def start_sound_effects_thread():
    threading.Thread(target=sound_effects, daemon=True).start()

"""
This function stops all sounds from repeating.
"""
def stop_all_sounds():
    global isPlaying
    isPlaying = False

"""
This function starts all sounds if they're not already playing.
"""
def start_all_sounds():
    global isPlaying
    if isPlaying is False:
        isPlaying = True
        binaural_thread_1()
        start_sound_effects_thread()
