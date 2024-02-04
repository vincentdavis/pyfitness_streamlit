import statistics

import pandas as pd
import plotly.express as px
import streamlit as st

from power_curve_area import power_area_calc

st.set_page_config(
    page_title="Critical Power area under curve",
    page_icon="\u1F6B2",
    layout="wide",
    initial_sidebar_state="auto",
)

"""
## Critical Power area under curve
Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

This is a work in progress. Planninng to add FIT file upload next.

### Calculate the area under the power curve
- You can adjust the numbers (seconds and watts) to match your power curve
- It is recommended to use the second intervals below for comparing to others.
- The area units if watts X seconds and converted to WattHrs
"""

with st.form(key="power_curve_area"):
    st.markdown("#### Rider Profile")
    kg = st.number_input("KG", min_value=1.0, max_value=500.0, value=75.0)
    st.markdown("##### From file or manual entry")
    st.markdown(
        "- If you have a CSV file, you can upload it below. File must have columns: (seconds, watts) or (x, y). Other columns are ignored"
    )
    st.markdown(
        "- You can get a power curve from zwiftpower.com here [ZwiftToCSV](https://zwifttocsv.streamlit.app/Profiles)"
    )
    zp_file = st.file_uploader(label="CSV file (over rides data below)", type=["csv"])
    st.markdown("- File upload options")
    wkg = st.radio("Uploaded file is watts or watts/kg", ["watts", "watts/kg"])
    st.markdown("If you choose yes, the file will be cropped to 20min and ftp will be esimated at 95% of 20min power")
    est_ftp = st.radio("Estimated FTP", ["Yes", "No"])
    end_at = st.number_input("End at (seconds) Default 20min", min_value=1, value=1200)
    st.markdown("#### Manual Entry")
    c0, c1 = st.columns(2)
    x1 = c0.number_input("seconds", min_value=1, value=1)
    x2 = c0.number_input("seconds", min_value=1, value=5)
    x3 = c0.number_input("seconds", min_value=1, value=10)
    x4 = c0.number_input("seconds", min_value=1, value=30)
    x5 = c0.number_input("seconds", min_value=1, value=60)
    x6 = c0.number_input("seconds", min_value=1, value=120)
    x7 = c0.number_input("seconds", min_value=1, value=300)
    x8 = c0.number_input("seconds", min_value=1, value=600)
    x9 = c0.number_input("seconds", min_value=1, value=1200)
    x10 = c0.number_input("(ftp)", min_value=1, value=3600)
    y1 = c1.number_input("Watts", min_value=1, max_value=5000, value=1000)
    y2 = c1.number_input("Watts", min_value=1, max_value=5000, value=900)
    y3 = c1.number_input("Watts", min_value=1, max_value=5000, value=850)
    y4 = c1.number_input("Watts", min_value=1, max_value=5000, value=650)
    y5 = c1.number_input("Watts", min_value=1, max_value=5000, value=400)
    y6 = c1.number_input("Watts", min_value=1, max_value=5000, value=300)
    y7 = c1.number_input("Watts", min_value=1, max_value=5000, value=275)
    y8 = c1.number_input("Watts", min_value=1, max_value=5000, value=250)
    y9 = c1.number_input("Watts", min_value=1, max_value=5000, value=245)
    y10 = c1.number_input("Watts", min_value=1, max_value=5000, value=240)
    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner("Processing..."):
        if zp_file:
            st.write("File uploaded, stadardizing column names")
            df = pd.read_csv(zp_file)
            df.rename(columns={c: c.lower() for c in df.columns}, inplace=True)
            df.rename(columns={"x": "seconds", "y": "watts"}, inplace=True)
            df.drop(columns=[c for c in df.columns if c not in ["seconds", "watts"]], inplace=True)
            if est_ftp == "Yes":
                df = df[df["seconds"] <= 1200]
                ftp = df["watts"].min() * 0.95
                st.write(f"Estimated FTP: {ftp:.2f}")
            df = df[df["seconds"] <= end_at]
            y_kg = []
            if wkg == "watts":
                df["watts/kg"] = df["watts"] / kg
                y_kg = (df["watts/kg"]).tolist()
            x = (df["seconds"]).tolist()
            y = (df["watts"]).tolist()
            if est_ftp == "Yes":
                x.append(3600)
                y.append(ftp)
                y_kg.append(ftp / kg)
            st.dataframe(df)

            points = list(zip(x, y, strict=False))
        else:
            points = [
                (x1, y1),
                (x2, y2),
                (x3, y3),
                (x4, y4),
                (x5, y5),
                (x6, y6),
                (x7, y7),
                (x8, y8),
                (x9, y9),
                (x10, y10),
            ]
            x = [x[0] for x in points]
            y = [y[1] for y in points]
            y_kg = [y[1] / kg for y in points]

        area = power_area_calc(points) / 3600
        st.write(f"{area:.2f} WattsHrs")
        st.write(f"{area / kg:.2f} WattsHrs/kg")

        fig0 = px.area(x=x, y=y, labels={"x": "Seconds", "y": "Watts"})
        fig0.add_annotation(
            text=f"Total Area: {area:.2f} WattsHrs",
            x=statistics.mean(x),
            y=statistics.mean(y),
            showarrow=False,
            font_size=14,
        )
        st.plotly_chart(fig0)
        if len(y_kg) == len(x):
            fig1 = px.area(x=x, y=y_kg, labels={"x": "Seconds", "y": "Watts/kg"})
            fig1.add_annotation(
                text=f"{area / kg:.2f} WattsHrs/kg",
                x=statistics.mean(x),
                y=statistics.mean(y_kg),
                showarrow=False,
                font_size=14,
            )
            st.plotly_chart(fig1)
