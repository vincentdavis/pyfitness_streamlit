import json

import streamlit as st

from zp import zwiftprofile

"""# Get your zwift profile data
This is a work in progress. Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)

You can also contact me on discord: [Vincent](discordapp.com/users/VincentDavis#3484

Username and password are not stored, they are sent directly to Zwift to get your profile data as a JSON file."""

c1, c2 = st.columns(2)
with c1:
    username = st.text_input("Username")
with c2:
    password = st.text_input("Password", type="password")

if len(username)>0 and (password is not None):
    st.write(f"Getting {username} Zwift Profile, this can be a bit slow")
    profile = zwiftprofile(username, password)
    st.download_button(label="Download JSON file", data=json.dumps(profile, indent=2), file_name="zwift_profile.json",
                       mime='application/json')
    st.write(profile)
