import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.optimize import fsolve

from dynamics import Dynamics, estimate_frontal_area

"""
## Comparing the tradeoff between riders of different size with drafting and climbing.
Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

## Scenarios:
### (1) WKG vs. Slope.
- Two riders of different size and power output.
- Shows the performance (speed) differance between the two riders on a given slope.

### (2) Two riders race without competitive drafting.
- Define course Each segment can be 0km in length
    1. Segment 1 [km]
    2. Segment 1 grade [%] (negative to decend)
    3. segment 2 [km]
    4. segment 2 grade [%] (negative to decend)
    5. segment 3 [km]
    6. segment 3 grade [%] (negative to decend)
    7. segment 4 [km]
    8. segment 4 grade [%] (negative to decend)
    9. segment 5 [km]
    10. segment 5 grade [%] (negative to decend)
- If you set the drafting effect > 0, this is like assuming the rider is drafting another rider.
- This is a static model, ignores energy to change speed
- The speed is calculated every 1 meter.
- Calculated speed is used to calculate the time to travel the next meter.
- max total distance is 100km

### (2) Two riders race with competitive drafting.
- Not implemented:	

#### Definitions:
- Altitude [m]:	0 m (starting altitude)
- Temperature [°C]: 20.0 °C
- Windspeed [m/s]: Fixed to 0 for no wind	0.0 m/s
- Wind Angle [°] 0.0 ° (0=Headwind, 90=Crosswind, 180=Tailwind)
- Drag Coefficient [Cd]:	0.800
- Drivetrain Losses [%]	4 %
- Coefficient of rolling resistance	0.005
- Drafting effect: Air_drag_watts * (1-10/100) for 10% drafting
- Weight [kg]	70.0 kg Default rider weight
- Frontal Area [m²]	0.565 m² (climbing): Estimate = height * pi * r^2 with r = 0.006894270128795239*(weight/height).
- Bike and Accessories Weight [kg]	10.0 kg

#### Future work:
- Consider Temperature as it related to rider size and the ability to dissipate heat. Need Reference.
- Add TSS, IF and other metrics and limited related to riders ftp.
- add Wind Direction
- ...

#### Sources
- Frontal Area:
  1. [New_Method_to_Estimate_the_Cycling_Frontal_Area](https://www.researchgate.net/publication/23986705_New_Method_to_Estimate_the_Cycling_Frontal_Area)
  2. [five-cyclist-positions-with-frontal-area](https://www.researchgate.net/figure/The-five-cyclist-positions-with-frontal-area-A-and-definition-and-values-of-1-sagittal_fig2_331366310)
- Drag Coefficient: https://link.springer.com/article/10.1007/s12283-017-0234-1
- Drivetrain Losses: https://core.ac.uk/download/pdf/29823669.pdf
- Coefficient of rolling resistance: https://www.sciencedirect.com/science/article/pii/S0165232X2100063X
"""

st.subheader("Tradeoff between riders from -30% to +30% slope")

