from time import sleep
import streamlit as st
import numpy as np
import pandas as pd
from zp import team_list, team_members

st.title("ZP Team List")
""" # Teams and Riders
### New page, needs lots of work.
This is a new section, work in progress.
Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)

You can also contact me on discord: [Vincent](discordapp.com/users/VincentDavis#3484)
"""
teams = team_list()
df= teams['teams_df']
df['riders'] = df['riders'].apply(pd.to_numeric, errors = 'coerce')
# df.riders.replace('', np.NaN, inplace=True)
df.sort_values('riders', ascending=False, inplace=True)
st.dataframe(teams['teams_df'])
st.write(f"Total teams: {len(df)}")

riders: dict = {}
riders_teams: dict = {}
for t in df.iloc[0:10].to_dict('records'):
    st.write(f"Getting rider list for {t['tln']}")
    members = team_members(t['team_id'])
    st.write(f"- {t['tln']} as {len(members['members_df'])} members")
    for r in members['members_df'].to_dict('records'):
        if r['zwid'] not in riders.keys():
            riders[r['zwid']] = r
            riders_teams[r['zwid']] = {'zwid': r['zwid'], 'name': r['name'], 'teams': [t['tln']]}
        else:
            print(riders_teams[r['zwid']]['teams'])
            riders_teams[r['zwid']]['teams'].append(t['tln'])
    sleep(.5)

st.write(f"Only inspecting the largest 5 teams at this time")
st.write(f"Only listing riders on more then 1 team")
# for k, v in riders_teams.items():
#     if len(v['teams'])>1:
#         st.write(f"{k} {v['name']} is on these teams: {[t['tln'] for t in v['teams']]}")
dt = pd.DataFrame(riders_teams.values())
dt['team_count'] = dt.teams.apply(lambda x: len(x))
st.dataframe(dt.loc[dt['team_count'] > 1])






