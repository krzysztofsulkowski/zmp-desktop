from types import SimpleNamespace

from utils.game_filters import filter_games, get_unique_genres, get_unique_platforms, sort_games


def game(title, genre=None, platform=None, collection_id=1):
    return SimpleNamespace(title=title, genre=genre, platform=platform, collection_id=collection_id)


def test_get_unique_genres_and_platforms_skip_empty_values_and_sort():
    games = [
        game("A", "RPG", "PC"),
        game("B", "Action", "Xbox"),
        game("C", "RPG", None),
        game("D", None, "PC"),
    ]

    assert get_unique_genres(games) == ["Action", "RPG"]
    assert get_unique_platforms(games) == ["PC", "Xbox"]


def test_filter_games_by_collection_genre_and_platform():
    games = [
        game("A", "RPG", "PC", 1),
        game("B", "RPG", "Xbox", 1),
        game("C", "Action", "PC", 2),
    ]

    assert filter_games(games, 1, "RPG", "PC") == [games[0]]
    assert filter_games(games, "all", "RPG", "all") == [games[0], games[1]]
    assert filter_games(games, 2, "all", "PC") == [games[2]]


def test_sort_games_by_title_genre_and_platform():
    games = [
        game("Zelda", "RPG", "Switch"),
        game("alan wake", "Horror", "PC"),
        game("Cyberpunk", "Action", "Xbox"),
    ]

    assert [item.title for item in sort_games(games, "title_asc")] == ["alan wake", "Cyberpunk", "Zelda"]
    assert [item.title for item in sort_games(games, "title_desc")] == ["Zelda", "Cyberpunk", "alan wake"]
    assert [item.title for item in sort_games(games, "genre_asc")] == ["Cyberpunk", "alan wake", "Zelda"]
    assert [item.title for item in sort_games(games, "platform_asc")] == ["alan wake", "Zelda", "Cyberpunk"]
