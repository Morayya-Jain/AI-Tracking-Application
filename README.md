# AI Study Focus Tracker

A local AI-powered study session tracker that monitors student presence and phone usage via webcam, logs events, and generates PDF reports with OpenAI-powered insights.

## Features

- **Webcam Monitoring**: Tracks student presence and detects potential phone usage
- **Session Analytics**: Computes focused time, away time, and phone usage statistics
- **AI-Powered Insights**: Uses OpenAI to generate friendly summaries and suggestions
- **PDF Reports**: Professional reports with statistics and AI-generated insights
- **Privacy-First**: All video processing happens locally; only statistics sent to OpenAI

## Requirements

- Python 3.11+
- Webcam
- OpenAI API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Usage

Run the tracker from the command line:

```bash
python main.py
```

### Session Flow

1. Press Enter to start a study session
2. The app monitors your presence via webcam
3. Events are logged (present, away, phone_suspected)
4. Press 'q' or Enter to end the session
5. A PDF report is automatically generated with:
   - Session statistics
   - Timeline of events
   - AI-generated summary and suggestions

### Reports

PDF reports are saved to the `reports/` directory with filenames like:
```
session_20251209_143000.pdf
```

Session data is also saved as JSON in `data/sessions/` for future analysis.

## Project Structure

```
focus_tracker/
├── main.py                    # CLI entry point
├── config.py                  # Configuration and constants
├── .env.example              # Example environment variables
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── camera/
│   ├── __init__.py
│   ├── capture.py           # Webcam management
│   └── detection.py         # Presence & phone detection
├── tracking/
│   ├── __init__.py
│   ├── session.py           # Session management & event logging
│   └── analytics.py         # Event summarization & statistics
├── reporting/
│   ├── __init__.py
│   └── pdf_report.py        # PDF generation
├── ai/
│   ├── __init__.py
│   └── summariser.py        # OpenAI API integration
├── data/
│   └── sessions/            # Stored session JSON files
├── reports/                  # Generated PDF reports
└── tests/
    ├── test_session.py
    └── test_analytics.py
```

## Configuration

Edit `config.py` to customize:
- Detection thresholds (face confidence, phone detection angle)
- Camera settings (resolution, FPS)
- OpenAI model selection
- Grace periods for state changes

## Privacy & Data

- **Video Processing**: All video analysis happens locally on your device
- **Data Sent to OpenAI**: Only anonymized statistics (durations, event counts)
- **Data Storage**: Session data stored locally as JSON files
- **No Cloud Storage**: All data remains on your computer

## Future Enhancements

- Session history viewer
- Dashboard with charts and trends
- Configurable detection sensitivity
- Multiple profile support
- Export to CSV/Excel

## License

MIT License - Feel free to use and modify for personal or educational purposes.

