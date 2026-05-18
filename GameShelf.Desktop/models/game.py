class Game:
    def __init__(self, game_id, title, genre, platform, image_url=None, collection_id=None):
        self.game_id = game_id
        self.title = title
        self.genre = genre
        self.platform = platform
        self.image_url = image_url
        self.collection_id = collection_id

    def __str__(self):
        return f"{self.title} ({self.genre})"