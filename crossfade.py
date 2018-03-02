#pydub sound generation

from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

tone1 = Sine(200).to_audio_segment(duration=2000)
tone2 = Sine(210).to_audio_segment(duration=2000)

left1 = tone1
right1 = tone2

tone3 = Sine(100).to_audio_segment(duration=2000)
tone4 = Sine(105).to_audio_segment(duration=2000)

left2 = tone3
right2 = tone4

alpha = AudioSegment.from_mono_audiosegments(left1, right1)
stereo2 = AudioSegment.from_mono_audiosegments(left2, right2)

#descend = alpha.append(stereo2, crossfade=1000)

play(alpha)

#play(descend)



