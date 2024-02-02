"""
# PLACEHOLDER.

"""
#
# st.subheader("Tradeoff between riders from -30% to +30% slope")
#
# with st.form("Main Form"):
#     st.markdown("### Choose Scenario")
#     scenario = st.selectbox("Scenario", options=["1", "2"], key="scenario")
#     st.markdown("### Environmental settings")
#     st.markdown("- Required for all Scenarios")
#
#     setup_cols = st.columns(3)
#     temperature = setup_cols[0].number_input(label="Temperature [°C]", value=20, min_value=0, max_value=50, step=1)
#     altitude = setup_cols[1].number_input(label="Starting Alt. [m]", value=0, min_value=0, max_value=5000, step=100)
#     wind_speed = setup_cols[2].number_input(label="Wind Speed [m/s]", value=0, min_value=0, max_value=50, step=1)
#     wind_direction = setup_cols[0].number_input(
#         label="Wind Direction 0-259 [°]", value=0, min_value=0, max_value=359, step=1
#     )
#     drag_coefficient = setup_cols[1].number_input(
#         label="Drag Coefficent[Cd]", value=0.8, min_value=0.5, max_value=1.0, step=0.1
#     )
#     drivetrain_loss = setup_cols[2].number_input(
#         label="Drivetrain Losses [%]", value=4.0, min_value=0.0, max_value=10.0, step=0.1
#     )
#     rolling_resistance = setup_cols[0].number_input(
#         label="Coefficient of rolling resistance", value=0.005, min_value=0.000, max_value=0.05, step=0.001
#     )
#     start_slope = setup_cols[1].number_input(
#         label="Starting Slope [%]", value=-10, min_value=-30, max_value=29, step=1, key="start_slope"
#     )
#     end_slope = setup_cols[2].number_input(
#         label="Starting Slope [%]", value=10, min_value=-30, max_value=30, step=1, key="end_slope"
#     )
#     est_front_method = setup_cols[0].selectbox(
#         label="Estimated Frontal area type (used if rider FA is 0)", options=["Standard", "Aero"], key="est_front_type"
#     )
#
#     ############ Scenarios ############
#     st.markdown("### Scenario: 2 settings")
#     cr_cols = st.columns(2)
#     cr_cols[0].markdown("##### Segment")
#     cr_cols[1].markdown("##### length [km]")
#     seg_1 = cr_cols[0].number_input(label="length [km]", value=10, min_value=0, max_value=100, step=1, key="cr1_len")
#     seg_1_slope = cr_cols[1].number_input(
#         label="slope [%]", value=0, min_value=-30, max_value=30, step=1, key="cr1_slope"
#     )
#     seg_2 = cr_cols[0].number_input(label="length [km]", value=10, min_value=0, max_value=100, step=1, key="cr2_len")
#     seg_2_slope = cr_cols[1].number_input(
#         label="slope [%]", value=10, min_value=-30, max_value=30, step=1, key="cr2_slope"
#     )
#     seg_3 = cr_cols[0].number_input(label="length [km]", value=8, min_value=0, max_value=100, step=1, key="cr3_len")
#     seg_3_slope = cr_cols[1].number_input(
#         label="slope [%]", value=-10, min_value=-30, max_value=30, step=1, key="cr3_slope"
#     )
#     seg_4 = cr_cols[0].number_input(label="length [km]", value=10, min_value=0, max_value=100, step=1, key="cr4_len")
#     seg_4_slope = cr_cols[1].number_input(
#         label="slope [%]", value=0, min_value=-30, max_value=30, step=1, key="cr4_slope"
#     )
#     seg_5 = cr_cols[0].number_input(label="length [km]", value=2, min_value=0, max_value=100, step=1, key="cr5_len")
#     seg_5_slope = cr_cols[1].number_input(
#         label="slope [%]", value=5, min_value=-30, max_value=30, step=1, key="cr5_slope"
#     )
#     st.markdown("### Setup Riders")
#     st.markdown("#### Required for all scenarios, start with defaults")
#     ############ Rider 1 ############
#     r1_cols = st.columns(2)
#     r1_cols[0].subheader("Rider 1")
#     r1_cols[0].markdown("Used for scenario (1) and (2)")
#     power_1 = r1_cols[0].number_input(label="Power [w]", value=250, min_value=100, max_value=1000, step=1, key="power1")
#     r1_cols[0].markdown("Used for scenario (2) to calculate TSS, NP, IF, etc.")
#     ftp_1 = r1_cols[0].number_input(
#         label="FTP in [watts]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="ftp1"
#     )
#     kg_1 = r1_cols[0].number_input(
#         label="Weight in [kg]", value=60.0, min_value=0.0, max_value=300.0, step=0.1, key="kg1"
#     )
#     height_1 = r1_cols[0].number_input(
#         label="Height in [cm]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="height1"
#     )
#     bike_1 = r1_cols[0].number_input(
#         label="Bike Weight in kg", value=10.0, min_value=0.0, max_value=20.0, step=0.1, key="bike1"
#     )
#     r1_cols[0].text("Leave zero to automatically estimate Frontal Area [m²]")
#     front_area_1 = r1_cols[0].number_input(
#         label="Frontal Area [m²]", value=0.423, min_value=0.0, max_value=1.0, key="front_area1"
#     )
#     drafting_1 = r1_cols[0].number_input(
#         label="Assume or enable drafting [%]", value=0, min_value=0, max_value=100, step=1, key="drafting_1"
#     )
#     #### Rider 2 ####
#     r1_cols[1].subheader("Rider 2")
#     r1_cols[1].markdown("Used for scenario (1) and (2)")
#     power_2 = r1_cols[1].number_input(label="Power [w]", value=300, min_value=100, max_value=1000, step=1, key="power2")
#     r1_cols[1].markdown("Used for scenario (2) to calculate TSS, NP, IF, etc.")
#     ftp_2 = r1_cols[1].number_input(
#         label="FTP in [watts]", value=175.0, min_value=100.0, max_value=250.0, step=0.1, key="ftp2"
#     )
#     kg_2 = r1_cols[1].number_input(
#         label="Weight in [kg]", value=75.0, min_value=0.0, max_value=300.0, step=0.1, key="kg2"
#     )
#     height_2 = r1_cols[1].number_input(
#         label="Height in [cm]", value=180.0, min_value=100.0, max_value=250.0, step=0.1, key="height2"
#     )
#     bike_2 = r1_cols[1].number_input(
#         label="Bike Weight in kg", value=10.0, min_value=0.0, max_value=20.0, step=0.1, key="bike2"
#     )
#     r1_cols[1].text("Leave at zero to automatically estimate Frontal Area [m²]")
#     front_area_2 = r1_cols[1].number_input(
#         label="Frontal Area [m²]", value=0.46, min_value=0.0, max_value=1.0, step=0.01, key="front_area2"
#     )
#     drafting_2 = r1_cols[1].number_input(
#         label="Assume or enable drafting [%]", value=0, min_value=0, max_value=100, step=1, key="drafting_2"
#     )
#
#     submit_button = st.form_submit_button(label="Submit")
#
# ############################################################################################################
#
#
# if submit_button:
#     with st.spinner("Processing..."):
#         if front_area_1 == 0:
#             tt = est_front_method == "Aero"
#             front_area_1 = estimate_frontal_area(kg_1, height_1, tt)
#
#         if front_area_2 == 0:
#             tt = est_front_method == "Aero"
#             front_area_2 = estimate_frontal_area(kg_1, height_1, tt)
#         if scenario == "2":
#             if sum([seg_1, seg_2, seg_3, seg_4, seg_5]) > 100:
#                 st.error("Total distance is greater than 100km, fix and try again.")
#                 st.stop()
#
#         rd1 = Dynamics(
#             kg=kg_1,
#             power=power_1,
#             bike_kg=bike_1,
#             height=height_1,
#             frontal_area=front_area_1,
#             # slope
#             altitude=altitude,
#             temperature=temperature,
#             wind_speed=wind_speed,
#             wind_direction=wind_direction,
#             drag_coefficient=drag_coefficient,
#             rolling_resistance=rolling_resistance,
#             drivetrain_loss=drivetrain_loss,
#             drafting_effect=drafting_1,
#         )
#         rd2 = Dynamics(
#             kg=kg_2,
#             power=power_2,
#             bike_kg=bike_2,
#             height=height_2,
#             frontal_area=front_area_2,
#             # slope
#             altitude=altitude,
#             temperature=temperature,
#             wind_speed=wind_speed,
#             wind_direction=wind_direction,
#             drag_coefficient=drag_coefficient,
#             rolling_resistance=rolling_resistance,
#             drivetrain_loss=drivetrain_loss,
#             drafting_effect=drafting_2,
#         )
#
#         if scenario == "1":
#             st.markdown("### Senario 1 Results")
#             st.markdown("#### Data")
#             points = []
#             # print("#####")
#             for slope in range(start_slope, end_slope + 1):
#                 rd1.slope = slope / 100
#                 rd2.slope = slope / 100
#                 r1_speed = fsolve(rd1.calc_speed, 20)[0]
#                 r2_speed = fsolve(rd2.calc_speed, 20)[0]
#                 points.append([slope, r1_speed, r2_speed])
#             column_names = ["slope", f"R1: {round(power_1/kg_1, 1)}wkg (kph)", f"R2 {round(power_2/kg_2, 1)}wkg (kph)"]
#             df = pd.DataFrame(points, columns=column_names)
#             for c in column_names[1:]:
#                 df[c] = df[c] * 3.6
#             df["R1 - R2 (kph)"] = df[column_names[1]] - df[column_names[2]]
#             st.dataframe(df)
#
#             plot1 = px.line(
#                 df,
#                 x="slope",
#                 y=[column_names[1], column_names[2]],
#                 labels={"value": "Speed kph"},
#                 title="SLOPE VS SPEED",
#             )
#             st.plotly_chart(plot1, theme="streamlit", use_container_width=True)
#
#             plot1 = px.line(
#                 df,
#                 x="slope",
#                 y="R1 - R2 (kph)",
#                 labels={"Rider 1 - Rider 2": "Rider 1 - Rider 2 kph"},
#                 title="SLOPE VS Difference in Speed",
#             )
#             print(plot1)
#             st.plotly_chart(plot1, theme="streamlit", use_container_width=True)
#         elif scenario == "2":
#             st.markdown("### Scenario 2 Results")
#             df_1 = rd1.race_course(
#                 seg_1, seg_1_slope, seg_2, seg_2_slope, seg_3, seg_3_slope, seg_4, seg_4_slope, seg_5, seg_5_slope
#             )
#             st.markdown("rider 1 computed")
#             df_2 = rd2.race_course(
#                 seg_1, seg_1_slope, seg_2, seg_2_slope, seg_3, seg_3_slope, seg_4, seg_4_slope, seg_5, seg_5_slope
#             )
#             st.markdown("rider 2 computed")
#
#             df_2.drop(columns=["segment", "slope", "distance"], inplace=True)
#             df_2.rename(columns={c: f"{c}_2" for c in df_2.columns}, inplace=True)
#             df = pd.concat([df_1, df_2], axis=1)
#             # st.markdown("results merged")
#             # df.rename({"slope_1": "slope"}, axis=1, inplace=True)
#             # df.drop(columns=["slope_2", "segment_point_1", "segment_point_2"], inplace=True)
#             df["time_diff"] = df["segment_time"] - df["segment_time_2"]
#             df["speed_diff"] = df["speed"] - df["speed_2"]
#             df["gap"] = df["elapsed_time"] - df["elapsed_time_2"]
#             st.dataframe(df)
#
#             plot1 = px.line(
#                 df,
#                 x="distance",
#                 y="gap",
#                 labels={"gap": "Rider 1 - Rider 2: Gap [s]", "distance": "Distance [km]"},
#                 title="Rider 1 vs Rider 2",
#                 height=800,
#             )
#
#             st.plotly_chart(plot1, theme="streamlit", use_container_width=True)
