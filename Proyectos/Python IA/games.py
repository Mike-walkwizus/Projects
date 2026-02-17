import random

class RockPaperScissors:
    def __init__(self):
        self.choices = ["pierre", "feuille", "ciseaux"]
        self.winning_combos = {
            "pierre": "ciseaux",
            "feuille": "pierre",
            "ciseaux": "feuille"
        }

    def bot_choice(self, user_history):
        """Intelligent bot choice based on user's history"""
        if not user_history:
            return random.choice(self.choices)
        
        # Counter the most common move
        most_common = max(user_history, key=user_history.get)
        
        # Return winning move against most common
        for move, beats in self.winning_combos.items():
            if beats == most_common:
                return move
        
        return random.choice(self.choices)

    def play(self, user_choice, bot_choice):
        """
        Returns: "win", "lose", or "tie"
        """
        if user_choice not in self.choices:
            return None
        
        if user_choice == bot_choice:
            return "tie"
        elif self.winning_combos[user_choice] == bot_choice:
            return "win"
        else:
            return "lose"

    def get_result_message(self, user_choice, bot_choice, result):
        """Returns a formatted result message"""
        if result == "win":
            return f"🎉 You win! You chose {user_choice}, I chose {bot_choice}"
        elif result == "lose":
            return f"😢 You lose! You chose {user_choice}, I chose {bot_choice}"
        else:
            return f"🤝 It's a tie! We both chose {user_choice}"
