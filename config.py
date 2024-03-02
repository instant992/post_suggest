from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = os.environ.get("BOT_USERNAME")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
POST_SAMPLE = os.environ.get("POST_SAMPLE")
TARGET_CHANNEL_ID = os.environ.get("TARGET_CHANNEL_ID")