with st.form("Main Form"):
    st.markdown("### Choose Scenario")
    scenario = st.selectbox("Scenario", options=["1", "2"], key="scenario")
    st.markdown("### Environmental settings")
    st.markdown("- Required for all Scenarios")

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
    start_slope = setup_cols[1].number_input(
        label="Starting Slope [%]", value=-10, min_value=-30, max_value=29, step=1, key="start_slope"
    )
    end_slope = setup_cols[2].number_input(
        label="Starting Slope [%]", value=10, min_value=-30, max_value=30, step=1, key="end_slope"
    )
    est_front_method = setup_cols[0].selectbox(
        label="Estimated Frontal area type (used if rider FA is 0)", options=["Standard", "Aero"], key="est_front_type"
    )

    ############ Scenarios ############
    st.markdown("### Scenario: 2 settings")
    cr_cols = st.columns(2)
    cr_cols[0].markdown("##### Segment")
    cr_cols[1].markdown("##### length [km]")
    seg_1 = cr_cols[0].number_input(label="length [km]", value=10, min_value=0, max_value=100, step=1, key="cr1_len")
    seg_1_slope = cr_cols[1].number_input(
        label="slope [%]", value=0, min_value=-30, max_value=30, step=1, key="cr1_slope"
    )
    seg_2 = cr_cols[0].number_input(label="length [km]", value=10, min_value=0, max_value=100, step=1, key="cr2_len")
    seg_2_slope = cr_cols[1].number_input(
        label="slope [%]", value=10, min_value=-30, max_value=30, step=1, key="cr2_slope"
    )
    seg_3 = cr_cols[0].number_input(label="length [km]", value=8, min_value=0, max_value=100, step=1, key="cr3_len")
    seg_3_slope = cr_cols[1].number_input(
        label="slope [%]", value=-10, min_value=-30, max_value=30, step=1, key="cr3_slope"
    )
    seg_4 = cr_cols[0].number_input(label="length [km]", value=10, min_value=0, max_value=100, step=1, key="cr4_len")
    seg_4_slope = cr_cols[1].number_input(
        label="slope [%]", value=0, min_value=-30, max_value=30, step=1, key="cr4_slope"
    )
    seg_5 = cr_cols[0].number_input(label="length [km]", value=2, min_value=0, max_value=100, step=1, key="cr5_len")
    seg_5_slope = cr_cols[1].number_input(
        label="slope [%]", value=5, min_value=-30, max_value=30, step=1, key="cr5_slope"
    )
    st.markdown("### Setup Riders")
    st.markdown("#### Required for all scenarios, start with defaults")
    ############ Rider 1 ############
    r1_cols = st.columns(2)
    r1_cols[0].subheader("Rider 1")
    r1_cols[0].markdown("Used for scenario (1) and (2)")
    power_1 = r1_cols[0].number_input(label="Power [w]", value=250, min_value=100, max_value=1000, step=1, key="power1")
    r1_cols[0].markdown("Used for scenario (2) to calculate TSS, NP, IF, etc.")
    ftp_1 = r1_cols[0].number_input(
        label="FTP in [watts]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="ftp1"
    )
    kg_1 = r1_cols[0].number_input(
        label="Weight in [kg]", value=60.0, min_value=0.0, max_value=300.0, step=0.1, key="kg1"
    )
    height_1 = r1_cols[0].number_input(
        label="Height in [cm]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="height1"
    )
    bike_1 = r1_cols[0].number_input(
        label="Bike Weight in kg", value=10.0, min_value=0.0, max_value=20.0, step=0.1, key="bike1"
    )
    r1_cols[0].text("Leave zero to automatically estimate Frontal Area [m²]")
    front_area_1 = r1_cols[0].number_input(
        label="Frontal Area [m²]", value=0.423, min_value=0.0, max_value=1.0, key="front_area1"
    )
    drafting_1 = r1_cols[0].number_input(
        label="Assume or enable drafting [%]", value=0, min_value=0, max_value=100, step=1, key="drafting_1"
    )
    #### Rider 2 ####
    r1_cols[1].subheader("Rider 2")
    r1_cols[1].markdown("Used for scenario (1) and (2)")
    power_2 = r1_cols[1].number_input(label="Power [w]", value=300, min_value=100, max_value=1000, step=1, key="power2")
    r1_cols[1].markdown("Used for scenario (2) to calculate TSS, NP, IF, etc.")
    ftp_2 = r1_cols[1].number_input(
        label="FTP in [watts]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="ftp2"
    )
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
        label="Frontal Area [m²]", value=0.46, min_value=0.0, max_value=1.0, step=0.01, key="front_area2"
    )
    drafting_2 = r1_cols[1].number_input(
        label="Assume or enable drafting [%]", value=0, min_value=0, max_value=100, step=1, key="drafting_2"
    )

    submit_button = st.form_submit_button(label="Submit")

############################################################################################################


