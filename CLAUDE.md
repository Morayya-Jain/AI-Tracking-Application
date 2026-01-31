# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BrainDock is an AI-powered focus tracking desktop application that monitors users via webcam to detect presence, gadget distractions, and screen distractions. It generates PDF reports with session analytics and AI-generated insights.

**Tech Stack:** Python 3.11+, tkinter (GUI), OpenAI/Gemini Vision APIs, OpenCV, ReportLab (PDF), Stripe (payments)

## Development Commands

```bash
# Run the application (GUI mode)
python main.py

# Run in CLI mode
python main.py --cli

# Run tests
python -m unittest tests.test_session
python -m unittest tests.test_analytics
python -m unittest tests.test_pdf_report

# Build macOS app bundle (from project root)
./build/build_macos.sh

# Build with PyInstaller directly
pyinstaller build/braindock.spec
```

## Environment Setup

Create `.env` with required keys:
```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_PRICE_ID=price_...
```

For development without license checks: `SKIP_LICENSE_CHECK=true`

## Architecture

### Detection Flow
```
Camera Frame → Vision API (OpenAI/Gemini) → Detection State → Session Logger → PDF Report
                    ↓
              Returns JSON:
              - person_present (any body part visible)
              - at_desk (working distance)
              - gadget_visible (active usage only)
              - distraction_type
```

### Event Types
- `present`: At desk, focused
- `away`: Not visible or far from desk
- `gadget_suspected`: Actively using phone/tablet/controller/TV
- `screen_distraction`: Distracting website/app detected
- `paused`: User manually paused session

### Monitoring Modes
- `camera_only`: Default - camera detection only
- `screen_only`: Screen monitoring only (no camera API calls)
- `both`: Camera + screen monitoring combined

### Key Modules
- `camera/vision_detector.py`, `camera/gemini_detector.py`: Vision API detection (base class in `base_detector.py`)
- `tracking/session.py`: Session lifecycle and event logging
- `tracking/analytics.py`: Statistics computation - **math must add up** (present + away + gadget + screen + paused = total)
- `screen/window_detector.py`, `screen/blocklist.py`: Screen monitoring and distraction blocklist
- `gui/app.py`: Main tkinter GUI application
- `licensing/license_manager.py`, `licensing/stripe_integration.py`: Payment and licensing
- `reporting/pdf_report.py`: PDF generation with ReportLab

### Vision Provider Selection
Set `VISION_PROVIDER` in `.env` or config: `"openai"` or `"gemini"` (default for bundled builds)

## Code Standards

- Type hints required for all function parameters and returns
- Docstrings for all functions
- Use `pathlib.Path` for file operations
- Use `logging` module for internal logs, `print()` only for user-facing output
- Time formatting: Use `format_duration()` from `tracking/analytics.py` → "1m 30s" not "1.5 minutes"
- Never use `cursor="hand2"` in tkinter UI - use native device cursor

## Critical Rules

1. **AI-Only Detection**: OpenAI/Gemini Vision API only - no hardcoded detection methods
2. **Gadget Detection**: Requires BOTH attention (looking at gadget) AND active engagement (device in use). Position irrelevant.
3. **Statistics Math**: `present + away + gadget + screen_distraction + paused = total` must always hold
4. **No Frame Storage**: Frames captured for analysis are never saved to disk (privacy)
5. **Cost Awareness**: Vision API costs ~$0.06-0.12/min at 1 FPS. Default is 0.33 FPS (~3s intervals)

## Key Configuration (config.py)

```python
DETECTION_FPS = 0.33          # ~3s between camera API calls
SCREEN_CHECK_INTERVAL = 3     # 3s between screen checks
OPENAI_VISION_MODEL = "gpt-4o-mini"
GEMINI_VISION_MODEL = "gemini-2.0-flash"
```

## Data Files

- `data/focus_statements.json`: **Required** - PDF feedback templates
- `data/blocklist.json`: Screen monitoring blocklist (auto-created in user data dir)

User data stored in:
- macOS: `~/Library/Application Support/BrainDock/`
- Windows: `%APPDATA%/BrainDock/`
- Reports: `~/Downloads/`

## Building for Distribution

The build process uses PyInstaller. API keys are embedded via `bundled_keys.py` (generated at build time from `bundled_keys_template.py`).

### Building macOS DMG (Step-by-Step for Agents)

**Prerequisites:**
- macOS (Darwin) system
- Python 3.9+
- Homebrew with `create-dmg` installed (`brew install create-dmg`)
- Developer ID certificate for signing (optional but recommended)

**Required Environment Variables:**
All keys are in the `.env` file. The build script needs them as environment variables:
- `GEMINI_API_KEY` (required - primary vision provider)
- `OPENAI_API_KEY` (optional - fallback)
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_PRICE_ID` (for payments)

**Build Commands:**

```bash
# Step 1: Create fresh build venv with PUBLIC PyPI
# IMPORTANT: The default pip may try to use internal Artifactory which fails
cd <project-root>  # e.g., /Users/you/Development/BrainDock
rm -rf .venv-build
python3 -m venv .venv-build
source .venv-build/bin/activate
pip config set global.index-url https://pypi.org/simple/
pip install --upgrade pip
pip install -r requirements.txt pyinstaller --quiet

# Step 2: Export keys from .env and run build
# NOTE: Don't use `source .env` - it fails on lines with spaces
export OPENAI_API_KEY="<from .env>"
export GEMINI_API_KEY="<from .env>"
export STRIPE_SECRET_KEY="<from .env>"
export STRIPE_PUBLISHABLE_KEY="<from .env>"
export STRIPE_PRICE_ID="<from .env>"
./build/build_macos.sh

# Step 3: Copy to Downloads for testing
cp dist/BrainDock-1.0.0-macOS.dmg ~/Downloads/
```

**Common Issues:**

1. **pip connection errors to Artifactory**: Run `pip config set global.index-url https://pypi.org/simple/` to force public PyPI

2. **"Resource busy" during DMG creation**: A previous DMG is still mounted. Fix:
   ```bash
   hdiutil info | grep -E "image-path|/dev/disk"  # Find mounted disk
   hdiutil detach /dev/diskN -force               # Eject it
   rm -f dist/rw.*.dmg dist/*.dmg                 # Clean up temp files
   ```

3. **`source .env` fails**: The `.env` file has lines with spaces (e.g., `PRODUCT_PRICE_DISPLAY=AUD 1.99...`). Export keys individually instead.

4. **Signing warnings**: Without `APPLE_ID` and `APPLE_APP_SPECIFIC_PASSWORD`, the app is signed but not notarized. Users may need to right-click → Open to bypass Gatekeeper.

**Build Output:**
- App bundle: `dist/BrainDock.app`
- DMG installer: `dist/BrainDock-1.0.0-macOS.dmg` (~99 MB)

**Cleanup:** The build script auto-removes `bundled_keys.py` after building. If it doesn't, delete it manually (contains secrets).

### Quick Local Build (No Keys Embedded)

For quick testing where the app reads from `.env` at runtime:
```bash
./build/build_local.sh
```
This creates an unsigned DMG in `~/Downloads/` but requires `.env` to be present at runtime.