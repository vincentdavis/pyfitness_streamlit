import statistics

import plotly.express as px
import streamlit as st

from power_curve_area import power_area_calc

"""
## Power Curve Area
Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

This is a work in progress. Planninng to add FIT file upload next.

### Calculate the area under the power curve
- You can adjust the numbers (seconds and watts) to match your power curve
- It is recommended to use the second intervals below for comparing to others.
- The area units if wattsXseconds and convered to WattHrs
"""

with st.form(key="power_curve_area"):
    st.markdown("#### Rider Profile")
    kg = st.number_input("KG", min_value=1.0, max_value=500.0, value=75.0)
    c0, c1 = st.columns(2)
    c0.markdown("#### Seconds")
    x1 = c0.number_input("1", min_value=1, value=1)
    x2 = c0.number_input("2", min_value=1, value=5)
    x3 = c0.number_input("3", min_value=1, value=10)
    x4 = c0.number_input("4", min_value=1, value=30)
    x5 = c0.number_input("5", min_value=1, value=60)
    x6 = c0.number_input("6", min_value=1, value=120)
    x7 = c0.number_input("7", min_value=1, value=300)
    x8 = c0.number_input("8", min_value=1, value=600)
    x9 = c0.number_input("9", min_value=1, value=1200)
    x10 = c0.number_input("10", min_value=1, value=2600)
    c1.markdown("#### Watts")
    y1 = c1.number_input("1", min_value=1, max_value=5000, value=1000)
    y2 = c1.number_input("2", min_value=1, max_value=5000, value=900)
    y3 = c1.number_input("3", min_value=1, max_value=5000, value=850)
    y4 = c1.number_input("4", min_value=1, max_value=5000, value=650)
    y5 = c1.number_input("5", min_value=1, max_value=5000, value=400)
    y6 = c1.number_input("6", min_value=1, max_value=5000, value=300)
    y7 = c1.number_input("7", min_value=1, max_value=5000, value=275)
    y8 = c1.number_input("8", min_value=1, max_value=5000, value=250)
    y9 = c1.number_input("9", min_value=1, max_value=5000, value=245)
    y10 = c1.number_input("10", min_value=1, max_value=5000, value=240)
    submit = st.form_submit_button("Submit")

if submit:
    points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8), (x9, y9), (x10, y10)]
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

    fig1 = px.area(x=x, y=y_kg, labels={"x": "Seconds", "y": "Watts/kg"})
    fig1.add_annotation(
        text=f"{area / kg:.2f} WattsHrs/kg",
        x=statistics.mean(x),
        y=statistics.mean(y_kg),
        showarrow=False,
        font_size=14,
    )
    st.plotly_chart(fig1)
