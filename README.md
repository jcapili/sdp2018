# sdp2018

To connect the muse device to server:
Connect to computer via bluetooth
muse-io --device Muse-XXXX --osc osc.udp://localhost:5000
replace the 4 X’s with your muse’s number shown in bluetooth
and then once that connects, run the server program in a different terminal tab

sound_generation globals:
sleep_time: This is the time between sounds in seconds as opposed to milliseconds so that the time library functions are compatible with it
switchTones: Used by server.py to switch tones if the difference in alpha waves is large enough
firstIsPlaying: If this is True, the current binaural beat is the first tone. If this is false, the current binaural beat is the second one.
isPlaying: Used to start/stop the threads from calling each other
freq1: Corresponds to the frequency played by play_tone_1. The frequency is determined by pick_rand_freq() and the specified frequencies in the "songs" dictionary

pip3 installs:
    -matplotlib
    -pydub
    -numpy
    -pyaudio
