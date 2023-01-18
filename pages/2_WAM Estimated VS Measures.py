import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pyfitness.load_data import fit2df

# from vam import FitVam
from vam2 import estimated_power, max_climb, average_estimated_power

""" # Estimated powewr VS Measured power
### Currently in development
Feel free to give it a try, but it is not ready for prime time yet.
"""
st.write("This is a work in progress. Please report any issues on the [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)
fit_file = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file1")
if fit_file is not None:
    df = fit2df(fit_file)
    # add a seconds col that starts at 0
    df['seconds'] = pd.to_datetime(df.index).astype(int) / 10 ** 9
    df['seconds'] = (df['seconds'] - df['seconds'].min()).astype(int)
    ########
    st.write("#### Enter start and end time")
    st.write("The time values are used to select the segment of the ride to analyze")
    with st.expander("Largest climbs segments"):
        min5 = max_climb(df, 300)
        st.text(min5['text'])
        st.text(max_climb(df, 600)['text'])
        st.text(max_climb(df, 1200)['text'])
    st.write("Default max 5min climb")
    t1, t2 = st.columns(2)
    with t1:
        start_time = st.number_input('Start time sec:', min_value=0, max_value=int(df['seconds'].max()),
                                     value=int(min5['start_time']), step=1)
    with t2:
        end_time = st.number_input('End time sec:', min_value=0, max_value=int(df['seconds'].max()),
                                   value=int(min5['end_time']),
                                   step=1)
    df_filtered = df[(df['seconds'] >= start_time) & (df['seconds'] <= end_time)]
    altitude_fig = px.line(df_filtered, x='seconds', y='altitude', title='Altitude')
    st.plotly_chart(altitude_fig, theme="streamlit", use_container_width=True)
    ########
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        rider_weight = st.number_input('Rider weight kg:', min_value=0, max_value=200, value=70, step=1)
        bike_weight = st.number_input('Bike weight kg:', min_value=5, max_value=30, value=10, step=1)
    with c2:
        wind_speed = st.number_input('Wind speed m/s:', min_value=0, max_value=50, value=0, step=1)
        wind_direction = st.number_input('Wind direction 0-360:', min_value=0, max_value=360, value=0, step=1)
    with c3:
        temperature = st.number_input('Temperature C:', min_value=-20, max_value=50, value=20, step=1)
        drag_coefficient = st.number_input('Drag coefficient:', min_value=0.0, max_value=1.0, value=0.8, step=0.05)
    with c4:
        frontal_area = st.number_input('Frontal area m^2:', min_value=0.0, max_value=2.0, value=0.565, step=0.1)
        rolling_resistance = st.number_input('Rolling resistance:', min_value=0.0000, max_value=0.1, value=0.0005,
                                             step=0.0001, format="%.4f")
    with c5:
        efficiency_loss = st.number_input('Efficiency: drivetrain, road, ... 0.05 = 5%', min_value=0.0, max_value=1.0,
                                          value=0.05, step=0.01)
        roll = st.number_input('Smooting:', min_value=0, max_value=30, value=15, step=1)
    avg_est_power = average_estimated_power(df=df_filtered, rider_weight=rider_weight,
                                            bike_weight=bike_weight,
                                            wind_speed=wind_speed, wind_direction=wind_direction,
                                            temperature=temperature,
                                            drag_coefficient=drag_coefficient, frontal_area=frontal_area,
                                            rolling_resistance=rolling_resistance, efficiency_loss=efficiency_loss)
    with st.expander("Climb stats", expanded=True):
        st.write("#### Climbs stats")
        c1, c2, c3 = st.columns(3)
        for i, (key, value) in enumerate(avg_est_power.items()):
            if i%3 == 0:
                with c1:
                    st.write(f"{key}: {value:.02f}")
            if i%3 == 1:
                with c2:
                    st.write(f"{key}: {value:.02f}")
            if i%3 == 2:
                with c3:
                    st.write(f"{key}: {value:.02f}")

        fitted = estimated_power(df=df_filtered, rider_weight=rider_weight,
                                 bike_weight=bike_weight,
                                 wind_speed=wind_speed, wind_direction=wind_direction, temperature=temperature,
                                 drag_coefficient=drag_coefficient, frontal_area=frontal_area,
                                 rolling_resistance=rolling_resistance, efficiency_loss=efficiency_loss)

    pvam_fig = go.Figure()
    pvam_fig.update_layout(
        title='Measured vs Estimated Power')
    pvam_fig.add_trace(go.Scatter(name="Est. Power", x=fitted['seconds'], y=fitted['est_power'].rolling(roll).mean()))
    pvam_fig.add_trace(go.Scatter(name="Power", x=fitted['seconds'], y=fitted['power'].rolling(roll).mean()))
    pvam_fig.add_trace(go.Scatter(name="Est. Power - acceleration", x=fitted['seconds'], y=fitted['est_power_no_acc'].rolling(roll).mean()))
    pvam_fig.add_trace(
        go.Scatter(name="Est. Power (point2point)", x=[start_time, end_time], y=[avg_est_power['est_power'],
                                                                                 avg_est_power['est_power']]))
    pvam_fig.add_trace(
        go.Scatter(name="Avg Power", x=[start_time, end_time], y=[fitted['power'].mean(), fitted['power'].mean()]))
    pvam_fig.add_trace(
        go.Scatter(name="Avg Est. Power", x=[start_time, end_time], y=[fitted['est_power'].mean(), fitted['est_power'].mean()]))


    st.plotly_chart(pvam_fig, theme="streamlit", use_container_width=True)

    comp_fig = go.Figure()
    comp_fig.add_trace(
        go.Scatter(name="Air", x=fitted['seconds'], y=fitted['air_drag_watts'].rolling(roll).mean()))
    comp_fig.add_trace(
        go.Scatter(name="Climbing", x=fitted['seconds'], y=fitted['climbing_watts'].rolling(roll).mean()))
    comp_fig.add_trace(
        go.Scatter(name="Rolling", x=fitted['seconds'], y=fitted['rolling_watts'].rolling(roll).mean()))
    comp_fig.add_trace(
        go.Scatter(name="Acceleration", x=fitted['seconds'], y=fitted['acceleration_watts'].rolling(roll).mean()))
    pvam_fig.update_layout(
        title='Components or Estimated VAM Power')
    st.plotly_chart(comp_fig, theme="streamlit", use_container_width=True)

    with st.expander("Inspect the data"):
        st.dataframe(fitted, use_container_width=True)

    st.download_button(label="Download FIT file and power estimates as csv for the segment",
                       data=fitted.to_csv(index=False).encode('utf-8'),
                       file_name="est_vs_actual.csv",
                       mime='text/csv')
