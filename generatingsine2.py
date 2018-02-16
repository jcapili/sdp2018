import pyaudio
import numpy as np
import sys

p = pyaudio.PyAudio()

volume = 0.5
fs = 44100
duration = 10 #need to figure out how to generate the tone indefinitely
#f = 200  #frequency in hz 


#try:  #if the while loop starts here, clicking sound as new tone is generated 
#	while True: #plays the tone forever 


#for f in range(200, 500, 5): #this changes the frequency 

while (1): #need to figure out how to make the sound continously play while waiting for next input 
	fL = int(input("enter a frequency: "))
	fR = fL+5
	sampleL = (np.sin(2*np.pi*np.arange(fs*duration)*fL/fs)).astype(np.float32)
	sampleR = (np.sin(2*np.pi*np.arange(fs*duration)*fR/fs)).astype(np.float32)
	#samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

	samples = np.zeros(fs*duration*2).astype(np.float32)
	samples[::2] = sampleL
	samples[1::2] = sampleR

	stream = p.open(
				format=pyaudio.paFloat32,
				channels=2,
				rate = fs,
				output = True)

	try:
	#	while True:
			stream.write(volume*samples) #the problem with this is that we need to change the pitch given input from muse, need to write a new stream 

	except KeyboardInterrupt:
		stream.stop_stream()
		stream.close()
		p.terminate()