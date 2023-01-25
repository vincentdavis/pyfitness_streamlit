import streamlit as st
import json
from PIL import Image
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
    wkg_list = {'wkg_ftp': 6.0, 'wkg1200': 100, 'wkg300': 7.19, 'wkg60': 11.04, 'wkg30': 100, 'wkg15': 100, 'wkg5': 22.95}
    for c, v in wkg_list.items():
        cmax = df[c].max()
        if float(cmax) >= float(v):
            st.write(f"{c} max value: {cmax}, Warning: :red[{cmax} >= {v}]")
        else:
            st.write(f"{c} max value: {cmax}, OK: :green[{cmax} < {v}]")
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