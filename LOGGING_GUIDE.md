# Logging Configuration Guide

## Overview

The app uses Python's logging system to display information about what's happening. You can control how much information is displayed.

---

## Quick Control: .env File

Add this line to your `.env` file to control log verbosity:

```bash
# Show less (only warnings and errors)
LOG_LEVEL=WARNING

# Show everything (useful for debugging)
LOG_LEVEL=DEBUG

# Balanced (default - shows info, warnings, errors)
LOG_LEVEL=INFO
```

---

## Log Levels Explained

| Level | What You'll See | Use Case |
|-------|-----------------|----------|
| **DEBUG** | Everything (API calls, frame processing, etc.) | Deep debugging |
| **INFO** | Important events (session start, gadget detected, etc.) | Normal development (default) |
| **WARNING** | Only warnings and errors | Clean terminal output |
| **ERROR** | Only errors | Production mode |

---

## Examples

### Current Output (INFO level)
```
2026-01-14 10:30:45 - main - INFO - Session started
2026-01-14 10:30:46 - httpx - DEBUG - HTTP Request: POST https://api.openai.com/v1/chat/completions
2026-01-14 10:30:47 - vision_detector - INFO - ⚡ Gadget detected by AI! Type: phone, Confidence: 0.85
2026-01-14 10:31:00 - main - INFO - Session ended
```

### With WARNING level (cleaner)
```
✓ Session started at 10:30 AM
💡 Monitoring your focus session...
⚡ On another gadget (10:30 AM)
Session ended. Duration: 30s
```

### With DEBUG level (very verbose)
```
2026-01-14 10:30:45 - main - INFO - Session started
2026-01-14 10:30:46 - httpx - DEBUG - HTTP Request: POST https://api.openai.com/v1/chat/completions
2026-01-14 10:30:46 - httpcore - DEBUG - connect_tcp.started host='api.openai.com' port=443
2026-01-14 10:30:46 - httpcore - DEBUG - connect_tcp.complete return_value=<...>
2026-01-14 10:30:47 - openai - DEBUG - Response status: 200
2026-01-14 10:30:47 - vision_detector - DEBUG - Vision API raw response: {"person_present": true...
2026-01-14 10:30:47 - vision_detector - INFO - ⚡ Gadget detected by AI! Type: phone, Confidence: 0.85
```

---

## HTTP Request Logs

Those HTTP logs you see are from the OpenAI library making API calls. They're now suppressed by default, but you can see them with `LOG_LEVEL=DEBUG`.

**Suppressed libraries:**
- `httpx` - HTTP client used by OpenAI
- `httpcore` - Low-level HTTP implementation
- `openai` - OpenAI SDK
- `urllib3` - Another HTTP library

These are controlled in `main.py` lines 27-35.

---

## When Building GUI/Desktop App

**Good news:** When you build a proper GUI:

✅ **Terminal logs are hidden automatically** - Users won't see them  
✅ **Logs can be redirected to files** - For debugging if needed  
✅ **GUI will show clean status messages** - No technical logs  
✅ **You can add a "debug mode" toggle** - For power users  

**Example GUI logging setup:**
```python
# In GUI app:
if debug_mode:
    logging.basicConfig(level=logging.DEBUG, filename='gavin_debug.log')
else:
    logging.basicConfig(level=logging.ERROR, filename='gavin_errors.log')
```

---

## Recommendation

**For Development (now):**
- Keep `LOG_LEVEL=INFO` (current default)
- Shows important events without being too noisy
- HTTP logs are suppressed

**For Testing:**
- Use `LOG_LEVEL=WARNING` for clean output
- Focus on user-facing messages

**For Debugging:**
- Use `LOG_LEVEL=DEBUG` to see everything
- Helpful when tracking down issues

**For GUI (future):**
- Logs will be invisible to users by default
- Redirect to log files for troubleshooting
- Add optional "Show Debug Logs" in settings

---

## How It Works Now

1. `config.py` reads `LOG_LEVEL` from `.env` (defaults to INFO)
2. `main.py` sets up logging and suppresses noisy third-party logs
3. Your code logs important events with `logger.info()`, `logger.error()`, etc.
4. Users see clean, relevant messages

---

## Summary

**TL;DR:** 

✅ Keep logs as-is for now - they're helpful during development  
✅ Add `LOG_LEVEL=WARNING` to `.env` if you want cleaner output  
✅ When you build GUI, logs won't be visible to users anyway  
✅ You can always redirect logs to files later  

No need to worry about them now - they'll naturally disappear when you move to a GUI! 🎯