if submit_button:
    with st.spinner("Processing..."):
        if front_area_1 == 0:
            tt = est_front_method == "Aero"
            front_area_1 = estimate_frontal_area(kg_1, height_1, tt)

        if front_area_2 == 0:
            tt = est_front_method == "Aero"
            front_area_2 = estimate_frontal_area(kg_1, height_1, tt)
        if scenario == "2":
            if sum([seg_1, seg_2, seg_3, seg_4, seg_5]) > 100:
                st.error("Total distance is greater than 100km, fix and try again.")
                st.stop()

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
            cd=drag_coefficient,
            crr=rolling_resistance,
            dt_loss=drivetrain_loss,
            drafting_effect=drafting_1,
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
            cd=drag_coefficient,
            crr=rolling_resistance,
            dt_loss=drivetrain_loss,
            drafting_effect=drafting_2,
        )

        if scenario == "1":
            st.markdown("### Senario 1 Results")
            st.markdown("#### Data")
            points = []
            # print("#####")
            for slope in range(start_slope, end_slope + 1):
                rd1.slope = slope / 100
                rd2.slope = slope / 100
                r1_speed = fsolve(rd1.calc_speed, 20)[0]
                r2_speed = fsolve(rd2.calc_speed, 20)[0]
                points.append([slope, r1_speed, r2_speed])
            column_names = ["slope", f"R1: {round(power_1/kg_1, 1)}wkg (kph)", f"R2 {round(power_2/kg_2, 1)}wkg (kph)"]
            df = pd.DataFrame(points, columns=column_names)
            for c in column_names[1:]:
                df[c] = df[c] * 3.6
            df["R1 - R2 (kph)"] = df[column_names[1]] - df[column_names[2]]
            st.dataframe(df)

            plot1 = px.line(
                df,
                x="slope",
                y=[column_names[1], column_names[2]],
                labels={"value": "Speed kph"},
                title="SLOPE VS SPEED",
            )
            st.plotly_chart(plot1, theme="streamlit", use_container_width=True)

            plot1 = px.line(
                df,
                x="slope",
                y="R1 - R2 (kph)",
                labels={"Rider 1 - Rider 2": "Rider 1 - Rider 2 kph"},
                title="SLOPE VS Difference in Speed",
            )
            print(plot1)
            st.plotly_chart(plot1, theme="streamlit", use_container_width=True)
        elif scenario == "2":
            st.markdown("### Scenario 2 Results")
            df_1 = rd1.race_course(
                seg_1, seg_1_slope, seg_2, seg_2_slope, seg_3, seg_3_slope, seg_4, seg_4_slope, seg_5, seg_5_slope
            )
            st.markdown("rider 1 computed")
            df_2 = rd2.race_course(
                seg_1, seg_1_slope, seg_2, seg_2_slope, seg_3, seg_3_slope, seg_4, seg_4_slope, seg_5, seg_5_slope
            )
            st.markdown("rider 2 computed")

            df_2.drop(columns=["segment", "slope", "distance"], inplace=True)
            df_2.rename(columns={c: f"{c}_2" for c in df_2.columns}, inplace=True)
            df = pd.concat([df_1, df_2], axis=1)
            # st.markdown("results merged")
            # df.rename({"slope_1": "slope"}, axis=1, inplace=True)
            # df.drop(columns=["slope_2", "segment_point_1", "segment_point_2"], inplace=True)
            df["time_diff"] = df["segment_time"] - df["segment_time_2"]
            df["speed_diff"] = df["speed"] - df["speed_2"]
            df["gap"] = df["elapsed_time"] - df["elapsed_time_2"]
            st.dataframe(df)

            plot1 = px.line(
                df,
                x="distance",
                y="gap",
                labels={"gap": "Rider 1 - Rider 2: Gap [s]", "distance": "Distance [km]"},
                title="Rider 1 vs Rider 2",
                height=800,
            )

            st.plotly_chart(plot1, theme="streamlit", use_container_width=True)
