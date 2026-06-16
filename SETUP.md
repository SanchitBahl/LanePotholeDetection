# Lane & Pothole Detection - Local Development Setup

## Quick Start Guide

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/LanePotholeDetection.git
cd LanePotholeDetection
```

#### 2. Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First install will download the YOLOv8n model (~36MB). Ensure you have stable internet.

#### 4. Run Locally
```bash
streamlit run src/app.py
```

The app will open at `http://localhost:8501`

#### 5. Access from Mobile Device
1. Get your machine's local IP address:
   - **macOS/Linux:** `ifconfig | grep inet`
   - **Windows:** `ipconfig` (look for IPv4 Address)

2. On mobile browser, navigate to: `http://<YOUR_LOCAL_IP>:8501`

3. Grant camera permission when prompted

### Alternative: Docker Local Testing

```bash
# Build image
docker build -t lane-pothole-detection .

# Run container
docker run -p 7860:7860 lane-pothole-detection

# Access at http://localhost:7860
```

### Troubleshooting Local Setup

#### Issue: Camera Permission Denied
- **Chrome/Firefox:** Check browser permissions in settings
- **iOS Safari:** Settings > Privacy > Camera (allow for websites)
- **Android:** App permissions in system settings

#### Issue: "ModuleNotFoundError" 
```bash
# Ensure venv is activated, then:
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue: Slow Inference
- Reduce inference resolution: `DetectionEngine(model_size=320)`
- Disable one detection type (lanes or potholes)
- Check system CPU usage

#### Issue: Model Download Fails
```bash
# Pre-download model manually
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Development Workflow

1. **Edit Code:** Modify files in `src/`
2. **Reload UI:** Streamlit auto-reloads on file changes
3. **Test Changes:** Use browser dev tools (F12) to inspect
4. **Commit:** `git add . && git commit -m "message"`
5. **Push:** `git push origin main` (triggers auto-deployment)

### Performance Profiling

Monitor detection performance:
```python
import time
from src.detection import DetectionEngine

engine = DetectionEngine()
start = time.time()
output, potholes, lanes, stats = engine.process_frame(frame)
print(f"Frame processing time: {time.time() - start:.3f}s")
```

### Debugging Tips

**Enable verbose YOLOv8 output:**
```python
# In src/detection.py, change verbose=False to verbose=True
results = self.model.predict(source=frame, verbose=True)
```

**Log detection stats:**
```python
# Add to src/app.py
st.write("Debug Stats:", stats)
```

**Inspect frame data:**
```python
import cv2
# Save frame to disk for analysis
cv2.imwrite(f"debug_frame_{time.time()}.jpg", frame)
```

### System Requirements

| Component | Requirement |
|-----------|------------|
| **RAM** | 2GB+ (4GB recommended) |
| **Disk** | 500MB free (for models) |
| **CPU** | Multi-core (2+ cores) |
| **Network** | Stable WiFi or cellular |

### File Descriptions

| File | Purpose |
|------|---------|
| `src/app.py` | Streamlit UI + WebRTC configuration |
| `src/detection.py` | YOLOv8n + lane detection engine |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Production container definition |
| `.github/workflows/deploy.yml` | CI/CD automation |
| `README.md` | Project documentation |
| `.gitignore` | Version control ignore rules |

### Environment Variables

Optional configuration:
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

### Next Steps

1. **Customize Detection:** Adjust thresholds in `src/detection.py`
2. **Deploy to Hugging Face:** See README.md for instructions
3. **Add Features:** Extend `DetectionEngine` class with new methods
4. **Optimize Performance:** Profile and benchmark your changes

---

For issues, refer to README.md or open a GitHub issue.
