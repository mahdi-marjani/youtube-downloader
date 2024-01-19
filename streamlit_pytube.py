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
                video_formats = yt.streams.filter(file_extension="mp4", progressive=True)
                audio_formats = yt.streams.filter(only_audio=True)

                st.session_state['video_formats'] = video_formats
                st.session_state['audio_formats'] = audio_formats

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")

if 'video_formats' in st.session_state and 'audio_formats' in st.session_state:
    video_format = st.radio("Select Video Format:", st.session_state['video_formats'])
    audio_format = st.radio("Select Audio Format:", st.session_state['audio_formats'])

    if st.button("download"):
        with st.spinner(text="downloading"):
            video_buffer = BytesIO()
            video_format.stream_to_buffer(buffer=video_buffer)
            video_bytes = video_buffer.getvalue()

            audio_buffer = BytesIO()
            audio_format.stream_to_buffer(buffer=audio_buffer)
            audio_bytes = audio_buffer.getvalue()

        # Create a download button for video
        video_download_button = st.download_button(
            label="Download Video",
            data=video_bytes,
            key=f"{video_format.title}.mp4",
            file_name=f"{video_format.title}.mp4",
        )

        # Create a download button for audio
        audio_download_button = st.download_button(
            label="Download Audio",
            data=audio_bytes,
            key=f"{audio_format.title}.mp3",
            file_name=f"{audio_format.title}.mp3",
        )

        st.success("Successfully Downloaded")
