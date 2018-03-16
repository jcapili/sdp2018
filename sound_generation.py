from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
from random import *
import threading
import time

#---Sound generation globals---
tone_length = 2000 # Changeable
fade_length = int(tone_length * 0.15) # Changeable
volume_reduction = 20 # Changeable
sleep_time = tone_length * 0.65 / 1000 # Changeable
switchTones = False
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
firstIsPlaying = True
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

    alpha = alpha - volume_reduction

    play(alpha)

"""
This function plays the specified freq2 tone as a binaural beat, with specified tone_length and fade_length.
"""
def play_tone_2():
    tone1 = Sine(freq2).to_audio_segment(duration=tone_length)
    tone2 = Sine(freq2+10).to_audio_segment(duration=tone_length)
    
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
        play(AudioSegment.from_file(file, format="mp3"))


"""
This function uses a while loop within the thread from the function start_timer to keep track of how long a binaural beat has been playing. Once the beat has been playing for sleep_time, the function uses the state of various global variables to either keep playing the current tone or switch to the other tone. It then breaks out of the while loop and terminates the daemon thread it's in.
"""
def timer():
    global firstIsPlaying, sleep_time, switchTones, freq1, freq2
    start = time.time()
    while(1):
        # sleep_time - 1 accounts for sleep before starting timer
        if (time.time() - start) > (sleep_time - 1):
            if firstIsPlaying is True and switchTones is False:
#                print("starting bin beat 1")
                binaural_thread_1()
            elif firstIsPlaying is True and switchTones is True:
#                print("starting bin beat 2")
                freq2 = pick_rand_freq()
                binaural_thread_2()
                firstIsPlaying = False
                switchTones = False
            elif firstIsPlaying is False and switchTones is False:
#                print("starting bin beat 2")
                binaural_thread_2()
            elif firstIsPlaying is False and switchTones is True:
#                print("starting bin beat 1")
                freq1 = pick_rand_freq()
                binaural_thread_1()
                firstIsPlaying = True
                switchTones = False
            break

"""
This function picks a random frequency within the current song's chord list based on the current note that's playing.
"""
# NEED TO IMPLEMENT MACHINE LEARNING HERE
def pick_rand_freq():
    global currentNote
    if currentNote is 0:
        currentNote = randint(1,2)
    elif currentNote is 1:
        random = randint(0,1)
        if random is 0:
            currentNote = 0
        elif random is 1:
            currentNote = 2
    elif currentNote is 2:
        currentNote = randint(0,1)

    return songs[song_id][currentNote]

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
This function starts the sound thread specified by id and contained in the "sounds" folder. Excludes binaural and timer threads.
"""
def start_sound_thread( id ):
    if id == "birds":
        threading.Thread(target=play_sound, args=[id], daemon=True).start()
    elif id in songs:
        threading.Thread(target=play_sound, args=[id], daemon=True).start()

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
    global isPlaying, freq1, freq2, songs, song_id
    if isPlaying is False:
        isPlaying = True
        song_id = id
        freq1 = songs[id][0]
        freq2 = songs[id][1]
        start_sound_thread(id)
        time.sleep(3)
        binaural_thread_1()
