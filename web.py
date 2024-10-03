import streamlit as st
from utils import record_audio, pepper_say
from connection import Connection
import time
import threading


#creating the connection
if 'pepper' not in st.session_state:
    st.session_state.pepper = Connection()
    # ip='127.0.0.1'
    # port=38215
    # ip='10.0.0.244'
    ip='192.168.1.53'
    port=9559
    st.session_state.session = st.session_state.pepper.connect(ip, port)
    # Create a proxy to the AL services
    st.session_state.behavior_mng_service = st.session_state.session.service("ALBehaviorManager")
    st.session_state.tts_service = st.session_state.session.service("ALTextToSpeech")
    # setting parameters
    st.session_state.tts_service.setParameter("speed", 85)

if 'messages' not in st.session_state:
    st.session_state.messages=[{"role": "system", "content": 'You are a robot named Pepper who acts as an assistance and resource person at the Collaborative Robotics Lab University of Canberra.' \
                                'Today you are helping at the University of Canberra Open day-'
                    'You are funny, Friendly and approachable. You always limit your response to 2 to 3 sentences' \
                    'You output only one of the following EMOTIONS = HAPPY, SAD, ANGRY, NEUTRAL, SURPRISED, DISGUSTED, FEARFUL, FRIENDLY, CHEEKY attached with the sentiment of each sentence' \
                    'An emotion should be output in the format [EMOTION]. Each and every sentence you output should should have an emotion attached to it' \
                    'You do not ever say the words "but hey"'}]

# Play an animation
def animation(button_name='listening',text='', behavior_mng_service=None,tts_service=None):
    if not button_name=='listening':
        behavior_mng_service.stopAllBehaviors()
    behavior_mng_service.startBehavior("pepper_web/"+button_name)
    if not text=='':
       tts_service.say(text)

# Function to simulate Pepper's actions
def perform_pepper_action(action):
    if action == "dance":
        st.success("Pepper is dancing")
    elif action == "tell_joke":
        st.success("Pepper is making a joke'")
    elif action == "animal":
        st.success("Pepper is acting as an animal'")
    elif action == "music":
        st.success("Pepper is singing")
        # st.session_state.behavior_mng_service .stopAllBehaviors()
        # st.session_state.tts_service.say("\\audio=\"/home/nao/seedevi.wav\"\\")
    elif action == "selfie":
        st.success("Smile!!!")
    elif action == "play_game":
        st.success("Pepper is playing")
    
    animation(action,behavior_mng_service=st.session_state.behavior_mng_service,tts_service=st.session_state.tts_service)


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

with col2:
    if st.button("Tell a Joke"):
        perform_pepper_action("tell_joke")
    if st.button("Sing a Song"):
        perform_pepper_action("music")
    if st.button("Play a Game"):
        perform_pepper_action("play_game")

# User text box to ask Pepper questions, with Ask button in the same row
st.header("Ask Pepper a Question")
col_text, col_button = st.columns([3, 1])




col1, col2, col3 = st.columns([1,3,1])

with col2:
    # Button for direct voice interaction with Pepper
    if st.button("Talk to Pepper"):
        # Create a placeholder for temporary text
        placeholder = st.empty()

        # Display the text "Wait for pepper"
        placeholder.write("Wait for pepper.")

        # Start animation in a separate thread
        animation_thread = threading.Thread(
            target=animation, 
            args=('listening', '', st.session_state.behavior_mng_service, st.session_state.tts_service)
        )
        animation_thread.start()

        txt = record_audio()

        # Replace "Peppa" with "Pepper" if it appears
        if "Peppa" in txt:
            txt = txt.replace("Peppa", "Pepper")

        if not txt=='':
            emotion, text = pepper_say(txt,st.session_state.messages)
            placeholder.write("Pepper Speaking...")
            emo1 = emotion[0][0].lower()
            # animation(emo1, text)

            # Start a second animation with parameters in a separate thread
            animation_thread_emo1 = threading.Thread(
                target=animation, 
                args=(emo1, text, st.session_state.behavior_mng_service, st.session_state.tts_service)
            )
            animation_thread_emo1.start()

            try:
                emo2 = emotion[1][0].lower()                
                time.sleep(1.5)
                # animation(emo2)

                # Start the second animation for emo2 in a separate thread
                animation_thread_emo2 = threading.Thread(
                    target=animation, 
                    args=(emo2, '', st.session_state.behavior_mng_service, st.session_state.tts_service)
                )
                animation_thread_emo2.start()
            except IndexError:
                pass

        # Clear the placeholder (removes the text after the actions are done)
        placeholder.empty()

# Add any additional layout or interactive elements if needed
st.text("Interact with Pepper using buttons, or ask your question.")
