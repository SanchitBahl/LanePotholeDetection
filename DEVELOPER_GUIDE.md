# 👨‍💻 Developer Guide - Lane & Pothole Detection

For developers who want to understand, extend, or debug the application.

## 🏗️ Code Architecture Overview

### Module Organization

```python
# src/app.py - Presentation Layer (500 lines)
├─ Streamlit configuration
├─ Session state management
├─ WebRTC setup & constraints
├─ UI components (toggles, metrics, alerts)
└─ Real-time stats display

# src/detection.py - Processing Layer (200 lines)
├─ DetectionEngine class (singleton)
├─ Pothole detection (YOLOv8n)
├─ Lane detection (Canny + Hough)
├─ Frame callback factory
└─ Statistics aggregation
```

---

## 📋 Function Reference

### `src/app.py`

#### `webrtc_streamer()` (Lines 98-130)
**Purpose:** Establish WebRTC connection and process video frames

```python
webrtc_streamer(
    key="rtc_stream",  # Unique per session
    mode=WebRtcMode.SENDRECV,  # Bidirectional
    rtc_configuration=rtc_configuration,  # STUN servers
    media_stream_constraints={...},  # Camera settings
    video_frame_callback=callback_func,  # Processing
    async_processing=False  # Synchronous (critical!)
)
```

**Flow:**
1. Browser sends WebRTC offer (camera stream)
2. Python server responds with answer
3. ICE candidates gathered via STUN
4. Each frame → video_frame_callback → processing → browser

---

### `src/detection.py`

#### `DetectionEngine.__init__(model_size=320, conf_threshold=0.5)` (Lines 17-31)
**Purpose:** Initialize CV engine and load YOLOv8n

```python
engine = DetectionEngine(model_size=320)
# model_size=320: Fast (~100ms per frame)
# model_size=640: Accurate (~140ms per frame)
```

**What happens:**
- YOLO model downloaded on first run (~36MB)
- Cached in `~/.cache/yolo/`
- Loaded into memory (~200MB)

---

#### `detect_potholes(frame)` (Lines 47-85)
**Purpose:** YOLOv8n inference + bounding box visualization

```python
annotated, detections = engine.detect_potholes(frame)

# detections = [
#   {box: (x1, y1, x2, y2), conf: 0.95, class_id: 0},
#   {box: (x2, y2, x3, y3), conf: 0.87, class_id: 0},
# ]
```

**Performance:** ~95-120ms per frame (10-12 FPS)

**Customization Points:**
```python
# Line 59: Change model
self.model = YOLO('yolov8s.pt')  # Small (faster accuracy)
self.model = YOLO('yolov8m.pt')  # Medium

# Line 64: Filter by class
if class_id == 0:  # Only car class (example)
    detections.append(...)

# Line 70: Adjust box drawing
cv2.rectangle(..., color=(0, 0, 255), thickness=3)  # thicker lines
```

---

#### `detect_lanes(frame)` (Lines 87-140)
**Purpose:** Traditional CV for lane detection (fast, interpretable)

```python
annotated, lanes = engine.detect_lanes(frame)

# lanes = [
#   ((x1, y1), (x2, y2)),  # Line segment
#   ((x1, y1), (x2, y2)),
# ]
```

**Performance:** ~25-30 FPS (fast enough for real-time)

**Customization Points:**
```python
# Line 105: Edge thresholds
edges = cv2.Canny(blurred, 100, 200)  # More conservative (fewer edges)

# Line 120: Hough line parameters
cv2.HoughLinesP(
    roi_edges,
    rho=1,
    theta=np.pi/180,
    threshold=30,        # Lower = more lines (more false positives)
    minLineLength=50,    # Longer = fewer short lines
    maxLineGap=5         # Tighter = fewer connected lines
)

# Line 127: Line color/thickness
cv2.line(annotated, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Blue, thicker
```

---

#### `process_frame(frame, detect_potholes, detect_lanes)` (Lines 142-170)
**Purpose:** Orchestrate both pipelines

```python
output, potholes, lanes, stats = engine.process_frame(
    frame,
    detect_potholes=True,
    detect_lanes=True
)

print(stats)  # {'potholes': 2, 'lanes': 5}
```

