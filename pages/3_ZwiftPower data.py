import json

import streamlit as st

from zp import event_results

"""## Get ZwiftPower data
This is a work in progress. Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)

You can also contact me on discord: [Vincent](discordapp.com/users/VincentDavis#3484
"""
st.write("Enter the api url, see browser developer tools")
st.write(
    "This is a work in progress. Please report any issues at [pyfitness_streamlit](https://github.com/vincentdavis/pyfitness_streamlit)"
)

try:
    params = st.experimental_get_query_params()
    event_url = f"https://zwiftpower.com/events.php?zid={params['zid'][0]}"
except:
    event_url = None
print(event_url)
st.write("#### Copy and paste a zwift power event result URL here")
st.write("Example: https://zwiftpower.com/events.php?zid=3438615")
if event_url is None:
    event_url = st.text_input(label="Event URL", placeholder="Event URL")
if "https://zwiftpower.com/events.php?zid=" in event_url:
    # st.write(f"is {event_url is not None}")
    st.write("Getting ZwiftPower data, wait for it.... Might take 5-10 seconds")
    results = event_results(event_url)
    for name in results.keys():
        if "_df" in name:
            with st.expander(f"Data from {name} api"):
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(
                        label="Download csv file",
                        data=results[name].to_csv(index=False).encode("utf-8"),
                        file_name=f"Event_ID_{results['event_id']}_{name.replace('_df', '')}.csv",
                        mime="text/csv",
                    )
                with c2:
                    if not "frr" in name:
                        st.download_button(
                            label="Download json file",
                            data=json.dumps(results[f"{name.replace('df', 'json')}"]).encode("utf-8"),
                            file_name=f"Event_ID_{results['event_id']}_{name.replace('_df', '')}.json",
                            mime="text/json",
                        )
                    else:
                        st.write("No json file for frr")

                st.dataframe(results[name])
