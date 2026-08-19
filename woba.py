from pprint import pprint

import pandas as pd


def league_obp() -> float:
    counts = pd.read_csv("data/run_values_counts.csv")
    counts = {k: v for k, v in counts.to_dict("tight")["data"]}

    numerator = (
        counts.get("single", 0)
        + counts.get("double", 0)
        + counts.get("triple", 0)
        + counts.get("home_run", 0)
        + counts.get("walk", 0)
        + counts.get("hit_by_pitch", 0)
    )
    denominator = (
        counts.get("out", 0)  # this already includes sacrifices
        + counts.get("single", 0)
        + counts.get("double", 0)
        + counts.get("triple", 0)
        + counts.get("home_run", 0)
        # + counts.get("wild_pitch", 0)
        # + counts.get("passed_ball", 0)
        + counts.get("fielders_choice", 0)
        + counts.get("walk", 0)
        + counts.get("hit_by_pitch", 0)
    )

    return numerator / denominator


if __name__ == "__main__":
    run_values = pd.read_csv("data/run_values.csv")

    # weight relative to out
    out_value = run_values[run_values["event_type"] == "out"]["run_value"].at[1]
    run_values["run_value"] = run_values["run_value"] - out_value  # type: ignore
    run_values = run_values[
        run_values["event_type"].isin(
            [
                "walk",
                "hit_by_pitch",
                "single",
                "double",
                "triple",
                "home_run",
            ]
        )
    ]
    run_values = {k: v for k, v in run_values.to_dict("tight")["data"]}

    # calculate league wOBA
    counts = pd.read_csv("data/run_values_counts.csv")
    counts = {k: v for k, v in counts.to_dict("tight")["data"]}

    numerator = sum(
        counts[event_type] * run_values[event_type] for event_type in run_values
    )

    denominator = (
        counts.get("out", 0)  # this already includes sacrifices
        + counts.get("single", 0)
        + counts.get("double", 0)
        + counts.get("triple", 0)
        + counts.get("home_run", 0)
        # + counts.get("wild_pitch", 0)
        # + counts.get("passed_ball", 0)
        + counts.get("fielders_choice", 0)
        + counts.get("walk", 0)
        + counts.get("hit_by_pitch", 0)
    )

    woba = numerator / denominator
    print(f"League wOBA: {woba:.3f}")

    # calculate wOBA scale
    obp = league_obp()
    print(f"League OBP: {obp:.3f}")

    scale = obp / woba
    print(f"wOBA scale: {scale:.3f}")

    # save wOBA weights
    weights = pd.DataFrame(
        {
            "event_type": run_values.keys(),
            "weight": [value * scale for value in run_values.values()],
        }
    )
    weights.to_csv("data/woba_weights.csv", index=False)
    print(weights)
