# Keylogger Project (Educational Use Only)

This Python script acts as a keylogger for cybersecurity. It will demonstrate how attackers collect keystrokes.

## ⚠ Disclaimer
This tool is for **educational and ethical research** only. Do **not** deploy it without permission. Unauthorized use is illegal.

## Features
- Records keystrokes in real-time
- Sends logged data automatically via email and Discord webhook at configurable intervals
- Designed for educational purposes to understand keylogging techniques

## How To Use
1. Clone Repository
    git clone https://github.com/yourusername/your-repo-name.git
Replace yourusername and your-repo-name with your actual GitHub details.

### 2. Change into the Project Direcctory
    cd your-repo-name

### 3. Install Dependencies
    pip install pynput pyperclip requests

### 4. Configure Credentials
Edit run_keylogger.ps1 and fill in your details:
    $env:EMAIL_SENDER = "your_email@gmail.com"
    $env:EMAIL_PASSWORD = "your_app_password"
    $env:DISCORD_WEBHOOK = "https://discord.com/api/webhooks/..."
Use .example as a reference for what fields are needed.

### 5. Run the keylogger
    .\run_keylogger.ps1
