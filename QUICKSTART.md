# Quick Start Guide

Get your AI Study Focus Tracker running in 3 minutes!

## 1. Install Dependencies (1 minute)

```bash
pip3 install -r requirements.txt
```

## 2. Set Your OpenAI API Key (30 seconds)

Create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

Replace `your-key-here` with your actual OpenAI API key from https://platform.openai.com/api-keys

## 3. Run It! (30 seconds)

```bash
python3 main.py
```

## What Happens Next?

1. You'll see a welcome screen
2. Press **Enter** to start tracking
3. Study while the app monitors via webcam
4. Press **Enter** or **'q'** to end the session
5. Get your PDF report with AI insights!

## Example Session

```
🎯 AI Study Focus Tracker v1.0
================================================

📚 Press Enter to start your study session...

✓ Session started at 02:30 PM
💡 Monitoring your study session...

⚠ Moved away from desk (02:35 PM)
✓ Back at desk (02:37 PM)
📱 Phone usage detected (02:42 PM)

Session ended. Duration: 45m

📊 Finalizing session...
✓ Report saved: reports/session_20251209_143000.pdf
```

## Tips for Best Results

- **Lighting:** Ensure good lighting on your face
- **Position:** Sit facing the camera
- **Distance:** Stay within 1-2 meters of the camera
- **Privacy:** All video processing is local - nothing is uploaded!

## Need Help?

- Camera not working? Check [INSTALL.md](INSTALL.md) troubleshooting section
- Questions? Read the full [README.md](README.md)

## What's in the Report?

Your PDF report includes:

✅ Total session duration  
✅ Focused time percentage  
✅ Away time tracking  
✅ Phone usage detection  
✅ Timeline of your session  
✅ AI-generated insights  
✅ Personalized improvement suggestions  

Happy studying! 🎯📚

