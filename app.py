import streamlit as st

# 로컬에 있는 MP4 파일 경로
video_file = open('playing_service.MP4', 'rb')
video_bytes = video_file.read()

# Streamlit에서 비디오를 표시
st.video(video_bytes)
