import pandas as pd


def ramp_test_activity(
    profile: list[tuple[int:float]], segment_time: int = 30, test_length: int = 1200, ftp: int = 1
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Convert a power profile to a ramp test workout
    The last 30sec is always 1 second ramp.
    profile: list of tuples of seconds and power [(1, 100), (2, 90), (3, 85), (4, 80)] must start with 1sec
    segment_time: int, the time in seconds of each segment of the ramp test workout, starting after 30sec
    :return: full dataframe, workout segment dataframe, workout segment dataframe with power per ftp
    """
    try:
        assert profile[0][0] == 1
    except AssertionError:
        raise ValueError("The profile must start with 1 second")
    try:
        assert profile[-1][0] >= test_length
    except AssertionError:
        raise ValueError("The profile must end with with a time >= test_length")
    df = pd.DataFrame(profile, columns=["seconds", "power"])
    df.set_index("seconds", inplace=True)
    # fill in missing seconds
    new_index = pd.Index(range(1, profile[-1][0] + 1), name="seconds")
    df = df.reindex(new_index)
    # Interpolate power for missing seconds
    df["power"] = df["power"].interpolate(method="linear")
    df.reset_index(inplace=True)
    df = df[df.seconds <= test_length].copy()
    df["power_seconds"] = df["power"] * df["seconds"]
    df["ramp_power"] = 0
    df["ramp_power"] = (df["power_seconds"] - df["power_seconds"].shift(1, fill_value=0)).clip(lower=0)
    df["bins"] = df.apply(lambda row: row.name // segment_time + 30 if int(row.name) > 30 else row.name, axis=1)
    df["bin_power"] = df.groupby("bins")["ramp_power"].transform("mean").round(0)
    df["bin_time"] = df.groupby("bins")["seconds"].transform("count")
    df["power_per_ftp"] = df["power"] / ftp
    df["ramp_power_per_ftp"] = df["ramp_power"] / ftp
    df["bin_power_per_ftp"] = df["bin_power"] / ftp
    df.drop(columns=["power_seconds"], inplace=True)
    df_wko = df.drop_duplicates(subset=["bins"], keep="first")
    df_wko = df_wko[["bins", "bin_time", "bin_power", "bin_power_per_ftp"]].copy()
    df_wko.rename(
        columns={"bin_power": "power", "bin_time": "duration", "bin_power_per_ftp": "power%ftp"}, inplace=True
    )
    df_wko.sort_values(by="bins", ascending=False, inplace=True)
    df_wko.reset_index(drop=True, inplace=True)
    df_wko["segment"] = df_wko.index + 1
    return df, df_wko[["segment", "duration", "power", "power%ftp"]]


def make_zwo_from_ramp(workout: pd.DataFrame, filename: str | None, name: str, ftp: int | None = 1):
    xml = ""
    xml += "<workout_file>\n"
    xml += "  <author>Vincent Davis</author>\n"
    xml += f"  <name>Most Painful Ramp Test {name}</name>\n"
    xml += "  <description>A ramp test based on power profile</description>\n"
    xml += "  <sportType>bike</sportType>\n"
    xml += "  <tags></tags>\n"
    if ftp:
        xml += f"  <ftpOverride>{ftp}</ftpOverride>\n"
    xml += "  <workout>\n"
    for r in workout.to_dict(orient="records"):
        d = r["duration"]
        p = r["power%ftp"]
        xml += f'      <SteadyState Duration="{d}" Power="{p}"/>\n'
    xml += "    </workout>\n"
    xml += "</workout_file>\n"
    if filename:
        with open(filename, "w") as f:
            f.write(xml)
    return xml
