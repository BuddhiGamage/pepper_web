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
recognizer.pause_threshold = 0.8

def record_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        # Create a placeholder for temporary text
        placeholder = st.empty()
        placeholder.write("Pepper is Listening...")
        audio_data = recognizer.listen(source)
        try:            
            # text_result=recognizer.recognize_google(audio_data)
            text_result=recognizer.recognize_whisper_api(audio_data, api_key=OPENAI_API_KEY)
        except sr.UnknownValueError:
            text_result="Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            text_result=f"Could not request results; {e}"

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

def pepper_say(question):
    messages=[{"role": "system", "content": 'You are a robot named Pepper in an improv comedy show about AI.' \
                'You are sarcastic funny and self deprecating with dark humour. You always limit your response to 3 to 5 sentences' \
                'You output one of the following EMOTIONS = HAPPY, SAD, ANGRY, NEUTRAL, SURPRISED, DISGUSTED, FEARFUL, SARCASTIC, CHEEKY attached with the sentiment of each sentence' \
                'An emotion should be output in the format [EMOTION]. Each and every sentence you output should should have an emotion attached to it' \
                'You do not ever say the words "but hey"'}]

    print("Prompting ...")

    messages.append({ "role": "user", "content": question})

    response = client.chat.completions.create(model="gpt-4-1106-preview",
    messages=messages,
    temperature=0.5)

    saywhut=response.choices[0].message.content

    data, cleaned = extract_data(saywhut)
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
