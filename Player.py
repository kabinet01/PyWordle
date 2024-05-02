from db import register_user, login_user, get_score, change_score


class Player:
    """A class representing a player in the game.

    Attributes:
        name (str): The name of the player.
        password (str): The password associated with the player's account.
        score (int): The score of the player in the game.
    """

    def __init__(self, name, password):
        """Initialize a new player instance with a name, password, and score."""
        self.name = name
        self.password = password
        self.score = 0

    def __str__(self):
        """Return a string representation of the player."""
        return f'Player Name: {self.name}\nPlayer Score: {self.score}'

    def calls_register_user(self):
        res = register_user(self.name, self.password, self.score)
        return res

    def calls_login_user(self):
        res = login_user(self.name, self.password)
        if res:
            self.score = get_score(self.name)
        return res

    def calls_change_score(self):
        res = change_score(self.name, self.score)
        return res

