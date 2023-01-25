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

st.write("#### Cheater or not")
st.write("Pastet the zwiftpower url for a rider below")
st.write("Example: https://zwiftpower.com/profile.php?zid=1234567890")
profile_url = st.text_input(label="PROFILE URL", placeholder="PROFILE URL")
if "https://zwiftpower.com/profile.php?z=" in profile_url:

    st.write("Getting ZwiftPower data, wait for it.... Might take 5-10 seconds")
    results = racer_results(profile_url)
    df = results['results_df']
    for c in df.columns:
        if 'wkg' in c and '_2' not in c:
            st.write(f"{c} max value: {df[c].max()}")
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