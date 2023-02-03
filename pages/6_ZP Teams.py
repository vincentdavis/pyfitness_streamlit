from time import sleep

import pandas as pd
import streamlit as st

from zp_teams import team_list, team_overlap_by_rider

st.title("ZP Team List")
""" # Teams and Riders
### New page, needs lots of work.
This is a new section, work in progress.
Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)

You can also contact me on discord: [Vincent](discordapp.com/users/VincentDavis#3484)
"""
teams = team_list()
df = teams['teams_df']
df.sort_values('riders', ascending=False, inplace=True)
st.dataframe(teams['teams_df'])
st.write(f"Total teams: {len(df)}")

overlaps = team_overlap_by_rider(df, include=None, depth=20)
dt = overlaps['team_overlap']
st.write(f"Only inspecting the largest 5 teams at this time")
st.write(f"Only listing riders on more then 1 team")
st.dataframe(dt.loc[dt['team_count'] > 1])
