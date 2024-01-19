import streamlit as st
from pytube import YouTube
from io import BytesIO
import base64
from moviepy.editor import VideoFileClip, AudioFileClip

st.title("YouTube Downloader")

video_url = st.text_input("Video URL:")

if st.button("get info"):
    if video_url:
        try:
            with st.spinner(text="getting info"):
                yt = YouTube(video_url)
                # Get both video and audio streams
                video_formats = yt.streams.filter(file_extension="mp4", progressive=True)
                audio_formats = yt.streams.get_audio_only()

                st.session_state[0] = {"video": video_formats, "audio": audio_formats}

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL")

if st.session_state != {}:
    video_format = st.radio("Video Format:", st.session_state[0]["video"])

    if st.button("download"):
        with st.spinner(text="downloading"):
            # Download video and audio separately
            video_buffer = BytesIO()
            audio_buffer = BytesIO()

            video_format.stream_to_buffer(buffer=video_buffer)
            st.session_state[0]["audio"].stream_to_buffer(buffer=audio_buffer)

            # Reset buffers to start position
            video_buffer.seek(0)
            audio_buffer.seek(0)

            # Combine video and audio using moviepy
            video_clip = VideoFileClip(video_buffer)
            audio_clip = AudioFileClip(audio_buffer)

            # Set audio of video clip with audio clip
            video_clip = video_clip.set_audio(audio_clip)

            # Write the final result to BytesIO buffer
            final_buffer = BytesIO()
            video_clip.write_videofile(final_buffer, codec="libx264", audio_codec="aac")

            # Get the raw bytes from the buffer
            video_bytes = final_buffer.getvalue()

        # Create a download button with raw bytes data
        download_button = st.download_button(
            label="Click here to download",
            data=video_bytes,
            key=f"{video_format.title}.mp4",
            file_name=f"{video_format.title}.mp4",
        )

        st.success("Successfully Downloaded")
