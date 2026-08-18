from glob import glob

import os
import pandas as pd


if __name__ == "__main__":
    games = glob("games/*.csv")
    all_plays_inner = []
    for game in games:
        game_plays = pd.read_csv(game)
        game_plays["game_id"] = game.split("/")[-1].split(".")[0]
        all_plays_inner.append(game_plays)
    all_plays = pd.concat(all_plays_inner)
    all_plays = all_plays[
        [
            "game_id",
            "inning",
            "half",
            "outs",
            "sequence",
            "first_base",
            "second_base",
            "third_base",
            "runs_scored",
        ]
    ]
    all_plays["first_base"] = ~pd.isnull(all_plays["first_base"])
    all_plays["second_base"] = ~pd.isnull(all_plays["second_base"])
    all_plays["third_base"] = ~pd.isnull(all_plays["third_base"])

    df = all_plays[all_plays["outs"] != 3]

    df["state"] = (
        (df["third_base"].map(lambda x: "3" if x else "-"))
        + (df["second_base"].map(lambda x: "2" if x else "-"))
        + (df["first_base"].map(lambda x: "1" if x else "-"))
        + "/"
        + df["outs"].astype(str)
    )

    df = df[
        [
            "game_id",
            "sequence",
            "inning",
            "half",
            "state",
            "runs_scored",
        ]
    ]

    if not os.path.exists("inputs"):
        os.mkdir("inputs")
    df.to_csv("inputs/all_plays_re24.csv", index=False)
