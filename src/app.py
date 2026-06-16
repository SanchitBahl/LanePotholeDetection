"""
Main Streamlit web application with real-time WebRTC video streaming.
Mobile-first UI for lane and pothole detection.
"""

import streamlit as st
from streamlit_webrtc import WebRtcMode, RTCConfiguration, webrtc_streamer
import av
from detection import DetectionEngine


# Page configuration
st.set_page_config(
    page_title="Lane & Pothole Detection",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-first responsive design
st.markdown("""
    <style>
    [data-testid="stMainBlockContainer"] {
        padding: 0rem 0.5rem;
    }
    .main {
        max-width: 100%;
    }
    /* Mobile optimized video container */
    .stApp > header {
        background-color: transparent;
    }
    h1 {
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 1.8rem;
    }
    .stMetric {
        text-align: center;
    }
    /* Alert styling */
    .alert-danger {
        background-color: #ffcccc;
        border: 2px solid #ff0000;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
        color: #cc0000;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "detection_engine" not in st.session_state:
    st.session_state.detection_engine = DetectionEngine(model_size=320)
    st.session_state.detect_potholes = True
    st.session_state.detect_lanes = True
    st.session_state.webrtc_key = 0

# Header
st.markdown("# 🚗 Lane & Pothole Detection")
st.markdown("**Real-time detection optimized for mobile devices**")

# Control Panel
st.subheader("⚙️ Detection Settings")
col1, col2 = st.columns(2)

with col1:
    detect_potholes = st.toggle(
        "🕳️ Detect Potholes",
        value=st.session_state.detect_potholes,
        help="Enable YOLOv8n pothole detection (higher CPU)"
    )
    st.session_state.detect_potholes = detect_potholes

with col2:
    detect_lanes = st.toggle(
        "🛣️ Detect Lanes",
        value=st.session_state.detect_lanes,
        help="Enable lane tracking (lower CPU)"
    )
    st.session_state.detect_lanes = detect_lanes

# WebRTC Configuration with STUN/TURN servers for mobile network stability
rtc_configuration = RTCConfiguration(
    {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["stun:stun1.l.google.com:19302"]},
            {"urls": ["stun:stun2.l.google.com:19302"]},
        ]
    }
)

# WebRTC Streamer - Mobile optimized
st.subheader("📹 Live Video Stream")
st.info(
    "Allow camera access when prompted. Ensure good lighting for accurate detection."
)

webrtc_streamer(
    key=str(st.session_state.webrtc_key),
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={
        "video": {
            "mandatory": {
                "minWidth": 320,
                "minHeight": 240,
                "maxWidth": 640,
                "maxHeight": 480
            },
            "optional": [
                {"facingMode": "environment"},  # Default to rear camera
            ]
        },
        "audio": False,
    },
    video_frame_callback=st.session_state.detection_engine.create_video_frame_callback(
        detect_potholes=detect_potholes,
        detect_lanes=detect_lanes
    ),
    async_processing=False,
)

# Statistics and Alerts
st.subheader("📊 Detection Statistics")

col1, col2 = st.columns(2)

with col1:
    stats = st.session_state.detection_engine.get_stats()
    st.metric(
        "🕳️ Potholes Detected",
        stats['last_potholes'],
        delta=None if stats['last_potholes'] == 0 else f"+{stats['last_potholes']}"
    )

with col2:
    st.metric(
        "🛣️ Lane Lines",
        stats['last_lanes'],
        delta=None if stats['last_lanes'] == 0 else f"+{stats['last_lanes']}"
    )

# Alert for detected potholes
if detect_potholes and stats['last_potholes'] > 0:
    st.markdown(
        f'<div class="alert-danger">⚠️ WARNING: {stats["last_potholes"]} POTHOLE(S) DETECTED!</div>',
        unsafe_allow_html=True
    )

# Instructions
st.divider()
st.subheader("📱 Mobile Instructions")
st.markdown("""
1. **Allow Camera Access** - Grant permission to your device camera
2. **Choose Detection Mode** - Enable/disable lanes and potholes as needed
3. **Position Device** - Aim camera at the road ahead
4. **Monitor Alerts** - Watch for pothole warnings below the video

**Tips for Best Results:**
- Good natural lighting improves detection accuracy
- Keep camera steady and level
- Move slowly for continuous monitoring
- Rear camera is recommended for road scanning
""")

st.divider()
st.markdown("**Built with Streamlit + YOLOv8n + OpenCV** | Optimized for Hugging Face Spaces")
