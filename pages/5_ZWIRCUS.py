import json

import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import numpy as np

from zp import racer_results

c1, c2 = st.columns(2)
with c1:
    zwircus_image = Image.open('images/zwircus.png')
    st.image(zwircus_image, caption='Who are you racing')
with c2:
    st.write("## Zwircus")
    st.write("### Discover who you are racing on Zwift")
    st.write("This page is built for [zwircus.com](https://zwircus.com)")

st.write("#### WKG and Coggan Levels")
st.write("Paste the zwiftpower url for a rider below")
st.write("Example: https://zwiftpower.com/profile.php?zid=1234567890")
profile_url = st.text_input(label="PROFILE URL", placeholder="PROFILE URL")
if "https://zwiftpower.com/profile.php?z=" in profile_url:

    st.write("Getting ZwiftPower data, wait for it.... Might take 5-10 seconds")
    results = racer_results(profile_url)
    df = results['results_df']
    # rank = {"HC": (100, 24.04),
    #         5: {name: "World class: international pro", 5: (24.04, 22.14) ,
    #         "Exceptional: domestic pro": }
    wkg_list = {'wkg_ftp': 6.0, 'wkg1200': 100, 'wkg300': 7.19, 'wkg60': 11.04, 'wkg30': 100, 'wkg15': 100,
                'wkg5': 22.95, 'avg_wkg': 100}
    for c, v in wkg_list.items():
        try:
            cmax = df[c].max()
        except Exception as e:
            cmax = 0
            print(e)
        if float(cmax) >= float(v):
            st.write(f"{c} max value: {cmax}, Warning: :red[{cmax} >= {v}]")
        else:
            st.write(f"{c} max value: {cmax}, OK: :green[{cmax} < {v}]")
    #### Historical WKG
    wkg_curve = go.Figure()
    wkg_curve.update_layout(
        title='Historical WKG')
    df_sorted = df.sort_values('event_date')
    for c in wkg_list.keys():
        wkg_curve.add_trace(
            go.Scatter(name=f"{c}", x=df_sorted['event_date'], y=df_sorted[c]))
    st.plotly_chart(wkg_curve, theme="streamlit", use_container_width=False)

    #### Historical WKG/HR
    wkg_hr = go.Figure()
    wkg_hr.update_layout(
        title='Historical WKG/HR')
    for c in wkg_list.keys():
        try:
            # print(df[[c, 'avg_hr']].dtypes)
            df[c] = df[c].replace('', np.nan)
            df[c] = df[c].astype(float)
            df_sorted = df[(df[c]>0) & (df['avg_hr']>0)].sort_values('event_date')
            df_sorted[f"{c}_hr"] = df_sorted[c] / df_sorted['avg_hr']
            wkg_hr.add_trace(
                go.Scatter(name=f"{c}", x=df_sorted['event_date'], y=df_sorted[f"{c}_hr"]))
        except Exception as e:
            print(e)
            print(f"Error with {c}")
    st.plotly_chart(wkg_hr, theme="streamlit", use_container_width=False)


    for name in results.keys():
        if '_df' in name:
            with st.expander(f"Data from {name} api"):
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(label="Download csv file",
                                       data=results[name].to_csv(index=False).encode('utf-8'),
                                       file_name=f"profile_id){results['profile_id']}_{name.replace('_df', '')}.csv",
                                       mime='text/csv')
                with c2:
                    st.download_button(label="Download json file",
                                       data=json.dumps(results[f"{name.replace('df', 'json')}"]).encode('utf-8'),
                                       file_name=f"profile_id){results['profile_id']}_{name.replace('_df', '')}.json",
                                       mime='text/json')
                st.dataframe(results[name])
