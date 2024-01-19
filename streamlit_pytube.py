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
                file_formats = yt.streams.filter(file_extension="mp4")
                st.session_state[0] = file_formats

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")

if st.session_state != {}:
    file_format = st.radio("File Format:", st.session_state[0])

    # Determine file extension based on the type of stream
    if "audio" in file_format.type:
        file_endwith = ".mp3"
    else:
        file_endwith = ".mp4"

    if st.button("download"):
        with st.spinner(text="downloading"):
            buffer = BytesIO()
            file_format.stream_to_buffer(buffer=buffer)

            # Get the raw bytes from the buffer
            video_bytes = buffer.getvalue()

        # Create a download button with raw bytes data
        download_button = st.download_button(
            label="Click here to download",
            data=video_bytes,
            key=f"{file_format.title}{file_endwith}",
            file_name=f"{file_format.title}{file_endwith}",
        )

        st.success("Successfully Downloaded")
