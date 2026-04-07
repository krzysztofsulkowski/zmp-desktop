class Game:
    def __init__(self, game_id, title, genre, platform, image_url):
        self.game_id = game_id
        self.title = title
        self.genre = genre
        self.platform = platform
        self.image_url = image_url

    def __repr__(self):
        return f"{self.title} ({self.genre})"