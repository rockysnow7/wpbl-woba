import os
import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("inputs/all_plays_re24.csv")

    df["runs_remaining"] = df.groupby(["game_id", "inning", "half"])[
        "runs_scored"
    ].transform(lambda x: x[::-1].cumsum()[::-1])

    re24 = df.groupby("state")["runs_remaining"].mean().round(2)
    if not os.path.exists("data"):
        os.mkdir("data")
    re24.to_csv("data/re24.csv")

    counts = df.groupby("state")["runs_remaining"].count()
    counts.to_csv("data/re24_counts.csv")
