
import streamlit as st

from zp_teams import team_riders

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
        assert id != '999999'
        int(id) >= 1
    except:
        st.write("Please enter a valid team id")
        raise
    st.write("Getting ZwiftPower data, wait for it.... Might take 5-10 seconds")
    result = team_riders(id)
    st.download_button(label="Download csv file",
                       data=result['team_riders_df'].to_csv(index=False).encode('utf-8'),
                       file_name=f"Team_ID_{id}.csv",
                       mime='text/csv')

    st.dataframe(result['team_riders_df'])


    # teams = team_list()
    # df = teams['teams_df']
    # df.sort_values('riders', ascending=False, inplace=True)
    # st.dataframe(teams['teams_df'])
    # st.write(f"Total teams: {len(df)}")
    #
    # overlaps = team_overlap_by_rider(df, include=None, depth=20)
    # dt = overlaps['team_overlap']
    # st.write(f"Only inspecting the largest 5 teams at this time")
    # st.write(f"Only listing riders on more then 1 team")
    # st.dataframe(dt.loc[dt['team_count'] > 1])
