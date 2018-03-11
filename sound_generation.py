from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

import threading

tone_length = 2000


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

def sound_effects():
    sound1 = AudioSegment.from_file("/Users/jasoncapili/Documents/GitHub/sdp2018/birds.m4a", format="m4a")
    play(sound1)


def start_binaural_thread_1():
    threading.Thread(target=play_tone_1, daemon=True).start()

def start_binaural_thread_2():
    threading.Thread(target=play_tone_2, daemon=True).start()

def start_sound_effects_thread():
    threading.Thread(target=sound_effects, daemon=True).start()

def start_all_sounds():
    threading.Thread(target=play_tone_1, daemon=True).start()
    threading.Thread(target=play_tone_2, daemon=True).start()
