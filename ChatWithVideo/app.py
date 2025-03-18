import streamlit as st
import videohelper
import raghelper

if "current_video_url" not in st.session_state:
    st.session_state.current_video_url = None
    st.session_state.current_transcript_docs = []
    st.session_state.videos = []
    
st.set_page_config(page_title="ChatWithVideo!", layout="centered")
st.image(image="./img/app_banner.png")
st.title("Chat With Video!")
st.divider()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROCESS-1 : find related videos -> download media files -> extract sound file -> converts to transcript (use videohelper)
# PROCESS-2 : Text -> RAG issues (use raghelper)

tab_url, tab_search = st.tabs(["By URL Entry", "By Searching"])

with tab_url:

    video_url = st.text_input(label="Enter Youtube Video URL:", key="url_video_url")
    if video_url:
        st.video(data=video_url)
        st.divider()
    prompt = st.text_input(label="Ask To Video?:", key="url_prompt")
    submit_btn = st.button("ASK", key="url_submit")

    if submit_btn:
        st.divider()
        if st.session_state.current_video_url != video_url:
            with st.spinner("Step-1: Video text is preparing..."):
                video_transcript_docs = videohelper.get_video_transcript(url=video_url)
                st.session_state.current_transcript_docs = video_transcript_docs

        st.success("Video transcript saved on cache!")
        st.divider()
        st.session_state.current_video_url = video_url

        with st.spinner("Step-2: Answering..."):
            AI_Response, relevant_documents = raghelper.rag_with_video_transcript(transcript_docs=st.session_state.current_transcript_docs, prompt=prompt)

        st.info("AI_Model Answer:")
        st.markdown(AI_Response)
        st.divider()

        for doc in relevant_documents:
            st.warning("Reference:")
            st.caption(doc.page_content)
            st.markdown(f"Source: {doc.metadata}")
            st.divider()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++
with tab_search:
    
    col_left, col_center, col_right = st.columns([20,1,10])
    # -----------------------------------
    with col_left:
        st.subheader("Video Searching Process!")
        st.divider()

        search_term = st.text_input(label="Enter the words to be searched:", key="search_term")
        video_count = st.slider(label="Result Count", min_value=1, max_value=5, value=5, key="search_video_count")
        sorting_options = ["Most Related", "By UploadDate", "By ViewCount", "By Rating"]
        sorting_criteria = st.selectbox(label="Ordering Criteria", options=sorting_options)
        search_btn = st.button(label="SEARCH", key="search_button")
        st.divider()

        if search_btn:
            st.session_state.videos = []
            videolist = videohelper.get_videos_for_search_term(search_term=search_term, video_count=video_count, sorting_criteria=sorting_criteria)
            
            for video in videolist:
                st.session_state.videos.append(video)
            
        video_urls = []
        video_titles = {}
        for video in st.session_state.videos:
            video_urls.append(video.video_url)
            video_titles.update(
                {
                video.video_url: video.video_title
                }
            )

        selected_video = st.selectbox(
            label="Pick to Video to Chat with it:",
            options=video_urls, # item options to be selected
            format_func=lambda url: video_titles[url], # formating selected item appearance in selectbox
            key="search_selectbox"
        )
            
        if selected_video:
            st.caption("Selected Video")
            st.video(data=selected_video)
            st.divider()
            search_prompt = st.text_input(label="Ask To Video:", key="search_prompt")
            search_ask_btn = st.button(label="ASK", key="search_ask_button")

            if search_ask_btn:
                st.divider()
                if st.session_state.current_video_url != selected_video:
                    with st.spinner("Step-1: Video text is preparing..."):
                        video_transcript_docs = videohelper.get_video_transcript(url=selected_video)
                        st.session_state.current_transcript_docs = video_transcript_docs

                    st.success("Video transcript saved on cache!")
                    st.divider()
                    st.session_state.current_video_url = selected_video
            

                with st.spinner("Step-2: Answering..."):
                    AI_Response, relevant_documents = raghelper.rag_with_video_transcript(transcript_docs=st.session_state.current_transcript_docs, prompt=search_prompt)
                st.info("Answer:")
                st.markdown(AI_Response)
                st.divider()

                for doc in relevant_documents:
                    st.warning("Reference:")
                    st.caption(doc.page_content)
                    st.markdown(f"Source: {doc.metadata}")
                    st.divider()
    # -----------------------------------
    with col_center:
        st.empty()
    # -----------------------------------
    with col_right:
        st.subheader("Related Videos")
        st.divider()

        for i, video in enumerate(st.session_state.videos):
            st.info(f"Video #: {i+1}")
            st.video(data=video.video_url)
            st.caption(f"Video Title: {video.video_title}")
            st.caption(f"Channel: {video.channel_name}")
            st.caption(f"Video Duration: {video.duration}")
            st.divider()  