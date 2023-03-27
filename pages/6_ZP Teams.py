
import streamlit as st

from zp_teams import team_riders, team_list, team_overlap_by_rider

st.title("ZP Team List")
""" # Teams and Riders
### New page, needs lots of work.
This is a new section, work in progress.
Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)

You can also contact me on discord: [Vincent](discordapp.com/users/VincentDavis#3484)
"""
st.markdown("**Export team list**")
st.write("Enter a full team url, such as https://zwiftpower.com/team.php?id=999999")
team_url = st.text_input(label="Team URL", placeholder="Team URL")
if 'https://zwiftpower.com/team.php?id=' in team_url:
    id = team_url.split("=")[-1]
    try:
        if id == '999999' or int(id) <= 1:
            st.write("Please enter a valid team id")
            raise ValueError(f"Please enter a valid team id: {id}")
    except:
        st.write(f"Please enter a valid team id: {id}")
        raise
    st.write("Getting ZwiftPower data, wait for it.... Might take 5-10 seconds")
    result = team_riders(id)
    st.download_button(label="Download csv file",
                       data=result['team_riders_df'].to_csv(index=False).encode('utf-8'),
                       file_name=f"Team_ID_{id}.csv",
                       mime='text/csv')

    st.dataframe(result['team_riders_df'])


st.markdown("#########")
st.markdown("**SHARED TEAM MEMBERS**")
st.write("Do you have members that are on other teams? This will compare your teams members with the 5 largest teams plus one additional team")
st.write("Your team full team url, such as https://zwiftpower.com/team.php?id=999999")
my_team_url = st.text_input(label="My Team URL", placeholder="My Team URL")
st.write("OPTIONAL: Other team full team url, such as https://zwiftpower.com/team.php?id=999999")
other_team_url = st.text_input(label="Other Team URL", placeholder="Other Team URL")
if st.button("Compare Teams") and 'https://zwiftpower.com/team.php?id=' in my_team_url:
    if 'https://zwiftpower.com/team.php?id=' in other_team_url:
        id2 = other_team_url.split("=")[-1]
        try:
            if id2 == '999999' or int(id2) <= 1:
                raise ValueError(f"Please enter a valid Other team id: {id2}")
        except:
            st.write(f"Please enter a valid Other team id: {id2}")
            raise
    else:
        id2 = None
    id1 = my_team_url.split("=")[-1]
    try:
        if id1 == '999999' or int(id1) <= 1:
            raise ValueError(f"Please enter a valid My team id: {id1}")
    except:
        st.write(f"Please enter a valid My team id:{id1}")
        raise

    st.write("Getting ZwiftPower data, wait for it.... Might take 15-30 seconds")
    teams = team_list()
    teams['teams_df'].sort_values('riders', ascending=False, inplace=True)
    with st.expander(f"View full list of {len(teams['teams_df'])} teams"):
        st.dataframe(teams['teams_df'])
    overlaps = team_overlap_by_rider(teams['teams_df'], include=[id1,id2], depth=5)
    dt = overlaps['team_overlap']
    st.write("Only inspecting the largest 5 teams at this time")
    st.write("Only listing riders on more then 1 team")
    st.dataframe(dt.loc[dt['team_count'] > 1])
