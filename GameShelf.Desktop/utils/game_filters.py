def get_unique_genres(games):
    return sorted({game.genre for game in games if game.genre})


def get_unique_platforms(games):
    return sorted({game.platform for game in games if game.platform})


def filter_games(games, collection_id, genre, platform):
    filtered_games = []

    for game in games:
        if collection_id != "all" and game.collection_id != collection_id:
            continue

        if genre != "all" and game.genre != genre:
            continue

        if platform != "all" and game.platform != platform:
            continue

        filtered_games.append(game)

    return filtered_games


def sort_games(games, sort_value):
    if sort_value == "title_desc":
        return sorted(games, key=lambda game: game.title.lower(), reverse=True)

    if sort_value == "genre_asc":
        return sorted(games, key=lambda game: (game.genre or "").lower())

    if sort_value == "platform_asc":
        return sorted(games, key=lambda game: (game.platform or "").lower())

    return sorted(games, key=lambda game: game.title.lower())
