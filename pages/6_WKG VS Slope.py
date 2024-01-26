import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.optimize import fsolve

from dynamics import Dynamics

"""
## Comparing the tradeoff between riders of different size with drafting and climbing.
Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

## Senerios:
### Compare tradeoff between w/kg as slope goes from -30% to +30%
- Implemented

### Two rider race without drafting
- Not implemented

### two rider race with drafting
- Not implemented:	

#### Definitions:
- Altitude [m]:	0 m (starting altitude)
- Temperature [°C]: 20.0 °C
- Windspeed [m/s]: Fixed to 0 for no wind	0.0 m/s
- Wind Angle [°] 0.0 ° (0=Headwind, 90=Crosswind, 180=Tailwind)
- Drag Coefficent [Cd]:	0.800
- Drivetrain Losses [%]	4 %
- Coefficient of rolling resistance	0.005
- Drafting effect: This is the percentage reduction of Air Drag. 0% is no drafting, 100% is perfect drafting.
- Weight [kg]	70.0 kg Default rider weight
- Frontal Area [m²]	0.565 m² (climbing) Should scale for rider weight using Area(volume) of a cylinder.
- Bike and Accessories Weight [kg]	10.0 kg

#### Future work:
- Consider Temperature as it related to rider size and the ability to dissipate heat. Need Reference.
- Add better Frontal Area calculations
- Add TSS, IF and other metrics and limited related to riders ftp.
- add Wind Direction
- ...

#### Sources
- Frontal Area: https://www.researchgate.net/publication/23986705_New_Method_to_Estimate_the_Cycling_Frontal_Area or https://www.researchgate.net/figure/The-five-cyclist-positions-with-frontal-area-A-and-definition-and-values-of-1-sagittal_fig2_331366310
- Drag Coefficient: https://link.springer.com/article/10.1007/s12283-017-0234-1
- Drivetrain Losses: https://core.ac.uk/download/pdf/29823669.pdf
- Coefficient of rolling resistance: https://www.sciencedirect.com/science/article/pii/S0165232X2100063X
"""

st.subheader("Tradeoff between riders from -30% to +30% slope")

with st.form("Tradeoff_Form"):
    st.header("Environmental settings, You can leave these unchanged.")
    setup_cols = st.columns(3)
    temperature = setup_cols[0].number_input(label="Temperature [°C]", value=20, min_value=0, max_value=50, step=1)
    altitude = setup_cols[1].number_input(label="Starting Alt. [m]", value=0, min_value=0, max_value=5000, step=100)
    wind_speed = setup_cols[2].number_input(label="Wind Speed [m/s]", value=0, min_value=0, max_value=50, step=1)
    wind_direction = setup_cols[0].number_input(
        label="Wind Direction 0-259 [°]", value=0, min_value=0, max_value=359, step=1
    )
    drag_coefficient = setup_cols[1].number_input(
        label="Drag Coefficent[Cd]", value=0.8, min_value=0.5, max_value=1.0, step=0.1
    )
    drivetrain_loss = setup_cols[2].number_input(
        label="Drivetrain Losses [%]", value=4.0, min_value=0.0, max_value=10.0, step=0.1
    )
    rolling_resistance = setup_cols[0].number_input(
        label="Coefficient of rolling resistance", value=0.005, min_value=0.000, max_value=0.05, step=0.001
    )
    frontal_area_base = setup_cols[1].number_input(
        label="Frontal Area base: [m²]", value=0.423, min_value=0.0, max_value=1.0, step=0.01
    )

    r1_cols = st.columns(2)
    r1_cols[0].subheader("Rider 1")
    power_1 = r1_cols[0].number_input(label="Power [w]", value=250, min_value=100, max_value=1000, step=1, key="ftp1")
    kg_1 = r1_cols[0].number_input(
        label="Weight in [kg]", value=60.0, min_value=0.0, max_value=300.0, step=0.1, key="kg1"
    )
    height_1 = r1_cols[0].number_input(
        label="Height in [cm]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="height1"
    )
    bike_1 = r1_cols[0].number_input(
        label="Bike Weight in kg", value=10.0, min_value=0.0, max_value=20.0, step=0.1, key="bike1"
    )
    r1_cols[0].text("Leave at zero to automatically estimate Frontal Area [m²]")
    front_area_1 = r1_cols[0].number_input(
        label="Frontal Area [m²]", value=0.423, min_value=0.0, max_value=1.0, key="front_area1"
    )

    r1_cols[1].subheader("Rider 2")
    power_2 = r1_cols[1].number_input(label="Power [w]", value=300, min_value=100, max_value=1000, step=1, key="ftp2")
    kg_2 = r1_cols[1].number_input(
        label="Weight in [kg]", value=75.0, min_value=0.0, max_value=300.0, step=0.1, key="kg2"
    )
    height_2 = r1_cols[1].number_input(
        label="Height in [cm]", value=180.0, min_value=100.0, max_value=250.0, step=0.1, key="height2"
    )
    bike_2 = r1_cols[1].number_input(
        label="Bike Weight in kg", value=10.0, min_value=0.0, max_value=20.0, step=0.1, key="bike2"
    )
    r1_cols[1].text("Leave at zero to automatically estimate Frontal Area [m²]")
    front_area_2 = r1_cols[1].number_input(
        label="Frontal Area [m²]", value=0.423, min_value=0.0, max_value=1.0, step=0.01, key="front_area2"
    )

    submit_button = st.form_submit_button(label="Submit")


if submit_button:
    with st.spinner("Processing..."):
        st.write("Rider 1")
        rd1 = Dynamics(
            kg=kg_1,
            power=power_1,
            bike_kg=bike_1,
            height=height_1,
            frontal_area=front_area_1,
            # slope
            altitude=altitude,
            temperature=temperature,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            drag_coefficient=drag_coefficient,
            rolling_resistance=rolling_resistance,
            drivetrain_loss=drivetrain_loss,
        )
        rd2 = Dynamics(
            kg=kg_2,
            power=power_2,
            bike_kg=bike_2,
            height=height_2,
            frontal_area=front_area_2,
            # slope
            altitude=altitude,
            temperature=temperature,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            drag_coefficient=drag_coefficient,
            rolling_resistance=rolling_resistance,
            drivetrain_loss=drivetrain_loss,
        )

        points = []
        # print("#####")
        for slope in range(-20, 21):
            rd1.slope = slope / 100
            rd2.slope = slope / 100
            r1_speed = fsolve(rd1.calc_speed, 20)[0]
            r2_speed = fsolve(rd2.calc_speed, 20)[0]
            points.append([slope, r1_speed, r2_speed])
        df = pd.DataFrame(points, columns=["slope", "speed_rider_1", "speed_rider_2"])
        st.dataframe(df)

        plot1 = px.line(
            df, x="slope", y=["speed_rider_1", "speed_rider_2"], labels={"value": "Speed kph"}, title="slope vs speed"
        )
        st.plotly_chart(plot1, theme="streamlit", use_container_width=True)
