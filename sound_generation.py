from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

import threading
import time

tone_length = 5000
fade_length = int(tone_length * 0.25)

# Sleep time between sounds in seconds, used with the time library
sleep_time = tone_length * 0.75 / 1000

# If this is True, the current binaural beat is the first tone
# If this is False, the current binaural beat is the second tone
firstIsPlaying = True

# Used to start/stop the threads from calling each other
isPlaying = False

# Used to switch tones if the difference in alpha waves is large enough
switchTones = False

def play_tone_1():
    global tone_length, fade_length
    tone1 = Sine(200).to_audio_segment(duration=tone_length)
    tone2 = Sine(210).to_audio_segment(duration=tone_length)
    
    left = tone1
    right = tone2

    alpha = AudioSegment.from_mono_audiosegments(left, right).fade_in(duration=fade_length).fade_out(duration=fade_length)

    play(alpha)

def play_tone_2():
    tone1 = Sine(400).to_audio_segment(duration=tone_length)
    tone2 = Sine(408).to_audio_segment(duration=tone_length)
    
    left = tone1
    right = tone2

    theta = AudioSegment.from_mono_audiosegments(left, right).fade_in(duration=fade_length).fade_out(duration=fade_length)

    play(theta)

def sound_effects():
    sound1 = AudioSegment.from_file("/Users/jasoncapili/Documents/GitHub/sdp2018/birds.m4a", format="m4a")
    play(sound1)

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
            elif firstIsPlaying is False and switchTones is False:
                print("starting bin beat 2")
                binaural_thread_2()
            elif firstIsPlaying is False and switchTones is True:
                print("starting bin beat 1")
                binaural_thread_1()
                firstIsPlaying = True
            break

def start_timer():
    if( isPlaying ):
        threading.Thread(target=timer, daemon=True).start()

def binaural_thread_1():
    threading.Thread(target=play_tone_1, daemon=True).start()
    # Sleep to avoid seg fault
    time.sleep(1)
    start_timer()

def binaural_thread_2():
    threading.Thread(target=play_tone_2, daemon=True).start()
    # Sleep to avoid seg fault
    time.sleep(1)
    start_timer()

def start_sound_effects_thread():
    threading.Thread(target=sound_effects, daemon=True).start()

def stop_all_sounds():
    global isPlaying
    isPlaying = False

def start_all_sounds():
    global isPlaying
    if isPlaying is False:
        isPlaying = True
        binaural_thread_1()
        start_sound_effects_thread()


