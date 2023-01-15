import pandas as pd
import streamlit as st
from pyfitness.load_data import fit2df
# from vam import FitVam
from vam2 import estimated_power
import plotly.express as px
import plotly.graph_objects as go

"""# Currently in development
Feel free to give it a try, but it is not ready for prime time yet.
"""
fit_file = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file1")
if fit_file is not None:
    df = fit2df(fit_file)
    df['seconds'] = pd.to_datetime(df.index).astype(int) / 10 ** 9
    df['seconds'] = (df['seconds'] - df['seconds'].min()).astype(int)


    st.write("#### Enter start and end times")
    st.write("The time values are used to select the segment of the ride to analyze")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        start_time = st.number_input('Start time sec:', min_value=0, max_value=df['seconds'].max(), value=0, step=1)
        end_time = st.number_input('End time sec:', min_value=0, max_value=df['seconds'].max(), value=df['seconds'].max(),
                                   step=1)
    with c2:
        rider_weight = st.number_input('Rider weight kg:', min_value=0, max_value=200, value=70, step=1)
        bike_weight = st.number_input('Bike weight kg:', min_value=5, max_value=30, value=10, step=1)
    with c3:
        wind_speed = st.number_input('Wind speed m/s:', min_value=0, max_value=50, value=0, step=1)
        wind_direction = st.number_input('Wind direction 0-360:', min_value=0, max_value=360, value=0, step=1)
    with c4:
        temperature = st.number_input('Temperature C:', min_value=-20, max_value=50, value=20, step=1)
        drag_coefficient = st.number_input('Drag coefficient:', min_value=0.0, max_value=1.0, value=0.8, step=0.05)
    with c5:
        frontal_area = st.number_input('Frontal area m^2:', min_value=0.0, max_value=2.0, value=0.565, step=0.1)
        rolling_resistance = st.number_input('Rolling resistance:', min_value=0.0, max_value=0.1, value=0.0005, step=0.0001)
        roll = st.number_input('VAM smooting:', min_value=0, max_value=30, value=5, step=1)

    fitted = estimated_power(df=df, start_time=start_time, end_time=end_time, rider_weight=rider_weight, bike_weight=bike_weight,
                wind_speed=wind_speed, wind_direction=wind_direction, temperature=temperature,
                drag_coefficient=drag_coefficient, frontal_area=frontal_area, rolling_resistance=rolling_resistance, roll=roll)

    filtered_df = fitted[(fitted['seconds'] >= start_time) & (fitted['seconds'] <= end_time)]
    filtered_df['roll_vam'] = filtered_df['vam'].rolling(roll).mean()
    altitude_fig = px.line(filtered_df, x='seconds', y='altitude', title='Altitude')
    with st.expander("See data fields and values"):
        st.write(filtered_df.head(50))
    rvam_fig = px.line(filtered_df, x='seconds', y='roll_vam', title='VAM')

    pvam_fig = go.Figure()
    pvam_fig.update_layout(
        title='Measured vs Estimated VAM Power')
    pvam_fig.add_trace(go.Scatter(name="Est VAM Power", x = filtered_df['seconds'], y = filtered_df['vam_power'].rolling(roll).mean()))
    pvam_fig.add_trace(go.Scatter(name="Power", x = filtered_df['seconds'], y = filtered_df['power'].rolling(roll).mean()))
    # pvam_fig = px.line(x = filtered_df['seconds'], y = filtered_df['vam_power'].rolling(roll).mean(), title='Est Power', label='Est Power')
    # pvam_fig.add_scatter(x=filtered_df['seconds'], y=filtered_df['power'].rolling(roll).mean(), mode='lines', name='Actual Power')

    st.plotly_chart(altitude_fig, theme="streamlit", use_container_width=True)
    st.write(f"#### {roll} sec VAM")
    st.plotly_chart(rvam_fig, theme="streamlit", use_container_width=True)
    st.plotly_chart(pvam_fig, theme="streamlit", use_container_width=True)

    comp_fig = go.Figure()
    comp_fig.add_trace(
        go.Scatter(name="Air", x=filtered_df['seconds'], y=filtered_df['air_drag'].rolling(roll).mean()))
    comp_fig.add_trace(go.Scatter(name="Climbing", x=filtered_df['seconds'], y=filtered_df['climbing_force'].rolling(roll).mean()))
    comp_fig.add_trace(go.Scatter(name="Rolling", x=filtered_df['seconds'], y=filtered_df['rolling_force'].rolling(roll).mean()))
    pvam_fig.update_layout(
        title='Components or Estimated VAM Power')
    st.plotly_chart(comp_fig, theme="streamlit", use_container_width=True)







