from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from pyfitness.load_data import fitfileinfo, fit2df

import plotly.express as px

"""
# Welcome to Vincent's experiments with cycling data files

This "dashboard will look at the details of the FIT file 
and the distribution on the data. You are able to compare two file side by side.
"""

def fit_stats(df: pd.DataFrame):
    """Display the stats of a dataframe"""
    st.write("Preview of the FIT file.\nYou can expand this")
    st.write(df.head(10))
    st.write("Detailed stats of for each fields")
    st.write(df.describe())
    for field in ['cadence', 'heart_rate', 'power']:
        try:
            st.write(f"{field} mean, without zeros: {df[df[field] > 0][field].mean()}")
            st.write(f"{field} max: {df[field].max()}")
            st.write(f"{field} max change: {df[field].diff().max()}")
            fig = px.histogram(df[df[f"{field}"] > 0], x=f"{field}", nbins=50,
                               title=f"{field} distribution", histnorm='probability density')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            fig = px.histogram(df[df[f"{field}"] > 0][f"{field}"].diff(), nbins=50,
                               title=f"{field} change distribution", histnorm='probability density')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        except Exception as e:
            st.write(f" Error with Field name: {field}\nError:\n{e}.")


col1, col2 = st.columns(2)

with col1:
    fit_buffer_1 = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file1")
    if fit_buffer_1 is not None:
        fit_file1 = fit_buffer_1.getbuffer()
        with st.expander("Expand file details"):
            if fit_file1 is not None:
                ffi1 = fitfileinfo(fit_file1)
                st.write(ffi1)
        df1 = fit2df(fit_file1)
        fit_stats(df1)


with col2:
    fit_buffer_2 = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file2")
    if fit_buffer_2 is not None:
        fit_file2 = fit_buffer_2.getbuffer()
        with st.expander("Expand file details"):
            if fit_file2 is not None:
                ffi2 = fitfileinfo(fit_file2)
                st.write(ffi2)
        df2 = fit2df(fit_file2)
        fit_stats(df2)

#
# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
#
#     Point = namedtuple('Point', 'x y')
#     data = []
#
#     points_per_turn = total_points / num_turns
#
#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))
#
#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))
