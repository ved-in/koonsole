import os
import json

dir = os.path.join(os.path.dirname(__file__), "..", "data")
CHANNELS_FILE = os.path.join(dir, "channels.json")

channels_list = []

def load_channel_list():
    global channels_list
    if os.path.exists(CHANNELS_FILE):
        try:
            with open(CHANNELS_FILE, "r") as f:
                channels_list = json.load(f)
        except Exception:
            channels_list = []

def save_channel_list():
    with open(CHANNELS_FILE, "w") as f:
        json.dump(channels_list, f)