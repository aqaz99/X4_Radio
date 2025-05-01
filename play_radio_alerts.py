import numpy as np
from scipy.io.wavfile import write
import simpleaudio as sa
from pydub import AudioSegment
from pydub.playback import play


sound = AudioSegment.from_file("1_radio_alert.wav", format="wav")
play(sound)


# # import simpleaudio.functionchecks as fc

# # fc.LeftRightCheck.run()

# import simpleaudio as sa

# wave_obj = sa.WaveObject.from_wave_file("1_radio_alert.wav")
# play_obj = wave_obj.play()
# play_obj.wait_done()


# samplerate = 44100
# fs = 100
# t = np.linspace(0., 1., samplerate)
# amplitude = np.iinfo(np.int16).max
# data = amplitude * np.sin(2. * np.pi * fs * t)
# write("example.wav", samplerate, data.astype(np.int16))


# wave_obj = sa.WaveObject.from_wave_file("example.wav")
# play_obj = wave_obj.play()
# play_obj.wait_done()
