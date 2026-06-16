---
title: Lane & Pothole Detection
emoji: 🚗
colorFrom: blue
colorTo: green
sdk: docker
app_file: src/app.py
pinned: false
---

# 🚗 Lane & Pothole Detection Web Application

A real-time computer vision application for detecting potholes and lane markings using YOLOv8n and OpenCV. Optimized for mobile browsers with WebRTC streaming and deployed on Hugging Face Spaces.

## 🎯 Features

- **Real-Time Pothole Detection**: YOLOv8n nano model optimized for edge inference
- **Lane Tracking**: Lightweight Canny edge + Hough line detection pipeline
- **Mobile-First UI**: Responsive Streamlit interface designed for iOS/Android
- **WebRTC Streaming**: Zero-latency bidirectional video from mobile device cameras
- **Network Resilient**: STUN/TURN servers configured for mobile carrier firewall bypass
- **Synchronous Processing**: No Redis/Celery dependencies—pure Python
- **Containerized**: Single-stage Docker build for Hugging Face Spaces deployment

## 🏗️ Project Architecture

```
LanePotholeDetection/
├── .github/workflows/
│   └── deploy.yml              # CI/CD pipeline for Hugging Face Spaces
├── src/
│   ├── app.py                  # Main Streamlit UI + WebRTC setup
│   └── detection.py            # YOLOv8n + lane detection engine
├── Dockerfile                  # Production container build
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit + streamlit-webrtc |
| **CV Engine** | Python OpenCV + Ultralytics YOLOv8n |
| **Video Codec** | PyAV (libav) |
| **Deployment** | Docker + Hugging Face Spaces |
| **ML Model** | YOLOv8n (pretrained COCO) |

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/LanePotholeDetection.git
   cd LanePotholeDetection
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run src/app.py
   ```

   The app will open at `http://localhost:8501`

5. **Access from mobile device**
   - Find your machine's local IP (e.g., `192.168.1.100`)
   - On mobile browser, navigate to `http://<YOUR_IP>:8501`
   - Grant camera permission when prompted

### Docker Build & Run

```bash
# Build the image
docker build -t lane-pothole-detection .

# Run the container
docker run -p 7860:7860 lane-pothole-detection
```

Access at `http://localhost:7860`

## 📋 Environment Variables

For local development, optional variables:

- `STREAMLIT_SERVER_PORT` (default: 7860)
- `STREAMLIT_SERVER_ADDRESS` (default: 0.0.0.0)
- `STREAMLIT_SERVER_HEADLESS` (default: true)

## 🎮 Usage

1. **Allow Camera Access**: Grant permission to your device's camera
2. **Choose Detection Mode**:
   - Toggle "Detect Potholes" for YOLOv8n inference
   - Toggle "Detect Lanes" for lane line tracking
3. **Position Device**: Aim at road ahead for optimal detection
4. **Monitor Alerts**: Real-time statistics and pothole warnings displayed below video

## 📊 Model Specifications

### Pothole Detection (YOLOv8n)

- **Model**: YOLOv8 Nano (pretrained on COCO)
- **Inference Size**: 320px (configurable to 640px)
- **Confidence Threshold**: 0.5 (adjustable)
- **Expected FPS**: ~10-15 FPS on CPU (varies by device)

### Lane Detection

- **Method**: Canny edge detection + Hough line transform
- **Region**: Lower 50% of frame (road area)
- **Edge Thresholds**: 50-150
- **Hough Parameters**: minLineLength=30, maxLineGap=10

## 🌐 Deployment to Hugging Face Spaces

### Prerequisites

1. Create a Hugging Face account: https://huggingface.co
2. Create a new Space:
   - Name: `lane-pothole-detection`
   - Space type: `Docker`
3. Get your HF token: https://huggingface.co/settings/tokens

### Setup GitHub Actions

1. Add secrets to your GitHub repository:
   - `HF_TOKEN`: Your Hugging Face API token
   - `HF_SPACE_REPO`: Format `username/lane-pothole-detection`

2. Push to `main` branch—GitHub Actions will auto-deploy:
   ```bash
   git push origin main
   ```

3. Monitor deployment in GitHub Actions tab

4. Access your Space at: `https://huggingface.co/spaces/username/lane-pothole-detection`

## 📱 Mobile Browser Compatibility

| Browser | iOS | Android |
|---------|-----|---------|
| Safari | ✅ | N/A |
| Chrome | ✅ | ✅ |
| Firefox | ✅ | ✅ |
| Edge | ✅ | ✅ |

**Requirements**: HTTPS connection (Hugging Face provides this automatically)

## 🔧 Configuration & Tuning

### Adjust Model Inference Size

In `src/detection.py`, modify `DetectionEngine` initialization:

```python
# For faster inference (lower accuracy)
engine = DetectionEngine(model_size=320)

# For better accuracy (slower inference)
engine = DetectionEngine(model_size=640)
```

### Adjust Confidence Threshold

```python
engine = DetectionEngine(conf_threshold=0.6)  # Higher = fewer false positives
```

### Adjust Lane Detection Sensitivity

In `src/detection.py`, modify `detect_lanes()`:

```python
edges = cv2.Canny(blurred, 50, 150)      # Edge thresholds
threshold=50,           # Hough votes required
minLineLength=30,       # Minimum line length
maxLineGap=10           # Maximum gap in line
```

## ⚡ Performance Optimization

- **Model Size 320px**: Fastest, lower accuracy (~15 FPS)
- **Model Size 640px**: Better accuracy, slower (~8 FPS)
- **Lane Detection Only**: 25-30 FPS
- **Potholes Only**: 10-15 FPS
- **Both Enabled**: 5-8 FPS

Toggle detection modes in the UI to balance accuracy vs responsiveness.

## 🐛 Troubleshooting

### Camera Not Connecting

- Check HTTPS is being used (required for WebRTC)
- Verify STUN servers are accessible (may be blocked by carrier)
- Test on WiFi instead of mobile data initially

### Low FPS

- Reduce inference resolution (320px instead of 640px)
- Disable one detection type
- Reduce frame resolution in constraints

### Model Not Downloading

- First run downloads YOLOv8n (~36MB)
- Ensure internet connection available
- Check disk space (minimum 500MB free)

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io)
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc)
- [Ultralytics YOLOv8](https://docs.ultralytics.com)
- [OpenCV Lane Detection](https://docs.opencv.org/master/da/d22/tutorial_py_canny.html)
- [Hugging Face Spaces](https://huggingface.co/spaces)

## 📄 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Open a GitHub issue
- Check existing documentation
- Review troubleshooting section

---

**Built with ❤️ for road safety using Computer Vision**
