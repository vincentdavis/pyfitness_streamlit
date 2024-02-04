import numpy as np
import plotly.express as px
import streamlit as st
from pyfitness.load_data import fit2df

st.set_page_config(
    page_title="Efficiency Analysis",
    page_icon="\u1F6B2",
    layout="wide",
    initial_sidebar_state="auto",
)

"""
#### Efficiency Analysis.
I am defining Efficiency like miles per gallon, that is how far do you go for a given amount of power or physiological 
effort.

Next steps.
- Back out the power/energy that is going into climbing/descending (why I ask for rider weight)
- Based on total ride TSS, when where you above of below optimal (IF), or power
- Improve plots
- Export data option.
- Choose segments of the file rather then only the whole file.
- Compare two files.

Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

### 

### Definitions:
 - R_norm_power: Rolling 30 second normalized power, the ride mean of this is called "Normilized Power" (NP)
 - IF: Rolling Intensity Factor, R_norm_power / FTP
 - speed_power: Rolling 30 second speed / power
 - speed_np_power: Rolling 30 second speed / NP power
 - segment_power: Rolling 30 second distance / power
 - segment_np_power: Rolling 30 second distance / NP power
 - IF_speed: Rolling 30 second speed / IF
 - IF_segment: Rolling 30 second distance / IF

Each plot contains an course altitude line for reference.

"""

with st.form("Efficiency Analisys form"):
    st.text("If uploading a csv file it should have the standard columns names that would be found in a FIT file.")
    fit_buffer = st.file_uploader("Upload a FIT or csv file", type=["fit", "FIT, csv"])
    ftp = st.number_input(label="Your FTP", value=250.0, min_value=1.0, max_value=2000.0, step=0.5)
    kg = st.number_input(label="Your weight in kg", value=70.0, min_value=1.0, max_value=300.0, step=0.5)
    submit_button = st.form_submit_button(label="Submit")


if submit_button:
    with st.spinner("Processing..."):
        fit_file = fit_buffer.getbuffer()
        df = fit2df(fit_file)
        if "enhanced_speed" in df.columns:
            df["speed"] = df["enhanced_speed"]
        st.markdown("## Data columns")
        st.dataframe(df.columns)
        # Power
        df["power_4"] = df["power"] ** 4
        df["R_power"] = df["power"].rolling(30).mean()
        df["R_norm_power"] = df["power_4"].rolling(30).mean() ** 0.25
        # df["R_norm_power"] = (df["power_4"] / df["R_power_4"]) ** 0.25
        # pseed
        df["R_speed"] = df["speed"].rolling(30).mean()
        df["segment"] = df["distance"].diff()
        df["R_segment"] = df["segment"].rolling(30).mean()
        df["R_power"] = df["R_power"].fillna(0)

        df["IF"] = df["R_norm_power"] / ftp

        df["speed_power"] = df["R_speed"] * df["R_power"]
        df["speed_power"].replace(np.inf, np.nan, inplace=True)

        df["segment_power"] = df["R_segment"] * df["R_power"]
        df["speed_power"].replace(np.inf, np.nan, inplace=True)

        df["speed_np_power"] = df["R_speed"] * df["R_norm_power"]
        df["speed_np_power"].replace(np.inf, np.nan, inplace=True)

        df["segment_np_power"] = df["R_segment"] * df["R_norm_power"]
        df["speed_np_power"].replace(np.inf, np.nan, inplace=True)

        df["IF_segment"] = df["R_segment"] / df["IF"]
        df["IF_segment"].replace(np.inf, np.nan, inplace=True)
        df["IF_speed"] = df["R_speed"] / df["IF"]
        df["IF_speed"].replace(np.inf, np.nan, inplace=True)

        st.markdown("## Data stats")
        st.dataframe(
            df[
                [
                    "distance",
                    "speed",
                    "power",
                    "R_norm_power",
                    "speed_power",
                    "speed_np_power",
                    "segment_power",
                    "segment_np_power",
                    "IF",
                    "IF_speed",
                    "IF_segment",
                ]
            ].describe()
        )

    if "enhanced_altitude" in df.columns:
        df["altitude"] = df["enhanced_altitude"]
    df["altitude_10"] = df["altitude"] * 10

    # st.dataframe(df[["distance", "speed", "power", "R_norm_power", "IF", "IF_speed"]])

    efficiency_plot = px.line(df, x="distance", y=["speed_power", "altitude_10"], title="Speed per watt")
    st.plotly_chart(efficiency_plot, theme="streamlit", use_container_width=True)
    efficiency_plot = px.line(df, x="distance", y=["segment_power", "altitude_10"], title="Distance per watt")
    st.plotly_chart(efficiency_plot, theme="streamlit", use_container_width=True)

    efficiency_plot = px.line(df, x="distance", y=["speed_np_power", "altitude_10"], title="Speed per NP power")
    st.plotly_chart(efficiency_plot, theme="streamlit", use_container_width=True)
    efficiency_plot = px.line(df, x="distance", y=["segment_np_power", "altitude_10"], title="Distance per NP power")
    st.plotly_chart(efficiency_plot, theme="streamlit", use_container_width=True)

    efficiency_plot = px.line(df, x="distance", y=["IF_speed", "altitude"], title="Speed per (IF)")
    st.plotly_chart(efficiency_plot, theme="streamlit", use_container_width=True)
    efficiency_plot = px.line(df, x="distance", y=["IF_segment", "altitude"], title="Distance per (IF)")
    st.plotly_chart(efficiency_plot, theme="streamlit", use_container_width=True)
