# Gavin AI - Agent Quick Reference

**TL;DR**: Python focus tracker using OpenAI Vision API to detect present/away/gadget/paused states. Generates PDF reports. AI-only detection, no hardcoded methods.

## 📁 Key Files

| File | Purpose |
|------|---------|
| `config.py` | **ALL constants** (models, FPS, thresholds, usage limits) |
| `camera/vision_detector.py` | Main detection logic (`analyze_frame()`) |
| `tracking/analytics.py` | **Stats computation - MATH MUST ADD UP** |
| `tracking/session.py` | Event logging, state changes |
| `tracking/usage_limiter.py` | MVP usage time tracking & limits |
| `reporting/pdf_report.py` | PDF generation (~/Downloads/) |
| `gui/app.py` | Desktop GUI (tkinter) - main application |

*Ignore: `detection.py`, `phone_detector.py` (legacy)*

## ⚠️ Critical Rules

1. **Math Must Add Up**: `present + away + gadget + paused = total` in `analytics.py`
2. **AI-Only Detection**: NO hardcoded detection. OpenAI Vision API only (~$0.06-0.12/min)
3. **Time Format**: Use `_format_time()` → "1m 30s" not "1.5 minutes"
4. **PDF Output**: Page 1 = Summary Statistics. Page 2+ = Session logs

## 📊 Event Types

- `present`: At desk, focused
- `away`: Not visible or far from desk
- `gadget_suspected`: Actively using phone/tablet/controller/TV (⚠️ NOT smartwatches)
- `paused`: User manually paused session (timer frozen, no API calls)

## ⏸️ Pause Feature

- Grey "Pause" button appears above Stop when session running (sky blue when "Resume")
- When paused: Timer freezes instantly, no API calls, usage countdown pauses
- Focus rate excludes paused time: `focus_rate = present / (active_time)` where `active_time = total - paused`
- PDF shows "Active Time" (excludes paused), paused rows in grey text

## 🔔 Unfocused Alerts

Audio alerts when unfocused: 20s → 60s → 120s, then stops until refocus. Sound: `data/gavin_alert_sound.mp3`

## 🔧 Key Constants (config.py)

```python
DETECTION_FPS = 0.33              # ~3s between API calls (cost control)
OPENAI_VISION_MODEL = "gpt-4o-mini"
UNFOCUSED_ALERT_TIMES = [20, 60, 120]
MVP_LIMIT_SECONDS = 7200          # 2 hours default
```

## 🐛 Common Issues

| Issue | Fix |
|-------|-----|
| "Vision API Error: Expecting value" | JSON parsing failed. Check markdown wrapping |
| "Statistics don't add up" | Verify math in `analytics.py` |
| "Gadget not detected" | Must be actively in use with person looking at it |

## 🚫 What NOT to Do

- ❌ Fallback detection (AI-only) | ❌ Save frames to disk (privacy) | ❌ Increase API frequency
- ❌ Decimal minutes | ❌ Stats that don't sum | ❌ Run multiple instances

## 🔐 Setup & Test

```bash
# Required: .env with OPENAI_API_KEY=sk-...
source venv/bin/activate
python3 main.py  # GUI launches, check ~/Downloads/ for PDF
python3 -m unittest tests.test_session tests.test_analytics
```

## ⏱️ MVP Usage Limit

Limits trial usage via `MVP_LIMIT_SECONDS`. Time badge in GUI header (click for details). When exhausted: lockout overlay appears, password unlock grants `MVP_EXTENSION_SECONDS`. Set `MVP_UNLOCK_PASSWORD` in `.env`.

## 📁 Data Files

- `data/focus_statements.json` - **REQUIRED** - PDF feedback templates
- `data/usage_data.json` - Usage tracking (gitignored)
- `data/.gavin_instance.lock` - Single instance lock (auto-managed)
- `data/gavin_alert_sound.mp3` - Custom alert sound for unfocused notifications

## 🔄 Add New Detection Type

1. Update `vision_detector.py` prompt → 2. Add to `config.py` → 3. Handle in `session.py` → 4. Stats in `analytics.py` → 5. PDF in `pdf_report.py`

## 🔄 Code Patterns

- **Vision API JSON**: Strip markdown wrappers (`if response.startswith("```")`)
- **Retry Logic**: Exponential backoff for OpenAI API calls
- **Logging**: `logger.info()` internal, `print()` user-facing • **Thread Safety**: `root.after()` for UI

## 📝 Code Standards

Type hints required • Docstrings on every function • Use `pathlib.Path` • Python 3.9+

**Privacy**: Frames → OpenAI (30-day retention) → deleted. No video saved locally.
