import os
import requests #Enables HTTP requests

# Need to create this from within Discord server
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord_log(text):
    data = {
        "content": text
    }
    try:
        # POST request to discord webhook with JSON data
        response = requests.post(DISCORD_WEBHOOK, json=data)
        # Status code is 204, 'The request completed successfully but returned no content.' for discord
        if response.status_code == 204:
            print("discord message sent successfully!")
        else:
            print("failed to send discord message")
    except:
        print("error: failed to send the discord message")