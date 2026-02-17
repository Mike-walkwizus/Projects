import json
import os
from config import DB_FILE

class Database:
    def __init__(self):
        self.file = DB_FILE
        self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {"users": {}, "warnings": {}}
            self.save()

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_user(self, user):
        if user not in self.data["users"]:
            self.data["users"][user] = {"points": 0, "games_won": 0, "games_lost": 0}
            self.save()

    def get_points(self, user):
        self.add_user(user)
        return self.data["users"][user]["points"]

    def add_points(self, user, points):
        self.add_user(user)
        self.data["users"][user]["points"] += points
        self.save()
        return self.data["users"][user]["points"]

    def remove_points(self, user, points):
        self.add_user(user)
        self.data["users"][user]["points"] = max(0, self.data["users"][user]["points"] - points)
        self.save()
        return self.data["users"][user]["points"]

    def add_game_win(self, user):
        self.add_user(user)
        self.data["users"][user]["games_won"] += 1
        self.save()

    def add_game_loss(self, user):
        self.add_user(user)
        self.data["users"][user]["games_lost"] += 1
        self.save()

    def get_stats(self, user):
        self.add_user(user)
        return self.data["users"][user]

    def add_warning(self, user):
        if user not in self.data["warnings"]:
            self.data["warnings"][user] = 0
        self.data["warnings"][user] += 1
        self.save()
        return self.data["warnings"][user]

    def get_warnings(self, user):
        return self.data["warnings"].get(user, 0)

    def reset_warnings(self, user):
        if user in self.data["warnings"]:
            del self.data["warnings"][user]
            self.save()

    def get_top_users(self, limit=5):
        sorted_users = sorted(self.data["users"].items(), key=lambda x: x[1]["points"], reverse=True)
        return sorted_users[:limit]
