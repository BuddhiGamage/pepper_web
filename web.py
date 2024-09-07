import streamlit as st
from utils import record_audio, pepper_say

# Function to simulate Pepper's actions
def perform_pepper_action(action):
    if action == "dance":
        st.success("Pepper says: 'Time to show off my moves! Let's dance together!'")
    elif action == "tell_joke":
        st.success("Pepper says: 'I’ve got a joke for you! Why don’t robots ever get lost? Because they always follow their GPS!'")
    elif action == "selfie_pose":
        st.success("Pepper says: 'Say cheese! I’ll hold this pose so you can snap the perfect selfie!'")
    elif action == "sing_song":
        st.success("Pepper says: 'Let me serenade you! I hope you like my voice. Here we go!'")
    elif action == "high_five":
        st.success("Pepper says: 'High-five! I’m ready, are you? Let’s do this!'")
    elif action == "play_game":
        st.success("Pepper says: 'Let’s play a quick game of Rock-Paper-Scissors! I bet I can guess your move!'")
    elif action == "greet":
        st.success("Pepper says: 'Hello there! It’s great to see you! How can I make your day more fun?'")
    elif action == "tell_story":
        st.success("Pepper says: 'Gather around! I’ve got a fun story to tell. Are you ready for an adventure?'")

# UI layout
st.title("Play with Pepper")

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
    if st.button("Selfie Pose"):
        perform_pepper_action("selfie_pose")
    if st.button("High-Five"):
        perform_pepper_action("high_five")
    if st.button("Greetings"):
        perform_pepper_action("greet")

with col2:
    if st.button("Tell a Joke"):
        perform_pepper_action("tell_joke")
    if st.button("Sing a Song"):
        perform_pepper_action("sing_song")
    if st.button("Play a Game"):
        perform_pepper_action("play_game")
    if st.button("Tell a Story"):
        perform_pepper_action("tell_story")

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
        st.write("Wait for pepper")
        txt=record_audio()
        res=pepper_say(txt)
        st.success(txt+' pepper told '+res)

# Add any additional layout or interactive elements if needed
st.text("Interact with Pepper using buttons, or ask it questions using the text input above!")
