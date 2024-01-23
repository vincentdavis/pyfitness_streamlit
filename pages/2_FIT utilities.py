
import streamlit as st
from pyfitness.load_data import fitfileinfo, fit2df
"""
# Welcome to Vincent's experiments with cycling data files

#### Fit file utilities
- See fit file details
- Export to CSV
Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)
"""

with st.form(key="FIT file upload"):
    fit_buffer_1 = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file1")
    submit_button = st.form_submit_button(label='Submit')
if submit_button:
    with st.spinner("Processing..."):
        fit_file = fit_buffer_1.getbuffer()
        df = fit2df(fit_file)
        with st.expander("Expand file details"):
            if fit_file is not None:
                ffi1 = fitfileinfo(fit_file)
                st.write(ffi1)
        st.download_button(label="Download FIT file as CSV",
                           data=df.to_csv(index=False).encode('utf-8'),
                           file_name="fit_to_csv.csv",
                           mime='text/csv')

