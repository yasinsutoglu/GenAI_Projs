import streamlit as st
import assistant_helper

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.thread_id = None


st.set_page_config(page_title="Python Coding Assistant", page_icon=":speech_balloon:")
st.title("Python Coding Assistant")
st.divider()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your Entry"):

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Preparing Answer..."):
        if st.session_state.thread_id is None:
            st.session_state.thread_id = assistant_helper.start_new_thread()
        
        assistant_helper.add_message_to_thread(thread_id=st.session_state.thread_id, prompt=prompt)

        AI_Response = assistant_helper.execute_run_cycle(thread_id=st.session_state.thread_id)

        with st.chat_message("assistant"):
            st.markdown(AI_Response)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": AI_Response})


        