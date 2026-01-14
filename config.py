import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

AI_API_KEY = os.getenv("AI_API_KEY")

AUTO_UNMUTE_SECONDS = 300