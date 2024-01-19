import streamlit as st
from pytube import YouTube
from io import BytesIO

st.title("YouTube Downloader")

video_url = st.text_input("Video URL:")

if st.button("Get Info"):
    if video_url:
        try:
            with st.spinner(text="Getting Info"):
                yt = YouTube(video_url)
                formats = yt.streams.filter(file_extension="mp4", progressive=True) + yt.streams.filter(only_audio=True)

                st.session_state['formats'] = formats

            st.success("Info Retrieved Successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")

if 'formats' in st.session_state:
    selected_format = st.radio("Select Format:", st.session_state['formats'])

    if st.button("Download"):
        with st.spinner(text="Downloading"):
            buffer = BytesIO()
            selected_format.stream_to_buffer(buffer=buffer)
            file_bytes = buffer.getvalue()

        # Create a download button for the selected format
        st.download_button(
            label="Click here to download",
            data=file_bytes,
            key=f"{selected_format.title}.{selected_format.extension}",
            file_name=f"{selected_format.title}.{selected_format.extension}",
        )

        st.success("Successfully Downloaded")
