import streamlit as st
import threading 
import time
# our custom modules
import recorder
import transcriptor
import painter

if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Ready to Go!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = "" 
    st.session_state.messages = [] 
    st.session_state.frames = [] 

# Callback Functions;
def start_recording():
    st.session_state.record_active.set() 
    st.session_state.frames = []
    st.session_state.recording_status = "🔴 **Voice is Recording...**"
    st.session_state.recording_completed = False
    threading.Thread(target=recorder.record, args=(st.session_state.record_active, st.session_state.frames)).start()

def stop_recording():
    st.session_state.record_active.clear() 
    st.session_state.recording_status = "✅ **Record Completed!**"
    st.session_state.recording_completed = True
# -------------------------------

# UI ISSUES
#  Header Part
st.set_page_config(page_title="TalkToImage", layout="wide", page_icon="./icons/app_icon.png")
st.image(image="./icons/top_banner.png", use_column_width=True)
st.title("TalkToImage: Konusarak Çiz!")
st.divider()
# -------------------------------
# Content Paerts
col_audio, col_image = st.columns([1,4]) # 1 birim soldaki kolon, 4 birim sağdaki kolon genişlik oranları

# Column-1
with col_audio:
    st.subheader("Ses Kayıt")
    st.divider()
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    # Inner Coulmns
    subcol_left, subcol_right = st.columns([1,2])

    with subcol_left:
        start_btn = st.button(label="Start", on_click=start_recording, disabled=st.session_state.record_active.is_set())
        stop_btn = st.button(label="Stop", on_click=stop_recording, disabled=not st.session_state.record_active.is_set())
    with subcol_right:
        recorded_audio = st.empty() 

        if st.session_state.recording_completed:
            with st.spinner("File getting ready!..."):
                time.sleep(1)
                recorded_audio.audio(data="voice_prompt.wav")

    st.divider()
    latest_image_use = st.checkbox(label="Use the last picture!")

# Column-2
with col_image:
    st.subheader("Image Outputs")
    st.divider()
    # chat messages history to be shown
    for message in st.session_state.messages:# message => dict obj. , messages => list obj.
        if message["role"] == "assistant":
            with st.chat_message(name=message["role"], avatar="./icons/ai_avatar.png"):
                st.warning("Here is your created image =>")
                st.image(image=message["content"], width=300) 
        elif message["role"] == "user":
            with st.chat_message(name=message["role"], avatar="./icons/user_avatar.png"):
                st.success(message["content"])

    # check stop button for new entry
    if stop_btn:
        with st.chat_message(name="user", avatar="./icons/user_avatar.png"):
            with st.spinner("Voice Analysing..."):
                voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name="voice_prompt.wav")
            st.success(voice_prompt) 

        st.session_state.messages.append({"role": "user", "content": voice_prompt}) 

        with st.chat_message(name="assistant", avatar="./icons/ai_avatar.png"):
            st.warning("Here is your created image =>")
            with st.spinner("Image is Composing..."):
                if latest_image_use:
                    image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
                else:
                    image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)

            st.image(image=image_file_name, width=300) 

            with open(image_file_name, "rb") as file:
                st.download_button(
                    label="Download",
                    data=file,
                    file_name=image_file_name,
                    mime="image/png"
                )

        st.session_state.messages.append({"role": "assistant", "content": image_file_name})
        st.session_state.latest_image = image_file_name