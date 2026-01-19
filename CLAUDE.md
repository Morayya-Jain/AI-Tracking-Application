# Gavin AI - Agent Quick Reference

**TL;DR**: Python focus tracker using OpenAI Vision API (1 FPS) to detect present/away/gadget distractions. Generates PDF reports. AI-only detection, no hardcoded methods.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point, camera loop |
| `config.py` | **ALL constants** (models, FPS, thresholds, usage limits) |
| `instance_lock.py` | **Single-instance enforcement** (cross-platform file lock) |
| `camera/vision_detector.py` | Main detection logic (`analyze_frame()`) |
| `tracking/analytics.py` | **Stats computation - MATH MUST ADD UP** |
| `tracking/session.py` | Event logging, state changes |
| `tracking/usage_limiter.py` | **MVP usage time tracking & limits** |
| `reporting/pdf_report.py` | PDF generation (~/Downloads/) |

*Ignore: `detection.py`, `phone_detector.py` (legacy)*

---

## ⚠️ Critical Rules

**#1 - Math Must Add Up**  
`present + away + gadget = total` in `analytics.py`. This broke twice. Always verify.

**#2 - AI-Only Detection**  
NO hardcoded detection. OpenAI Vision API only. Cost: ~$0.06-0.12/min (intentional).

**#3 - Time Format**  
Use `_format_time()` → "1m 30s" not "1.5 minutes"

**#4 - PDF Output**  
Single combined PDF: Page 1 = Summary Statistics table. Page 2+ = All session logs.

---

## 📊 Event Types

- `present`: At desk, focused
- `away`: Not visible
- `gadget_suspected`: Actively using gadget (phone, tablet, controller, TV, etc.)
  - ⚠️ Smartwatches are NOT detected (used for time/notifications, not distractions)

---

## 🔧 Key Constants (config.py)

```python
DETECTION_FPS = 1                       # Don't increase (cost doubles)
GADGET_CONFIDENCE_THRESHOLD = 0.5
GADGET_DETECTION_DURATION_SECONDS = 2
OPENAI_VISION_MODEL = "gpt-4o-mini"    # Detection
UNFOCUSED_ALERT_TIMES = [20, 60, 120]   # Alerts at 20s, 60s, 120s unfocused
```

---

## 🔔 Unfocused Alert System

When user is unfocused (away or on gadget), audio alerts play:
- **1st alert**: After 20 seconds
- **2nd alert**: After 60 seconds
- **3rd alert**: After 120 seconds
- **Then stops** until user refocuses (resets the cycle)

Uses custom sound file: `data/gavin alert sound.mp3` (cross-platform: afplay on macOS, powershell on Windows, mpg123/ffplay on Linux)

---

## 🐛 Common Issues

| Issue | Fix |
|-------|-----|
| "Vision API Error: Expecting value" | JSON parsing failed. Check markdown wrapping in `vision_detector.py` |
| "Statistics don't add up" | Verify `present + away + gadget = total` in `analytics.py` |
| "Gadget not detected" | Actively in use? Person looking at it? Check Vision API logs. Threshold? |
| "Credits not decreasing" | Vision API not called. Check HTTP POST logs |

---

## 🔄 Code Patterns

**Vision API JSON**: Strip markdown wrappers (`if response.startswith("```")`)  
**Retry Logic**: Exponential backoff for OpenAI API calls  
**Logging**: `logger.info()` for internal, `print()` only for user-facing state changes

---

## 🚫 What NOT to Do

- ❌ Fallback detection (AI-only by design)
- ❌ Save frames to disk (privacy)
- ❌ Increase API frequency (cost)
- ❌ Decimal minutes
- ❌ Stats that don't sum
- ❌ Run multiple instances (single-instance enforced via file lock)

---

## 🔐 Setup

**Required**: `.env` with `OPENAI_API_KEY=sk-...`  
**Stack**: Python 3.9+, OpenCV, OpenAI, ReportLab  
**Network**: Square's Artifactory mirror

---

## 📝 Code Standards

- Type hints required: `def func(x: int) -> str:`
- Docstrings on every function
- Use `pathlib.Path` not strings
- Python 3.9+ features

---

## 🧪 Quick Test

```bash
source venv/bin/activate
python3 main.py  # ~30s, press 'q', check ~/Downloads/
python3 -m unittest tests.test_session tests.test_analytics
```

---

## 🔄 Add New Detection Type

1. Update `vision_detector.py` prompt
2. Add event type to `config.py`
3. Handle in `session.py`
4. Add stats in `analytics.py`
5. Update `pdf_report.py`

---

**Privacy**: Frames → OpenAI (30-day retention) → deleted. No local session data saved. No video saved.

---

## 📁 Data Files

- `data/focus_statements.json` - **REQUIRED** - Contains feedback message templates for PDF reports
- `data/.privacy_accepted` - User-specific flag, gitignored
- `data/.gavin_instance.lock` - Instance lock file (auto-managed, gitignored)
- `data/usage_data.json` - MVP usage tracking (time used, extensions granted)

---

## 🔒 Single Instance Lock

Only one instance of Gavin AI can run at a time. Implemented via cross-platform file locking:
- **macOS/Linux**: `fcntl.flock()` - kernel-level lock, auto-released on crash
- **Windows**: `msvcrt.locking()` - same behavior

Lock file: `data/.gavin_instance.lock` - automatically cleaned up on exit.

---

## ⏱️ MVP Usage Limit

**Purpose**: Limits trial usage to prevent unbounded API costs.

**Key Files**:
- `tracking/usage_limiter.py` - Time tracking logic
- `config.py` - `MVP_LIMIT_SECONDS`, `MVP_EXTENSION_SECONDS`, `MVP_UNLOCK_PASSWORD`

**Behavior**:
- Default: Configurable via `MVP_LIMIT_SECONDS` (cumulative across all sessions)
- Time badge shown in GUI header (click for details)
- When exhausted: Session stops immediately, lockout overlay appears
- Password unlock: Grants `MVP_EXTENSION_SECONDS` per successful unlock

**Config (.env)**:
```
MVP_UNLOCK_PASSWORD=your-secret-password
```

**Data stored**: `data/usage_data.json` - total_used_seconds, total_granted_seconds, extensions_granted