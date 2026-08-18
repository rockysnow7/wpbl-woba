import numpy as np
import os
import pandas as pd


# outs that don't advance runners
OUTS = [
    "sacrifice",
    "out",
    "groundout",
    "lineout",
    "flyout",
    "popup",
    "foul_out",
    "strikeout",
    # "caught_stealing",
]


if __name__ == "__main__":
    re24 = pd.read_csv("data/re24.csv").to_dict("tight")["data"]
    re24 = {k: v for k, v in re24}

    df = pd.read_csv("inputs/all_plays_run_values.csv")
    df["event_type"] = np.where(
        df["event_type"].isin(OUTS),
        "out",
        df["event_type"],
    )

    df["re_before"] = df["state"].map(re24)
    df["re_after"] = df["runs_scored"] + df["next_state"].map(re24)
    df["re_after"] = np.where(df["half_over"], 0.0, df["re_after"])

    df = df[["event_type", "re_before", "re_after"]]
    df["run_value"] = df["re_after"] - df["re_before"]

    run_values = (
        df.groupby("event_type")
        .agg({"run_value": "mean"})
        .sort_values("run_value", ascending=True)
    )
    if not os.path.exists("data"):
        os.mkdir("data")
    run_values.to_csv("data/run_values.csv")

    counts = df["event_type"].value_counts()
    counts.to_csv("data/run_values_counts.csv")
