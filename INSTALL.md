# Installation Guide

## Prerequisites

- Python 3.11 or higher
- Webcam (built-in or external)
- OpenAI API key (get one from https://platform.openai.com/api-keys)

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using pip3:

```bash
pip3 install -r requirements.txt
```

### Dependencies Installed

- `opencv-python` - For camera access and image processing
- `mediapipe` - For face detection and pose estimation
- `reportlab` - For PDF generation
- `openai` - For AI-powered summaries
- `python-dotenv` - For environment variable management

## Step 2: Set Up Environment Variables

1. Create a `.env` file in the project root:

```bash
touch .env
```

2. Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Note:** You can get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## Step 3: Test Your Camera

Run a quick camera test:

```bash
python3 camera/capture.py
```

You should see output confirming your camera is working.

## Step 4: Run the Application

```bash
python3 main.py
```

## Troubleshooting

### Camera Issues

**Problem:** "Failed to open camera"

**Solutions:**
- Check if another application is using your webcam
- On macOS, grant camera permissions in System Preferences > Security & Privacy > Camera
- Try changing `CAMERA_INDEX` in `config.py` (try 0, 1, or 2)

### OpenCV Installation Issues

**Problem:** OpenCV won't install or import

**Solutions:**
- Try installing with: `pip3 install opencv-python-headless`
- On macOS with M1/M2: `arch -arm64 pip3 install opencv-python`

### MediaPipe Issues

**Problem:** MediaPipe import errors

**Solutions:**
- Update pip: `pip3 install --upgrade pip`
- Install with: `pip3 install mediapipe --no-cache-dir`

### OpenAI API Errors

**Problem:** "OpenAI API key not found"

**Solutions:**
- Verify `.env` file exists in the project root
- Check the API key is correctly formatted (starts with `sk-`)
- Ensure there are no extra spaces or quotes around the key

**Problem:** "Rate limit exceeded"

**Solutions:**
- The app uses `gpt-4o-mini` which is cost-effective
- Check your OpenAI account has available credits
- Add rate limiting in `config.py` if needed

## Optional: Virtual Environment

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Next Steps

Once installed, check out the [README.md](README.md) for usage instructions!

