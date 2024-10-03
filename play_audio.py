from connection import Connection
import time

pepper = Connection()
ip='10.0.0.244'
port=9559
session = pepper.connect(ip, port)

audio_player_service = session.service("ALAudioPlayer")
fileId = audio_player_service.loadFile("/usr/share/naoqi/wav/random.wav")
audio_player_service.play(fileId, _async=True)

time.sleep(3)

#The audio file must be a WAV file that contains linear 16-bit PCM samples at 22050Hz
# can change the voices for getAvailableVoices()

tts_service = session.service("ALTextToSpeech")
tts_service.say("\\audio=\"/usr/share/naoqi/wav/0.wav\"\\")