**Execution Flow:**
```
frame → detect_potholes() → output, potholes
  ↓
output → detect_lanes() → final_output, lanes
  ↓
Aggregate stats & return
```

---

#### `create_video_frame_callback(detect_potholes, detect_lanes)` (Lines 172-196)
**Purpose:** Create WebRTC callback closure

```python
callback = engine.create_video_frame_callback(
    detect_potholes=True,
    detect_lanes=False
)

# Later, streamlit-webrtc calls:
output_frame = callback(input_frame)  # av.VideoFrame
```

**Why closure?** Captures toggle state at creation time. If toggles change, new callback created.

---

## 🔧 Extending the Engine

### Add a New Detection Pipeline

```python
# src/detection.py

class DetectionEngine:
    # ... existing code ...
    
    def detect_speed_limits(self, frame: np.ndarray) -> tuple:
        """
        Example: Detect speed limit signs (custom YOLO model)
        """
        # Load custom model
        model = YOLO('speed_limit_model.pt')
        results = model.predict(source=frame, imgsz=320)
        
        signs = []
        output = frame.copy()
        
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            
            # Extract text from sign region (OCR)
            sign_region = frame[y1:y2, x1:x2]
            # ... OCR logic ...
            
            signs.append({'region': (x1, y1, x2, y2), 'speed': 50})
            cv2.rectangle(output, (x1, y1), (x2, y2), (255, 165, 0), 2)
        
        return output, signs
    
    def process_frame(self, frame, detect_potholes=True, detect_lanes=True):
        output = frame.copy()
        potholes = []
        lanes = []
        stats = {}
        
        if detect_potholes:
            output, potholes = self.detect_potholes(output)
            stats['potholes'] = len(potholes)
        
        if detect_lanes:
            output, lanes = self.detect_lanes(output)
            stats['lanes'] = len(lanes)
        
        # ADD NEW:
        if self.detect_speed_limits:
            output, signs = self.detect_speed_limits(output)
            stats['speed_limits'] = len(signs)
        
        return output, potholes, lanes, stats
```

### Add UI Toggle for New Feature

```python
# src/app.py

# In control panel section (around line 62-80):

col1, col2, col3 = st.columns(3)

with col1:
    detect_potholes = st.toggle("🕳️ Potholes", ...)

with col2:
    detect_lanes = st.toggle("🛣️ Lanes", ...)

with col3:
    detect_speed = st.toggle("🚦 Speed Limits", ...)  # NEW

st.session_state.detect_potholes = detect_potholes
st.session_state.detect_lanes = detect_lanes
st.session_state.detect_speed = detect_speed  # NEW

# In callback creation (around line 118):
video_frame_callback=engine.create_video_frame_callback(
    detect_potholes=detect_potholes,
    detect_lanes=detect_lanes,
    detect_speed=detect_speed  # NEW
)
```

---

## 🐛 Debugging Tips

### Log Detection Stats

```python
# In src/detection.py, line 58 (in detect_potholes):
print(f"[DEBUG] Detected {len(detections)} potholes in {frame.shape}")

# Or return detailed stats:
stats = {
    'potholes_count': len(detections),
    'avg_confidence': sum(d['conf'] for d in detections) / len(detections) if detections else 0,
    'frame_size': frame.shape,
    'inference_time': 0.105  # seconds
}
```

### Profile Performance

```python
import time
import cv2
from src.detection import DetectionEngine

engine = DetectionEngine(model_size=320)
frame = cv2.imread('test_image.jpg')

start = time.time()
output, potholes, lanes, stats = engine.process_frame(frame)
elapsed = time.time() - start

print(f"Frame processing: {elapsed*1000:.1f}ms ({1/elapsed:.1f} FPS)")
print(f"Detections: {stats}")
```

### Save Debug Frames

```python
# In video callback (src/app.py):
import os
os.makedirs('debug_frames', exist_ok=True)

def callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")
    processed, _, _, _ = engine.process_frame(image)
    
    # Save every 10th frame
    if time.time() % 10 < 0.03:
        cv2.imwrite(f"debug_frames/{time.time()}.jpg", processed)
    
    return av.VideoFrame.from_ndarray(processed, format="bgr24")
```

### Test Camera Locally

