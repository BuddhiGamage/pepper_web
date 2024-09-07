import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np
import tempfile

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_data = AudioSegment.silent(duration=0)  # Store the recorded audio
        self.silence_threshold = -50  # in dBFS (decibel relative to full scale)

    def recv(self, frame):
        # Convert audio frame to pydub AudioSegment
        audio_frame = np.frombuffer(frame.to_ndarray().flatten(), np.int16)
        audio_segment = AudioSegment(
            data=audio_frame.tobytes(),
            sample_width=2,  # 2 bytes = 16 bits
            frame_rate=frame.sample_rate,
            channels=1
        )

        # Add the current segment to the stored audio data
        self.audio_data += audio_segment

        # Detect non-silent parts
        non_silent_ranges = detect_nonsilent(self.audio_data, min_silence_len=1000, silence_thresh=self.silence_threshold)

        # Stop recording when no non-silent parts are detected for 1 second
        if not non_silent_ranges:
            return None  # Signal to stop the recording by returning None

        return frame

    def get_audio(self):
        return self.audio_data

def save_audio_to_file(audio_segment, filename):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        audio_segment.export(f.name, format="wav")
        return f.name

st.title("Real-time Audio Recording with Silence Detection")

# Set up the WebRTC streamer
ctx = webrtc_streamer(
    key="audio-recorder",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=512,
    video_receiver_size=None,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if ctx.audio_processor:
    st.write("Recording audio... Speak into your microphone.")
    audio_processor = ctx.audio_processor

    # Stop the recording when the user manually stops or the stream is closed
    if not ctx.state.playing:
        st.write("Recording finished.")
        recorded_audio = audio_processor.get_audio()

        if len(recorded_audio) > 0:
            # Save the recorded audio to a file
            audio_file_path = save_audio_to_file(recorded_audio, "recorded_audio.wav")
            st.write(f"Audio saved: {audio_file_path}")
            st.audio(audio_file_path)
