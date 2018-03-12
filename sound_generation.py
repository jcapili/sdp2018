from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

import threading
import time

tone_length = 2000
fade_length = int(tone_length * 0.25)

# Sleep time between sounds in seconds, used with the time library
sleep_time = tone_length * 0.95 / 1000

# If this is True, the current binaural beat is the first one, so play the second one.
# If this is False, the current binaural beat is the second one, so play the first one.
thread_tracker = True

isPlaying = True

def play_tone_1():
    global tone_length, fade_length
    tone1 = Sine(200).to_audio_segment(duration=tone_length)
    tone2 = Sine(210).to_audio_segment(duration=tone_length)
    
    left1 = tone1
    right1 = tone2
    
    tone3 = Sine(200).to_audio_segment(duration=tone_length)
    tone4 = Sine(204).to_audio_segment(duration=tone_length)
    
    left2 = tone3
    right2 = tone4
    
    alpha = AudioSegment.from_mono_audiosegments(left1, right1).fade_in(duration=fade_length)
    theta = AudioSegment.from_mono_audiosegments(left2, right2).fade_out(duration=fade_length)
    
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
    
    alpha = AudioSegment.from_mono_audiosegments(left1, right1).fade_in(duration=fade_length)
    theta = AudioSegment.from_mono_audiosegments(left2, right2).fade_out(duration=fade_length)
    
    #descend = alpha.append(stereo2, crossfade=1000)
    alpha_to_theta = alpha.append(theta, crossfade=1000)
    play(alpha_to_theta)

def sound_effects():
    sound1 = AudioSegment.from_file("/Users/jasoncapili/Documents/GitHub/sdp2018/birds.m4a", format="m4a")
    play(sound1)

def timer():
    start = time.time()
    while(1):
        # sleep_time - 1 accounds for sleep before starting timer
        if (time.time() - start) > (sleep_time - 1):
            global thread_tracker
            if( thread_tracker ):
                print("starting bin beat 2")
                binaural_thread_2()
                thread_tracker = False
            else:
                print("starting bin beat 1")
                binaural_thread_1()
                thread_tracker = True
            break

def start_timer():
    global isPlaying
    if( isPlaying ):
        threading.Thread(target=timer, daemon=True).start()

def binaural_thread_1():
    global sleep_time, isPlaying
    threading.Thread(target=play_tone_1, daemon=True).start()
    # Sleep to avoid seg fault
#    time.sleep(sleep_time)
#    if isPlaying:
#        binaural_thread_2()
    time.sleep(1)
    start_timer()

def binaural_thread_2():
    global sleep_time, isPlaying
    threading.Thread(target=play_tone_2, daemon=True).start()
    # Sleep to avoid seg fault
#    time.sleep(sleep_time)
#    if isPlaying:
#        binaural_thread_1()
    time.sleep(1)
    start_timer()

def start_sound_effects_thread():
    threading.Thread(target=sound_effects, daemon=True).start()

def stop_all_sounds():
    global isPlaying
    isPlaying = False

def restart_all_sounds():
    global isPlaying
    isPlaying = True

def start_all_sounds():
    binaural_thread_1()
    start_sound_effects_thread()


