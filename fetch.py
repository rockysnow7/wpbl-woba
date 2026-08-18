from wpybl.data import GamesCollection

import os


if __name__ == "__main__":
    games = GamesCollection.all()

    if not os.path.exists("games"):
        os.mkdir("games")
    for game in games:
        game.plays_to_df(save_to_path=f"games/{game.game_id}.csv")
