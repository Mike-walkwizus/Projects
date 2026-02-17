import os
from dotenv import load_dotenv

load_dotenv()

# Twitch Configuration
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")
CHANNEL = os.getenv("CHANNEL")
BOT_NICK = os.getenv("BOT_NICK")

# Database file
DB_FILE = "bot_data.json"

# Moderation settings
BANNED_WORDS = ["badword1", "badword2"]  # Add words to ban
WARN_THRESHOLD = 3  # Warns before timeout
TIMEOUT_DURATION = 300  # 5 minutes in seconds

# Points system
POINTS_PER_MESSAGE = 1
POINTS_FOR_GAME_WIN = 100
POINTS_FOR_GAME_LOSS = 10

# Game settings
ROCK_PAPER_SCISSORS_COST = 50  # Points to play
