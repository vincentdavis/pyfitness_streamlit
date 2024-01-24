import json

import pandas as pd
import streamlit as st
from pyfitness.load_data import fit2df

from zp import event_results

"""### This page has been moved to [ZwiftToCSV](https://zwifttocsv.streamlit.app) with more data and features.

You can also contact me on discord: [vincent.davis](discordapp.com/users/Vincent.Davis)

Instantanious Intensity Factor (IIF) is used to simulate instantanious normilized power. It is calculated by (power/ftp)^(IFP)

For example, IF^4 

"""

with st.form("Efficiency Analisys form"):
    st.text("If uploading a csv file it should have the standard columns namees that would be found in a FIT file.")
    fit_buffer = st.file_uploader("Upload a FIT or csv file", type=["fit", "FIT, csv"], key="fit_file")
    ftp = st.number_input(label="Your FTP", value=250, key="ftp")
    kg = st.number_input(label="Your weight in kg", value=70, key="kg")
    ifp = st.number_input(label="Intesity factor ^ power (IFP)", value=4, key="ifp")
    submit_button = st.form_submit_button(label="Submit")


if submit_button:
    with st.spinner("Processing..."):
        fit_file = fit_buffer.getbuffer()
        df = fit2df(fit_file)
        df["IIF"] = df["power"] * (df["power"]/ftp)**ifp
        df["IFF_force"] = df['distance']/df["IIF"]
        df["IFF_power"] = df['speed'] / df["IIF"]
    st.dataframe(df[['distance', 'speed', "IFF_force", "IFF_power"]])

