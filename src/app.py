"""
Main Streamlit web application with real-time WebRTC video streaming.
Mobile-first UI for lane and pothole detection.
"""

import streamlit as st
from streamlit_webrtc import WebRtcMode, RTCConfiguration, webrtc_streamer
from detection import DetectionEngine

# Page configuration
st.set_page_config(
    page_title="Lane & Pothole Detection",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    body { margin: 0; padding: 0; }
    .stApp { max-width: 100%; }
    h1 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🚗 Lane & Pothole Detection")
st.markdown("**Real-time road monitoring with live video feed**")

# Control Panel
st.subheader("⚙️ Detection Settings")
col1, col2 = st.columns(2)

with col1:
    detect_potholes = st.toggle(
        "🕳️ Detect Potholes",
        value=True,
        help="Enable pothole detection"
    )

with col2:
    detect_lanes = st.toggle(
        "🛣️ Detect Lanes",
        value=True,
        help="Enable lane detection"
    )

# WebRTC Configuration
rtc_configuration = RTCConfiguration(
    {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["stun:stun1.l.google.com:19302"]},
        ]
    }
)

# Initialize detection engine
if "detection_engine" not in st.session_state:
    st.session_state.detection_engine = DetectionEngine(model_size=320)

# WebRTC Streamer
st.subheader("📹 Live Video Stream")
st.info("Allow camera access when prompted. Grant permission to see the live feed.")

webrtc_streamer(
    key="lane-pothole-detection",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 640},
            "height": {"ideal": 480}
        },
        "audio": False,
    },
    video_frame_callback=st.session_state.detection_engine.create_video_frame_callback(
        detect_potholes=detect_potholes,
        detect_lanes=detect_lanes
    ),
    async_processing=True,
)

# Instructions
st.divider()
st.subheader("📱 How It Works")
st.markdown("""
- **Potholes**: Detected in real-time and marked with 🔴 **red bounding boxes**
- **Lanes**: Detected in real-time and marked with 🟢 **green lines**
- **Mobile**: Works on any device with a camera (iOS/Android)
- **Privacy**: All processing happens on our server, video not stored

**Tips:**
- Grant camera permission when prompted
- Use good lighting
- Point camera at the road
- Keep device steady for best results
""")

st.divider()
st.markdown("*Built with Streamlit + YOLOv8n + OpenCV | Deployed on Hugging Face Spaces*")
