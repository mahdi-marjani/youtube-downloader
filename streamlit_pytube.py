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
    video_format = st.radio("Video Format:", st.session_state[0])

    if st.button("download"):
        with st.spinner(text="downloading"):
            buffer = BytesIO()
            video_format.stream_to_buffer(buffer=buffer)

            # Get the raw bytes from the buffer
            video_bytes = buffer.getvalue()
        
        # Create a download button with raw bytes data
        download_button = st.download_button(
            label="Click here to download",
            data=video_bytes,
            key=f"{video_format.title}.mp4",
            file_name=f"{video_format.title}.mp4",
        )

        st.success("Successfully Downloaded")
