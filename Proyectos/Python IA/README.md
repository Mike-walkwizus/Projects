# Twitch Bot - Complete Features

A powerful Twitch chat bot with custom commands, Rock-Paper-Scissors game, moderation, and points system.

## 🎯 Features

- **Custom Commands**: !hello, !help, !points, !stats, !leaderboard
- **Rock-Paper-Scissors Game**: !rps pierre/feuille/ciseaux with intelligent AI
- **Points System**: Earn points per message, win bonuses, spend on games
- **Moderation**: Automatic word filtering with warnings and timeouts
- **Statistics Tracking**: Track wins, losses, and points per user
- **Intelligent AI**: Bot learns user patterns and counters them

## 📋 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Twitch OAuth Token
1. Go to https://twitchapps.com/tmi/
2. Click "Connect with Twitch"
3. Copy the OAuth token (starts with `oauth:`)

### 3. Configure Environment
1. Rename `.env.example` to `.env`
2. Fill in:
   - `TWITCH_TOKEN=oauth:your_token_here`
   - `CHANNEL=your_channel_name` (lowercase)
   - `BOT_NICK=your_bot_name` (the bot account username)

### 4. Run the Bot
```bash
python bot.py
```

## 📝 Available Commands

| Command | Usage | Description |
|---------|-------|-------------|
| !hello | !hello | Bot greets you |
| !points | !points | Check your current points |
| !stats | !stats | Show your game statistics |
| !leaderboard | !leaderboard | Show top 5 users by points |
| !rps | !rps pierre/feuille/ciseaux | Play Rock-Paper-Scissors |
| !help | !help | Show all commands |

## ⚙️ Configuration

Edit `config.py` to customize:
- **Banned words** for moderation
- **Points rewards** for games and messages
- **Timeout duration** for violations
- **Game costs** in points

## 📊 Database

User data is stored in `bot_data.json`:
- Points balance
- Games won/lost
- Warning count

## 🎮 Game: Rock-Paper-Scissors

- **Cost**: 50 points
- **Win Reward**: +100 points
- **Lose Reward**: +10 points
- **Tie Reward**: +25 points

The bot learns from your game history and tries to counter your most common moves!

## 🔒 Moderation

- Automatic word filtering
- Warning system (default 3 warnings before timeout)
- Timeout duration: 5 minutes (configurable)

## ✨ Future Enhancements

- Raid notifications
- Follower alerts
- Custom games
- Streamer commands
- Song requests integration
- Discord webhook integration

## 📝 Notes

- Bot account should be mod in your channel
- Test in a small stream first before going live
- Keep your OAuth token secret!
