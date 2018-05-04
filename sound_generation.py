from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
from pydub.utils import make_chunks
from random import *
import threading
import time

#---Sound generation globals---
tone_length = 2000 # Changeable
fade_length = int(tone_length * 0.15) # Changeable
volume_reduction = 20 # Changeable
sleep_time = tone_length * 0.65 / 1000 # Changeable
switchTones = False
playAlpha = True
freq1 = 217
freq2 = 274
song_id = None
songs = {
         "Ab":[202, 261, 306],
         "A":[215, 272, 324],
         "Bb":[228, 289, 344],
         "B":[241, 306, 365],
         "C":[257, 324, 387],
         "Db":[133, 142, 202],
         "D":[141, 180, 215],
         "Eb":[150, 191, 228],
         "E":[160, 203, 242],
         "F":[170, 215, 257],
         "Gb":[180, 228, 272],
         "G":[191, 242, 289]
        }

#---Threading globals---
currentNote = 0
isPlaying = False
phases = []
phaseIsPlaying = [False,False,False]

"""
This function plays the specified freq1 tone as a binaural beat, with specified tone_length and fade_length
"""
def play_tone_1():
    tone1 = Sine(freq1).to_audio_segment(duration=tone_length)
    tone2 = Sine(freq1+10).to_audio_segment(duration=tone_length)
    
    left = tone1
    right = tone2

    alpha = AudioSegment.from_mono_audiosegments(left, right).fade_in(duration=fade_length).fade_out(duration=fade_length)

    alpha = alpha - volume_reduction

    play(alpha)

"""
This function plays the specified freq2 tone as a binaural beat, with specified tone_length and fade_length.
"""
def play_tone_2():
    tone1 = Sine(freq1).to_audio_segment(duration=tone_length)
    tone2 = Sine(freq1+5).to_audio_segment(duration=tone_length)
    
    left = tone1
    right = tone2

    theta = AudioSegment.from_mono_audiosegments(left, right).fade_in(duration=fade_length).fade_out(duration=fade_length)
    
    theta = theta - volume_reduction

    play(theta)

"""
This function plays the sound file specified by id
"""
def play_sound(id):
    file = "/Users/jasoncapili/Documents/GitHub/sdp2018/sounds/"
    if id == "birds":
        file += "birds.m4a"
        play(AudioSegment.from_file(file, format="m4a"))
    elif id in songs:
        print( "playing ", id )
        file = file + id + ".mp3"
        custom_play(AudioSegment.from_file(file, format="mp3").fade_in(duration=fade_length).fade_out(duration=fade_length))
        print("playing next song")
        custom_play(AudioSegment.from_file(file, format="mp3").fade_in(duration=fade_length).fade_out(duration=fade_length))

"""
This function stops the song file from playing without needing to do a KeyboardInterrupt
"""
def custom_play(seg):
    import pyaudio
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)
        
    # break audio into half-second chunks (to allows keyboard interrupts)
    for chunk in make_chunks(seg, 500):
        if isPlaying is True:
            stream.write(chunk._data)
        else:
            break

    stream.stop_stream()
    stream.close()

    p.terminate()

"""
This function uses a while loop within the thread from the function start_timer to keep track of how long a binaural beat has been playing. Once the beat has been playing for sleep_time, the function uses the state of various global variables to either keep playing the current tone or switch to the other tone. It then breaks out of the while loop and terminates the daemon thread it's in.
"""
def timer():
    global phases, phaseIsPlaying, playAlpha
    start = time.time()
    while isPlaying is True:
#        print("hello")
        elapsed = time.time() - start
        print(elapsed)
        if elapsed > phases[0] and elapsed < phases[1] and phaseIsPlaying[0] is False:
            print("starting alpha")
            phaseIsPlaying[0] = True
            binaural_thread_1()
        elif elapsed > phases[1] and elapsed < phases[2] and phaseIsPlaying[1] is False:
            print("starting theta")
            phaseIsPlaying[0] = False
            phaseIsPlaying[1] = True
            binaural_thread_2()
        elif elapsed > phases[2] and elapsed < phases[3] and phaseIsPlaying[2] is False:
            phaseIsPlaying[1] = False
            phaseIsPlaying[2] = True
            if playAlpha:
                print("starting alpha")
                binaural_thread_1()
            else:
                print("starting theta")
                binaural_thread_2()
        elif elapsed > phases[3]:
            print("terminating...")
            phaseIsPlaying[2] = False
            stop_session()
        time.sleep(1)

def bin_timer():
    start = time.time()
    while(1):
        if (time.time() - start ) > (sleep_time-1):
            if phaseIsPlaying[0] is True:
                binaural_thread_1()
            elif phaseIsPlaying[1] is True:
                binaural_thread_2()
            elif phaseIsPlaying[2] is True:
                if playAlpha:
                    binaural_thread_1()
                else:
                    binaural_thread_2()
            break

"""
This function starts the thread that contains the timer for each binaural beat.
"""
def start_timer():
    if( isPlaying ):
        threading.Thread(target=timer, daemon=True).start()

def start_bin_timer():
    if( isPlaying ):
        threading.Thread(target=bin_timer, daemon=True).start()
"""
This function starts the thread that contains play_tone_1.
"""
def binaural_thread_1():
    threading.Thread(target=play_tone_1, daemon=True).start()
    # Sleep to avoid seg fault
    time.sleep(1)
    start_bin_timer()

"""
This function starts the thread that contains play_tone_2.
"""
def binaural_thread_2():
    threading.Thread(target=play_tone_2, daemon=True).start()
    # Sleep to avoid seg fault
    time.sleep(1)
    start_bin_timer()

"""
This function starts the sound thread specified by id and contained in the "sounds" folder. Excludes binaural and timer threads.
"""
def start_sound_thread( id ):
    if id == "birds":
        threading.Thread(target=play_sound, args=[id], daemon=True).start()
    elif id in songs:
        threading.Thread(target=play_sound, args=[id], daemon=True).start()
    time.sleep(1)
    start_timer()

"""
This function stops all sounds from repeating.
"""
def stop_session():
    global isPlaying
    isPlaying = False

"""
This function starts all sounds if they're not already playing.
"""
def start_session(id):
    global isPlaying, freq1, freq2, songs, song_id, phases
    if isPlaying is False:
        isPlaying = True
        song_id = id

        name = "/Users/jasoncapili/Documents/GitHub/sdp2018/sounds/"+ id + ".mp3"
        length = len(AudioSegment.from_file(name, format="mp3")) # milliseconds
        phaseLength = 2*length/4
        phases.append( phaseLength )
        phases.append( 2*phaseLength )
        phases.append( 3*phaseLength )
        phases.append( 4*phaseLength )
#        phases.append( 10 )
#        phases.append( 20 )
#        phases.append( 30 )
#        phases.append( 40 )

        freq1 = songs[id][0]
        start_sound_thread(id)
