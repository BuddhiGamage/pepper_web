from connection import Connection
import time

pepper = Connection()
ip='10.0.0.244'
port=9559
session = pepper.connect(ip, port)


audio_device = session.service("ALAudioDevice")

# audio will recored inside the pepper
audio_device.startMicrophonesRecording("sample_recording.wav")
time.sleep(5)
audio_device.stopMicrophonesRecording()