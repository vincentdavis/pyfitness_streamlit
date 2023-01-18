import json

import streamlit as st

from zp import ZwiftLogin

st.write("## Get ZwiftPower data")
st.write("Enter the api url, see browser developer tools")
api_url = st.text_input("Enter zwift api url",
                        value="https://zwiftpower.com/cache3/results/3421716_view.json?_=1673971594335")
if api_url is not None:
    st.write("Getting ZwiftPower data, wait for it....")
    z = ZwiftLogin()
    res = z.get_request(viewurl=api_url)
    st.text(json.dumps(res, indent=2))
