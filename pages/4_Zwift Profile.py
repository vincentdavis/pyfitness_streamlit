import json

import streamlit as st

from zp import zwiftprofile

"""# Get your zwift profile data
Username and password are not stored, they are sent directly to Zwift to get your profile data as a JSON file."""
c1, c2 = st.columns(2)
with c1:
    username = st.text_input("Username", key="username")
with c2:
    password = st.text_input("Password", type="password", key="password")

if username is not None and password is not None:
    st.write("Getting Your Zwift Profile, this can be a bit slow")
    profile = zwiftprofile(username, password)
    st.download_button(label="Download JSON file", data=json.dumps(profile, indent=2), file_name="zwift_profile.json",
                       mime='application/json')
    st.write(profile)
