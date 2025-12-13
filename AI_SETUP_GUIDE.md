# AI Features Setup Guide

## 🤖 What AI Does in This App

The app uses **OpenAI GPT-4o-mini** to analyze your study sessions and provide:

1. **Friendly Summaries** - Natural language description of your session
2. **Personalized Suggestions** - 3-5 actionable tips to improve focus
3. **Encouraging Feedback** - Positive, supportive coaching tone

### Important: Privacy First! 🔒

- ✅ Only **statistics** are sent to OpenAI (durations, percentages)
- ❌ **NO video frames** are ever sent
- ❌ **NO personal information** is sent
- ✅ All video processing stays **100% local**

**Example of what's sent to OpenAI:**
```
Total Duration: 45 minutes
Focused Time: 35 minutes (78%)
Away Time: 7 minutes
Phone Usage: 3 minutes
Event timeline with timestamps
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Your OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. **Save it somewhere safe** - you won't see it again!

**Cost:** ~$0.001 per session (very cheap using gpt-4o-mini)

### Step 2: Add API Key to Your Project

Create a `.env` file in your project directory:

```bash
cd "/Users/morayya/Development/AI Tracking Application"
nano .env
```

Add this line (replace with your actual key):
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Save and exit (Ctrl+O, Enter, Ctrl+X in nano)

### Step 3: Run the App

```bash
python3 main.py
```

That's it! AI is now active. The app will automatically use OpenAI when available.

---

## 🎯 How It Works

### Without API Key (Current State):
```
Session Data → Built-in Summary Generator → Basic Report
```

### With API Key (Enhanced):
```
Session Data → OpenAI GPT-4o-mini → Personalized AI Summary → Enhanced Report
```

### Code Flow:

```python
# From ai/summariser.py

if API_KEY_EXISTS:
    # Use OpenAI for smart summaries
    summary = call_openai_with_retry(statistics)
else:
    # Use fallback summaries (still good!)
    summary = generate_basic_summary(statistics)
```

---

## 📊 Example Output Comparison

### Fallback Mode (No API Key):
```
Session Summary:
Total Duration: 1h 0m
Focused Time: 45.0 minutes (75.0%)
Away Time: 10.0 minutes
Phone Usage: 5.0 minutes

Good session! You maintained decent focus with some breaks.

Suggestions:
1. Set specific goals before each session
2. Use the Pomodoro Technique: 25 min work, 5 min breaks
```

### AI Mode (With API Key):
```
Session Summary:
Excellent work today! You maintained strong focus for 75% of 
your hour-long session. The brief breaks you took were actually 
beneficial - research shows short breaks improve retention. 
Your phone usage was minimal, which is fantastic!

Suggestions:
1. Since you're already doing well, try extending your focused 
   periods to 30 minutes using the Pomodoro technique
2. Your away time suggests good break habits - keep it up!
3. Consider tracking what triggers your phone usage (boredom, 
   specific tasks?) to minimize it further
4. Celebrate this win! 75% focus is above average
5. Next session, try a "phone in another room" challenge
```

**Notice:** AI summaries are more personalized, contextual, and encouraging!

---

## ⚙️ Configuration Options

Edit `config.py` to customize AI behavior:

```python
# AI Model Selection
OPENAI_MODEL = "gpt-4o-mini"  # Cheap and fast
# Other options: "gpt-4o", "gpt-4" (more expensive)

# Retry Settings
OPENAI_MAX_RETRIES = 3  # Retry failed API calls
OPENAI_RETRY_DELAY = 1  # Seconds between retries
```

---

## 💰 Pricing Guide

Using **gpt-4o-mini** (current setting):

- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

**Typical Session Cost:**
- Input: ~500 tokens (~$0.00008)
- Output: ~300 tokens (~$0.00018)
- **Total: ~$0.0003 per session** (less than a penny!)

**Monthly estimate:** 100 sessions = ~$0.03/month

---

## 🔧 Troubleshooting

### "OpenAI API key not found"
✅ Create `.env` file in project root
✅ Format: `OPENAI_API_KEY=sk-...` (no quotes, no spaces)
✅ Restart the app after adding key

### "Rate limit exceeded"
✅ You're making too many requests
✅ Wait a minute and try again
✅ Check your OpenAI account usage limits

### "Invalid API key"
✅ Double-check the key copied correctly
✅ Ensure no extra spaces or newlines
✅ Generate a new key if needed

### "API Success: False" in report
✅ This means fallback was used (still works!)
✅ Check if API key is set correctly
✅ Check OpenAI account has credits

---

## 🧪 Testing Your Setup

Run this test to verify OpenAI integration:

```bash
cd "/Users/morayya/Development/AI Tracking Application"
python3 -c "
import sys
sys.path.insert(0, '.')
from ai.summariser import SessionSummariser

summariser = SessionSummariser()

if summariser.client:
    print('✅ OpenAI API key found and client initialized!')
    print(f'   Using model: {summariser.model}')
else:
    print('⚠️  No API key - using fallback mode')
    print('   Add OPENAI_API_KEY to .env file to enable AI')
"
```

---

## 🎓 What the AI Analyzes

The AI receives these statistics and generates insights:

1. **Time Metrics:**
   - Total session duration
   - Focused time percentage
   - Away time patterns
   - Phone usage frequency

2. **Event Timeline:**
   - When you were focused
   - When you took breaks
   - When phone usage occurred
   - Duration of each period

3. **Context:**
   - Time of day (morning/afternoon/evening)
   - Session length (short/medium/long)
   - Focus patterns (consistent/sporadic)

**The AI uses this to:**
- Identify your strengths
- Suggest specific improvements
- Provide encouraging feedback
- Offer personalized strategies

---

## 🔐 Security & Privacy

### Data Sent to OpenAI:
- ✅ Anonymous session statistics
- ✅ Generic event timeline
- ❌ NO video or images
- ❌ NO personal identifying information
- ❌ NO screen content

### OpenAI's Data Policy:
- API data is NOT used to train models (as of 2024)
- Data retained for 30 days for abuse monitoring
- Then permanently deleted
- Read more: https://openai.com/policies/api-data-usage-policies

### Your Control:
- You can use the app WITHOUT OpenAI (fallback mode)
- You can delete your API key anytime
- Local fallback summaries still work great!

---

## 📚 Further Customization

### Change the AI's Personality

Edit `ai/summariser.py` line ~172 to customize the system prompt:

```python
"role": "system",
"content": "You are a supportive study coach who provides "
          "encouraging feedback and practical suggestions."
```

Try:
- "You are a strict but fair professor..."
- "You are an enthusiastic cheerleader..."
- "You are a data analyst providing clinical insights..."

### Adjust Summary Length

Edit the prompt to request longer/shorter summaries:

```python
"Please provide:"
"1. A 2-3 sentence summary..."  # Make longer: "4-5 sentences"
"2. 3-5 specific suggestions..."  # More: "7-10 suggestions"
```

---

## ✨ Ready to Enable AI?

Just follow the 3 steps at the top of this guide:
1. Get API key from OpenAI
2. Add to `.env` file
3. Run the app!

The AI features will activate automatically when it detects the key. No code changes needed! 🎉


