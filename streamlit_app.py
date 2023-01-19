import pandas as pd
import plotly.express as px
import streamlit as st
from pyfitness.load_data import fitfileinfo, fit2df, fit2csv

st.set_page_config(layout="wide")

"""
# Welcome to Vincent's experiments with cycling data files

This "dashboard" will look at the details of the FIT file 
and the distribution on the data. You are able to compare two file side by side.
"""
st.write("This is a work in progress. Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)")



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
        # Provide a CSV download option
        # st.download_button(label="Download FIT file as CSV",
        #                    data=fit_file1.to_csv(index=False).encode('utf-8'),
        #                    file_name="fit_file1.csv",
        #                    mime='text/csv')

        with st.expander("Expand file details"):
            if fit_file1 is not None:
                ffi1 = fitfileinfo(fit_file1)
                st.write(ffi1)
        df1 = fit2df(fit_file1)
        df1['seconds'] = pd.to_datetime(df1.index).astype(int) / 10 ** 9
        df1['seconds'] = df1['seconds'].max() - df1['seconds']
        st.write("Enter start and end times")
        st.write("These values will be applied to the stats below")
        start_time = st.number_input('Start time in seconds', min_value=0, max_value=int(df1.seconds.max()), value=0,
                                     step=1)
        end_time = st.number_input('End time in seconds', min_value=0, max_value=int(df1.seconds.max()),
                                   value=int(df1.seconds.max()), step=1)
        df_filtered = df1[(df1.seconds >= start_time) & (df1.seconds <= end_time)]
        fig = px.line(df_filtered, x="seconds", y="power")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        fit_stats(df_filtered)

with col2:
    fit_buffer_2 = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file2")
    if fit_buffer_2 is not None:
        fit_file2 = fit_buffer_2.getbuffer()
        # Provide a CSV download option
        # st.download_button(label="Download FIT file as CSV",
        #                    data=fit_file2.to_csv(index=False).encode('utf-8'),
        #                    file_name="fit_file2.csv",
        #                    mime='text/csv')

        with st.expander("Expand file details"):
            if fit_file2 is not None:
                ffi2 = fitfileinfo(fit_file2)
                st.write(ffi2)
        df2 = fit2df(fit_file2)
        df2['seconds'] = pd.to_datetime(df2.index).astype(int) / 10 ** 9
        df2['seconds'] = df2['seconds'].max() - df2['seconds']
        st.write("Enter start and end times")
        st.write("These values will be applied to the stats below")
        start_time = st.number_input('Start time in seconds', min_value=0, max_value=int(df2.seconds.max()), value=0,
                                     step=1)
        end_time = st.number_input('End time in seconds', min_value=0, max_value=int(df2.seconds.max()),
                                   value=int(df2.seconds.max()), step=1)
        df_filtered = df2[(df2.seconds >= start_time) & (df2.seconds <= end_time)]
        fig = px.line(df_filtered, x="seconds", y="power")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        fit_stats(df_filtered)
