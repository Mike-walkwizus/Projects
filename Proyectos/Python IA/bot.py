import twitchio
from twitchio.ext import commands
from config import (
    TWITCH_TOKEN, CHANNEL, BOT_NICK, BANNED_WORDS, WARN_THRESHOLD,
    TIMEOUT_DURATION, POINTS_PER_MESSAGE, POINTS_FOR_GAME_WIN, 
    POINTS_FOR_GAME_LOSS, ROCK_PAPER_SCISSORS_COST
)
from database import Database
from games import RockPaperScissors
import random

class TwitchBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.rps = RockPaperScissors()
        self.user_history = {}  # Track user's game choices

    @commands.command(name="hello")
    async def hello(self, ctx):
        """Basic greeting command"""
        await ctx.send(f"Hello {ctx.author.name}! 👋")

    @commands.command(name="points")
    async def points(self, ctx):
        """Check your current points"""
        user = ctx.author.name
        points = self.db.get_points(user)
        await ctx.send(f"{user} has {points} points!")

    @commands.command(name="stats")
    async def stats(self, ctx):
        """Check your game statistics"""
        user = ctx.author.name
        stats = self.db.get_stats(user)
        wins = stats["games_won"]
        losses = stats["games_lost"]
        points = stats["points"]
        await ctx.send(f"{user} Stats - Points: {points} | Wins: {wins} | Losses: {losses}")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        """Show top 5 users by points"""
        top_users = self.db.get_top_users(5)
        if not top_users:
            await ctx.send("No stats yet!")
            return
        
        leaderboard = "🏆 Top 5: "
        for i, (user, data) in enumerate(top_users, 1):
            leaderboard += f"{i}. {user} ({data['points']}pts) | "
        await ctx.send(leaderboard)

    @commands.command(name="rps")
    async def rock_paper_scissors(self, ctx, choice: str = None):
        """Play Rock-Paper-Scissors! Usage: !rps pierre/feuille/ciseaux"""
        user = ctx.author.name
        
        if choice is None:
            await ctx.send(f"{user}, use: !rps pierre, !rps feuille, or !rps ciseaux")
            return
        
        choice = choice.lower()
        
        # Check points
        user_points = self.db.get_points(user)
        if user_points < ROCK_PAPER_SCISSORS_COST:
            await ctx.send(f"{user}, you need {ROCK_PAPER_SCISSORS_COST} points to play! You have {user_points}")
            return
        
        # Deduct points
        self.db.remove_points(user, ROCK_PAPER_SCISSORS_COST)
        
        # Track user's choice for AI learning
        if user not in self.user_history:
            self.user_history[user] = {}
        self.user_history[user][choice] = self.user_history[user].get(choice, 0) + 1
        
        # Bot plays
        bot_choice = self.rps.bot_choice(self.user_history.get(user, {}))
        result = self.rps.play(choice, bot_choice)
        
        if result is None:
            await ctx.send(f"{user}, that's not a valid choice! Use: pierre, feuille, or ciseaux")
            self.db.add_points(user, ROCK_PAPER_SCISSORS_COST)  # Refund
            return
        
        # Calculate rewards
        if result == "win":
            self.db.add_points(user, POINTS_FOR_GAME_WIN)
            self.db.add_game_win(user)
            message = self.rps.get_result_message(choice, bot_choice, result)
            await ctx.send(f"{user} {message} +{POINTS_FOR_GAME_WIN} points!")
        elif result == "lose":
            self.db.add_points(user, POINTS_FOR_GAME_LOSS)
            self.db.add_game_loss(user)
            message = self.rps.get_result_message(choice, bot_choice, result)
            await ctx.send(f"{user} {message} +{POINTS_FOR_GAME_LOSS} points")
        else:
            self.db.add_points(user, 25)  # Tie reward
            message = self.rps.get_result_message(choice, bot_choice, result)
            await ctx.send(f"{user} {message} +25 points")

    @commands.command(name="help")
    async def help(self, ctx):
        """List all available commands"""
        commands_list = (
            "Available commands: !hello, !points, !stats, !leaderboard, "
            "!rps (pierre/feuille/ciseaux), !help"
        )
        await ctx.send(commands_list)

    @commands.Cog.event()
    async def event_message(self, message):
        """Handle every message in chat"""
        if message.echo:
            return
        
        user = message.author.name
        self.db.add_points(user, POINTS_PER_MESSAGE)
        
        # Moderation - check for banned words
        content_lower = message.content.lower()
        for banned_word in BANNED_WORDS:
            if banned_word in content_lower:
                warnings = self.db.add_warning(user)
                await message.channel.send(
                    f"{user} ⚠️ Watch your language! (Warning {warnings}/{WARN_THRESHOLD})"
                )
                
                if warnings >= WARN_THRESHOLD:
                    await message.channel.timeout(user, TIMEOUT_DURATION)
                    await message.channel.send(f"{user} has been timed out for {TIMEOUT_DURATION}s")
                    self.db.reset_warnings(user)
                break
        
        await self.bot.handle_commands(message)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )
        self.add_cog(TwitchBot(self))

    async def event_ready(self):
        print(f"✅ Bot is online as {self.nick}")
        print(f"📺 Connected to {CHANNEL}")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
