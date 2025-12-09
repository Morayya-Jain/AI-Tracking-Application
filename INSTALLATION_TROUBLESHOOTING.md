# Installation Troubleshooting Guide

## Issue Detected

Your system has security software that's modifying pip downloads, causing hash verification failures. This is common with:
- Corporate/Enterprise security software
- Antivirus programs (like Norton, McAfee, Kaspersky)
- VPN with SSL inspection
- Network proxies with deep packet inspection

## Solutions (Try in Order)

### Option 1: Temporarily Disable Security Software

1. Temporarily disable your antivirus/security software
2. Run the installation:
   ```bash
   cd "/Users/morayya/Development/AI Tracking Application"
   pip3 install opencv-python mediapipe reportlab openai python-dotenv --user
   ```
3. Re-enable your security software after installation

### Option 2: Use Homebrew (Recommended for macOS)

Install packages via Homebrew, which often bypasses these issues:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python packages
brew install python@3.11

# Use brew's pip
/opt/homebrew/bin/pip3 install opencv-python mediapipe reportlab openai python-dotenv
```

### Option 3: Install Without Hash Checking (Least Secure)

**Warning:** Only do this if you trust your network.

Create a pip configuration to disable hash checking:

```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[install]
trusted-host = pypi.org
               files.pythonhosted.org
[global]
disable-pip-version-check = true
EOF

# Then try installing
pip3 install opencv-python mediapipe reportlab openai python-dotenv --user
```

After installation, remove the config:
```bash
rm ~/.pip/pip.conf
```

### Option 4: Manual Download and Install

Download wheels manually from [PyPI](https://pypi.org/) and install:

```bash
cd /tmp

# Download packages manually (visit pypi.org for each)
# Or use curl:
curl -O https://files.pythonhosted.org/packages/.../opencv_python-...whl
curl -O https://files.pythonhosted.org/packages/.../mediapipe-...whl
# ... etc

# Install from local files
pip3 install opencv_python-*.whl mediapipe-*.whl --user
```

### Option 5: Use Conda/Miniconda

Conda often works when pip doesn't:

```bash
# Install Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# Create environment
conda create -n focus_tracker python=3.11
conda activate focus_tracker

# Install packages
conda install -c conda-forge opencv
pip install mediapipe reportlab openai python-dotenv
```

### Option 6: Docker (Most Isolated)

Run the app in Docker to completely bypass system restrictions:

```bash
# Create a Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
EOF

# Build and run
docker build -t focus-tracker .
docker run -it --device=/dev/video0 focus-tracker
```

## Checking What's Blocking

To identify what's interfering:

```bash
# Check for running security software
ps aux | grep -iE "norton|mcafee|kaspersky|avast|avg|sophos"

# Check network proxy settings
scutil --proxy

# Check firewall
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

## After Successful Installation

Verify installation:
```bash
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
python3 -c "import mediapipe; print('MediaPipe:', mediapipe.__version__)"
python3 -c "import reportlab; print('ReportLab:', reportlab.Version)"
python3 -c "import openai; print('OpenAI:', openai.__version__)"
python3 -c "import dotenv; print('python-dotenv: OK')"
```

If all imports work, you're ready to run:
```bash
python3 main.py
```

## Still Having Issues?

Contact me with:
1. Output of `pip3 --version`
2. Output of `python3 --version`
3. Your macOS version (`sw_vers`)
4. Any security software you have installed