```python
import cv2

cap = cv2.VideoCapture(0)  # Rear camera (device-dependent)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process with engine
    from src.detection import DetectionEngine
    engine = DetectionEngine()
    output, _, _, _ = engine.process_frame(frame)
    
    cv2.imshow('Detection', output)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 📊 Performance Profiling

### CPU Usage by Component

```python
import cProfile
import pstats
from io import StringIO

pr = cProfile.Profile()
pr.enable()

# Run frame processing
for i in range(100):
    engine.process_frame(frame)

pr.disable()
s = StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(10)
print(s.getvalue())

# Output shows:
# - detect_potholes: ~40% of time
# - detect_lanes: ~30% of time
# - Overhead: ~30% of time
```

### Memory Profiling

```python
from memory_profiler import profile

@profile
def process_frame_memory(engine, frame):
    return engine.process_frame(frame)

# Run with: python -m memory_profiler detect.py
# Shows line-by-line memory usage
```

---

## 🔌 Integrating Custom Models

### Use a Fine-Tuned Pothole Model

```python
# Train on custom dataset (e.g., using Roboflow)
# Export as yolov8n-pothole.pt

# src/detection.py, line 24:
self.model = YOLO('models/yolov8n-pothole.pt')  # Custom weights

# The rest of detect_potholes() stays the same!
```

### Switch to Different Model Architecture

```python
# YOLOv5 instead of YOLOv8
from yolov5 import YOLOv5

# src/detection.py
model = YOLOv5('yolov5n')  # Tiny model, very fast
results = model.predict(frame)

# Or TFLite (mobile inference)
interpreter = tf.lite.Interpreter('model.tflite')
interpreter.allocate_tensors()
# ... TFLite inference pipeline ...
```

---

## 🌐 WebRTC Troubleshooting

### Check ICE Connectivity

```python
# In browser console (F12):
console.log(peerConnection.iceConnectionState);
// Should be: "connected" or "completed"

// If "failed": STUN servers blocked by network
// Solutions:
// - Test on WiFi instead of mobile data
// - Add backup STUN servers in deploy.yml
// - Use TURN relay server (requires auth)
```

### Test STUN Servers

```bash
# Test Google STUN from command line:
stunclient stun.l.google.com 19302

# If timeout: STUN blocked by firewall
# Solution: Configure enterprise proxy or use TURN
```

---

## 📦 Dependency Management

### Lock Versions (requirements.txt)

✅ **Current:** Specific versions pinned (reproducible)
```
streamlit==1.40.1
ultralytics==8.3.20
```

❌ **Avoid:** Floating versions (unpredictable)
```
streamlit>=1.0  # Could break on minor update
ultralytics~=8.0  # Same issue
```

### Update Dependencies Safely

```bash
# Check for updates
pip list --outdated

# Update one package at a time, test thoroughly
pip install ultralytics==8.3.21 --upgrade
streamlit run src/app.py

# If works, update requirements.txt
# If breaks, revert: pip install ultralytics==8.3.20
```

---

## 🚢 Release Checklist

Before deploying to production:

- [ ] Test locally with real mobile device
- [ ] Test on WiFi and mobile data (cellular)
- [ ] Verify camera permissions flow
- [ ] Check pothole detection accuracy on 5+ test images
- [ ] Verify lane detection on road footage
- [ ] Monitor CPU/memory during 10-min session
- [ ] Test on different mobile browsers (iOS/Android)
- [ ] Review logs for errors (Hugging Face UI)
- [ ] Verify Dockerfile builds without errors
- [ ] Test Docker image locally
- [ ] Update README with any changes
- [ ] Tag commit with version (e.g., v1.0.0)

---

## 📚 Further Reading

- **YOLOv8 Docs:** https://docs.ultralytics.com/tasks/detect/
- **OpenCV Tutorial:** https://docs.opencv.org/master/d3/d63/classcv_1_1Mat.html
- **Streamlit Docs:** https://docs.streamlit.io/library/api-reference
- **WebRTC RFC:** https://tools.ietf.org/html/rfc8825
- **PyAV Docs:** https://pyav.org/

---

**Last Updated:** 2026-06-16  
**Maintainer:** Development Team  
**Status:** Production Ready
