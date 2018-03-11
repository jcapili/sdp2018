#pydub sound generation

from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

tone_length = 5000

def main():
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

#play(descend)

if __name__ == "__main__":
#    main()
#    sound1 = AudioSegment.from_wav("/Users/jasoncapili/Documents/GitHub/sdp2018/birds.wav")
    sound1 = AudioSegment.from_file("/Users/jasoncapili/Documents/GitHub/sdp2018/birds.m4a", format="m4a")

    play(sound1)

