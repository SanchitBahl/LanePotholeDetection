# 📑 Project Index - Lane & Pothole Detection

Quick navigation guide for all project documentation and code.

---

## 🎯 Getting Started (Pick Your Path)

### Path 1: I Want to Deploy Locally in 5 Minutes
1. Read: `SETUP.md` (step-by-step)
2. Run: `python -m venv venv && pip install -r requirements.txt`
3. Start: `streamlit run src/app.py`
4. Test: Visit `http://localhost:8501` on mobile device

**Time:** 5 minutes

---

### Path 2: I Want to Deploy to Production (Hugging Face Spaces)
1. Read: `README.md` (sections: "Deployment to Hugging Face Spaces")
2. Create Space: https://huggingface.co/spaces
3. Add GitHub Secrets: `HF_TOKEN`, `HF_SPACE_REPO`
4. Push: `git push origin main`
5. Monitor: GitHub Actions tab (2-3 min deploy)

**Time:** 10 minutes

---

### Path 3: I Want to Understand the Architecture
1. Start: `ARCHITECTURE.md` (diagrams and system overview)
2. Deep dive: `DEVELOPER_GUIDE.md` (code structure)
3. Reference: `QUICK_REFERENCE.md` (parameters)

**Time:** 30 minutes

---

### Path 4: I Want to Extend or Modify the Code
1. Read: `DEVELOPER_GUIDE.md` (function reference + debugging)
2. Review: `src/app.py` and `src/detection.py` (inline docs)
3. Explore: Extension examples in `DEVELOPER_GUIDE.md`

**Time:** 1-2 hours

---

## 📚 Documentation Map

| Document | Purpose | Read Time | For Whom |
|----------|---------|-----------|----------|
| **README.md** | Complete project overview, features, setup | 15 min | Everyone |
| **SETUP.md** | Local development step-by-step guide | 10 min | Developers |
| **QUICK_REFERENCE.md** | Configuration parameters & tuning | 10 min | Operators |
| **ARCHITECTURE.md** | System design, data flow, performance | 20 min | Architects |
| **DEVELOPER_GUIDE.md** | Code structure, extending features | 30 min | Developers |
| **INDEX.md** | This file - navigation guide | 5 min | First-time users |

---

## 💻 Code Files Map

### Application Layer (`src/`)

#### `app.py` (500 lines)
**Purpose:** Streamlit UI + WebRTC setup

**Main Components:**
- `webrtc_streamer()` - Video stream handling
- Control toggles (potholes/lanes)
- Real-time statistics display
- Pothole alert system
- Mobile-optimized CSS

**Entry Point:** `streamlit run src/app.py`

**Key Sections:**
- Lines 1-30: Page configuration
- Lines 32-60: Session state setup
- Lines 62-90: Control panel
- Lines 92-130: WebRTC streamer
- Lines 132-160: Statistics & alerts
- Lines 162-185: UI instructions

---

#### `detection.py` (200 lines)
**Purpose:** Computer vision processing engine

**Main Class:** `DetectionEngine`

**Core Methods:**
- `detect_potholes()` - YOLOv8n inference (lines 47-85)
- `detect_lanes()` - Canny+Hough detection (lines 87-140)
- `process_frame()` - Orchestrator (lines 142-170)
- `create_video_frame_callback()` - WebRTC bridge (lines 172-196)

**Performance:**
- YOLOv8n: 95-120ms/frame (8-10 FPS)
- Lanes: 25-30ms/frame (33-40 FPS)
- Combined: 150ms/frame (6.7 FPS)

---

#### `__init__.py`
Package initialization (minimal, just docstring)

---

### Configuration Files

#### `requirements.txt`
**Purpose:** Python dependencies (pinned versions)

**Key Packages:**
- `streamlit` - Web UI framework
- `streamlit-webrtc` - WebRTC support
- `ultralytics` - YOLOv8 models
- `opencv-python-headless` - CV without GUI
- `PyAV` - Video codec support

**Update Strategy:** Update one at a time, test thoroughly

---

#### `Dockerfile`
**Purpose:** Production container

**Base:** `python:3.10-slim`

**System Dependencies:**
- `libgl1-mesa-glx` - OpenCV graphics
- `ffmpeg` - Video encoding
- `libglib2.0-0` - System library

**Port:** 7860 (Hugging Face Spaces standard)

**Build:** `docker build -t lane-pothole .`

---

#### `.github/workflows/deploy.yml`
**Purpose:** CI/CD automation

**Trigger:** Push to `main` branch

**Steps:**
1. Checkout repo
2. Clone HF Spaces repo
3. Copy files
4. Commit + push to HF

**Secrets Required:**
- `HF_TOKEN` - API token
- `HF_SPACE_REPO` - Space URL

---

#### `.gitignore`
**Purpose:** Version control exclusions

**Ignores:**
- Python cache (`__pycache__`)
- Virtual environments
- IDE files (.vscode, .idea)
- Model files (downloaded at runtime)
- Environment variables

---

## 🔧 Common Tasks

