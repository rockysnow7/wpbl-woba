from wpybl.data import GamesCollection
from wpybl.stats.batting import batting_counting_stats

import os
import pandas as pd


weights = pd.read_csv("data/woba_weights.csv")
weights = {k: v for k, v in weights.to_dict("tight")["data"]}


def wOBA_df(
    walks: pd.Series,
    hit_by_pitches: pd.Series,
    singles: pd.Series,
    doubles: pd.Series,
    triples: pd.Series,
    home_runs: pd.Series,
    at_bats: pd.Series,
    sac_flies: pd.Series,
) -> pd.Series:
    numerator = (
        weights["walk"] * walks
        + weights["hit_by_pitch"] * hit_by_pitches
        + weights["single"] * singles
        + weights["double"] * doubles
        # + weights["triple"] * triples
        + weights["home_run"] * home_runs
    )
    denominator = at_bats + walks + hit_by_pitches + sac_flies
    woba = numerator / denominator

    return woba.sort_values(ascending=False)


if __name__ == "__main__":
    games = GamesCollection.all()

    stats = batting_counting_stats(games)
    stats = stats[(stats["plate_appearances"] / stats["games"]) >= 3.1]
    stats = stats[
        [
            "bases_on_balls",
            "hit_by_pitches",
            "singles",
            "doubles",
            "triples",
            "home_runs",
            "at_bats",
            "sacrifice_flies",
        ]
    ]
    stats = stats.reset_index().rename(columns={"index": "name"})

    # merge "Maggie Foxx" into "Maggie Fox"
    stats["name"] = stats["name"].str.replace("Maggie Foxx", "Maggie Fox")
    stats = stats.groupby("name").agg(
        {
            "name": "first",
            "bases_on_balls": "sum",
            "hit_by_pitches": "sum",
            "singles": "sum",
            "doubles": "sum",
            "triples": "sum",
            "home_runs": "sum",
            "at_bats": "sum",
            "sacrifice_flies": "sum",
        }
    )

    woba = wOBA_df(
        stats["bases_on_balls"],
        stats["hit_by_pitches"],
        stats["singles"],
        stats["doubles"],
        stats["triples"],
        stats["home_runs"],
        stats["at_bats"],
        stats["sacrifice_flies"],
    )
    print(woba)

    if not os.path.exists("data"):
        os.mkdir("data")
    woba.to_csv("data/leaderboard.csv")
