import streamlit as st
from utils import record_audio, pepper_say
from connection import Connection
import time


#creating the connection
st.session_state.pepper = Connection()
ip='127.0.0.1'
port=43521

# ip='10.0.0.244'
# port=9559
st.session_state.session = st.session_state.pepper.connect(ip, port)

# Create a proxy to the AL services
st.session_state.behavior_mng_service = st.session_state.session.service("ALBehaviorManager")
st.session_state.tts_service = st.session_state.session.service("ALTextToSpeech")
# setting parameters
st.session_state.tts_service.setParameter("speed", 85)

# Play an animation
def animation(button_name='listening',text=''):
    st.session_state.behavior_mng_service .stopAllBehaviors()
    st.session_state.behavior_mng_service .startBehavior("pepper_web/"+button_name)
    if not text=='':
        st.session_state.tts_service.say(text)

# Function to simulate Pepper's actions
def perform_pepper_action(action):
    if action == "dance":
        st.success("Pepper is dancing")
    elif action == "tell_joke":
        st.success("Pepper is making a joke'")
    elif action == "animal":
        st.success("Pepper is acting as an animal'")
    elif action == "sing_song":
        st.success("Pepper is singing")
    elif action == "selfie":
        st.success("Smile!!!")
    elif action == "play_game":
        st.success("Pepper is playing")
    # # elif action == "greet":
    # #     st.success("Pepper says: 'Hello there! It’s great to see you! How can I make your day more fun?'")
    # elif action == "tell_story":
    #     st.success("Pepper says: 'Gather around! I’ve got a fun story to tell. Are you ready for an adventure?'")
    animation(action)


# UI layout
st.markdown("<h1 style='text-align: center;'>Play with Pepper</h1>", unsafe_allow_html=True)
# st.title("Play with Pepper")

st.header("Interactive Actions with Pepper")
st.text("Click any button below to see Pepper in action:")

# Apply CSS to ensure buttons have the same width
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create two columns for the 8 buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Dance"):
        perform_pepper_action("dance")
    if st.button("Animal Poses"):
        perform_pepper_action("animal")
    if st.button("Selfie Pose"):
        perform_pepper_action("selfie")
    # if st.button("Greetings"):
    #     perform_pepper_action("greet")

with col2:
    if st.button("Tell a Joke"):
        perform_pepper_action("tell_joke")
    if st.button("Sing a Song"):
        perform_pepper_action("sing_song")
    if st.button("Play a Game"):
        perform_pepper_action("play_game")
    # if st.button("Tell a Story"):
    #     perform_pepper_action("tell_story")

# User text box to ask Pepper questions, with Ask button in the same row
st.header("Ask Pepper a Question")
col_text, col_button = st.columns([3, 1])

# with col_text:
#     user_input = st.text_input("Type your question here:")

# with col_button:
#     st.write("")
#     st.write("")
#     if st.button("Ask"):
#         st.success(f"Pepper says: 'You asked: {user_input}. I will answer shortly!'")


col1, col2, col3 = st.columns([1,3,1])

with col2:
    # Button for direct voice interaction with Pepper
    if st.button("Talk to Pepper"):
        # Create a placeholder for temporary text
        placeholder = st.empty()

        # Display the text "Wait for pepper"
        placeholder.write("Wait for pepper.")

        # Perform actions
        animation()
        txt = record_audio()
        emotion, text = pepper_say(txt)
        placeholder.write("Pepper Speaking...")
        emo1 = emotion[0][0].lower()
        emo2 = emotion[1][0].lower()
        animation(emo1, text)
        time.sleep(1.5)
        animation(emo2)

        # Clear the placeholder (removes the text after the actions are done)
        placeholder.empty()

# Add any additional layout or interactive elements if needed
st.text("Interact with Pepper using buttons, or ask it questions using the text input above!")