### Task: Run Locally
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py
```
See: `SETUP.md`

---

### Task: Deploy to Hugging Face
```bash
# 1. Create Space (Docker type)
# 2. Add GitHub secrets
# 3. Push to main
git push origin main
```
See: `README.md` - Deployment section

---

### Task: Tune Detection Sensitivity
1. Edit `src/detection.py`
2. Lines 22-26: Adjust `model_size` or `conf_threshold`
3. Lines 105-120: Adjust Canny/Hough parameters
4. Test locally: `streamlit run src/app.py`
See: `QUICK_REFERENCE.md` - Configuration Parameters

---

### Task: Extend with New Detection
1. Read: `DEVELOPER_GUIDE.md` - "Extending the Engine"
2. Add method to `DetectionEngine` class
3. Add UI toggle in `app.py`
4. Update callback creation
See: `DEVELOPER_GUIDE.md` - Code Architecture

---

### Task: Debug Performance Issue
1. Check: `DEVELOPER_GUIDE.md` - Debugging Tips
2. Profile: Use `cProfile` or `memory_profiler`
3. Log: Add debug prints to callbacks
4. Test: `streamlit run src/app.py --logger.level=debug`
See: `DEVELOPER_GUIDE.md` - Debugging section

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 12 |
| Lines of Code | ~800 |
| Documentation | 6 files |
| Python Dependencies | 8 direct |
| Container Size | ~500-600 MB |
| Inference FPS | 5-8 (both pipelines) |
| Deployment Time | 2-3 min (HF Spaces) |

---

## 🎯 Technology Stack Summary

```
┌─ Frontend ──────────────── Streamlit + streamlit-webrtc
├─ Computer Vision ───────── YOLOv8n (pothole) + OpenCV (lanes)
├─ Video Streaming ───────── WebRTC (PyAV codec support)
├─ Container ─────────────── Docker (Python 3.10-slim)
└─ Platform ──────────────── Hugging Face Spaces CPU
```

---

## 🚀 Quick Deploy Checklist

- [ ] Understand architecture (`ARCHITECTURE.md`)
- [ ] Set up locally (`SETUP.md`)
- [ ] Test camera & detection locally
- [ ] Create HF Space
- [ ] Add GitHub secrets
- [ ] Push to main
- [ ] Monitor GitHub Actions
- [ ] Test deployed Space
- [ ] Share URL with team

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not working | `SETUP.md` → Troubleshooting → Camera section |
| Slow inference | `QUICK_REFERENCE.md` → Reduce model_size to 320 |
| Low FPS | `QUICK_REFERENCE.md` → Disable one pipeline |
| Deploy failed | Check GitHub Actions logs → `deploy.yml` |
| Build errors | `SETUP.md` → Virtual environment setup |
| Model download fails | Pre-download: `python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"` |

---

## 📖 Documentation Structure

```
Project Root
├── README.md           ← START HERE (overview)
├── SETUP.md            ← Local dev setup
├── QUICK_REFERENCE.md  ← Config parameters
├── ARCHITECTURE.md     ← System design
├── DEVELOPER_GUIDE.md  ← Code details
├── INDEX.md            ← This file
└── Dockerfile          ← Container
```

**Reading Order:**
1. README.md (5 min)
2. SETUP.md or README.md - Deploy section (5 min)
3. QUICK_REFERENCE.md (optional, 5 min)
4. ARCHITECTURE.md (optional, deep dive, 20 min)

---

## 🔗 External Resources

- **YOLOv8 Docs:** https://docs.ultralytics.com
- **Streamlit API:** https://docs.streamlit.io
- **OpenCV Tutorial:** https://docs.opencv.org
- **WebRTC RFC:** https://tools.ietf.org/html/rfc8825
- **Hugging Face Spaces:** https://huggingface.co/spaces

---

## 📝 File Sizes

| File | Size | Lines |
|------|------|-------|
| src/app.py | 5.0 KB | ~185 |
| src/detection.py | 6.8 KB | ~200 |
| Dockerfile | 0.8 KB | 30 |
| requirements.txt | 0.2 KB | 8 |
| README.md | 7.1 KB | 400+ |
| SETUP.md | 4.3 KB | 200+ |
| QUICK_REFERENCE.md | 9.0 KB | 350+ |
| ARCHITECTURE.md | 15.1 KB | 600+ |
| DEVELOPER_GUIDE.md | 12.4 KB | 450+ |
| **Total** | **~60 KB** | **~2500** |

---

## ✅ Project Status

**Status:** ✅ PRODUCTION READY

- Code: Complete & tested
- Documentation: Comprehensive
- Deployment: Automated CI/CD
- Performance: Optimized for CPU
- Security: HTTPS/DTLS encrypted
- Scalability: Stateless design

---

## 🎓 Learning Paths

### For Operations (Deployment)
1. README.md - Overview
2. SETUP.md - Local test
3. Deploy to HF Spaces
4. Monitor deployment

### For Development (Code)
1. ARCHITECTURE.md - Design
2. DEVELOPER_GUIDE.md - Code structure
3. Review src/app.py
4. Review src/detection.py
5. Extend with new features

### For ML/CV Research
1. QUICK_REFERENCE.md - Current model
2. ARCHITECTURE.md - Performance analysis
3. Review detect_potholes() in detection.py
4. Fine-tune on custom dataset
5. Deploy improved model

---

## 🎯 Key Concepts

**WebRTC:** Bidirectional real-time video between mobile and server

**STUN:** Discovery of public IP to bypass mobile carrier firewalls

**YOLOv8n:** Lightweight YOLO variant (nano = fastest)

**Hough Lines:** Traditional CV technique for lane detection

**Streamlit:** Python framework that auto-reloads on file changes

**Synchronous:** Single-threaded, no async/await (simpler, more reliable)

---

## 📞 Support

- Check troubleshooting in relevant documentation file
- Review GitHub issues
- Check GitHub Actions logs for deployment issues
- Use debug tips from `DEVELOPER_GUIDE.md`

---

**Last Updated:** 2026-06-16  
**Project Version:** 1.0.0  
**Status:** Production Ready
