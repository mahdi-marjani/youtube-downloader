import streamlit as st
from pytube import YouTube
from io import BytesIO
import base64

st.title("YouTube Downloader")

video_url = st.text_input("Video URL:")

if st.button("get info"):
    if video_url:
        try:
            with st.spinner(text="getting info"):
                yt = YouTube(video_url)

                video_formats = yt.streams.filter(file_extension="mp4")
                st.session_state[0] = video_formats

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")

if st.session_state != {}:
    selected_video_format_index = st.radio("Video Format:", range(len(st.session_state[0])))
    video_format = st.session_state[0][selected_video_format_index]

    if st.button("download"):
        with st.spinner(text="downloading"):
            buffer = BytesIO()
            video_format.stream_to_buffer(buffer=buffer)

            # Convert the video data to base64
            video_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        with st.spinner(text="displaying video"):
            # Display the video using HTML5 video tag
            st.markdown(f'<video controls width="640" height="360" src="data:video/mp4;base64,{video_base64}" type="video/mp4"></video>', unsafe_allow_html=True)

        st.success("Successfully Downloaded")
