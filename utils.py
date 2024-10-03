import streamlit as st
import speech_recognition as sr
from dotenv import load_dotenv
import os
from openai import OpenAI
import re


client = OpenAI()

# Load environment variables from .env file
load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the recognizer
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5

def record_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        # Create a placeholder for temporary text
        placeholder = st.empty()
        placeholder.write("Pepper is Listening...")
        try: 
            audio_data = recognizer.listen(source, phrase_time_limit=5,timeout=10)

            # Save the audio data to a temporary WAV file
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data.get_wav_data())

            # Use OpenAI client to call Whisper API for transcription
            audio_file = open("temp_audio.wav", "rb")
            response = client.audio.transcriptions.create(
                model="whisper-1",      # Whisper model version
                file=audio_file,        # The audio file to transcribe
                language='en'           # Set the language to English
            )

            # Extract the transcription result from the response
            text_result = response.text

            # text_result=recognizer.recognize_google(audio_data, language='en')
            # text_result=recognizer.recognize_whisper_api(audio_data, api_key=OPENAI_API_KEY)
        except sr.UnknownValueError:
            placeholder.write("Google Speech Recognition could not understand audio")
            return ''
        except sr.RequestError as e:
            placeholder.write("Could not request results; {e}")
            return ''
        except sr.WaitTimeoutError:
            placeholder.write("Time out. Please ask the question again.")
            return ''

        # st.write("Finished listening.")
        placeholder.empty()
        return text_result
    
def extract_data(s):
    # Find all words within brackets
    brackets = re.findall(r'\[(.*?)\]', s)

    # Split string by words within brackets
    split_str = re.split(r'\[.*?\]', s)

    # Filter out empty strings and count words
    word_counts = [len(re.findall(r'\w+', segment)) for segment in split_str if segment]

    # Pair each word from the bracket with the corresponding word count
    result = list(zip(brackets, word_counts))

    # Create a cleaned string without words in brackets
    cleaned_string = ''.join(split_str).strip()

    return result, cleaned_string

def pepper_say(question,messages):
    print(question)

    print("Prompting ...")

    messages.append({ "role": "user", "content": question})

    print(messages)

    response = client.chat.completions.create(
        # model="gpt-4-1106-preview",
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5)

    saywhut=response.choices[0].message.content

    data, cleaned = extract_data(saywhut)
    print(data)
    print (cleaned)
    return data,cleaned

def main():
    st.title("Speech Recognition Web App")

    if st.button("Start Listening"):
        # Record audio
        text_result=record_audio()

        st.write("Text output:", text_result)

if __name__ == "__main__":
    main()
